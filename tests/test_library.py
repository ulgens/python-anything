import re


def test_common_structure(generated_lib: dict) -> None:
    """
    Verify the generated library has the expected file structure.
    """
    path = generated_lib["path"]

    expected_files = (
        ".editorconfig",
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


def test_package_flag(generated_lib: dict) -> None:
    path = generated_lib["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert "package = false" not in content


def test_library_specific_files(generated_lib: dict) -> None:
    """
    Verify library-specific files (CHANGELOG, release workflow) are present.
    """
    path = generated_lib["path"]
    package_name = generated_lib["answers"]["package_name"]

    expected_files = (
        "CHANGELOG.md",
        f"src/{package_name}/__init__.py",
        ".github/workflows/release.yml",
        ".github/workflows/tests.yml",
        ".github/workflows/git-hooks.yml",
    )

    for f in expected_files:
        assert (path / f).is_file(), f"{f} is missing."


def test_library_requires_python_range(generated_lib: dict) -> None:
    path = generated_lib["path"]
    min_ver = generated_lib["answers"]["min_python_version"]
    max_ver = generated_lib["answers"]["max_python_version"]
    expected = f'requires-python = ">={min_ver},<{max_ver}"'

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert expected in content
    assert "package = false" not in content


def test_library_init_py_has_version(generated_lib: dict) -> None:
    path = generated_lib["path"]
    package_name = generated_lib["answers"]["package_name"]

    content = (path / f"src/{package_name}/__init__.py").read_text(encoding="utf-8")
    assert '__version__ = "0.1.0"' in content


def test_library_uv_lock_in_gitignore(generated_lib: dict) -> None:
    path = generated_lib["path"]

    content = (path / ".gitignore").read_text(encoding="utf-8")
    assert any(re.match(r"^uv\.lock$", line) for line in content.splitlines())


def test_library_readme_has_install_section(generated_lib: dict) -> None:
    path = generated_lib["path"]

    content = (path / "README.md").read_text(encoding="utf-8")
    assert "pip install" in content


def test_build_backend_is_hatchling(generated_lib: dict) -> None:
    path = generated_lib["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")

    assert "[build-system]\n" in content
    assert 'build-backend = "hatchling.build"\n' in content
    assert 'requires = [ "hatchling" ]\n' in content
