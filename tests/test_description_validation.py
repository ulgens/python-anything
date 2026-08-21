from extensions.description_validation import DescriptionValidationExtension

# TODO:
#   While test cases are pretty specific about what string / chars to validate,
#   find a way to add randomness.


def test_validate_description_valid() -> None:
    """Test that valid strings pass validation."""
    assert DescriptionValidationExtension.validate("hello world") == ""
    assert DescriptionValidationExtension.validate("A simple description") == ""
    assert DescriptionValidationExtension.validate("") == ""


def test_validate_description_quotes() -> None:
    """Test that strings with double quotes fail validation."""
    result = DescriptionValidationExtension.validate('say "hello"')
    assert result == "String cannot contain double quotes"


def test_validate_description_backslashes() -> None:
    """Test that strings with backslashes fail validation."""
    result = DescriptionValidationExtension.validate("path\\to\\file")
    assert result == "String cannot contain backslashes"


def test_validate_description_newlines() -> None:
    """Test that strings with newlines fail validation."""
    result = DescriptionValidationExtension.validate("line1\nline2")
    assert result == "String cannot contain newlines"


def test_validate_description_carriage_returns() -> None:
    """Test that strings with carriage returns fail validation."""
    result = DescriptionValidationExtension.validate("line1\rline2")
    assert result == "String cannot contain carriage returns"
