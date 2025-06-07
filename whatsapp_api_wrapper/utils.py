"""
Utility functions for the WhatsApp API wrapper.
"""

import re
import time
import uuid
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urljoin, quote, urlparse


def build_url(base_url: str, endpoint: str, **params) -> str:
    """
    Build a complete URL from base URL and endpoint.
    
    Args:
        base_url: Base API URL
        endpoint: API endpoint path
        **params: URL parameters to include
        
    Returns:
        Complete URL string
    """
    # Ensure base_url ends with /
    if not base_url.endswith('/'):
        base_url += '/'
    
    # Remove leading / from endpoint if present
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]
    
    url = urljoin(base_url, endpoint)
    
    # Add query parameters if provided
    if params:
        query_parts = []
        for key, value in params.items():
            if value is not None:
                query_parts.append(f"{quote(str(key))}={quote(str(value))}")
        if query_parts:
            url += "?" + "&".join(query_parts)
    
    return url


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format (alphanumeric, hyphens, underscores, dots only).
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not session_id or not session_id.strip():
        return False
    if len(session_id) > 100:
        return False
    # Allow alphanumeric, hyphens, underscores, and dots
    return bool(re.match(r'^[a-zA-Z0-9_.-]+$', session_id))


def validate_chat_id(chat_id: str) -> bool:
    """
    Validate WhatsApp chat ID format.
    
    Args:
        chat_id: Chat ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    # WhatsApp chat IDs typically end with @c.us for individual chats
    # or @g.us for group chats
    return bool(re.match(r'^\d+@[cg]\.us$', chat_id))


def validate_phone_number(phone_number: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone_number: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone_number:
        return False
    
    # Must be properly formatted WhatsApp ID with @c.us
    if phone_number.endswith('@c.us'):
        # Extract just the number part
        number_part = phone_number.replace('@c.us', '')
        
        # Handle + prefix (it's valid in WhatsApp format)
        if number_part.startswith('+'):
            number_part = number_part[1:]
        
        # Should be 4-14 digits (15 digits is too long per test)
        return bool(re.match(r'^\d{4,14}$', number_part))
    elif phone_number.endswith('@g.us'):
        # Group format, not individual phone number
        return False
    else:
        # Plain numbers without @c.us are invalid
        return False


def validate_group_id(group_id: str) -> bool:
    """
    Validate WhatsApp group ID format.
    
    Args:
        group_id: Group ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not group_id:
        return False
    
    # Group IDs have format: timestamp-timestamp@g.us
    pattern = r'^\d+-\d+@g\.us$'
    return bool(re.match(pattern, group_id))


def format_phone_number(phone_number: str) -> str:
    """
    Format phone number for WhatsApp (remove non-digits, add @c.us if needed).
    
    Args:
        phone_number: Phone number to format
        
    Returns:
        Formatted phone number with @c.us suffix
    """
    if not phone_number or not phone_number.strip():
        raise ValueError("Phone number cannot be empty")
    
    # If already formatted, return as-is
    if phone_number.endswith('@c.us'):
        return phone_number
    
    # Check for invalid characters like letters
    if re.search(r'[a-zA-Z]', phone_number):
        raise ValueError("Invalid phone number contains letters")
    
    # Remove all non-digit characters (including +)
    clean_number = re.sub(r'[^\d]', '', phone_number)
    
    # Validate length after cleaning
    if len(clean_number) < 4 or len(clean_number) > 14:
        raise ValueError("Invalid phone number length")
    
    return f"{clean_number}@c.us"


def format_group_id(group_id: str) -> str:
    """
    Format group ID for WhatsApp (add @g.us if needed).
    
    Args:
        group_id: Group ID to format
        
    Returns:
        Formatted group ID
    """
    if not group_id:
        raise ValueError("Group ID cannot be empty")
    
    # If already formatted, return as-is
    if group_id.endswith('@g.us'):
        return group_id
    
    # Check if it matches the basic pattern (timestamp-timestamp)
    if re.match(r'^\d+-\d+$', group_id):
        return f"{group_id}@g.us"
    
    raise ValueError("Invalid group ID format")


def parse_contact_id(contact_id: str) -> Dict[str, str]:
    """
    Parse WhatsApp contact ID into components.
    
    Args:
        contact_id: WhatsApp contact ID
        
    Returns:
        Dictionary with parsed components
    """
    if not contact_id or not contact_id.strip():
        raise ValueError("Contact ID cannot be empty")
    
    # Check if it's an individual contact
    if contact_id.endswith('@c.us'):
        number = contact_id.replace('@c.us', '')
        if not number:  # Empty number part
            raise ValueError("Invalid contact ID format")
        return {
            'type': 'individual',
            'number': number,
            'domain': 'c.us',
            'full_id': contact_id
        }
    
    # Check if it's a group contact
    elif contact_id.endswith('@g.us'):
        group_part = contact_id.replace('@g.us', '')
        if not group_part:  # Empty group part
            raise ValueError("Invalid contact ID format")
        return {
            'type': 'group',
            'group_id': group_part,
            'domain': 'g.us',
            'full_id': contact_id
        }
    
    else:
        raise ValueError("Invalid contact ID format")


def extract_phone_number(contact_id: str) -> str:
    """
    Extract phone number from WhatsApp contact ID.
    
    Args:
        contact_id: WhatsApp contact ID
        
    Returns:
        Phone number
    """
    if not contact_id:
        raise ValueError("Contact ID cannot be empty")
    
    if contact_id.endswith('@g.us'):
        raise ValueError("Cannot extract phone number from group ID")
    
    if contact_id.endswith('@c.us'):
        return contact_id.replace('@c.us', '')
    
    raise ValueError("Invalid contact ID format")


