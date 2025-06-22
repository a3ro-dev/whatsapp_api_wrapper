"""
Unit tests for WhatsApp API client.
"""

from unittest.mock import Mock, patch

import httpx
import pytest

from whatsapp_api_wrapper.client import WhatsAppAPI
from whatsapp_api_wrapper.exceptions import (
    WhatsAppAPIError,
    WhatsAppConnectionError,
    WhatsAppHTTPError,
    WhatsAppTimeoutError,
)


class TestWhatsAppAPIInit:
    """Test WhatsApp API initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        api = WhatsAppAPI("test-key")
        assert api.api_key == "test-key"
        assert api.base_url == "http://localhost:3000"
        assert api.timeout == 30.0
        assert api.max_retries == 3

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        api = WhatsAppAPI(
            api_key="custom-key",
            base_url="https://api.example.com",
            timeout=60.0,
            max_retries=5,
        )
        assert api.api_key == "custom-key"
        assert api.base_url == "https://api.example.com"
        assert api.timeout == 60.0
        assert api.max_retries == 5

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is stripped from base URL."""
        api = WhatsAppAPI("test-key", base_url="http://localhost:3000/")
        assert api.base_url == "http://localhost:3000"


class TestWhatsAppAPIHttpMethods:
    """Test HTTP methods of WhatsApp API client."""

    @patch("httpx.Client")
    def test_make_request_success(self, mock_client_class, whatsapp_api):
        """Test successful HTTP request."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"test": "data"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api._make_request("GET", "/test")

        assert result == {"test": "data"}
        mock_client.request.assert_called_once()

    @patch("httpx.Client")
    def test_make_request_api_error(self, mock_client_class, whatsapp_api):
        """Test API error response."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_response.json.return_value = {
            "success": False,
            "error": "Bad request",
            "code": "BAD_REQUEST",
        }
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        with pytest.raises(WhatsAppAPIError) as exc_info:
            whatsapp_api._make_request("GET", "/test")

        assert "Bad request" in str(exc_info.value)

    @patch("httpx.Client")
    def test_make_request_http_error(self, mock_client_class, whatsapp_api):
        """Test HTTP error handling."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=Mock(), response=mock_response
        )
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        with pytest.raises(WhatsAppHTTPError):
            whatsapp_api._make_request("GET", "/test")

    @patch("httpx.Client")
    def test_make_request_timeout(self, mock_client_class, whatsapp_api):
        """Test timeout handling."""
        mock_client = Mock()
        mock_client.request.side_effect = httpx.TimeoutException("Timeout")
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        with pytest.raises(WhatsAppTimeoutError):
            whatsapp_api._make_request("GET", "/test")

    @patch("httpx.Client")
    def test_make_request_connection_error(
        self, mock_client_class, whatsapp_api
    ):
        """Test connection error handling."""
        mock_client = Mock()
        mock_client.request.side_effect = httpx.ConnectError(
            "Connection failed"
        )
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        with pytest.raises(WhatsAppConnectionError):
            whatsapp_api._make_request("GET", "/test")


class TestSessionMethods:
    """Test session management methods."""

    @patch("httpx.Client")
    def test_start_session(self, mock_client_class, whatsapp_api, session_id):
        """Test starting a session."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"sessionId": session_id, "status": "started"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.start_session(session_id)

        assert result["sessionId"] == session_id
        mock_client.request.assert_called_once_with(
            "GET",
            f"http://localhost:3000/session/start/{session_id}",
            headers={"X-API-Key": "test-api-key-12345"},
            timeout=30.0,
        )

    @patch("httpx.Client")
    def test_get_session_status(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test getting session status."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"sessionId": session_id, "status": "authenticated"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.get_session_status(session_id)

        assert result["status"] == "authenticated"
        mock_client.request.assert_called_once_with(
            "GET",
            f"http://localhost:3000/session/status/{session_id}",
            headers={"X-API-Key": "test-api-key-12345"},
            timeout=30.0,
        )

    @patch("httpx.Client")
    def test_get_qr_code(self, mock_client_class, whatsapp_api, session_id):
        """Test getting QR code."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"qr": "qr-code-data"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.get_qr_code(session_id)

        assert result["qr"] == "qr-code-data"

    @patch("httpx.Client")
    def test_terminate_session(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test terminating a session."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Session terminated"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.terminate_session(session_id)

        assert result["message"] == "Session terminated"


class TestMessageMethods:
    """Test message-related methods."""

    @patch("httpx.Client")
    def test_send_message(
        self, mock_client_class, whatsapp_api, session_id, sample_message_data
    ):
        """Test sending a message."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"messageId": "msg_123", "status": "sent"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.send_message(session_id, sample_message_data)

        assert result["messageId"] == "msg_123"
        mock_client.request.assert_called_once_with(
            "POST",
            f"http://localhost:3000/client/sendMessage/{session_id}",
            headers={"X-API-Key": "test-api-key-12345"},
            json=sample_message_data,
            timeout=30.0,
        )

    @patch("httpx.Client")
    def test_delete_message(self, mock_client_class, whatsapp_api, session_id):
        """Test deleting a message."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Message deleted"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        message_data = {"messageId": "msg_123"}
        result = whatsapp_api.delete_message(session_id, message_data)

        assert result["message"] == "Message deleted"

    @patch("httpx.Client")
    def test_forward_message(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test forwarding a message."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"messageId": "msg_456", "status": "forwarded"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        forward_data = {"messageId": "msg_123", "to": "1234567890@c.us"}
        result = whatsapp_api.forward_message(session_id, forward_data)

        assert result["status"] == "forwarded"

    @patch("httpx.Client")
    def test_react_to_message(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test reacting to a message."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Reaction added"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        reaction_data = {"messageId": "msg_123", "reaction": "👍"}
        result = whatsapp_api.react_to_message(session_id, reaction_data)

        assert result["message"] == "Reaction added"


class TestChatMethods:
    """Test chat-related methods."""

    @patch("httpx.Client")
    def test_get_chats(self, mock_client_class, whatsapp_api, session_id):
        """Test getting chats."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"chats": [{"id": "chat1"}, {"id": "chat2"}]},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.get_chats(session_id)

        assert len(result["chats"]) == 2

    @patch("httpx.Client")
    def test_get_chat_by_id(self, mock_client_class, whatsapp_api, session_id):
        """Test getting a specific chat by ID."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"id": "chat_123", "name": "Test Chat"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        chat_data = {"chatId": "chat_123"}
        result = whatsapp_api.get_chat_by_id(session_id, chat_data)

        assert result["id"] == "chat_123"

    @patch("httpx.Client")
    def test_archive_chat(self, mock_client_class, whatsapp_api, session_id):
        """Test archiving a chat."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Chat archived"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        chat_data = {"chatId": "chat_123"}
        result = whatsapp_api.archive_chat(session_id, chat_data)

        assert result["message"] == "Chat archived"


class TestContactMethods:
    """Test contact-related methods."""

    @patch("httpx.Client")
    def test_get_contacts(self, mock_client_class, whatsapp_api, session_id):
        """Test getting contacts."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"contacts": [{"id": "contact1"}, {"id": "contact2"}]},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        result = whatsapp_api.get_contacts(session_id)

        assert len(result["contacts"]) == 2

    @patch("httpx.Client")
    def test_get_contact_by_id(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test getting a specific contact by ID."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"id": "contact_123", "name": "Test Contact"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        contact_data = {"contactId": "contact_123"}
        result = whatsapp_api.get_contact_by_id(session_id, contact_data)

        assert result["id"] == "contact_123"

    @patch("httpx.Client")
    def test_block_contact(self, mock_client_class, whatsapp_api, session_id):
        """Test blocking a contact."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Contact blocked"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        contact_data = {"contactId": "contact_123"}
        result = whatsapp_api.block_contact(session_id, contact_data)

        assert result["message"] == "Contact blocked"


class TestGroupMethods:
    """Test group-related methods."""

    @patch("httpx.Client")
    def test_create_group(self, mock_client_class, whatsapp_api, session_id):
        """Test creating a group."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"groupId": "group_123", "name": "Test Group"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        group_data = {
            "name": "Test Group",
            "participants": ["1111111111@c.us"],
        }
        result = whatsapp_api.create_group(session_id, group_data)

        assert result["groupId"] == "group_123"

    @patch("httpx.Client")
    def test_add_participants(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test adding participants to a group."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Participants added"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        group_data = {
            "groupId": "group_123",
            "participants": ["2222222222@c.us"],
        }
        result = whatsapp_api.add_group_participants(session_id, group_data)

        assert result["message"] == "Participants added"

    @patch("httpx.Client")
    def test_remove_participants(
        self, mock_client_class, whatsapp_api, session_id
    ):
        """Test removing participants from a group."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"message": "Participants removed"},
        }
        mock_response.raise_for_status.return_value = None
        mock_client.request.return_value = mock_response
        mock_client.__enter__ = Mock(return_value=mock_client)
        mock_client.__exit__ = Mock(return_value=None)
        mock_client_class.return_value = mock_client

        group_data = {
            "groupId": "group_123",
            "participants": ["2222222222@c.us"],
        }
        result = whatsapp_api.remove_group_participants(session_id, group_data)

        assert result["message"] == "Participants removed"


class TestContextManager:
    """Test context manager functionality."""

    def test_context_manager(self, whatsapp_api):
        """Test that the API can be used as a context manager."""
        with whatsapp_api as api:
            assert api is whatsapp_api
            assert hasattr(api, "_client")

    def test_context_manager_cleanup(self, whatsapp_api):
        """Test that resources are cleaned up properly."""
        with whatsapp_api:
            pass
        # Context manager should handle cleanup automatically
