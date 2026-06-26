def test_common_structure(generated_lib: dict) -> None:
    """
    Verify the generated library has the expected file structure.
    """
    path = generated_lib["path"]

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


def test_library_specific_files(generated_lib: dict) -> None:
    """
    Verify library-specific files (CHANGELOG, release workflow) are present.
    """
    path = generated_lib["path"]

    expected_files = (
        "CHANGELOG.md",
        ".github/workflows/release.yml",
    )

    for f in expected_files:
        assert (path / f).is_file(), f"{f} is missing."
