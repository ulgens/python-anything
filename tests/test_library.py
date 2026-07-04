import re


def test_expected_files(generated_lib: dict) -> None:
    """
    Verify the generated library has the expected files
    """
    path = generated_lib["path"]
    package_name = generated_lib["answers"]["package_name"]

    expected_files = (
        ".copier-answers.yml",
        ".editorconfig",
        ".gitignore",
        ".github/workflows/git-hooks.yml",
        ".github/workflows/release.yml",
        ".github/workflows/tests.yml",
        ".pre-commit-config.yaml",
        "CHANGELOG.md",
        "README.md",
        "pyproject.toml",
        "pyproject-fmt.toml",
        "pytest.toml",
        "renovate.json5",
        "ruff.toml",
        f"src/{package_name}/__init__.py",
        # TODO: Revisit this. Do we want tests/ under src/ ?
        "src/tests/__init__.py",
        "src/tests/test_sample.py",
        "yamlfmt.yaml",
        # TODO: Missing license check
    )

    for f in expected_files:
        assert (path / f).is_file(), f"{f} is missing."


def test_unexpected_files(generated_lib: dict) -> None:
    """
    Verify application-only files are not present in the generated library
    """
    path = generated_lib["path"]

    unexpected_files = (
        "src/__init__.py",
        "src/main.py",
        "uv.lock",
    )

    for f in unexpected_files:
        assert not (path / f).exists(), f"{f} should not be present."


def test_build_backend(generated_lib: dict) -> None:
    """
    Libraries should have build backend details in their pyproject.toml
    """
    path = generated_lib["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")

    assert "[build-system]\n" in content
    assert 'build-backend = "hatchling.build"\n' in content
    assert 'requires = [ "hatchling" ]\n' in content


def test_init_py(generated_lib: dict) -> None:
    path = generated_lib["path"]
    package_name = generated_lib["answers"]["package_name"]

    content = (path / f"src/{package_name}/__init__.py").read_text(encoding="utf-8")
    assert '__version__ = "0.1.0"' in content


def test_package(generated_lib: dict) -> None:
    """
    Libraries shouldn't have "package = false" in their pyproject.toml
    """
    path = generated_lib["path"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert "package = false" not in content


def test_readme(generated_lib: dict) -> None:
    path = generated_lib["path"]

    content = (path / "README.md").read_text(encoding="utf-8")
    assert "pip install" in content


def test_requires_python(generated_lib: dict) -> None:
    path = generated_lib["path"]
    min_ver = generated_lib["answers"]["min_python_version"]
    max_ver = generated_lib["answers"]["max_python_version"]
    expected = f'requires-python = ">={min_ver},<{max_ver}"'

    content = (path / "pyproject.toml").read_text(encoding="utf-8")
    assert expected in content
    assert "package = false" not in content


def test_urls(generated_lib: dict) -> None:
    path = generated_lib["path"]
    github_username = generated_lib["answers"]["github_username"]
    package_name = generated_lib["answers"]["package_name"]

    content = (path / "pyproject.toml").read_text(encoding="utf-8")

    assert f'Homepage = "https://github.com/{github_username}/{package_name}"' in content
    assert f'Source = "https://github.com/{github_username}/{package_name}"' in content
    assert f'Issues = "https://github.com/{github_username}/{package_name}/issues"' in content


def test_uv_lock_gitignore(generated_lib: dict) -> None:
    path = generated_lib["path"]

    content = (path / ".gitignore").read_text(encoding="utf-8")
    assert any(re.match(r"^uv\.lock$", line) for line in content.splitlines())
