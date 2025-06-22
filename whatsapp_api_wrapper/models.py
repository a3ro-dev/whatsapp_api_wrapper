"""
Pydantic models for request and response validation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


# Message Models (needed by tests)
class TextMessage(BaseModel):
    to: str = Field(..., description="Recipient WhatsApp ID")
    body: str = Field(..., description="Message text", min_length=1)
    type: str = Field(default="text", description="Message type")

    @validator("to")
    def validate_to(cls, v):
        if not v or not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v


class MediaMessage(BaseModel):
    to: str = Field(..., description="Recipient WhatsApp ID")
    media: str = Field(..., description="Media URL or base64")
    type: str = Field(..., description="Media type (image, video, audio, document)")
    caption: Optional[str] = Field(None, description="Media caption")
    filename: Optional[str] = Field(None, description="Filename for documents")

    @validator("to")
    def validate_to(cls, v):
        if not v or not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v


class LocationMessage(BaseModel):
    to: str = Field(..., description="Recipient WhatsApp ID")
    latitude: float = Field(..., description="Latitude coordinate", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude coordinate", ge=-180, le=180)
    description: Optional[str] = Field(None, description="Location description")
    type: str = Field(default="location", description="Message type")

    @validator("to")
    def validate_to(cls, v):
        if not v or not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v


class ContactMessage(BaseModel):
    to: str = Field(..., description="Recipient WhatsApp ID")
    contact: str = Field(..., description="Contact ID to share")
    type: str = Field(default="contact", description="Message type")

    @validator("to")
    def validate_to(cls, v):
        if not v or not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v


# Contact Models (needed by tests)
class Contact(BaseModel):
    id: str = Field(..., description="Contact WhatsApp ID", min_length=1)
    name: str = Field(..., description="Contact name")
    number: str = Field(..., description="Phone number")
    pushname: Optional[str] = Field(None, description="Push name")
    isUser: bool = Field(default=True, description="Is WhatsApp user")
    isGroup: bool = Field(default=False, description="Is group contact")
    isWAContact: bool = Field(default=True, description="Is WhatsApp contact")
    isMyContact: bool = Field(default=False, description="Is my contact")
    isBlocked: bool = Field(default=False, description="Is contact blocked")

    @validator("id")
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Contact ID cannot be empty")
        return v


# Chat Models (needed by tests)
class Chat(BaseModel):
    id: str = Field(..., description="Chat WhatsApp ID")
    name: str = Field(..., description="Chat name")
    timestamp: int = Field(..., description="Last message timestamp", ge=0)
    isGroup: bool = Field(default=False, description="Is group chat")
    isReadOnly: bool = Field(default=False, description="Is read-only")
    unreadCount: int = Field(default=0, description="Unread message count", ge=0)
    archived: bool = Field(default=False, description="Is chat archived")
    pinned: bool = Field(default=False, description="Is chat pinned")
    isMuted: bool = Field(default=False, description="Is chat muted")

    @validator("timestamp")
    def validate_timestamp(cls, v):
        if v < 0:
            raise ValueError("Timestamp cannot be negative")
        return v


# Group Models (needed by tests)
class GroupParticipant(BaseModel):
    id: str = Field(..., description="Participant WhatsApp ID")
    isAdmin: bool = Field(default=False, description="Is group admin")
    isSuperAdmin: bool = Field(default=False, description="Is group super admin")


class GroupChat(BaseModel):
    id: str = Field(..., description="Group WhatsApp ID")
    name: str = Field(..., description="Group name")
    participants: List[GroupParticipant] = Field(..., description="Group participants", min_items=1)
    admins: List[str] = Field(default_factory=list, description="Admin participant IDs")
    owner: Optional[str] = Field(None, description="Group owner ID")
    description: Optional[str] = Field(None, description="Group description")

    @validator("participants")
    def validate_participants(cls, v):
        if not v:
            raise ValueError("Group must have at least one participant")
        return v


# Session Models (corrected)
class SessionStatusModel(BaseModel):
    sessionId: str = Field(..., description="Session ID", min_length=1)
    status: str = Field(..., description="Session status")
    ready: bool = Field(default=False, description="Is session ready")
    qr: Optional[str] = Field(None, description="QR code data")

    @validator("sessionId")
    def validate_session_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Session ID cannot be empty")
        return v


# Response Models (needed by tests)
class APIResponse(BaseModel):
    success: bool = Field(..., description="Request success status")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    message: Optional[str] = Field(None, description="Response message")


# Request Models (needed by tests)
class SendMessageRequest(BaseModel):
    to: str = Field(..., description="Recipient WhatsApp ID")
    body: str = Field(..., description="Message text")
    type: str = Field(default="text", description="Message type")
    quotedMessageId: Optional[str] = Field(None, description="Quoted message ID")
    mentions: Optional[List[str]] = Field(None, description="Mentioned contacts")

    @validator("to")
    def validate_to(cls, v):
        if not v or not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v

    @validator("body")
    def validate_body(cls, v):
        if not v or not v.strip():
            raise ValueError("Message body cannot be empty")
        return v


class GroupActionRequest(BaseModel):
    groupId: str = Field(..., description="Group WhatsApp ID")
    participants: List[str] = Field(..., description="Participant IDs", min_items=1)

    @validator("participants")
    def validate_participants(cls, v):
        if not v:
            raise ValueError("Participants list cannot be empty")
        return v


# Base Response Models
class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


class ErrorResponse(BaseResponse):
    success: bool = False
    error: str


# Session Models
class StartSessionResponse(BaseResponse):
    success: bool = True
    message: str = "Session initiated successfully"
    sessionId: Optional[str] = Field(default=None, description="Session ID that was started")
    status: Optional[str] = Field(default=None, description="Session status")


# Tests expect SessionStatus to be a model with sessionId, status, ready
class SessionStatus(BaseModel):
    sessionId: str = Field(..., description="Session ID")
    status: str = Field(..., description="Session status")
    ready: bool = Field(default=False, description="Is session ready")
    qr: Optional[str] = Field(default=None, description="QR code data")
    webhook: Optional[str] = Field(default=None, description="Webhook URL")

    @validator("sessionId")
    def validate_session_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Session ID cannot be empty")
        return v


# Keep SessionStatus as the enum, but tests expect a model, so create alias
# Tests expect SessionStatus to be constructible with sessionId, status, ready
class SessionStatusResponse(BaseModel):
    sessionId: str = Field(..., description="Session ID")
    status: str = Field(..., description="Session status")
    ready: bool = Field(default=False, description="Is session ready")
    qr: Optional[str] = Field(default=None, description="QR code data")


class StatusSessionResponse(BaseResponse):
    success: bool = True
    state: SessionStatus
    message: str


class QRCodeResponse(BaseResponse):
    qr: Optional[str] = None
    message: str


class RestartSessionResponse(BaseResponse):
    success: bool = True
    message: str = "Restarted successfully"


class TerminateSessionResponse(BaseResponse):
    success: bool = True
    message: str = "Logged out successfully"


class TerminateSessionsResponse(BaseResponse):
    success: bool = True
    message: str = "Flush completed successfully"


# Message Models
class MessageRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    message: str = Field(..., description="Message content")
    quotedMessageId: Optional[str] = Field(None, description="ID of message to quote")


class MediaMessageRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    media: str = Field(..., description="Base64 encoded media or URL")
    caption: Optional[str] = Field(None, description="Media caption")
    filename: Optional[str] = Field(None, description="Filename for document")


class LocationMessageRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    description: Optional[str] = Field(None, description="Location description")


class ContactMessageRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    contactId: str = Field(..., description="Contact ID to share")


class SendMessageResponse(BaseResponse):
    messageId: Optional[str] = None
    success: bool = True


class MessageInfo(BaseModel):
    id: str
    body: str
    timestamp: int
    from_: str = Field(alias="from")
    to: str
    type: str
    hasMedia: bool = False
    hasQuotedMsg: bool = False


class GetMessagesResponse(BaseResponse):
    messages: List[MessageInfo] = []


class DownloadMediaRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    messageId: str = Field(..., description="Message ID containing media")


class DownloadMediaResponse(BaseResponse):
    mimetype: Optional[str] = None
    data: Optional[str] = None  # Base64 encoded media data
    filename: Optional[str] = None


class ReactRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    messageId: str = Field(..., description="Message ID to react to")
    emoji: str = Field(..., description="Emoji to react with")


class DeleteMessageRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    messageId: str = Field(..., description="Message ID to delete")


class ForwardMessageRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    messageId: str = Field(..., description="Message ID to forward")
    toChatId: str = Field(..., description="Destination chat ID")


# Chat Models
class ChatInfo(BaseModel):
    id: str
    name: str
    isGroup: bool
    isReadOnly: bool = False
    unreadCount: int = 0
    timestamp: Optional[int] = None


class GetChatsResponse(BaseResponse):
    chats: List[ChatInfo] = []


class GetChatByIdRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class GetChatByIdResponse(BaseResponse):
    chat: Optional[ChatInfo] = None


class ArchiveChatRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class MuteChatRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    duration: Optional[int] = Field(None, description="Mute duration in seconds")


class PinChatRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class ClearMessagesRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class DeleteChatRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class MarkChatUnreadRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class SearchMessagesRequest(BaseModel):
    query: str = Field(..., description="Search query")
    page: Optional[int] = Field(1, description="Page number")
    count: Optional[int] = Field(20, description="Number of results per page")


# Contact Models
class ContactInfo(BaseModel):
    id: str
    name: Optional[str] = None
    pushname: Optional[str] = None
    number: str
    isUser: bool = True
    isGroup: bool = False
    isWAContact: bool = True


class GetContactsResponse(BaseResponse):
    contacts: List[ContactInfo] = []


class GetContactByIdRequest(BaseModel):
    contactId: str = Field(..., description="WhatsApp contact ID")


class GetContactByIdResponse(BaseResponse):
    contact: Optional[ContactInfo] = None


class GetNumberIdRequest(BaseModel):
    number: str = Field(..., description="Phone number")


class GetNumberIdResponse(BaseResponse):
    numberId: Optional[str] = None


class IsRegisteredUserRequest(BaseModel):
    number: str = Field(..., description="Phone number")


class IsRegisteredUserResponse(BaseResponse):
    isRegistered: bool


class BlockContactRequest(BaseModel):
    contactId: str = Field(..., description="WhatsApp contact ID")


class GetProfilePicUrlRequest(BaseModel):
    contactId: str = Field(..., description="WhatsApp contact ID")


class GetProfilePicUrlResponse(BaseResponse):
    profilePicUrl: Optional[str] = None


class GetAboutRequest(BaseModel):
    contactId: str = Field(..., description="WhatsApp contact ID")


class GetAboutResponse(BaseResponse):
    about: Optional[str] = None


# Group Chat Models
class CreateGroupRequest(BaseModel):
    name: str = Field(..., description="Group name")
    participants: List[str] = Field(
        ..., description="List of participant contact IDs", min_length=1
    )

    @validator("participants")
    def validate_participants(cls, v):
        if not v:
            raise ValueError("Group must have at least one participant")
        return v


class CreateGroupResponse(BaseResponse):
    groupId: Optional[str] = None


class AddParticipantsRequest(BaseModel):
    chatId: Optional[str] = Field(None, description="Group chat ID")
    groupId: Optional[str] = Field(None, description="Group ID (alias for chatId)")
    participants: List[str] = Field(..., description="List of contact IDs to add")

    def __init__(self, **data):
        # Handle groupId -> chatId conversion for backward compatibility
        if "groupId" in data and "chatId" not in data:
            data["chatId"] = data["groupId"]
        elif "chatId" not in data and "groupId" not in data:
            raise ValueError("Either chatId or groupId must be provided")
        super().__init__(**data)


class RemoveParticipantsRequest(BaseModel):
    chatId: Optional[str] = Field(None, description="Group chat ID")
    groupId: Optional[str] = Field(None, description="Group ID (alias for chatId)")
    participants: List[str] = Field(..., description="List of contact IDs to remove")

    def __init__(self, **data):
        # Handle groupId -> chatId conversion for backward compatibility
        if "groupId" in data and "chatId" not in data:
            data["chatId"] = data["groupId"]
        elif "chatId" not in data and "groupId" not in data:
            raise ValueError("Either chatId or groupId must be provided")
        super().__init__(**data)


class PromoteParticipantsRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    participants: List[str] = Field(..., description="List of contact IDs to promote")


class DemoteParticipantsRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    participants: List[str] = Field(..., description="List of contact IDs to demote")


class SetGroupSubjectRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    subject: str = Field(..., description="New group subject")


class SetGroupDescriptionRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    description: str = Field(..., description="New group description")


class SetGroupPictureRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    media: str = Field(..., description="Base64 encoded image")


class GetInviteCodeRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")


class GetInviteCodeResponse(BaseResponse):
    inviteCode: Optional[str] = None


class RevokeInviteRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")


class LeaveGroupRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")


class SetMessagesAdminsOnlyRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    adminsOnly: bool = Field(..., description="Whether only admins can send messages")


class SetInfoAdminsOnlyRequest(BaseModel):
    chatId: str = Field(..., description="Group chat ID")
    adminsOnly: bool = Field(..., description="Whether only admins can edit group info")


# Client Models
class ClientInfo(BaseModel):
    platform: Optional[str] = None
    phoneNumber: Optional[str] = None
    displayName: Optional[str] = None
    state: Optional[SessionStatus] = None


class GetClientInfoResponse(BaseResponse):
    clientInfo: Optional[ClientInfo] = None


class SetDisplayNameRequest(BaseModel):
    displayName: str = Field(..., description="New display name")


class SetStatusRequest(BaseModel):
    status: str = Field(..., description="New status message")


class SetProfilePictureRequest(BaseModel):
    media: str = Field(..., description="Base64 encoded image")


class GetWWebVersionResponse(BaseResponse):
    version: Optional[str] = None


class AcceptInviteRequest(BaseModel):
    inviteCode: str = Field(..., description="Group invite code")


class GetInviteInfoRequest(BaseModel):
    inviteCode: str = Field(..., description="Group invite code")


class GetInviteInfoResponse(BaseResponse):
    inviteInfo: Optional[Dict[str, Any]] = None


class SendPresenceRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class SendSeenRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class SendStateTypingRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class SendStateRecordingRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


# Label Models
class LabelInfo(BaseModel):
    id: str
    name: str
    color: Optional[str] = None


class GetLabelsResponse(BaseResponse):
    labels: List[LabelInfo] = []


class GetLabelByIdRequest(BaseModel):
    labelId: str = Field(..., description="Label ID")


class GetLabelByIdResponse(BaseResponse):
    label: Optional[LabelInfo] = None


class AddOrRemoveLabelsRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    labelIds: List[str] = Field(..., description="List of label IDs")


class GetChatLabelsRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")


class GetChatsByLabelIdRequest(BaseModel):
    labelId: str = Field(..., description="Label ID")


# Miscellaneous Models
class PingResponse(BaseResponse):
    message: str = "pong"
    success: bool = True


class GetCommonGroupsRequest(BaseModel):
    contactId: str = Field(..., description="WhatsApp contact ID")


class GetCommonGroupsResponse(BaseResponse):
    groups: List[ChatInfo] = []


class GetBlockedContactsResponse(BaseResponse):
    contacts: List[ContactInfo] = []


class FetchMessagesRequest(BaseModel):
    chatId: str = Field(..., description="WhatsApp chat ID")
    count: Optional[int] = Field(50, description="Number of messages to fetch")


class GetFormattedNumberRequest(BaseModel):
    number: str = Field(..., description="Phone number")


class GetFormattedNumberResponse(BaseResponse):
    formattedNumber: Optional[str] = None


class GetCountryCodeRequest(BaseModel):
    number: str = Field(..., description="Phone number")


class GetCountryCodeResponse(BaseResponse):
    countryCode: Optional[str] = None
