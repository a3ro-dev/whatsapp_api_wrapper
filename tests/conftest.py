"""
Pytest configuration and fixtures for WhatsApp API wrapper tests.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from whatsapp_api_wrapper import WhatsAppAPI
from whatsapp_api_wrapper.exceptions import *
from whatsapp_api_wrapper.models import *


@pytest.fixture
def api_key():
    """Test API key."""
    return "test-api-key-12345"


@pytest.fixture
def base_url():
    """Test base URL."""
    return "http://localhost:3000"


@pytest.fixture
def session_id():
    """Test session ID."""
    return "test-session"


@pytest.fixture
def whatsapp_api(api_key, base_url):
    """WhatsApp API client instance for testing."""
    return WhatsAppAPI(api_key=api_key, base_url=base_url)


@pytest.fixture
def mock_httpx_client():
    """Mock httpx client for unit tests."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "data": {}}
    mock_response.raise_for_status.return_value = None
    mock_client.request.return_value = mock_response
    mock_client.__enter__ = Mock(return_value=mock_client)
    mock_client.__exit__ = Mock(return_value=None)
    return mock_client


@pytest.fixture
def sample_message_data():
    """Sample message data for testing."""
    return {"to": "1234567890@c.us", "body": "Test message", "type": "text"}


@pytest.fixture
def sample_contact_data():
    """Sample contact data for testing."""
    return {
        "id": "1234567890@c.us",
        "name": "Test Contact",
        "pushname": "Test",
        "number": "1234567890",
        "isGroup": False,
        "isUser": True,
        "isMyContact": True,
        "isBlocked": False,
    }


@pytest.fixture
def sample_chat_data():
    """Sample chat data for testing."""
    return {
        "id": "1234567890@c.us",
        "name": "Test Chat",
        "isGroup": False,
        "isReadOnly": False,
        "unreadCount": 0,
        "timestamp": 1623456789,
        "archived": False,
        "pinned": False,
        "isMuted": False,
    }


@pytest.fixture
def sample_group_data():
    """Sample group data for testing."""
    return {
        "id": "123456789-987654321@g.us",
        "name": "Test Group",
        "description": "Test group description",
        "participants": [
            {"id": "1111111111@c.us", "isAdmin": True},
            {"id": "2222222222@c.us", "isAdmin": False},
        ],
        "admins": ["1111111111@c.us"],
        "inviteCode": "test-invite-code",
    }


@pytest.fixture
def sample_session_data():
    """Sample session data for testing."""
    return {
        "sessionId": "test-session",
        "ready": True,
        "qr": None,
        "status": "authenticated",
        "webhook": None,
    }


@pytest.fixture
def sample_error_response():
    """Sample error response data."""
    return {"success": False, "error": "Test error message", "code": "TEST_ERROR"}


@pytest.fixture
def mock_successful_response():
    """Mock successful HTTP response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "data": {"message": "Operation successful"}}
    mock_response.raise_for_status.return_value = None
    return mock_response


@pytest.fixture
def mock_error_response():
    """Mock error HTTP response."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "success": False,
        "error": "Bad request",
        "code": "BAD_REQUEST",
    }
    return mock_response
