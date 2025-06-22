"""
WhatsApp API Python Wrapper

A comprehensive Python wrapper around the WhatsApp API that provides
strongly-typed interfaces, error handling, and retry logic.
"""

from .client import WhatsAppAPI
from .exceptions import WhatsAppAPIError
from .models import (
    ContactMessage,
    LocationMessage,
    MediaMessage,
    TextMessage,
)

__version__ = "1.0.0"

__all__ = [
    "WhatsAppAPI",
    "WhatsAppAPIError",
    "TextMessage",
    "MediaMessage",
    "LocationMessage",
    "ContactMessage",
]

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
