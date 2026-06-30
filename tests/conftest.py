from pathlib import Path

import pytest
from copier import run_copy
from faker import Faker

PROJECT_DIR = Path(__file__).resolve().parent.parent
faker = Faker()

__all__ = (
    "generated_app",
    "generated_lib",
)


@pytest.fixture()
def generated_app(tmp_path: Path) -> dict:
    inputs = {
        "project_name": faker.catch_phrase(),
        "author_name": faker.name(),
        "author_email": faker.email(),
        "github_username": faker.user_name(),
        "project_type": "Application",
    }
    run_copy(
        src_path=str(PROJECT_DIR),
        dst_path=str(tmp_path),
        data=inputs,
        defaults=True,
        unsafe=True,
    )
    return {"path": tmp_path, "inputs": inputs}


@pytest.fixture()
def generated_lib(tmp_path: Path) -> dict:
    inputs = {
        "project_name": faker.catch_phrase(),
        "author_name": faker.name(),
        "author_email": faker.email(),
        "github_username": faker.user_name(),
        "project_type": "Library",
    }
    run_copy(
        src_path=str(PROJECT_DIR),
        dst_path=str(tmp_path),
        data=inputs,
        defaults=True,
        unsafe=True,
    )
    return {"path": tmp_path, "inputs": inputs}
