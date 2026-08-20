import tomllib
from pathlib import Path

import ancova_ops

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SCRIPTS = {
    "ancova-analyze",
    "ancova-evaluate",
    "ancova-governance-check",
    "ancova-longitudinal",
    "ancova-management-report",
    "ancova-policy",
    "ancova-showcase",
}


def _project_metadata() -> dict[str, object]:
    return tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_package_version_matches_project_metadata() -> None:
    project = _project_metadata()

    assert ancova_ops.__version__ == project["version"]
    assert ancova_ops.__version__ == "0.5.2"


def test_v052_cli_surface_is_registered() -> None:
    project = _project_metadata()

    assert set(project["scripts"]) == EXPECTED_SCRIPTS


def test_apache_license_metadata_and_file_are_present() -> None:
    project = _project_metadata()
    license_text = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert project["license"] == "Apache-2.0"
    assert "Apache License" in license_text
    assert "Version 2.0, January 2004" in license_text