def clean_phone_number(phone_number: str) -> str:
    """
    Clean phone number by removing formatting characters.
    
    Args:
        phone_number: Phone number to clean
        
    Returns:
        Cleaned phone number (digits only), empty string for invalid input
    """
    if not phone_number:
        return ""
    
    # Check if input contains non-digit characters that aren't valid formatting
    # Invalid inputs like "abc" or "123abc456" should return empty string
    if re.search(r'[a-zA-Z]', phone_number):
        return ""
    
    # Remove all non-digit characters 
    cleaned = re.sub(r'[^\d]', '', phone_number)
    
    return cleaned


def sanitize_message_text(text: str, preserve_newlines: bool = False) -> str:
    """
    Sanitize message text by removing/replacing unwanted characters.
    
    Args:
        text: Text to sanitize
        preserve_newlines: Whether to preserve newline characters
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    if preserve_newlines:
        # Replace carriage returns and tabs with spaces, keep newlines
        sanitized = re.sub(r'[\r\t]', ' ', text)
    else:
        # Replace all whitespace with single spaces
        sanitized = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    return sanitized.strip()


def is_group_id(contact_id: str) -> bool:
    """
    Check if contact ID is a group ID.
    
    Args:
        contact_id: WhatsApp contact ID
        
    Returns:
        True if group ID, False otherwise
    """
    return contact_id.endswith('@g.us') if contact_id else False


def is_individual_id(contact_id: str) -> bool:
    """
    Check if contact ID is an individual ID.
    
    Args:
        contact_id: WhatsApp contact ID
        
    Returns:
        True if individual ID, False otherwise
    """
    return contact_id.endswith('@c.us') if contact_id else False


def generate_message_id() -> str:
    """
    Generate a unique message ID.
    
    Returns:
        Unique message ID
    """
    return f"msg_{uuid.uuid4().hex[:12]}"


def get_timestamp() -> int:
    """
    Get current timestamp in seconds.
    
    Returns:
        Current timestamp
    """
    return int(time.time())


def format_timestamp(timestamp: int, format_type: str = "iso") -> str:
    """
    Format timestamp to human-readable string.
    
    Args:
        timestamp: Unix timestamp
        format_type: Format type ('iso', 'human')
        
    Returns:
        Formatted timestamp string
    """
    from datetime import datetime
    
    dt = datetime.fromtimestamp(timestamp)
    
    if format_type == "iso":
        return dt.isoformat()
    elif format_type == "human":
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return str(timestamp)


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid HTTP/HTTPS URL, False otherwise
    """
    if not url:
        return False
    
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False


def create_chat_id(phone_number: str) -> str:
    """
    Create a chat ID from a phone number.
    
    Args:
        phone_number: Phone number
        
    Returns:
        WhatsApp chat ID
    """
    formatted_number = format_phone_number(phone_number)
    return f"{formatted_number}@c.us"


def extract_session_id_from_path(path: str) -> Optional[str]:
    """
    Extract session ID from API endpoint path.
    
    Args:
        path: API endpoint path
        
    Returns:
        Session ID if found, None otherwise
    """
    match = re.search(r'/([^/]+)$', path)
    return match.group(1) if match else None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    safe_chars = re.sub(r'[^\w\-_\.]', '_', filename)
    # Remove multiple consecutive underscores
    safe_chars = re.sub(r'_+', '_', safe_chars)
    # Remove leading/trailing underscores and dots
    safe_chars = safe_chars.strip('_.')
    
    return safe_chars or 'untitled'


def parse_media_type(mimetype: str) -> str:
    """
    Parse media type from MIME type.
    
    Args:
        mimetype: MIME type string
        
    Returns:
        Media type (image, video, audio, document)
    """
    if not mimetype:
        return 'document'
    
    mimetype = mimetype.lower()
    
    if mimetype.startswith('image/'):
        return 'image'
    elif mimetype.startswith('video/'):
        return 'video'
    elif mimetype.startswith('audio/'):
        return 'audio'
    else:
        return 'document'


def is_base64(data: str) -> bool:
    """
    Check if string is valid base64 encoding.
    
    Args:
        data: String to check
        
    Returns:
        True if valid base64, False otherwise
    """
    try:
        import base64
        base64.b64decode(data, validate=True)
        return True
    except Exception:
        return False


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.
    
    Args:
        filename: Filename
        
    Returns:
        File extension (without dot)
    """
    return filename.split('.')[-1].lower() if '.' in filename else ''


def build_pagination_params(page: int = 1, count: int = 20) -> Dict[str, Any]:
    """
    Build pagination parameters.
    
    Args:
        page: Page number (1-based)
        count: Items per page
        
    Returns:
        Dictionary with pagination parameters
    """
    return {
        'page': max(1, page),
        'count': max(1, min(100, count))  # Limit to reasonable range
    }


def clean_message_text(text: str) -> str:
    """
    Clean message text by removing/replacing problematic characters.
    
    Args:
        text: Original message text
        
    Returns:
        Cleaned message text
    """
    if not text:
        return ""
    
    # Remove null bytes and other control characters
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    return cleaned.strip()


def validate_emoji(emoji: str) -> bool:
    """
    Basic emoji validation.
    
    Args:
        emoji: Emoji string to validate
        
    Returns:
        True if appears to be valid emoji, False otherwise
    """
    # Very basic check - just ensure it's not empty and not too long
    return bool(emoji and len(emoji.strip()) <= 10)


def extract_error_message(response_text: str) -> str:
    """
    Extract error message from API response.
    
    Args:
        response_text: Raw response text
        
    Returns:
        Extracted error message
    """
    try:
        import json
        data = json.loads(response_text)
        return data.get('error', 'Unknown error')
    except (json.JSONDecodeError, AttributeError):
        return response_text or 'Unknown error'
