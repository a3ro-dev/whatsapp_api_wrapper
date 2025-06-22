"""
Unit tests for WhatsApp API exceptions.
"""

import pytest

from whatsapp_api_wrapper.exceptions import (
    WhatsAppAPIError,
    WhatsAppAuthenticationError,
    WhatsAppAuthorizationError,
    WhatsAppConnectionError,
    WhatsAppHTTPError,
    WhatsAppMessageError,
    WhatsAppNotFoundError,
    WhatsAppRateLimitError,
    WhatsAppServerError,
    WhatsAppSessionError,
    WhatsAppTimeoutError,
    WhatsAppValidationError,
)


class TestWhatsAppExceptions:
    """Test WhatsApp API exception classes."""

    def test_whatsapp_api_error_base(self):
        """Test base WhatsApp API error."""
        error = WhatsAppAPIError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    def test_whatsapp_api_error_with_code(self):
        """Test WhatsApp API error with error code."""
        error = WhatsAppAPIError("Test error", error_code="TEST_ERROR")
        assert str(error) == "Test error"
        assert error.error_code == "TEST_ERROR"

    def test_whatsapp_api_error_with_details(self):
        """Test WhatsApp API error with additional details."""
        details = {"field": "value", "status": 400}
        error = WhatsAppAPIError(
            "Test error", error_code="TEST_ERROR", details=details
        )
        assert error.details == details
        assert error.details["field"] == "value"

    def test_whatsapp_authentication_error(self):
        """Test authentication error."""
        error = WhatsAppAuthenticationError("Invalid API key")
        assert str(error) == "Invalid API key"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_authorization_error(self):
        """Test authorization error."""
        error = WhatsAppAuthorizationError("Access denied")
        assert str(error) == "Access denied"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_validation_error(self):
        """Test validation error."""
        error = WhatsAppValidationError("Invalid request data")
        assert str(error) == "Invalid request data"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_not_found_error(self):
        """Test not found error."""
        error = WhatsAppNotFoundError("Resource not found")
        assert str(error) == "Resource not found"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_rate_limit_error(self):
        """Test rate limit error."""
        error = WhatsAppRateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_server_error(self):
        """Test server error."""
        error = WhatsAppServerError("Internal server error")
        assert str(error) == "Internal server error"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_timeout_error(self):
        """Test timeout error."""
        error = WhatsAppTimeoutError("Request timeout")
        assert str(error) == "Request timeout"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_connection_error(self):
        """Test connection error."""
        error = WhatsAppConnectionError("Connection failed")
        assert str(error) == "Connection failed"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_http_error(self):
        """Test HTTP error."""
        error = WhatsAppHTTPError("HTTP error occurred")
        assert str(error) == "HTTP error occurred"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_session_error(self):
        """Test session error."""
        error = WhatsAppSessionError("Session not found")
        assert str(error) == "Session not found"
        assert isinstance(error, WhatsAppAPIError)

    def test_whatsapp_message_error(self):
        """Test message error."""
        error = WhatsAppMessageError("Message delivery failed")
        assert str(error) == "Message delivery failed"
        assert isinstance(error, WhatsAppAPIError)


class TestExceptionHierarchy:
    """Test exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all custom exceptions inherit from WhatsAppAPIError."""
        exceptions = [
            WhatsAppAuthenticationError,
            WhatsAppAuthorizationError,
            WhatsAppValidationError,
            WhatsAppNotFoundError,
            WhatsAppRateLimitError,
            WhatsAppServerError,
            WhatsAppTimeoutError,
            WhatsAppConnectionError,
            WhatsAppHTTPError,
            WhatsAppSessionError,
            WhatsAppMessageError,
        ]

        for exc_class in exceptions:
            exception = exc_class("Test message")
            assert isinstance(exception, WhatsAppAPIError)
            assert isinstance(exception, Exception)

    def test_exception_can_be_caught_by_base(self):
        """Test that specific exceptions can be caught by base exception."""
        try:
            raise WhatsAppAuthenticationError("Auth failed")
        except WhatsAppAPIError as e:
            assert str(e) == "Auth failed"
        except Exception:
            pytest.fail("Should have been caught by WhatsAppAPIError")

    def test_exception_can_be_caught_specifically(self):
        """Test that exceptions can be caught by their specific type."""
        try:
            raise WhatsAppValidationError("Validation failed")
        except WhatsAppValidationError as e:
            assert str(e) == "Validation failed"
        except WhatsAppAPIError:
            pytest.fail("Should have been caught by WhatsAppValidationError")
        except Exception:
            pytest.fail("Should have been caught by WhatsAppValidationError")


class TestExceptionAttributes:
    """Test exception attributes and methods."""

    def test_exception_str_representation(self):
        """Test string representation of exceptions."""
        error = WhatsAppAPIError("Test message")
        assert str(error) == "Test message"
        assert repr(error) == "WhatsAppAPIError('Test message')"

    def test_exception_with_code_str_representation(self):
        """Test string representation with error code."""
        error = WhatsAppAPIError("Test message", error_code="TEST_CODE")
        expected = "Test message"
        assert str(error) == expected

    def test_exception_attributes_accessible(self):
        """Test that exception attributes are accessible."""
        details = {"status_code": 400, "field": "to"}
        error = WhatsAppValidationError(
            "Validation failed", error_code="VALIDATION_ERROR", details=details
        )

        assert error.error_code == "VALIDATION_ERROR"
        assert error.details == details
        assert error.details["status_code"] == 400

    def test_exception_without_optional_attributes(self):
        """Test exceptions without optional attributes."""
        error = WhatsAppAPIError("Simple error")
        assert error.error_code is None
        assert error.details is None

    def test_exception_equality(self):
        """Test exception equality comparison."""
        error1 = WhatsAppAPIError("Test message", error_code="TEST")
        error2 = WhatsAppAPIError("Test message", error_code="TEST")
        error3 = WhatsAppAPIError("Different message", error_code="TEST")

        # Note: Exception instances are not equal by default
        assert error1 is not error2
        assert str(error1) == str(error2)
        assert str(error1) != str(error3)
