from pathlib import Path
import tomllib

import ancova_ops


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SCRIPTS = {
    "ancova-analyze",
    "ancova-evaluate",
    "ancova-governance-check",
    "ancova-longitudinal",
    "ancova-management-report",
    "ancova-policy",
}


def _project_metadata() -> dict[str, object]:
    return tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_package_version_matches_project_metadata() -> None:
    project = _project_metadata()

    assert ancova_ops.__version__ == project["version"]
    assert ancova_ops.__version__ == "0.5.0"


def test_v050_cli_surface_is_registered() -> None:
    project = _project_metadata()

    assert set(project["scripts"]) == EXPECTED_SCRIPTS
