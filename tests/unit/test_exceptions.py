# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 XCENA Inc.
"""Unit tests for Maru exception hierarchy."""

from unittest.mock import MagicMock

import pytest

from maru_common import (
    MaruAllocationError,
    MaruConfig,
    MaruConnectionError,
    MaruError,
    MaruRPCError,
    MaruTimeoutError,
)
from maru_handler.handler import MaruHandler


class TestExceptionHierarchy:
    """Verify the exception inheritance chain."""

    def test_maru_error_is_runtime_error(self):
        assert issubclass(MaruError, RuntimeError)

    def test_connection_error_is_maru_error(self):
        assert issubclass(MaruConnectionError, MaruError)
        assert isinstance(MaruConnectionError("msg"), MaruError)

    def test_allocation_error_is_maru_error(self):
        assert issubclass(MaruAllocationError, MaruError)
        assert isinstance(MaruAllocationError("msg"), MaruError)

    def test_rpc_error_is_maru_error(self):
        assert issubclass(MaruRPCError, MaruError)
        assert isinstance(MaruRPCError("msg"), MaruError)

    def test_timeout_error_is_maru_error(self):
        assert issubclass(MaruTimeoutError, MaruError)
        assert isinstance(MaruTimeoutError("msg"), MaruError)

    def test_exception_messages_preserved(self):
        e = MaruConnectionError("connection refused")
        assert str(e) == "connection refused"


class TestHandlerRaisesSpecificExceptions:
    """Verify handler.py raises the correct Maru exception types."""

    def _make_connected_handler(self):
        """Create a MaruHandler with mocked RPC/memory internals."""
        config = MaruConfig(
            server_url="tcp://localhost:5555",
            pool_size=4096,
            chunk_size_bytes=1024,
            auto_connect=False,
        )
        handler = MaruHandler(config)
        handler._connected = True
        handler._owned = MagicMock()
        handler._owned.get_chunk_size.return_value = 1024
        handler._owned.is_owned.return_value = True
        handler._mapper = MagicMock()
        handler._rpc = MagicMock()
        return handler

    def test_not_connected_raises_maru_connection_error(self):
        """Calling alloc() when not connected raises MaruConnectionError."""
        config = MaruConfig(
            pool_size=4096, chunk_size_bytes=1024, auto_connect=False
        )
        handler = MaruHandler(config)
        with pytest.raises(MaruConnectionError, match="Not connected"):
            handler.alloc(512)

    def test_closing_raises_maru_error(self):
        """Calling alloc() when closing raises MaruError."""
        handler = self._make_connected_handler()
        handler._closing.set()
        with pytest.raises(MaruError, match="Handler is closing"):
            handler.alloc(512)

    def test_alloc_size_exceeds_chunk_raises_maru_allocation_error(self):
        """alloc() with size > chunk_size raises MaruAllocationError."""
        handler = self._make_connected_handler()
        with pytest.raises(MaruAllocationError, match="exceeds chunk_size"):
            handler.alloc(2048)

    def test_alloc_pool_exhausted_raises_maru_allocation_error(self):
        """alloc() when pool exhausted and auto_expand disabled raises MaruAllocationError."""
        handler = self._make_connected_handler()
        handler._owned.allocate.return_value = None
        handler._auto_expand = False
        with pytest.raises(MaruAllocationError, match="pool exhausted"):
            handler.alloc(512)

    def test_keyboard_interrupt_not_swallowed(self):
        """KeyboardInterrupt (BaseException) propagates through _ensure_connected."""
        handler = self._make_connected_handler()
        handler._closing = MagicMock()
        handler._closing.is_set.side_effect = KeyboardInterrupt
        with pytest.raises(KeyboardInterrupt):
            handler._ensure_connected()
