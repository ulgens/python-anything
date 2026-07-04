from pathlib import Path

import pytest
from copier import run_copy
from faker import Faker

PROJECT_DIR = Path(__file__).resolve().parent.parent

__all__ = (
    "generated_app",
    "generated_lib",
)


def get_common_inputs(faker: Faker) -> dict:
    return {
        "project_name": faker.catch_phrase(),
        "author_name": faker.name(),
        "author_email": faker.email(),
        "github_username": faker.user_name(),
    }


@pytest.fixture()
def generated_app(tmp_path: Path, faker: Faker) -> dict:
    inputs = {
        **get_common_inputs(faker),
        "project_type": "Application",
    }

    result = run_copy(
        src_path=str(PROJECT_DIR),
        dst_path=str(tmp_path),
        data=inputs,
        defaults=True,
        unsafe=True,
    )

    return {
        "path": tmp_path,
        "inputs": inputs,
        "answers": result.answers.user,
    }


@pytest.fixture()
def generated_lib(tmp_path: Path, faker: Faker) -> dict:
    inputs = {
        **get_common_inputs(faker),
        "project_type": "Library",
    }
    result = run_copy(
        src_path=str(PROJECT_DIR),
        dst_path=str(tmp_path),
        data=inputs,
        defaults=True,
        unsafe=True,
    )

    return {
        "path": tmp_path,
        "inputs": inputs,
        "answers": result.answers.user,
    }
