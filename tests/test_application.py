import subprocess


def test_expected_files(generated_app: dict) -> None:
    """
    Verify the generated application has the expected files
    """
    path = generated_app["path"]

    expected_files = (
        ".copier-answers.yml",
        ".editorconfig",
        ".gitignore",
        ".github/workflows/git-hooks.yml",
        ".github/workflows/tests.yml",
        ".pre-commit-config.yaml",
        "README.md",
        "pyproject.toml",
        "pyproject-fmt.toml",
        "pytest.toml",
        "renovate.json5",
        "ruff.toml",
        "src/__init__.py",
        "src/main.py",
        "src/tests/__init__.py",
        "src/tests/test_sample.py",
        "uv.lock",
        "yamlfmt.yaml",
        # TODO: Missing license check
    )

    for f in expected_files:
        assert (path / f).is_file(), f"{f} is missing."


def test_unexpected_files(generated_app: dict) -> None:
    """
    Verify library-only files are not present in the generated application
    """

    path = generated_app["path"]
    package_name = generated_app["answers"]["package_name"]

    unexpected_files = (
        ".github/workflows/release.yml",
        "CHANGELOG.md",
        f"src/{package_name}/__init__.py",
    )

    for f in unexpected_files:
        assert not (path / f).exists(), f"{f} should not be present."


def test_build_backend(generated_app: dict) -> None:
    """
    Applications shouldn't have build backend details in their pyproject.toml
    """
    path = generated_app["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")

    assert "[build-system]\n" not in content
    assert "hatchling" not in content


def test_package(generated_app: dict) -> None:
    """
    Applications should have "package = false" in their pyproject.toml
    """
    path = generated_app["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert "package = false" in content


def test_pyproject_toml_lockable(generated_app: dict) -> None:
    """
    Verify pyproject.toml can be locked with uv.
    """
    path = generated_app["path"]
    result = subprocess.run(
        ["uv", "lock"],
        cwd=str(path),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"uv lock failed:\n{result.stderr}"


def test_pyproject_toml_locked_properly(generated_app: dict) -> None:
    """
    Verify pyproject.toml locked properly.
    """
    path = generated_app["path"]
    result = subprocess.run(
        ["uv", "lock", "--check"],
        cwd=str(path),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"uv lock --check failed:\n{result.stderr}"


def test_requires_python(generated_app: dict) -> None:
    path = generated_app["path"]
    python_version = generated_app["answers"]["python_version"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert f'requires-python = "=={python_version}"' in content


def test_license(generated_app: dict) -> None:
    path = generated_app["path"]
    license_type = generated_app["answers"]["license"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")

    if license_type == "None":
        assert "license = " not in content
    else:
        assert f'license = "{license_type}"' in content


def test_urls(generated_app: dict) -> None:
    path = generated_app["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert "[project.urls]" not in content
