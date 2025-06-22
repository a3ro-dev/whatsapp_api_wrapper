"""
Unit tests for WhatsApp API models.
"""

import pytest
from pydantic import ValidationError

from whatsapp_api_wrapper.models import (
    APIResponse,
    Chat,
    Contact,
    ContactMessage,
    CreateGroupRequest,
    GroupActionRequest,
    GroupChat,
    GroupParticipant,
    LocationMessage,
    MediaMessage,
    SendMessageRequest,
    SessionStatus,
    TextMessage,
)


class TestMessageModels:
    """Test message-related models."""

    def test_text_message_valid(self):
        """Test valid text message creation."""
        message = TextMessage(to="1234567890@c.us", body="Hello World")
        assert message.to == "1234567890@c.us"
        assert message.body == "Hello World"
        assert message.type == "text"

    def test_text_message_invalid_to(self):
        """Test text message with invalid recipient."""
        with pytest.raises(ValidationError):
            TextMessage(to="", body="Hello World")

    def test_text_message_invalid_body(self):
        """Test text message with empty body."""
        with pytest.raises(ValidationError):
            TextMessage(to="1234567890@c.us", body="")

    def test_media_message_valid(self):
        """Test valid media message creation."""
        message = MediaMessage(
            to="1234567890@c.us",
            media="https://example.com/image.jpg",
            type="image",
            caption="Test image",
        )
        assert message.to == "1234567890@c.us"
        assert message.media == "https://example.com/image.jpg"
        assert message.type == "image"
        assert message.caption == "Test image"

    def test_location_message_valid(self):
        """Test valid location message creation."""
        message = LocationMessage(
            to="1234567890@c.us",
            latitude=40.7128,
            longitude=-74.0060,
            description="New York City",
        )
        assert message.to == "1234567890@c.us"
        assert message.latitude == 40.7128
        assert message.longitude == -74.0060
        assert message.description == "New York City"
        assert message.type == "location"

    def test_location_message_invalid_coordinates(self):
        """Test location message with invalid coordinates."""
        with pytest.raises(ValidationError):
            LocationMessage(
                to="1234567890@c.us",
                latitude=200,
                longitude=-74.0060,  # Invalid latitude
            )

    def test_contact_message_valid(self):
        """Test valid contact message creation."""
        message = ContactMessage(to="1234567890@c.us", contact="9876543210@c.us")
        assert message.to == "1234567890@c.us"
        assert message.contact == "9876543210@c.us"
        assert message.type == "contact"


class TestContactModels:
    """Test contact-related models."""

    def test_contact_valid(self):
        """Test valid contact creation."""
        contact = Contact(
            id="1234567890@c.us",
            name="John Doe",
            pushname="John",
            number="1234567890",
        )
        assert contact.id == "1234567890@c.us"
        assert contact.name == "John Doe"
        assert contact.pushname == "John"
        assert contact.number == "1234567890"

    def test_contact_defaults(self):
        """Test contact with default values."""
        contact = Contact(id="1234567890@c.us", name="John Doe", number="1234567890")
        assert contact.isGroup is False
        assert contact.isUser is True
        assert contact.isMyContact is False
        assert contact.isBlocked is False
        assert contact.pushname is None

    def test_contact_invalid_id(self):
        """Test contact with invalid ID."""
        with pytest.raises(ValidationError):
            Contact(id="", name="John Doe", number="1234567890")  # Empty ID


class TestChatModels:
    """Test chat-related models."""

    def test_chat_valid(self):
        """Test valid chat creation."""
        chat = Chat(id="1234567890@c.us", name="Test Chat", timestamp=1623456789)
        assert chat.id == "1234567890@c.us"
        assert chat.name == "Test Chat"
        assert chat.timestamp == 1623456789

    def test_chat_defaults(self):
        """Test chat with default values."""
        chat = Chat(id="1234567890@c.us", name="Test Chat", timestamp=1623456789)
        assert chat.isGroup is False
        assert chat.isReadOnly is False
        assert chat.unreadCount == 0
        assert chat.archived is False
        assert chat.pinned is False
        assert chat.isMuted is False

    def test_chat_invalid_timestamp(self):
        """Test chat with invalid timestamp."""
        with pytest.raises(ValidationError):
            Chat(id="1234567890@c.us", name="Test Chat", timestamp=-1)  # Invalid timestamp


