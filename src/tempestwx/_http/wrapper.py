from __future__ import annotations

from collections.abc import Coroutine

from .base import Transport
from .concrete import SyncTransport


class TransportWrapper(Transport):
    """
    Base class for transports that wrap/delegate to another transport.

    Parameters
    ----------
    transport
        request transport, :class:`SyncTransport` if not specified
    """

    def __init__(self, transport: Transport | None) -> None:
        self.transport = transport or SyncTransport()

    @property
    def is_async(self) -> bool:
        """Transport asynchronicity, delegated to the underlying transport."""
        return self.transport.is_async

    def close(self) -> None | Coroutine[None, None, None]:
        """
        Close the underlying transport.

        To close synchronous transports, call :meth:`close`.
        To close asynchronous transports, await :meth:`close`.
        """
        return self.transport.close()
