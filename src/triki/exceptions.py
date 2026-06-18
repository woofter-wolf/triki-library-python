class TRIKIError(Exception):
    """Base exception for triki errors."""


class TRIKIConnectionError(TRIKIError):
    """Raised when connection to a TRIKI device fails."""


class TRIKIDeviceNotFoundError(TRIKIError):
    """Raised when a TRIKI device cannot be found."""


class TRIKINotConnectedError(TRIKIError):
    """Raised when called operation requires a connected TRIKI device."""
