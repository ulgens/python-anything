import json
from pathlib import Path
from typing import Any

from jinja2.ext import Extension
from packaging.version import InvalidVersion, Version

__all__ = ("PythonVersionsExtension",)


python_versions = Path(__file__).resolve().parent / "python_versions.json"
python_versions = json.loads(python_versions.read_text())


class PythonVersionsExtension(Extension):
    """
    Jinja2 extension that validates Python versions against a vendored release list.
    """

    releases: list[str]
    latest_version: str

    def __init__(self, environment: Any) -> None:
        super().__init__(environment)

        cls = self.__class__
        cls.releases = python_versions["releases"]
        cls.latest_version = python_versions["latest_version"]

        environment.globals["validate_python_version"] = cls.validate
        environment.globals["latest_python_version"] = cls.latest_version

    @classmethod
    def validate(cls, version: str) -> str:
        check_existing_text = "Check the existing versions here: https://www.python.org/downloads/"

        try:
            Version(version)
        except InvalidVersion:
            return f"{version} is not a valid version. {check_existing_text}"

        if version in cls.releases:
            return ""

        return f"{version} is not a known release. {check_existing_text}"
