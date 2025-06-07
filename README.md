# WhatsApp API Python Wrapper

A comprehensive, production-ready Python wrapper around the WhatsApp Web API that provides strongly-typed interfaces, comprehensive error handling, automatic retries, and full test coverage.

[![Python Version](https://img.shields.io/pypi/pyversions/whatsapp-api-py)](https://pypi.org/project/whatsapp-api-py/)
[![PyPI Version](https://img.shields.io/pypi/v/whatsapp-api-py)](https://pypi.org/project/whatsapp-api-py/)
[![License](https://img.shields.io/pypi/l/whatsapp-api-py)](https://github.com/a3ro-dev/whatsapp_api_wrapper/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-green)](https://github.com/a3ro-dev/whatsapp_api_wrapper/actions)

## About This Project

This project is a Python wrapper for the Node.js-based WhatsApp REST API located in the [`whatsapp-api/`](../whatsapp-api/) directory. The underlying API is a REST wrapper for the [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) library, designed to be used as a Docker container and to provide easy integration with non-Node.js projects.

### Underlying WhatsApp API

The core WhatsApp API server (located in [`whatsapp-api/`](whatsapp-api/)) provides:

- **REST API Endpoints**: Complete WhatsApp Web functionality via HTTP endpoints
- **Docker Support**: Ready-to-use Docker container for easy deployment
- **Session Management**: Multiple WhatsApp sessions with QR code authentication
- **Media Support**: Send/receive images, videos, documents, and audio files
- **Group Management**: Create groups, manage participants, and handle group settings
- **Real-time Callbacks**: WebSocket callbacks for incoming messages and status changes

For detailed information about setting up and running the underlying API server, see the [WhatsApp API README](whatsapp-api/README.md).

### Prerequisites

Before using this Python wrapper, you need to have the WhatsApp API server running:

```bash
# Navigate to the WhatsApp API directory
cd whatsapp-api

# Run with Docker Compose
docker-compose pull && docker-compose up
```

The API server will be available at `http://localhost:3000` with documentation at `http://localhost:3000/api-docs/`.

#### API Server Features

The underlying WhatsApp API server supports a comprehensive range of WhatsApp Web functionalities:

**Messaging:**
- Send text, image, video, audio, and document messages
- Send contact and location messages
- Send button and list messages
- Message reactions and replies
- Download media attachments

**Session Management:**
- Multiple concurrent WhatsApp sessions
- QR code authentication
- Session health monitoring
- Automatic session recovery

**Chat & Contact Management:**
- Retrieve all chats and contacts
- Block/unblock contacts
- Archive/unarchive chats
- Check if number is registered on WhatsApp

**Group Operations:**
- Create and manage groups
- Add/remove participants
- Promote/demote administrators
- Group invite management

**Profile & Status:**
- Update profile picture and status
- Get user presence information
- Send typing/recording indicators

For a complete list of available endpoints and features, visit the API documentation at `http://localhost:3000/api-docs/` when the server is running.

## Features

- 🚀 **Full API Coverage**: Complete implementation of all WhatsApp Web API endpoints
- 🔒 **Type Safety**: Fully typed with Pydantic models for request/response validation
- 🛡️ **Error Handling**: Comprehensive error handling with custom exceptions
- 🔄 **Automatic Retries**: Built-in retry logic with exponential backoff for transient failures
- 📊 **Logging**: Detailed logging for debugging and monitoring
- 🧪 **Well Tested**: Comprehensive test suite with unit and integration tests
- 📖 **Documentation**: Complete API documentation and examples

## Architecture

This Python wrapper is built with the following key components:

- **HTTP Client**: Uses `httpx` for robust HTTP communication with retry mechanisms
- **Data Validation**: `Pydantic` models ensure type safety for all requests and responses
- **Error Handling**: Custom exception hierarchy for different error types
- **Retry Logic**: `tenacity` library provides automatic retries with exponential backoff
- **Testing**: Comprehensive test suite using `pytest` with unit and integration tests

### Package Structure

```
whatsapp_api_wrapper/
├── __init__.py         # Main package exports
├── client.py           # WhatsAppAPI client class
├── models.py           # Pydantic models for requests & responses
├── exceptions.py       # Custom exception classes
├── utils.py            # Utility functions and helpers
└── py.typed           # Type hints marker file
tests/                  # Pytest test suites
├── unit/              # Unit tests
└── integration/       # Integration tests
```

## Installation

### From PyPI (Recommended)

```bash
pip install whatsapp-api-py
```

### From Source

```bash
# Clone the repository
git clone https://github.com/a3ro-dev/whatsapp_api_wrapper.git
cd whatsapp_api_wrapper/whatsapp-api-py

# Install the package
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install all optional dependencies
pip install -e ".[all]"
```

## Quick Start

```python
from whatsapp_api_wrapper import WhatsAppAPI
from whatsapp_api_wrapper.models import TextMessage

# Initialize the client
api = WhatsAppAPI(
    api_key="your-api-key",  # Optional, can be None for local development
    base_url="http://localhost:3000"  # Your WhatsApp API server URL
)

# Start a session
session_id = "my-session-123"
session_status = api.start_session(session_id)
print(f"Session started: {session_status.success}")

# Get QR code for initial setup
qr_response = api.get_qr_code(session_id)
print(f"QR Code: {qr_response.qr}")

# Send a text message
message_request = TextMessage(
    to="1234567890@c.us",  # Phone number with @c.us suffix
    body="Hello from Python!"
)
response = api.send_message(session_id, message_request)
print(f"Message sent: {response.success}, ID: {response.messageId}")

# Get all chats
chats = api.get_chats(session_id)
for chat in chats.chats:
    print(f"Chat: {chat.name} ({chat.id})")

# Get all contacts
contacts = api.get_contacts(session_id)
for contact in contacts.contacts:
    print(f"Contact: {contact.name} ({contact.number})")
```

## Advanced Usage

### Media Messages

```python
from whatsapp_api_wrapper.models import MediaMessage

# Send an image
media_request = MediaMessage(
    to="1234567890@c.us",
    media="base64-encoded-image-data",  # or URL to image
    type="image",
    caption="Check out this photo!",
    filename="photo.jpg"
)
response = api.send_message(session_id, media_request)
```

### Group Management

```python
from whatsapp_api_wrapper.models import GroupActionRequest

# Create a group
group_request = GroupActionRequest(
    name="My Python Group",
    participants=["1234567890@c.us", "0987654321@c.us"]
)
group_response = api.create_group(session_id, group_request)

# Add participants to the group
add_request = GroupActionRequest(
    chatId=group_response.groupId,
    participants=["1111111111@c.us"]
)
api.add_participants(session_id, add_request)
```

### Error Handling

```python
from whatsapp_api_wrapper.exceptions import (
    WhatsAppAPIError,
    WhatsAppConnectionError,
    WhatsAppHTTPError,
    WhatsAppSessionError,
    WhatsAppRateLimitError
)

try:
    response = api.send_message(session_id, message_request)
except WhatsAppSessionError as e:
    print(f"Session error: {e.message}")
except WhatsAppRateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after} seconds")
except WhatsAppConnectionError as e:
    print(f"Connection failed: {e.message}")
except WhatsAppHTTPError as e:
    print(f"HTTP error {e.status_code}: {e.message}")
except WhatsAppAPIError as e:
    print(f"API error: {e.message}")
```

### Context Manager

```python
# Use as a context manager for automatic cleanup
with WhatsAppAPI(base_url="http://localhost:3000") as api:
    api.start_session(session_id)
    # ... do work ...
# Session automatically closed
```

### Custom Configuration

```python
import httpx

# Custom HTTP client with specific timeout and headers
custom_client = httpx.Client(
    timeout=60.0,
    headers={"User-Agent": "My-Custom-Agent"}
)

api = WhatsAppAPI(
    api_key="your-api-key",
    base_url="http://localhost:3000",
    timeout=60,
    max_retries=5,
    backoff_factor=2.0,
    session=custom_client
)
)
```

## API Reference

### Session Management

- `start_session(session_id)` - Start a new WhatsApp session
- `get_session_status(session_id)` - Get session status
- `get_qr_code(session_id)` - Get QR code for session setup
- `get_qr_code_image(session_id)` - Get QR code as PNG image
- `restart_session(session_id)` - Restart a session
- `terminate_session(session_id)` - Terminate a session
- `terminate_inactive_sessions()` - Terminate all inactive sessions
- `terminate_all_sessions()` - Terminate all sessions

### Messaging

- `send_message(session_id, request)` - Send various types of messages
- `delete_message(session_id, request)` - Delete a message
- `forward_message(session_id, request)` - Forward a message
- `react_to_message(session_id, request)` - React to a message
- `download_media(session_id, request)` - Download media from a message

### Chat Management

- `get_chats(session_id)` - Get all chats
- `get_chat_by_id(session_id, request)` - Get specific chat
- `archive_chat(session_id, request)` - Archive a chat
- `unarchive_chat(session_id, request)` - Unarchive a chat
- `mute_chat(session_id, request)` - Mute a chat
- `unmute_chat(session_id, request)` - Unmute a chat
- `pin_chat(session_id, request)` - Pin a chat
- `unpin_chat(session_id, request)` - Unpin a chat
- `clear_messages(session_id, request)` - Clear chat messages
- `delete_chat(session_id, request)` - Delete a chat
- `fetch_messages(session_id, request)` - Fetch chat messages
- `search_messages(session_id, request)` - Search messages

### Contact Management

- `get_contacts(session_id)` - Get all contacts
- `get_contact_by_id(session_id, request)` - Get specific contact
- `block_contact(session_id, request)` - Block a contact
- `unblock_contact(session_id, request)` - Unblock a contact
- `get_blocked_contacts(session_id)` - Get blocked contacts
- `is_registered_user(session_id, request)` - Check if number is registered
- `get_number_id(session_id, request)` - Get WhatsApp ID for number
- `get_profile_pic_url(session_id, request)` - Get profile picture URL
- `get_contact_about(session_id, request)` - Get contact's about text

### Group Management

- `create_group(session_id, request)` - Create a new group
- `add_participants(session_id, request)` - Add group participants
- `remove_participants(session_id, request)` - Remove group participants
- `promote_participants(session_id, request)` - Promote to admin
- `demote_participants(session_id, request)` - Demote from admin
- `get_invite_code(session_id, request)` - Get group invite code
- `revoke_invite(session_id, request)` - Revoke group invite
- `leave_group(session_id, request)` - Leave a group
- `set_group_subject(session_id, request)` - Set group name
- `set_group_description(session_id, request)` - Set group description
- `set_group_picture(session_id, request)` - Set group picture
- `delete_group_picture(session_id, request)` - Delete group picture

### Profile Management

- `set_status(session_id, request)` - Set status message
- `set_display_name(session_id, request)` - Set display name
- `set_profile_picture(session_id, request)` - Set profile picture
- `send_presence_available(session_id, request)` - Set presence as available
- `send_presence_unavailable(session_id, request)` - Set presence as unavailable

### State Management

- `send_seen(session_id, request)` - Mark messages as seen
- `send_state_typing(session_id, request)` - Send typing indicator
- `send_state_recording(session_id, request)` - Send recording indicator

## Error Handling

The wrapper provides comprehensive error handling with specific exception types:

- `WhatsAppAPIError` - Base exception for all API errors
- `WhatsAppConnectionError` - Network connectivity issues
- `WhatsAppHTTPError` - HTTP errors (4xx, 5xx status codes)
- `WhatsAppValidationError` - Request/response validation errors
- `WhatsAppSessionError` - Session-related errors
- `WhatsAppRateLimitError` - Rate limiting errors (429 status)
- `WhatsAppAuthenticationError` - Authentication errors (403 status)
- `WhatsAppNotFoundError` - Resource not found errors (404 status)

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=whatsapp_api_wrapper

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/a3ro-dev/whatsapp_api_wrapper.git
cd whatsapp_api_wrapper/whatsapp-api-py

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code formatting

```bash
# Format code
black whatsapp_api_wrapper/ tests/
isort whatsapp_api_wrapper/ tests/

# Type checking
mypy whatsapp_api_wrapper/

# Linting
flake8 whatsapp_api_wrapper/ tests/
```

## Requirements

- **Python 3.10+**
- **WhatsApp Web API server** (from [`../whatsapp-api/`](../whatsapp-api/) directory) running at `http://localhost:3000`
  - This is the underlying Node.js API that this wrapper communicates with
  - Must be running before using this Python wrapper
- Optional: API key for authentication

### Starting the Required API Server

```bash
# Navigate to the WhatsApp API directory (from the project root)
cd ../whatsapp-api

# Start the API server with Docker
docker-compose pull && docker-compose up

# The server will be available at http://localhost:3000
# API documentation will be at http://localhost:3000/api-docs/
```

## Dependencies

- `httpx` - Modern HTTP client
- `pydantic` - Data validation and serialization
- `tenacity` - Retry logic with exponential backoff

## Future Enhancements

- **Bulk Operations**: Enhanced support for bulk message sending with rate limiting and queue management
- **Concurrency**: Improved concurrent session handling for high-throughput applications
- **Async Support**: Full async/await support using `httpx.AsyncClient` for better performance
- **Advanced Retry Strategies**: Configurable retry strategies for different error types
- **Webhook Support**: Built-in webhook handling for real-time message callbacks
- **Message Templates**: Template system for common message types and formats

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**IMPORTANT**: This wrapper uses WhatsApp Web protocol through the underlying API server. WhatsApp does not allow bots or unofficial clients on their platform. Use this wrapper at your own risk - there's no guarantee you won't be blocked by WhatsApp for using unofficial API methods.

This project is for educational and development purposes. Always comply with WhatsApp's Terms of Service and local regulations when using this tool.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Disclaimer

This project is not affiliated with WhatsApp or Meta. Use at your own risk and ensure compliance with WhatsApp's Terms of Service.
