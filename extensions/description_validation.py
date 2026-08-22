from typing import Any

from jinja2.ext import Extension

__all__ = ("DescriptionValidationExtension",)


class DescriptionValidationExtension(Extension):
    """
    Jinja2 extension that provides TOML string validation.

    These characters break pyproject.toml file structure when not escaped.
    Escaping them requires making assumptions about what user aims for and what end result is acceptable,
    we are playing it safe and rejecting them instead of trying to escape them.
    """

    def __init__(self, environment: Any) -> None:
        super().__init__(environment)
        environment.globals["validate_description"] = self.validate

    @staticmethod
    def validate(value: str) -> str:
        """
        Validate that a string can be safely used in a TOML basic string.

        Returns an error message if invalid, empty string if valid.
        """
        if '"' in value:
            return "String cannot contain double quotes"

        if "\\" in value:
            return "String cannot contain backslashes"

        if "\n" in value:
            return "String cannot contain newlines"

        if "\r" in value:
            return "String cannot contain carriage returns"

        return ""
