from __future__ import annotations

from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar, TypeVarTuple, Unpack, cast
from warnings import warn

from .base import Request, Response, Transport
from .concrete import AsyncTransport, SyncTransport
from .error import Unauthorised
from .wrapper import TransportWrapper


class TransportConflictWarning(RuntimeWarning):
    """Transport arguments to a client are in conflict."""


class Client(TransportWrapper):
    """
    Base class for clients.

    Parameters
    ----------
    transport
        request transport - If not specified, a :class:`SyncTransport` is used
    asynchronous
        synchronicity requirement - If specified, overrides the passed transport
        if they are in conflict and instantiates a transport of the requested type
    """

    def __init__(self, transport: Transport | None, asynchronous: bool | None = None) -> None:
        super().__init__(transport)

        if self.transport.is_async and asynchronous is False:
            self.transport = SyncTransport()
        elif not self.transport.is_async and asynchronous is True:
            self.transport = AsyncTransport()

        if transport is not None and self.transport.is_async != transport.is_async:
            msg = (
                f"{type(transport)} with is_async={transport.is_async} passed"
                f" but asynchronous={asynchronous}!"
                f"\nA new {type(self.transport).__name__} was instantiated."
            )
            warn(msg, TransportConflictWarning, stacklevel=3)

    def send(self, request: Request) -> Response | Coroutine[None, None, Response]:
        """Send request with underlying transport."""
        return self.transport.send(request)


R = TypeVar("R")
P = ParamSpec("P")
Ts = TypeVarTuple("Ts")


def send_and_process(
    post_func: Callable[[Request, Response, Unpack[Ts]], R],
) -> Callable[
    [Callable[Concatenate[Transport, P], tuple[Request, tuple[Unpack[Ts]]]]],
    Callable[Concatenate[Transport, P], R | Coroutine[None, None, R]],
]:
    """
    Decorate a Client function to send a request and process its content.

    The first parameter of a decorated function must be the instance (self)
    of a :class:`Transport` (has :meth:`send` and :attr:`is_async`).
    The decorated function must return a tuple with two items:
    a :class:`Request` and a tuple with arguments to unpack to ``post_func``.
    The result of ``post_func`` is returned to the caller.

    Parameters
    ----------
    post_func
        function to call with the request and response
        and possible additional arguments
    """

    def decorator(
        function: Callable[Concatenate[Transport, P], tuple[Request, tuple[Unpack[Ts]]]],
    ) -> Callable[Concatenate[Transport, P], R | Coroutine[None, None, R]]:
        def try_post_func(request: Request, response: Response, *params: Unpack[Ts]) -> R:
            try:
                return post_func(request, response, *params)
            except Unauthorised:
                raise

        async def async_send(
            self: AsyncTransport, request: Request, params: tuple[Unpack[Ts]]
        ) -> R:
            response = await self.send(request)
            return try_post_func(request, response, *params)

        @wraps(function)
        def wrapper(
            self: Transport, *args: P.args, **kwargs: P.kwargs
        ) -> R | Coroutine[None, None, R]:
            request, params = function(self, *args, **kwargs)

            if isinstance(self, AsyncTransport):
                return async_send(self, request, params)

            # Synchronous path: 'send' returns a Response immediately.
            sync_self = cast(SyncTransport, self)
            response = sync_self.send(request)
            return try_post_func(request, response, *params)

        return wrapper

    return decorator
