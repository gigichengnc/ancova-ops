from pathlib import Path
import tomllib

import ancova_ops


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_package_version_matches_project_metadata() -> None:
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert ancova_ops.__version__ == pyproject["project"]["version"]
    assert ancova_ops.__version__ == "0.5.0"
