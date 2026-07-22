import tomllib
from pathlib import Path

from vulntrack.main import create_app


def test_package_and_api_versions_match() -> None:
    project_root = Path(__file__).parents[2]
    metadata = tomllib.loads((project_root / "pyproject.toml").read_text())

    assert create_app(":memory:").version == metadata["project"]["version"]
