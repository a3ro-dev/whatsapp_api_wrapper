"""
WhatsApp API Python Wrapper

A comprehensive Python wrapper around the WhatsApp API that provides
strongly-typed interfaces, error handling, and retry logic.
"""

from .client import WhatsAppAPI
from .exceptions import (
    WhatsAppAPIError,
    WhatsAppConnectionError,
    WhatsAppHTTPError,
    WhatsAppValidationError,
    WhatsAppSessionError,
    WhatsAppTimeoutError,
    WhatsAppRateLimitError,
    WhatsAppAuthenticationError,
    WhatsAppNotFoundError,
    WhatsAppServerError,
    ConnectionError,
    HTTPError,
    ValidationError,
    SessionError,
    RateLimitError,
    AuthenticationError,
    NotFoundError,
)
from .models import (
    # Core models
    TextMessage,
    MediaMessage,
    LocationMessage,
    ContactMessage,
    Contact,
    Chat,
    GroupParticipant,
    GroupChat,
    SessionStatusResponse,
    APIResponse,
    SendMessageRequest,
    GroupActionRequest,
    BaseResponse,
    StartSessionResponse,
    SessionStatus,
    StatusSessionResponse,
    QRCodeResponse,
    RestartSessionResponse,
    TerminateSessionResponse,
)

__version__ = "1.0.0"
__all__ = [
    "WhatsAppAPI",
    "WhatsAppAPIError",
    "WhatsAppConnectionError", 
    "WhatsAppHTTPError",
    "WhatsAppValidationError",
    "WhatsAppSessionError",
    "WhatsAppTimeoutError",
    "WhatsAppRateLimitError",
    "WhatsAppAuthenticationError",
    "WhatsAppNotFoundError",
    # Core models
    "TextMessage",
    "MediaMessage", 
    "LocationMessage",
    "ContactMessage",
    "Contact",
    "Chat",
    "GroupParticipant",
    "GroupChat",
    "SessionStatus",
    "APIResponse",
    "SendMessageRequest",
    "GroupActionRequest",
]
