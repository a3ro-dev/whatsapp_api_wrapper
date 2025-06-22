"""
Unit tests for WhatsApp API utilities.
"""

import pytest

from whatsapp_api_wrapper.utils import (
    clean_phone_number,
    extract_phone_number,
    format_group_id,
    format_phone_number,
    format_timestamp,
    generate_message_id,
    get_timestamp,
    is_group_id,
    is_individual_id,
    parse_contact_id,
    sanitize_message_text,
    validate_group_id,
    validate_phone_number,
    validate_session_id,
    validate_url,
)


class TestValidationFunctions:
    """Test validation utility functions."""

    def test_validate_phone_number_valid(self):
        """Test phone number validation with valid numbers."""
        valid_numbers = [
            "1234567890@c.us",
            "911234567890@c.us",
            "+1234567890@c.us",
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True

    def test_validate_phone_number_invalid(self):
        """Test phone number validation with invalid numbers."""
        invalid_numbers = [
            "",
            "invalid",
            "123@c.us",  # Too short
            "123456789012345@c.us",  # Too long
            "1234567890",  # Missing @c.us
            "1234567890@g.us",  # Group format, not individual
        ]

        for number in invalid_numbers:
            assert validate_phone_number(number) is False

    def test_validate_group_id_valid(self):
        """Test group ID validation with valid IDs."""
        valid_ids = [
            "123456789-987654321@g.us",
            "111111111-222222222@g.us",
            "999999999-111111111@g.us",
        ]

        for group_id in valid_ids:
            assert validate_group_id(group_id) is True

    def test_validate_group_id_invalid(self):
        """Test group ID validation with invalid IDs."""
        invalid_ids = [
            "",
            "invalid",
            "123456789@g.us",  # Missing second part
            "123456789-987654321@c.us",  # Individual format, not group
            "123456789-987654321",  # Missing @g.us
            "abc-def@g.us",  # Non-numeric parts
        ]

        for group_id in invalid_ids:
            assert validate_group_id(group_id) is False

    def test_validate_session_id_valid(self):
        """Test session ID validation with valid IDs."""
        valid_ids = [
            "session1",
            "test-session",
            "my_session_123",
            "SESSION",
            "session.test",
        ]

        for session_id in valid_ids:
            assert validate_session_id(session_id) is True

    def test_validate_session_id_invalid(self):
        """Test session ID validation with invalid IDs."""
        invalid_ids = [
            "",
            " ",
            "session with spaces",
            "session@invalid",
            "session#invalid",
            "a" * 101,  # Too long
        ]

        for session_id in invalid_ids:
            assert validate_session_id(session_id) is False


class TestFormatFunctions:
    """Test formatting utility functions."""

    def test_format_phone_number_with_country_code(self):
        """Test phone number formatting with country code."""
        test_cases = [
            ("911234567890", "911234567890@c.us"),
            ("+911234567890", "911234567890@c.us"),
            ("1234567890", "1234567890@c.us"),
        ]

        for input_number, expected in test_cases:
            result = format_phone_number(input_number)
            assert result == expected

    def test_format_phone_number_already_formatted(self):
        """Test phone number formatting with already formatted numbers."""
        formatted_numbers = ["1234567890@c.us", "911234567890@c.us"]

        for number in formatted_numbers:
            result = format_phone_number(number)
            assert result == number

    def test_format_phone_number_invalid(self):
        """Test phone number formatting with invalid input."""
        invalid_inputs = [
            "",
            "abc",
            "123",
            "123456789012345",
        ]  # Too short  # Too long

        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                format_phone_number(invalid_input)

    def test_format_group_id_valid(self):
        """Test group ID formatting."""
        test_cases = [
            ("123456789-987654321", "123456789-987654321@g.us"),
            ("123456789-987654321@g.us", "123456789-987654321@g.us"),
        ]

        for input_id, expected in test_cases:
            result = format_group_id(input_id)
            assert result == expected

    def test_format_group_id_invalid(self):
        """Test group ID formatting with invalid input."""
        invalid_inputs = [
            "",
            "invalid",
            "123456789",  # Missing second part
            "abc-def",  # Non-numeric
        ]

        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                format_group_id(invalid_input)


class TestParsingFunctions:
    """Test parsing utility functions."""

    def test_parse_contact_id_individual(self):
        """Test parsing individual contact ID."""
        contact_id = "1234567890@c.us"
        result = parse_contact_id(contact_id)

        assert result["type"] == "individual"
        assert result["number"] == "1234567890"
        assert result["domain"] == "c.us"

    def test_parse_contact_id_group(self):
        """Test parsing group contact ID."""
        contact_id = "123456789-987654321@g.us"
        result = parse_contact_id(contact_id)

        assert result["type"] == "group"
        assert result["group_id"] == "123456789-987654321"
        assert result["domain"] == "g.us"

    def test_parse_contact_id_invalid(self):
        """Test parsing invalid contact ID."""
        invalid_ids = [
            "",
            "invalid",
            "1234567890",
            "@c.us",
        ]  # Missing domain  # Missing number

        for invalid_id in invalid_ids:
            with pytest.raises(ValueError):
                parse_contact_id(invalid_id)

    def test_extract_phone_number(self):
        """Test extracting phone number from contact ID."""
        test_cases = [
            ("1234567890@c.us", "1234567890"),
            ("911234567890@c.us", "911234567890"),
            ("+911234567890@c.us", "+911234567890"),
        ]

        for contact_id, expected in test_cases:
            result = extract_phone_number(contact_id)
            assert result == expected

    def test_extract_phone_number_group(self):
        """Test extracting phone number from group ID should fail."""
        group_id = "123456789-987654321@g.us"
        with pytest.raises(ValueError):
            extract_phone_number(group_id)


class TestCleaningFunctions:
    """Test data cleaning utility functions."""

    def test_clean_phone_number(self):
        """Test phone number cleaning."""
        test_cases = [
            ("+91 12345 67890", "911234567890"),
            ("(91) 12345-67890", "911234567890"),
            ("91.12345.67890", "911234567890"),
            ("91 12345 67890", "911234567890"),
            ("911234567890", "911234567890"),
        ]

        for input_number, expected in test_cases:
            result = clean_phone_number(input_number)
            assert result == expected

    def test_clean_phone_number_invalid(self):
        """Test phone number cleaning with invalid input."""
        invalid_inputs = ["", "abc", "123abc456"]

        for invalid_input in invalid_inputs:
            result = clean_phone_number(invalid_input)
            assert result == ""

    def test_sanitize_message_text(self):
        """Test message text sanitization."""
        test_cases = [
            ("Hello World", "Hello World"),
            ("Hello\nWorld", "Hello World"),
            ("Hello\tWorld", "Hello World"),
            ("  Hello World  ", "Hello World"),
            ("Hello\r\nWorld", "Hello World"),
            ("", ""),
        ]

        for input_text, expected in test_cases:
            result = sanitize_message_text(input_text)
            assert result == expected

    def test_sanitize_message_text_preserve_newlines(self):
        """Test message text sanitization preserving newlines."""
        input_text = "Line 1\nLine 2\nLine 3"
        result = sanitize_message_text(input_text, preserve_newlines=True)
        assert result == "Line 1\nLine 2\nLine 3"


class TestHelperFunctions:
    """Test helper utility functions."""

    def test_is_group_id(self):
        """Test group ID detection."""
        group_ids = ["123456789-987654321@g.us", "111111111-222222222@g.us"]

        individual_ids = ["1234567890@c.us", "911234567890@c.us"]

        for group_id in group_ids:
            assert is_group_id(group_id) is True

        for individual_id in individual_ids:
            assert is_group_id(individual_id) is False

    def test_is_individual_id(self):
        """Test individual ID detection."""
        individual_ids = ["1234567890@c.us", "911234567890@c.us"]

        group_ids = ["123456789-987654321@g.us", "111111111-222222222@g.us"]

        for individual_id in individual_ids:
            assert is_individual_id(individual_id) is True

        for group_id in group_ids:
            assert is_individual_id(group_id) is False

    def test_generate_message_id(self):
        """Test message ID generation."""
        message_id = generate_message_id()

        assert isinstance(message_id, str)
        assert len(message_id) > 0
        assert message_id.startswith("msg_")

        # Test uniqueness
        message_id2 = generate_message_id()
        assert message_id != message_id2

    def test_get_timestamp(self):
        """Test timestamp generation."""
        timestamp = get_timestamp()

        assert isinstance(timestamp, int)
        assert timestamp > 0

        # Test that it's roughly current time (within 10 seconds)
        import time

        current_time = int(time.time())
        assert abs(timestamp - current_time) < 10

    def test_format_timestamp(self):
        """Test timestamp formatting."""
        timestamp = 1623456789
        formatted = format_timestamp(timestamp)

        assert isinstance(formatted, str)
        assert len(formatted) > 0
        # Should be in ISO format
        assert "T" in formatted or " " in formatted

    def test_validate_url(self):
        """Test URL validation."""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://example.com/path",
            "https://example.com/path?query=value",
        ]

        invalid_urls = [
            "",
            "invalid",
            "ftp://example.com",  # Not HTTP/HTTPS
            "example.com",  # Missing protocol
            "https://",  # Incomplete
        ]

        for url in valid_urls:
            assert validate_url(url) is True

        for url in invalid_urls:
            assert validate_url(url) is False