class TestGroupModels:
    """Test group-related models."""

    def test_group_participant_valid(self):
        """Test valid group participant creation."""
        participant = GroupParticipant(id="1234567890@c.us", isAdmin=True)
        assert participant.id == "1234567890@c.us"
        assert participant.isAdmin is True

    def test_group_participant_defaults(self):
        """Test group participant with default values."""
        participant = GroupParticipant(id="1234567890@c.us")
        assert participant.isAdmin is False

    def test_group_chat_valid(self):
        """Test valid group chat creation."""
        participants = [
            GroupParticipant(id="1111111111@c.us", isAdmin=True),
            GroupParticipant(id="2222222222@c.us", isAdmin=False),
        ]
        group = GroupChat(
            id="123456789-987654321@g.us",
            name="Test Group",
            description="Test group description",
            participants=participants,
            admins=["1111111111@c.us"],
        )
        assert group.id == "123456789-987654321@g.us"
        assert group.name == "Test Group"
        assert group.description == "Test group description"
        assert len(group.participants) == 2
        assert len(group.admins) == 1

    def test_group_chat_empty_participants(self):
        """Test group chat with empty participants list."""
        with pytest.raises(ValidationError):
            GroupChat(
                id="123456789-987654321@g.us",
                name="Test Group",
                participants=[],  # Empty participants
                admins=[],
            )


class TestSessionModels:
    """Test session-related models."""

    def test_session_status_valid(self):
        """Test valid session status creation."""
        status = SessionStatus(sessionId="test-session", ready=True, status="authenticated")
        assert status.sessionId == "test-session"
        assert status.ready is True
        assert status.status == "authenticated"

    def test_session_status_defaults(self):
        """Test session status with default values."""
        status = SessionStatus(sessionId="test-session", status="connecting")
        assert status.ready is False
        assert status.qr is None
        assert status.webhook is None

    def test_session_status_invalid_id(self):
        """Test session status with invalid session ID."""
        with pytest.raises(ValidationError):
            SessionStatus(sessionId="", status="authenticated")  # Empty session ID


class TestResponseModels:
    """Test API response models."""

    def test_api_response_success(self):
        """Test successful API response."""
        response = APIResponse(success=True, data={"message": "Operation successful"})
        assert response.success is True
        assert response.data["message"] == "Operation successful"
        assert response.error is None
        assert response.code is None

    def test_api_response_error(self):
        """Test error API response."""
        response = APIResponse(success=False, error="Something went wrong", code="ERROR_CODE")
        assert response.success is False
        assert response.error == "Something went wrong"
        assert response.code == "ERROR_CODE"
        assert response.data is None

    def test_api_response_invalid(self):
        """Test invalid API response."""
        with pytest.raises(ValidationError):
            APIResponse()  # Missing required 'success' field


class TestRequestModels:
    """Test API request models."""

    def test_send_message_request_valid(self):
        """Test valid send message request."""
        request = SendMessageRequest(to="1234567890@c.us", body="Hello World")
        assert request.to == "1234567890@c.us"
        assert request.body == "Hello World"
        assert request.type == "text"

    def test_send_message_request_with_options(self):
        """Test send message request with optional fields."""
        request = SendMessageRequest(
            to="1234567890@c.us",
            body="Hello World",
            quotedMessageId="msg_123",
            mentions=["9876543210@c.us"],
        )
        assert request.quotedMessageId == "msg_123"
        assert len(request.mentions) == 1

    def test_create_group_request_valid(self):
        """Test valid create group request."""
        request = CreateGroupRequest(
            name="Test Group",
            participants=["1111111111@c.us", "2222222222@c.us"],
        )
        assert request.name == "Test Group"
        assert len(request.participants) == 2

    def test_create_group_request_empty_participants(self):
        """Test create group request with empty participants."""
        with pytest.raises(ValidationError):
            CreateGroupRequest(name="Test Group", participants=[])  # Empty participants

    def test_group_action_request_valid(self):
        """Test valid group action request."""
        request = GroupActionRequest(
            groupId="123456789-987654321@g.us",
            participants=["1111111111@c.us"],
        )
        assert request.groupId == "123456789-987654321@g.us"
        assert len(request.participants) == 1

    def test_group_action_request_empty_participants(self):
        """Test group action request with empty participants."""
        with pytest.raises(ValidationError):
            GroupActionRequest(
                groupId="123456789-987654321@g.us",
                participants=[],  # Empty participants
            )
