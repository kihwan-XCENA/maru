# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 XCENA Inc.
"""Maru exception hierarchy."""


class MaruError(RuntimeError):
    """Base class for all Maru errors."""


class MaruConnectionError(MaruError):
    """Raised when connection to the Maru server fails or is lost."""


class MaruAllocationError(MaruError):
    """Raised when memory allocation fails."""


class MaruRPCError(MaruError):
    """Raised when an RPC call to the server fails."""


class MaruTimeoutError(MaruError):
    """Raised when an operation times out."""
