"""
Custom exceptions for the WhatsApp API wrapper.
"""


class WhatsAppAPIError(Exception):
    """Base exception for all WhatsApp API related errors."""

    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details

    def __str__(self):
        return self.message


class ConnectionError(WhatsAppAPIError):
    """Raised when there are network connectivity issues."""

    def __init__(self, message: str = "Failed to connect to WhatsApp API"):
        super().__init__(message, "CONNECTION_ERROR")


class HTTPError(WhatsAppAPIError):
    """Raised when the API returns a non-2xx HTTP status code."""

    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        super().__init__(
            message,
            str(status_code) if status_code else None,
            {"response_body": response_body} if response_body else None,
        )
        self.status_code = status_code
        self.response_body = response_body


class ValidationError(WhatsAppAPIError):
    """Raised when response data doesn't match expected schema."""

    def __init__(self, message: str, validation_details: str = None):
        super().__init__(
            message,
            "VALIDATION_ERROR",
            {"details": validation_details} if validation_details else None,
        )
        self.validation_details = validation_details


class SessionError(WhatsAppAPIError):
    """Raised when there are session-related errors."""

    def __init__(self, message: str, session_id: str = None):
        super().__init__(
            message, "SESSION_ERROR", {"session_id": session_id} if session_id else None
        )
        self.session_id = session_id


class RateLimitError(HTTPError):
    """Raised when API rate limits are exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        super().__init__(
            message, 429, f"Retry after {retry_after} seconds" if retry_after else None
        )
        self.retry_after = retry_after


class AuthenticationError(WhatsAppAPIError):
    """Raised when API key is invalid or missing."""

    def __init__(
        self, message: str = "Invalid API key", status_code: int = None, response_body: str = None
    ):
        super().__init__(
            message,
            str(status_code) if status_code else "AUTHENTICATION_ERROR",
            {"response_body": response_body} if response_body else None,
        )
        self.status_code = status_code
        self.response_body = response_body


class NotFoundError(WhatsAppAPIError):
    """Raised when requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = None,
        response_body: str = None,
    ):
        super().__init__(
            message,
            str(status_code) if status_code else "NOT_FOUND",
            {"response_body": response_body} if response_body else None,
        )
        self.status_code = status_code
        self.response_body = response_body


# Additional exception classes expected by tests
class WhatsAppAuthenticationError(WhatsAppAPIError):
    """Authentication-related errors."""

    pass


class WhatsAppAuthorizationError(WhatsAppAPIError):
    """Authorization-related errors."""

    pass


class WhatsAppValidationError(WhatsAppAPIError):
    """Validation-related errors."""

    pass


class WhatsAppNotFoundError(WhatsAppAPIError):
    """Not found errors."""

    pass


class WhatsAppRateLimitError(WhatsAppAPIError):
    """Rate limit errors."""

    pass


class WhatsAppServerError(WhatsAppAPIError):
    """Server errors."""

    pass


class WhatsAppTimeoutError(WhatsAppAPIError):
    """Timeout errors."""

    pass


class WhatsAppConnectionError(WhatsAppAPIError):
    """Connection errors."""

    pass


class WhatsAppHTTPError(WhatsAppAPIError):
    """HTTP errors."""

    pass


class WhatsAppSessionError(WhatsAppAPIError):
    """Session errors."""

    pass


class WhatsAppMessageError(WhatsAppAPIError):
    """Message-related errors."""

    pass
