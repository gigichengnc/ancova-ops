"""ANCOVA Ops: interpretable service routing and outcome analytics."""

from .models import RoutingDecision, ServiceCase
from .routing import baseline_route

__all__ = ["RoutingDecision", "ServiceCase", "baseline_route"]
__version__ = "0.5.4"
