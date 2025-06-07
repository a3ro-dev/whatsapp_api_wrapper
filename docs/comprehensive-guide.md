# WhatsApp API Python Wrapper - Comprehensive Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Quick Start](#quick-start)
4. [Architecture Overview](#architecture-overview)
5. [API Reference](#api-reference)
6. [Advanced Usage](#advanced-usage)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Testing](#testing)
10. [Real-World Examples](#real-world-examples)
11. [Performance & Optimization](#performance--optimization)
12. [Troubleshooting](#troubleshooting)

## Introduction

The WhatsApp API Python Wrapper is a comprehensive, production-ready Python library that provides a strongly-typed interface to the WhatsApp Web API. It's built on top of a Node.js-based WhatsApp REST API server and offers features like automatic retries, error handling, data validation, and comprehensive logging.

### Key Features

- 🚀 **Full API Coverage**: Complete implementation of all WhatsApp Web API endpoints
- 🔒 **Type Safety**: Fully typed with Pydantic models for request/response validation
- 🛡️ **Error Handling**: Comprehensive error handling with custom exceptions
- 🔄 **Automatic Retries**: Built-in retry logic with exponential backoff for transient failures
- 📊 **Logging**: Detailed logging for debugging and monitoring
- 🧪 **Well Tested**: Comprehensive test suite with unit and integration tests
- ⚡ **Performance**: Optimized for high-throughput applications
- 🔌 **Extensible**: Easy to extend and customize for specific use cases

### Architecture Flow

```
WhatsApp Web ←→ whatsapp-web.js ←→ Node.js API Server ←→ Python Wrapper ←→ Your Application
```

The wrapper communicates with a local Node.js server that handles the actual WhatsApp Web connection, providing a clean REST API interface.

## Installation & Setup

### Prerequisites

1. **Python 3.8+** is required
2. **WhatsApp API Server** must be running at `http://localhost:3000`
3. **Docker & Docker Compose** for running the API server

### Step 1: Setup the WhatsApp API Server

The Python wrapper requires the underlying Node.js WhatsApp API server to be running. This server handles the actual WhatsApp Web connection.

```bash
# Clone the repository if you haven't already
git clone https://github.com/a3ro-dev/waSpammer.git
cd waSpammer

# Navigate to the WhatsApp API directory
cd whatsapp-api

# Start the API server with Docker Compose
docker-compose pull && docker-compose up -d

# Verify the server is running
curl http://localhost:3000/health
```

The server will be available at:
- **API Endpoint**: `http://localhost:3000`
- **API Documentation**: `http://localhost:3000/api-docs/`

### Step 2: Install the Python Wrapper

```bash
# Navigate back to the project root
cd ..

# Install the wrapper package
pip install -e .

# For development (includes testing and linting tools)
pip install -e ".[dev]"

# For documentation generation
pip install -e ".[docs]"

# For async support (future feature)
pip install -e ".[async]"

# Install all optional dependencies
pip install -e ".[all]"
```

### Step 3: Verify Installation

```python
from wrapper import WhatsAppAPI
from wrapper.models import SendMessageRequest

# This should not raise any import errors
print("WhatsApp API Wrapper installed successfully!")
```

## Quick Start

### Your First WhatsApp Message

Here's a complete example showing how to send your first message:

```python
import time
from wrapper import WhatsAppAPI
from wrapper.models import SendMessageRequest
from wrapper.exceptions import WhatsAppAPIError, WhatsAppSessionError

def send_first_message():
    # Initialize the API client
    api = WhatsAppAPI(
        api_key="your-api-key",  # Set your API key
        base_url="http://localhost:3000",
        timeout=30,
        max_retries=3
    )
    
    session_id = "my-first-session"
    
    try:
        # Step 1: Start a WhatsApp session
        print("Starting WhatsApp session...")
        session_response = api.start_session(session_id)
        print(f"Session started: {session_response}")
        
        # Step 2: Get QR code for authentication
        print("Getting QR code...")
        qr_response = api.get_qr_code(session_id)
        print(f"QR Code: {qr_response.qr}")
        print("Please scan this QR code with your WhatsApp mobile app")
        
        # Step 3: Wait for session to be ready
        print("Waiting for QR code scan...")
        max_wait = 60  # Wait up to 60 seconds
        wait_time = 0
        
        while wait_time < max_wait:
            status = api.get_session_status(session_id)
            if status.authenticated:
                print("Session authenticated successfully!")
                break
            print("Waiting for QR code scan...")
            time.sleep(5)
            wait_time += 5
        else:
            raise WhatsAppSessionError("QR code not scanned within timeout period")
        
        # Step 4: Send a message
        print("Sending message...")
        message_request = SendMessageRequest(
            chatId="1234567890@c.us",  # Replace with actual phone number
            content="Hello from Python! 🐍",
            contentType="string"
        )
        
        response = api.send_message(session_id, message_request)
        print(f"Message sent successfully: {response.success}")
        print(f"Message ID: {response.messageId}")
        
        # Step 5: Get your contacts (optional)
        print("Fetching contacts...")
        contacts = api.get_contacts(session_id)
        print(f"Found {len(contacts.contacts)} contacts")
        for contact in contacts.contacts[:5]:  # Show first 5
            print(f"  - {contact.name}: {contact.number}")
            
    except WhatsAppAPIError as e:
        print(f"API Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        # Cleanup: Terminate the session
        try:
            print("Cleaning up session...")
            api.terminate_session(session_id)
            print("Session terminated successfully")
        except Exception as e:
            print(f"Error terminating session: {e}")
    
    return True

if __name__ == "__main__":
    success = send_first_message()
    if success:
        print("✅ First message sent successfully!")
    else:
        print("❌ Failed to send message")
```

### Environment Configuration

For production use, it's recommended to use environment variables:

```python
import os
from wrapper import WhatsAppAPI

# Set environment variables
# export WHATSAPP_API_KEY="your-api-key"
# export WHATSAPP_BASE_URL="http://localhost:3000"

api = WhatsAppAPI(
    api_key=os.getenv("WHATSAPP_API_KEY"),
    base_url=os.getenv("WHATSAPP_BASE_URL", "http://localhost:3000"),
    timeout=int(os.getenv("WHATSAPP_TIMEOUT", "30")),
    max_retries=int(os.getenv("WHATSAPP_MAX_RETRIES", "3"))
)
```

### Using Context Manager

The API client supports context manager for automatic cleanup:

```python
from wrapper import WhatsAppAPI

with WhatsAppAPI(api_key="your-api-key") as api:
    session_id = "context-session"
    
    # Start session
    api.start_session(session_id)
    
    # Get QR and authenticate
    qr = api.get_qr_code(session_id)
    print(f"QR: {qr.qr}")
    
    # ... do your work ...
    
    # Session automatically terminated when exiting context
```

## Architecture Overview

### Core Components

#### 1. Client (`wrapper.client.WhatsAppAPI`)

The main API client that handles all communication with the WhatsApp API server.

```python
class WhatsAppAPI:
    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:3000",
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        session: Optional[httpx.Client] = None
    ):
        # Implementation details...
```

#### 2. Models (`wrapper.models`)

Pydantic models for request/response validation and type safety.

```python
from wrapper.models import (
    # Message types
    SendMessageRequest,
    TextMessage,
    MediaMessage,
    LocationMessage,
    ContactMessage,
    
    # Chat types
    Chat,
    GroupChat,
    
    # Session types
    SessionStatus,
    QRCodeResponse,
    
    # Response types
    APIResponse,
    BaseResponse
)
```

#### 3. Exceptions (`wrapper.exceptions`)

Custom exception hierarchy for different error types.

```python
from wrapper.exceptions import (
    WhatsAppAPIError,         # Base exception
    WhatsAppConnectionError,  # Network issues
    WhatsAppHTTPError,        # HTTP errors (4xx, 5xx)
    WhatsAppValidationError,  # Data validation errors
    WhatsAppSessionError,     # Session-related errors
    WhatsAppTimeoutError,     # Request timeouts
    WhatsAppRateLimitError,   # Rate limiting (429)
    WhatsAppAuthenticationError,  # Auth errors (403)
    WhatsAppNotFoundError,    # Resource not found (404)
)
```

#### 4. Utilities (`wrapper.utils`)

Common helper functions for URL building, validation, etc.

```python
from wrapper.utils import (
    build_url,
    validate_session_id,
    validate_phone_number,
    format_chat_id
)
```

### Package Structure

```
wrapper/
├── __init__.py          # Package exports
├── client.py            # Main WhatsAppAPI class
├── models.py            # Pydantic models
├── exceptions.py        # Custom exceptions
├── utils.py             # Helper functions
└── backend.py           # Backend utilities
```

## API Reference

### Session Management

All session operations require a unique session ID to identify the WhatsApp session.

#### Start Session

```python
# Start a new WhatsApp session
response = api.start_session(session_id: str)
# Returns: StartSessionResponse with sessionId and success status

# Example
session_response = api.start_session("my-bot-session")
print(f"Session ID: {session_response.sessionId}")
print(f"Success: {session_response.success}")
```

#### Get Session Status

```python
# Check if session is authenticated and ready
status = api.get_session_status(session_id: str)
# Returns: StatusSessionResponse

# Example
status = api.get_session_status("my-bot-session")
print(f"Authenticated: {status.authenticated}")
print(f"Ready: {status.ready}")
print(f"Status: {status.status}")
```

#### Get QR Code

```python
# Get QR code as text for terminal display
qr_response = api.get_qr_code(session_id: str)
# Returns: QRCodeResponse with qr field

# Get QR code as PNG image data
qr_image_bytes = api.get_qr_code_image(session_id: str)
# Returns: bytes (PNG image data)

# Example
qr = api.get_qr_code("my-bot-session")
print("Scan this QR code with WhatsApp:")
print(qr.qr)

# Save QR as image file
qr_image = api.get_qr_code_image("my-bot-session")
with open("qr_code.png", "wb") as f:
    f.write(qr_image)
```

#### Session Cleanup

```python
# Restart an existing session
restart_response = api.restart_session(session_id: str)

# Terminate a specific session
terminate_response = api.terminate_session(session_id: str)

# Terminate all inactive sessions
api.terminate_inactive_sessions()

# Terminate all sessions (use with caution!)
api.terminate_all_sessions()
```

### Messaging

#### Text Messages

```python
from wrapper.models import SendMessageRequest

# Simple text message
request = SendMessageRequest(
    chatId="1234567890@c.us",  # Phone number with @c.us
    content="Hello World! 👋",
    contentType="string"
)
response = api.send_message(session_id, request)
print(f"Message sent: {response.success}, ID: {response.messageId}")

# Message with formatting
formatted_request = SendMessageRequest(
    chatId="1234567890@c.us",
    content="*Bold text* _italic text_ ~strikethrough~ ```code```",
    contentType="string"
)
api.send_message(session_id, formatted_request)
```

#### Media Messages

```python
import base64

# Send image
with open("photo.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

image_request = SendMessageRequest(
    chatId="1234567890@c.us",
    content={
        "mimetype": "image/jpeg",
        "data": image_data,
        "filename": "photo.jpg",
        "caption": "Check out this photo!"
    },
    contentType="MessageMedia"
)
api.send_message(session_id, image_request)

# Send document
with open("document.pdf", "rb") as f:
    doc_data = base64.b64encode(f.read()).decode()

doc_request = SendMessageRequest(
    chatId="1234567890@c.us",
    content={
        "mimetype": "application/pdf",
        "data": doc_data,
        "filename": "document.pdf"
    },
    contentType="MessageMedia"
)
api.send_message(session_id, doc_request)

# Send audio
audio_request = SendMessageRequest(
    chatId="1234567890@c.us",
    content={
        "mimetype": "audio/ogg; codecs=opus",
        "data": audio_base64_data,
        "filename": "voice_note.ogg"
    },
    contentType="MessageMedia"
)
api.send_message(session_id, audio_request)
```

#### Location Messages

```python
location_request = SendMessageRequest(
    chatId="1234567890@c.us",
    content={
        "latitude": 37.7749,
        "longitude": -122.4194,
        "description": "San Francisco, CA"
    },
    contentType="Location"
)
api.send_message(session_id, location_request)
```

#### Contact Messages

```python
contact_request = SendMessageRequest(
    chatId="1234567890@c.us",
    content={
        "displayName": "John Doe",
        "vcard": "BEGIN:VCARD\nVERSION:3.0\nFN:John Doe\nTEL:+1234567890\nEND:VCARD"
    },
    contentType="Contact"
)
api.send_message(session_id, contact_request)
```

#### Message Reactions

```python
from wrapper.models import MessageReactionRequest

reaction_request = MessageReactionRequest(
    chatId="1234567890@c.us",
    messageId="message_id_here",
    reaction="👍"  # Use emoji or empty string to remove reaction
)
api.react_to_message(session_id, reaction_request)
```

#### Message Operations

```python
from wrapper.models import (
    DeleteMessageRequest,
    ForwardMessageRequest,
    DownloadMediaRequest
)

# Delete a message
delete_request = DeleteMessageRequest(
    chatId="1234567890@c.us",
    messageId="message_id_to_delete"
)
api.delete_message(session_id, delete_request)

# Forward a message
forward_request = ForwardMessageRequest(
    fromChatId="1234567890@c.us",
    toChatId="0987654321@c.us",
    messageId="message_id_to_forward"
)
api.forward_message(session_id, forward_request)

# Download media from a message
download_request = DownloadMediaRequest(
    chatId="1234567890@c.us",
    messageId="message_id_with_media"
)
media_data = api.download_media(session_id, download_request)
```

### Chat Management

#### Get Chats

```python
# Get all chats
chats_response = api.get_chats(session_id)
print(f"Total chats: {len(chats_response.chats)}")

for chat in chats_response.chats:
    print(f"Chat: {chat.name} ({chat.id})")
    print(f"  Type: {chat.type}")
    print(f"  Unread: {chat.unreadCount}")
    print(f"  Last message: {chat.lastMessage}")
```

#### Get Specific Chat

```python
from wrapper.models import GetChatByIdRequest

chat_request = GetChatByIdRequest(chatId="1234567890@c.us")
chat = api.get_chat_by_id(session_id, chat_request)
print(f"Chat name: {chat.name}")
print(f"Participants: {len(chat.participants)}")
```

#### Chat Actions

```python
from wrapper.models import (
    ArchiveChatRequest,
    MuteChatRequest,
    PinChatRequest,
    ClearMessagesRequest
)

# Archive/unarchive chat
archive_request = ArchiveChatRequest(chatId="1234567890@c.us")
api.archive_chat(session_id, archive_request)
api.unarchive_chat(session_id, archive_request)

# Mute/unmute chat
mute_request = MuteChatRequest(chatId="1234567890@c.us", duration=3600)  # 1 hour
api.mute_chat(session_id, mute_request)
api.unmute_chat(session_id, mute_request)

# Pin/unpin chat
pin_request = PinChatRequest(chatId="1234567890@c.us")
api.pin_chat(session_id, pin_request)
api.unpin_chat(session_id, pin_request)

# Clear chat messages
clear_request = ClearMessagesRequest(chatId="1234567890@c.us")
api.clear_messages(session_id, clear_request)
```

#### Message History

```python
from wrapper.models import (
    FetchMessagesRequest,
    SearchMessagesRequest
)

# Fetch recent messages
fetch_request = FetchMessagesRequest(
    chatId="1234567890@c.us",
    limit=50
)
messages = api.fetch_messages(session_id, fetch_request)

# Search messages
search_request = SearchMessagesRequest(
    chatId="1234567890@c.us",
    query="important",
    limit=20
)
search_results = api.search_messages(session_id, search_request)
```

### Contact Management

#### Get Contacts

```python
# Get all contacts
contacts_response = api.get_contacts(session_id)
print(f"Total contacts: {len(contacts_response.contacts)}")

for contact in contacts_response.contacts:
    print(f"Contact: {contact.name} ({contact.number})")
    print(f"  WhatsApp ID: {contact.id}")
    print(f"  Is business: {contact.isBusiness}")
```

#### Contact Operations

```python
from wrapper.models import (
    GetContactByIdRequest,
    BlockContactRequest,
    IsRegisteredUserRequest,
    GetNumberIdRequest,
    GetProfilePicUrlRequest
)

# Get specific contact
contact_request = GetContactByIdRequest(contactId="1234567890@c.us")
contact = api.get_contact_by_id(session_id, contact_request)

# Block/unblock contact
block_request = BlockContactRequest(contactId="1234567890@c.us")
api.block_contact(session_id, block_request)
api.unblock_contact(session_id, block_request)

# Get blocked contacts
blocked = api.get_blocked_contacts(session_id)

# Check if number is registered on WhatsApp
check_request = IsRegisteredUserRequest(number="1234567890")
is_registered = api.is_registered_user(session_id, check_request)

# Get WhatsApp ID for phone number
id_request = GetNumberIdRequest(number="1234567890")
number_id = api.get_number_id(session_id, id_request)

# Get profile picture URL
pic_request = GetProfilePicUrlRequest(contactId="1234567890@c.us")
pic_url = api.get_profile_pic_url(session_id, pic_request)
```

### Group Management

#### Create and Manage Groups

```python
from wrapper.models import (
    CreateGroupRequest,
    AddParticipantsRequest,
    RemoveParticipantsRequest,
    PromoteParticipantsRequest,
    DemoteParticipantsRequest
)

# Create a group
group_request = CreateGroupRequest(
    name="Python Developers",
    participants=["1234567890@c.us", "0987654321@c.us"]
)
group_response = api.create_group(session_id, group_request)
group_id = group_response.groupId

# Add participants
add_request = AddParticipantsRequest(
    chatId=group_id,
    participants=["1111111111@c.us", "2222222222@c.us"]
)
api.add_participants(session_id, add_request)

# Remove participants
remove_request = RemoveParticipantsRequest(
    chatId=group_id,
    participants=["1111111111@c.us"]
)
api.remove_participants(session_id, remove_request)

# Promote to admin
promote_request = PromoteParticipantsRequest(
    chatId=group_id,
    participants=["0987654321@c.us"]
)
api.promote_participants(session_id, promote_request)

# Demote from admin
demote_request = DemoteParticipantsRequest(
    chatId=group_id,
    participants=["0987654321@c.us"]
)
api.demote_participants(session_id, demote_request)
```

#### Group Settings

```python
from wrapper.models import (
    GetInviteCodeRequest,
    RevokeInviteRequest,
    LeaveGroupRequest,
    SetGroupSubjectRequest,
    SetGroupDescriptionRequest,
    SetGroupPictureRequest
)

# Get group invite link
invite_request = GetInviteCodeRequest(chatId=group_id)
invite_code = api.get_invite_code(session_id, invite_request)
print(f"Invite link: https://chat.whatsapp.com/{invite_code.inviteCode}")

# Revoke group invite
revoke_request = RevokeInviteRequest(chatId=group_id)
api.revoke_invite(session_id, revoke_request)

# Leave group
leave_request = LeaveGroupRequest(chatId=group_id)
api.leave_group(session_id, leave_request)

# Update group name
name_request = SetGroupSubjectRequest(
    chatId=group_id,
    subject="Advanced Python Developers"
)
api.set_group_subject(session_id, name_request)

# Update group description
desc_request = SetGroupDescriptionRequest(
    chatId=group_id,
    description="A group for Python developers to share knowledge and tips"
)
api.set_group_description(session_id, desc_request)

# Set group picture
with open("group_photo.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

pic_request = SetGroupPictureRequest(
    chatId=group_id,
    image=image_data
)
api.set_group_picture(session_id, pic_request)
```

### Profile Management

#### Update Profile

```python
from wrapper.models import (
    SetStatusRequest,
    SetDisplayNameRequest,
    SetProfilePictureRequest
)

# Update status message
status_request = SetStatusRequest(status="Available for Python consulting 🐍")
api.set_status(session_id, status_request)

# Update display name
name_request = SetDisplayNameRequest(displayName="Python Bot")
api.set_display_name(session_id, name_request)

# Update profile picture
with open("profile.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

pic_request = SetProfilePictureRequest(image=image_data)
api.set_profile_picture(session_id, pic_request)
```

#### Presence Management

```python
from wrapper.models import (
    SendPresenceAvailableRequest,
    SendPresenceUnavailableRequest
)

# Set as available
available_request = SendPresenceAvailableRequest(chatId="1234567890@c.us")
api.send_presence_available(session_id, available_request)

# Set as unavailable
unavailable_request = SendPresenceUnavailableRequest(chatId="1234567890@c.us")
api.send_presence_unavailable(session_id, unavailable_request)
```

### Chat State Management

#### Message Status

```python
from wrapper.models import (
    SendSeenRequest,
    SendStateTypingRequest,
    SendStateRecordingRequest
)

# Mark messages as seen/read
seen_request = SendSeenRequest(chatId="1234567890@c.us")
api.send_seen(session_id, seen_request)

# Send typing indicator
typing_request = SendStateTypingRequest(chatId="1234567890@c.us")
api.send_state_typing(session_id, typing_request)

# Send recording indicator (for voice messages)
recording_request = SendStateRecordingRequest(chatId="1234567890@c.us")
api.send_state_recording(session_id, recording_request)
```


## Advanced Usage

### Context Manager

```python
with WhatsAppAPI(api_key="your-key") as api:
    session_id = "context-session"
    api.start_session(session_id)
    
    # Do work...
    api.send_message(session_id, message_request)
    
    # Session automatically terminated on exit
```

### Custom HTTP Client

```python
import httpx

# Custom client with specific configuration
custom_client = httpx.Client(
    timeout=60.0,
    headers={"User-Agent": "My-Custom-Agent"},
    verify=False  # Disable SSL verification if needed
)

api = WhatsAppAPI(
    api_key="your-key",
    session=custom_client
)
```

### Retry Configuration

```python
api = WhatsAppAPI(
    api_key="your-key",
    max_retries=5,
    backoff_factor=2.0,  # Exponential backoff
    timeout=45
)
```

### Logging Configuration

```python
import logging

# Configure detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("wrapper")
logger.setLevel(logging.DEBUG)

# Use the API with detailed logs
api = WhatsAppAPI(api_key="your-key")
```

## Error Handling

### Exception Hierarchy

```python
try:
    response = api.send_message(session_id, request)
except WhatsAppTimeoutError as e:
    print(f"Request timed out: {e}")
    # Implement retry logic
except WhatsAppRateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after} seconds")
    time.sleep(e.retry_after)
except WhatsAppAuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check API key
except WhatsAppSessionError as e:
    print(f"Session error: {e}")
    # Restart session
except WhatsAppValidationError as e:
    print(f"Validation error: {e}")
    # Check request data
except WhatsAppConnectionError as e:
    print(f"Connection error: {e}")
    # Check server availability
except WhatsAppHTTPError as e:
    print(f"HTTP error {e.status_code}: {e}")
    # Handle specific HTTP errors
except WhatsAppAPIError as e:
    print(f"General API error: {e}")
    # Handle any other API errors
```

### Error Recovery Patterns

#### Automatic Session Recovery

```python
def robust_send_message(api, session_id, message_request, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return api.send_message(session_id, message_request)
        except WhatsAppSessionError:
            if attempt < max_attempts - 1:
                # Restart session and try again
                api.restart_session(session_id)
                time.sleep(5)  # Wait for session to be ready
            else:
                raise
```

#### Rate Limit Handling

```python
def send_with_rate_limit_handling(api, session_id, message_request):
    while True:
        try:
            return api.send_message(session_id, message_request)
        except WhatsAppRateLimitError as e:
            print(f"Rate limited. Waiting {e.retry_after} seconds...")
            time.sleep(e.retry_after)
```

## Best Practices

### 1. Session Management

```python
# Use descriptive session IDs
session_id = f"user_{user_id}_{timestamp}"

# Monitor session status
def ensure_session_ready(api, session_id, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        status = api.get_session_status(session_id)
        if status.status == "CONNECTED":
            return True
        time.sleep(2)
    return False

# Always clean up sessions
try:
    api.start_session(session_id)
    # Do work...
finally:
    api.terminate_session(session_id)
```

### 2. Message Handling

```python
# Validate phone numbers before sending
def send_safe_message(api, session_id, phone_number, content):
    # Format phone number
    chat_id = f"{phone_number.replace('+', '')}@c.us"
    
    # Check if registered
    is_registered = api.is_registered_user(
        session_id, 
        IsRegisteredRequest(number=phone_number)
    )
    
    if not is_registered.isRegistered:
        raise ValueError(f"Number {phone_number} is not registered on WhatsApp")
    
    # Send message
    request = SendMessageRequest(
        chatId=chat_id,
        content=content,
        contentType="string"
    )
    return api.send_message(session_id, request)
```

### 3. Bulk Operations

```python
def send_bulk_messages(api, session_id, recipients, message_content):
    results = []
    
    for recipient in recipients:
        try:
            request = SendMessageRequest(
                chatId=f"{recipient}@c.us",
                content=message_content,
                contentType="string"
            )
            response = api.send_message(session_id, request)
            results.append({
                "recipient": recipient,
                "success": True,
                "message_id": response.messageId
            })
            
            # Rate limiting
            time.sleep(1)  # Wait 1 second between messages
            
        except Exception as e:
            results.append({
                "recipient": recipient,
                "success": False,
                "error": str(e)
            })
    
    return results
```

### 4. Configuration Management

```python
import os
from dataclasses import dataclass

@dataclass
class WhatsAppConfig:
    api_key: str
    base_url: str = "http://localhost:3000"
    timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_env(cls):
        return cls(
            api_key=os.getenv("WHATSAPP_API_KEY"),
            base_url=os.getenv("WHATSAPP_BASE_URL", "http://localhost:3000"),
            timeout=int(os.getenv("WHATSAPP_TIMEOUT", "30")),
            max_retries=int(os.getenv("WHATSAPP_MAX_RETRIES", "3"))
        )

# Usage
config = WhatsAppConfig.from_env()
api = WhatsAppAPI(**config.__dict__)
```

## Testing

### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch
from wrapper import WhatsAppAPI
from wrapper.models import SendMessageRequest

def test_send_message_success():
    # Mock HTTP response
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "data": {"messageId": "msg_123"}
    }
    mock_response.status_code = 200
    
    with patch.object(WhatsAppAPI, '_request', return_value=mock_response):
        api = WhatsAppAPI(api_key="test-key")
        request = SendMessageRequest(
            chatId="test@c.us",
            content="test message",
            contentType="string"
        )
        
        response = api.send_message("test-session", request)
        assert response.success == True
        assert response.messageId == "msg_123"
```

### Integration Tests

```python
import pytest
from wrapper import WhatsAppAPI

@pytest.mark.integration
def test_session_lifecycle():
    api = WhatsAppAPI(api_key=os.getenv("TEST_API_KEY"))
    session_id = f"test_session_{int(time.time())}"
    
    try:
        # Start session
        start_response = api.start_session(session_id)
        assert start_response.sessionId == session_id
        
        # Get status
        status = api.get_session_status(session_id)
        assert status.status in ["STARTING", "QR_CODE", "CONNECTED"]
        
    finally:
        # Clean up
        api.terminate_session(session_id)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wrapper

# Run only unit tests
pytest -m unit

# Run only integration tests (requires running API server)
pytest -m integration

# Run specific test file
pytest tests/unit/test_client.py -v
```

## Examples

### Example 1: Simple Message Bot

```python
#!/usr/bin/env python3
"""
Simple WhatsApp message bot that responds to incoming messages.
"""

import time
from wrapper import WhatsAppAPI
from wrapper.models import SendMessageRequest

def message_bot():
    api = WhatsAppAPI(api_key="your-api-key")
    session_id = "bot-session"
    
    try:
        # Start session
        api.start_session(session_id)
        
        # Wait for QR code scan
        print("Please scan the QR code to connect WhatsApp")
        while True:
            status = api.get_session_status(session_id)
            if status.authenticated:
                print("WhatsApp connected!")
                break
            time.sleep(5)
        
        # Bot logic would go here
        # In a real implementation, you'd set up webhooks
        # to receive incoming messages
        
        print("Bot is running... Press Ctrl+C to stop")
        while True:
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("Stopping bot...")
    finally:
        api.terminate_session(session_id)

if __name__ == "__main__":
    message_bot()
```

### Example 2: Bulk Message Sender

```python
#!/usr/bin/env python3
"""
Bulk message sender with CSV input.
"""

import csv
import time
from wrapper import WhatsAppAPI
from wrapper.models import SendMessageRequest, IsRegisteredRequest

def send_bulk_messages_from_csv(csv_file, message_template):
    api = WhatsAppAPI(api_key="your-api-key")
    session_id = "bulk-sender"
    
    try:
        # Start session
        api.start_session(session_id)
        
        # Wait for connection
        print("Waiting for WhatsApp connection...")
        while True:
            status = api.get_session_status(session_id)
            if status.status == "CONNECTED":
                break
            time.sleep(5)
        
        # Read CSV and send messages
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                phone = row['phone']
                name = row['name']
                
                # Personalize message
                message = message_template.format(name=name)
                
                try:
                    # Check if number is registered
                    is_registered = api.is_registered_user(
                        session_id,
                        IsRegisteredRequest(number=phone)
                    )
                    
                    if not is_registered.isRegistered:
                        print(f"Skipping {phone} - not registered")
                        continue
                    
                    # Send message
                    request = SendMessageRequest(
                        chatId=f"{phone}@c.us",
                        content=message,
                        contentType="string"
                    )
                    
                    response = api.send_message(session_id, request)
                    print(f"Message sent to {name} ({phone}): {response.success}")
                    
                    # Rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Failed to send to {name} ({phone}): {e}")
                    
    finally:
        api.terminate_session(session_id)

# Usage
if __name__ == "__main__":
    message_template = "Hello {name}! This is a test message."
    send_bulk_messages_from_csv("contacts.csv", message_template)
```

### Example 3: Group Management

```python
#!/usr/bin/env python3
"""
Group management example.
"""

from wrapper import WhatsAppAPI
from wrapper.models import CreateGroupRequest, GroupActionRequest

def manage_group():
    api = WhatsAppAPI(api_key="your-api-key")
    session_id = "group-manager"
    
    try:
        api.start_session(session_id)
        
        # Create group
        create_request = CreateGroupRequest(
            name="Python Developers",
            participants=[
                "1234567890@c.us",
                "0987654321@c.us"
            ]
        )
        
        group_response = api.create_group(session_id, create_request)
        group_id = group_response.groupId
        print(f"Group created: {group_id}")
        
        # Add more participants
        add_request = GroupActionRequest(
            chatId=group_id,
            participants=["1111111111@c.us"]
        )
        api.add_participants(session_id, add_request)
        
        # Set group description
        from wrapper.models import SetGroupDescriptionRequest
        desc_request = SetGroupDescriptionRequest(
            chatId=group_id,
            description="A group for Python developers to share knowledge and collaborate."
        )
        api.set_group_description(session_id, desc_request)
        
        print("Group setup completed!")
        
    finally:
        api.terminate_session(session_id)

if __name__ == "__main__":
    manage_group()
```

### Example 4: Media Message Sender

```python
#!/usr/bin/env python3
"""
Send media messages (images, documents, etc.).
"""

import base64
from wrapper import WhatsAppAPI
from wrapper.models import SendMessageRequest

def send_media_message():
    api = WhatsAppAPI(api_key="your-api-key")
    session_id = "media-sender"
    
    try:
        api.start_session(session_id)
        
        # Send image
        with open("image.jpg", "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
        
        image_request = SendMessageRequest(
            chatId="1234567890@c.us",
            content={
                "mimetype": "image/jpeg",
                "data": img_data,
                "filename": "image.jpg",
                "caption": "Check out this image!"
            },
            contentType="MessageMedia"
        )
        
        response = api.send_message(session_id, image_request)
        print(f"Image sent: {response.success}")
        
        # Send document
        with open("document.pdf", "rb") as doc_file:
            doc_data = base64.b64encode(doc_file.read()).decode()
        
        doc_request = SendMessageRequest(
            chatId="1234567890@c.us",
            content={
                "mimetype": "application/pdf",
                "data": doc_data,
                "filename": "document.pdf"
            },
            contentType="MessageMedia"
        )
        
        response = api.send_message(session_id, doc_request)
        print(f"Document sent: {response.success}")
        
    finally:
        api.terminate_session(session_id)

if __name__ == "__main__":
    send_media_message()
```

## Troubleshooting

### Common Issues

#### 1. Session Not Starting

```python
# Check if API server is running
import requests
try:
    response = requests.get("http://localhost:3000/health")
    print(f"API server status: {response.status_code}")
except:
    print("API server is not running")
```

#### 2. Authentication Errors

```python
# Verify API key
api = WhatsAppAPI(api_key="your-key")
try:
    sessions = api.get_all_sessions()
    print("API key is valid")
except WhatsAppAuthenticationError:
    print("Invalid API key")
```

#### 3. Message Delivery Issues

```python
# Check if number is registered
def verify_number(api, session_id, phone_number):
    try:
        result = api.is_registered_user(
            session_id,
            IsRegisteredRequest(number=phone_number)
        )
        return result.isRegistered
    except Exception as e:
        print(f"Error checking number: {e}")
        return False
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create API client with debug info
api = WhatsAppAPI(
    api_key="your-key",
    timeout=60,  # Longer timeout for debugging
    max_retries=1  # Disable retries to see errors immediately
)
```

This comprehensive guide covers all aspects of using the WhatsApp API Python Wrapper. For more specific use cases or advanced configurations, refer to the API documentation or create custom implementations based on these examples.
