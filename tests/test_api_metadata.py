import reasoned_ops
from reasoned_ops.api import app


def test_canonical_api_identity_matches_package_version() -> None:
    assert app.title == "ReasonedOps API"
    assert app.version == reasoned_ops.__version__
