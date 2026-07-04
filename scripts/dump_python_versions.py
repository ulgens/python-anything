"""Fetch known Python 3.x releases from python.org and dump as JSON."""

import json
from pathlib import Path

import httpx
from packaging.version import Version

API_URL = "https://www.python.org/api/v2/downloads/release/"
TIMEOUT = 10
BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    releases = []
    latest = ""

    response = httpx.get(API_URL, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()

    for entry in data:
        # We are only interested in 3.x series
        if entry["version"] != 3:
            continue

        name = entry["name"]
        version = name.removeprefix("Python ")

        releases.append(version)

        # Trusting to the API that it will only return once is_latest
        if entry["is_latest"]:
            latest = version

    releases.sort(key=Version)
    result = json.dumps(
        {"releases": releases, "latest_version": latest},
        indent=4,
    )
    result = result + "\n"

    output_file = BASE_DIR / "extensions" / "python_versions.json"
    output_file.write_text(result)

    print(f"Wrote {len(releases)} versions to {output_file}")  # noqa: T201


if __name__ == "__main__":
    main()
