import re
from typing import Any

import httpx
from jinja2.ext import Extension

__all__ = ("PythonVersionsExtension",)


API_URL = "https://www.python.org/api/v2/downloads/release/"
TIMEOUT = 10

_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+[a-z]*\d*$")


# FIXME:
#   Keeping this in an utils file causes
#   'No module named 'copier_template_extensions.utils''
class classproperty:  # noqa: N801
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.

    Vendored from https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.functional.classproperty
    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


class PythonVersionsExtension(Extension):
    """
    Jinja2 extension that validates Python versions against official releases.
    """

    # TODO:
    #   Recheck the RUF012 case.
    #   I'm not happy with the class-focused approach here, something instance based would be nicer.
    _releases = []  # noqa: RUF012
    _latest_version = ""

    def __init__(self, environment: Any) -> None:
        super().__init__(environment)
        environment.globals["validate_python_version"] = self.validate
        environment.globals["latest_python_version"] = self.latest_version

    @classmethod
    def update_release_cache(cls):
        response = httpx.get(API_URL, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        for entry in data:
            # We are only interested in 3.x series
            if entry["version"] != 3:
                continue

            name = entry["name"]
            version = name.removeprefix("Python ")

            cls._releases.append(version)

            # Trusting to the API that it will only return once is_latest
            if entry["is_latest"]:
                cls._latest_version = version

    @classproperty
    def releases(cls):  # noqa: N805
        if not cls._releases:
            cls.update_release_cache()

        return cls._releases

    @classproperty
    def latest_version(cls) -> str:  # noqa: N805
        if not cls._latest_version:
            cls.update_release_cache()

        return cls._latest_version

    @classmethod
    def validate(cls, version: str) -> str:
        if not _VERSION_PATTERN.match(version):
            return f"Version must be in X.Y.Z format (e.g., {cls.latest_version})"

        if version in cls.releases:
            return ""

        return f"Python {version} is not a known release"
