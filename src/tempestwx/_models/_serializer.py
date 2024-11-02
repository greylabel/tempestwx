from enum import Enum, EnumMeta
from warnings import warn

from pydantic import AliasChoices, AliasPath, BaseModel


class StrEnumMeta(EnumMeta):
    """
    Metaclass for StrEnum that provides case-insensitive get.

    This does not change values.
    """

    def __new__(mcs, cls, bases, classdict, **kwds):  # noqa: N804
        """Override `__new__` to make all keys lowercase."""
        enum_class = super().__new__(mcs, cls, bases, classdict, **kwds)
        copied_member_map = dict(enum_class._member_map_)
        enum_class._member_map_.clear()
        for k, v in copied_member_map.items():
            enum_class._member_map_[k.lower()] = v
        return enum_class

    def __getitem__(cls, name: str):
        # Ignore case on get item
        return super().__getitem__(name.lower())


class StrEnum(str, Enum, metaclass=StrEnumMeta):
    """
    Convert enumeration members to strings using their name.

    Ignores case when getting items. This does not change values.
    Works with Pydantic strict mode by providing custom validation.
    """

    @classmethod
    def _missing_(cls, value):
        return cls[value.lower()]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """
        Provide Pydantic schema for string-to-enum coercion.

        Works with strict mode by accepting both enum instances and strings.
        """
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.union_schema(
                [
                    core_schema.is_instance_schema(cls),
                    core_schema.str_schema(),
                ]
            ),
        )

    @classmethod
    def _validate(cls, v):
        """Convert string values to enum instances."""
        if isinstance(v, cls):
            return v
        if isinstance(v, str):
            try:
                return cls(v)
            except ValueError:
                # Try case-insensitive match using _missing_
                return cls._missing_(v)
        return v


class Model(BaseModel):
    """Response model base."""

    def __init__(self, **data) -> None:
        """"""  # noqa: D419
        super().__init__(**data)

        # Build a set of known keys that includes both field names and any
        # accepted aliases used during validation (e.g., Field(alias="type")).
        known_keys = set(self.__dict__.keys())

        # Use class-level __pydantic_fields__ to avoid deprecation of
        # model_fields
        fields = type(self).__pydantic_fields__  # dict[str, FieldInfo]
        for _name, field_info in fields.items():
            # Primary alias
            alias = getattr(field_info, "alias", None)
            if isinstance(alias, str):
                known_keys.add(alias)

            # validation_alias may be a string, AliasChoices, or AliasPath
            v_alias = getattr(field_info, "validation_alias", None)
            if v_alias is None:
                pass
            elif isinstance(v_alias, str):
                known_keys.add(v_alias)
            else:
                # Handle AliasChoices
                if isinstance(v_alias, AliasChoices):
                    for c in v_alias.choices:
                        if isinstance(c, str):
                            known_keys.add(c)
                        elif isinstance(c, AliasPath):
                            if (
                                c.path
                                and isinstance(c.path, (list, tuple))
                                and isinstance(c.path[0], str)
                            ):
                                known_keys.add(c.path[0])
                # Handle AliasPath (take top-level key if present)
                elif isinstance(v_alias, AliasPath):
                    if (
                        v_alias.path
                        and isinstance(v_alias.path, (list, tuple))
                        and isinstance(v_alias.path[0], str)
                    ):
                        known_keys.add(v_alias.path[0])

        unknowns = set(data.keys()) - known_keys
        cls_name = self.__class__.__name__
        for arg in unknowns:
            msg = (
                f"{cls_name} contains unknown attribute: `{arg}`, "
                "which was discarded. This warning may be safely ignored. "
                "Please consider upgrading."
            )
            warn(msg, UnknownModelAttributeWarning, stacklevel=5)


class UnknownModelAttributeWarning(RuntimeWarning):
    """The response model contains an unknown attribute."""
