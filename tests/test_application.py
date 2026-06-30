import subprocess


def test_common_structure(generated_app: dict) -> None:
    """
    Verify the generated application has the expected file structure.
    """
    path = generated_app["path"]

    expected_files = (
        "pyproject.toml",
        ".pre-commit-config.yaml",
        ".gitignore",
        "renovate.json5",
        "ruff.toml",
    )
    for f in expected_files:
        assert (path / f).is_file(), f"{f} is missing."

    expected_dirs = (
        "src",
        ".github/workflows",
    )
    for d in expected_dirs:
        assert (path / d).is_dir(), f"{d} is missing."


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


def test_package_flag(generated_app: dict) -> None:
    path = generated_app["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert "package = false" in content


def test_application_no_cross_type_files(generated_app: dict) -> None:
    """
    Verify library-only files are not present in the generated application.
    """
    path = generated_app["path"]
    package_name = generated_app["answers"]["package_name"]

    unexpected_files = (
        "CHANGELOG.md",
        ".github/workflows/release.yml",
        f"src/{package_name}/__init__.py",
    )

    for f in unexpected_files:
        assert not (path / f).exists(), f"{f} is missing."
