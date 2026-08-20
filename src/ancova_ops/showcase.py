from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from . import __version__
from .adaptive import build_offline_comparison
from .analytics import build_ancova_report
from .evaluation import baseline_predict, evaluate_predictor, load_dataset
from .governance import load_policy, validate_policy
from .intelligence import INTELLIGENCE_VERSION, BaselineRequestIntelligence
from .longitudinal import run_longitudinal_benchmark
from .models import ServiceCase
from .routing import ROUTER_VERSION, baseline_route
from .synthetic import generate_logged_routing_history, generate_outcomes

DEFAULT_OUTPUT_PATH = Path(".ancova_ops/showcase/showcase.md")
SHOWCASE_MESSAGE = (
    "The air conditioner is leaking again. This is the third time and an elderly "
    "resident could slip on the wet floor."
)


def build_showcase_payload(
    *,
    seed: int = 2026,
    outcome_rows: int = 400,
    logged_rows: int = 1200,
    longitudinal_entities: int = 120,
    longitudinal_days: int = 600,
) -> dict[str, Any]:
    """Run the existing development workflows and assemble one showcase payload."""

    governance = load_policy()
    validate_policy(governance)

    intelligence = BaselineRequestIntelligence()
    features = intelligence.analyze(
        SHOWCASE_MESSAGE,
        previous_related_cases=2,
        vulnerability_flag=True,
    )
    service_case = ServiceCase(
        case_id="showcase-routing-001",
        message=SHOWCASE_MESSAGE,
        issue_category=features.issue_category,
        urgency=features.urgency,
        frustration=features.frustration,
        complexity=features.complexity,
        previous_related_cases=2,
        vulnerability_flag=True,
    )
    decision = baseline_route(service_case)

    fixture = load_dataset()
    routing_benchmark = evaluate_predictor(
        fixture,
        baseline_predict,
        system_name="transparent-baseline-v1",
    )

    outcome_data = generate_outcomes(n=outcome_rows, seed=seed)
    outcome_report = build_ancova_report(outcome_data).to_dict()

    logged_data = generate_logged_routing_history(n=logged_rows, seed=seed)
    adaptive_comparison, adaptive_candidate = build_offline_comparison(logged_data)

    longitudinal_report = run_longitudinal_benchmark(
        n_entities=longitudinal_entities,
        n_days=longitudinal_days,
        seed=seed,
    )

    return {
        "showcase_version": __version__,
        "evidence_status": {
            "routing_fixture": fixture.provenance,
            "routing_label_status": fixture.label_status,
            "outcome_analysis": "synthetic",
            "adaptive_policy": "synthetic_logged_policy",
            "longitudinal": longitudinal_report.provenance,
            "real_world_performance_claims_allowed": False,
        },
        "governance": {
            "policy_version": governance.policy_version,
            "mode": governance.mode,
            "deployment_status": governance.deployment_status,
            "pilot_ready": False,
            "production_ready": False,
        },
        "service_request": {
            "message": SHOWCASE_MESSAGE,
            "previous_related_cases": 2,
            "vulnerability_flag": True,
            "intelligence_version": INTELLIGENCE_VERSION,
            "router_version": ROUTER_VERSION,
            "features": asdict(features),
            "routing": asdict(decision),
        },
        "routing_benchmark": {
            "dataset_name": fixture.name,
            "dataset_version": fixture.version,
            "provenance": fixture.provenance,
            "label_status": fixture.label_status,
            "metrics": asdict(routing_benchmark.metrics),
            "department_errors": list(routing_benchmark.department_errors),
            "human_review_misses": list(routing_benchmark.human_review_misses),
        },
        "outcome_analysis": {
            "formula": outcome_report["formula"],
            "provenance": outcome_report["provenance"],
            "sample": outcome_report["sample"],
            "adjusted_estimates": outcome_report["adjusted_estimates"],
            "warnings": outcome_report["warnings"],
            "interpretation_note": outcome_report["interpretation_note"],
        },
        "adaptive_routing": {
            "candidate_version": adaptive_candidate.version,
            **adaptive_comparison.to_dict(),
        },
        "longitudinal_benchmark": longitudinal_report.to_dict(),
        "readiness": {
            "repository_checkpoint_ready": True,
            "private_data_pilot_ready": False,
            "production_ready": False,
            "sequence_model_status": longitudinal_report.sequence_model_status,
        },
    }


def render_showcase_markdown(payload: dict[str, Any]) -> str:
    routing = payload["service_request"]
    benchmark = payload["routing_benchmark"]
    outcome = payload["outcome_analysis"]
    adaptive = payload["adaptive_routing"]
    longitudinal = payload["longitudinal_benchmark"]
    governance = payload["governance"]

    routing_metrics = benchmark["metrics"]
    route = routing["routing"]
    features = routing["features"]

    adjusted_rows = "\n".join(
        "| {department} | {mean:.2f} | {low:.2f} | {high:.2f} |".format(
            department=row["department"],
            mean=row["adjusted_mean_resolution_hours"],
            low=row["mean_ci_lower"],
            high=row["mean_ci_upper"],
        )
        for row in outcome["adjusted_estimates"]
    )
    warning_lines = "\n".join(f"- {warning}" for warning in outcome["warnings"])
    if not warning_lines:
        warning_lines = "- No warning triggered by the current development screening rules."

    return f"""# ANCOVA Ops Portfolio Showcase

**Showcase version:** {payload['showcase_version']}  
**Development boundary:** synthetic / hand-authored evidence only  
**Real-world performance claims:** not supported

This report is generated by `ancova-showcase`. It demonstrates the existing ANCOVA Ops
Phase 1–4 research/software workflows in one place. It does not introduce a new model and
must not be presented as evidence of production performance.

## 1. Service-intelligence example

> {routing['message']}

| Signal | Value |
| --- | ---: |
| Issue category | {features['issue_category']} |
| Urgency | {features['urgency']} |
| Frustration / communication intensity | {features['frustration']} |
| Complexity | {features['complexity']} |
| Recommended department | {route['department']} |
| Priority | {route['priority']} |
| Human review required | {route['requires_human_review']} |
| Secondary notification | {route['secondary_notify']} |

Intelligence version: `{routing['intelligence_version']}`  
Router version: `{routing['router_version']}`

## 2. Routing benchmark

Dataset: `{benchmark['dataset_name']}` v{benchmark['dataset_version']}  
Provenance: `{benchmark['provenance']}`  
Label status: `{benchmark['label_status']}`

| Metric | Result |
| --- | ---: |
| Department accuracy | {routing_metrics['department_correct']}/{routing_metrics['sample_count']} ({routing_metrics['department_accuracy']:.1%}) |
| Human-review recall | {routing_metrics['high_risk_reviewed']}/{routing_metrics['high_risk_count']} ({routing_metrics['human_review_recall']:.1%}) |
| Explanation coverage | {routing_metrics['explained_count']}/{routing_metrics['sample_count']} ({routing_metrics['explanation_coverage']:.1%}) |

These are software-development fixture results, not production estimates.

## 3. ANCOVA / outcome analysis

Formula:

`{outcome['formula']}`

Adjusted department estimates from synthetic development outcomes:

| Department | Adjusted mean hours | 95% CI lower | 95% CI upper |
| --- | ---: | ---: | ---: |
{adjusted_rows}

Warnings:

{warning_lines}

**Interpretation boundary:** {outcome['interpretation_note']}

The adjusted comparison is not an automatic staff-performance league table and does not
establish causal department effects.

## 4. Offline adaptive-routing research

| Item | Result |
| --- | --- |
| Candidate | `{adaptive['candidate_version']}` |
| Training rows | {adaptive['training_count']} |
| Validation rows | {adaptive['validation_count']} |
| Offline signal | `{adaptive['offline_signal']}` |
| Offline gate passed | {adaptive['offline_gate_passed']} |
| Deployment eligible | {adaptive['deployment_eligible']} |

The adaptive result is an offline estimate on synthetic logged-policy data. Registry or
offline-gate status does not authorise deployment and does not replace `/v1/route`.

## 5. Longitudinal benchmark

| Model | ROC-AUC | Brier score |
| --- | ---: | ---: |
| Recency/frequency logistic | {longitudinal['baseline']['metrics']['roc_auc']:.3f} | {longitudinal['baseline']['metrics']['brier_score']:.3f} |
| Discrete-time hazard | {longitudinal['survival']['metrics']['roc_auc']:.3f} | {longitudinal['survival']['metrics']['brier_score']:.3f} |
| Random forest | {longitudinal['tree']['metrics']['roc_auc']:.3f} | {longitudinal['tree']['metrics']['brier_score']:.3f} |

Best AUC model: `{longitudinal['best_auc_model']}`  
Best Brier model: `{longitudinal['best_brier_model']}`  
Sequence-model status: `{longitudinal['sequence_model_status']}`

The benchmark uses synthetic longitudinal histories. It does not predict real resident or
customer behaviour.

## 6. Governance and readiness

| Boundary | Status |
| --- | --- |
| Governance mode | `{governance['mode']}` |
| Deployment status | `{governance['deployment_status']}` |
| Repository checkpoint | READY |
| Private-data pilot | NOT READY / NOT APPROVED |
| Production deployment | NOT READY / NOT APPROVED |

## What this showcase demonstrates

ANCOVA Ops can reproducibly connect explainable request routing, auditable human-centred
operations, downstream statistical outcome analysis, offline policy research and
leakage-aware longitudinal benchmarking while keeping evidence provenance and deployment
boundaries explicit.

It does **not** demonstrate real service improvement, causal operational impact, production
safety, or readiness to process private resident/customer data.
"""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the ANCOVA Ops portfolio showcase.")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--outcome-rows", type=int, default=400)
    parser.add_argument("--logged-rows", type=int, default=1200)
    parser.add_argument("--longitudinal-entities", type=int, default=120)
    parser.add_argument("--longitudinal-days", type=int, default=600)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--json", action="store_true", help="Print the structured payload.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = build_showcase_payload(
        seed=args.seed,
        outcome_rows=args.outcome_rows,
        logged_rows=args.logged_rows,
        longitudinal_entities=args.longitudinal_entities,
        longitudinal_days=args.longitudinal_days,
    )
    markdown = render_showcase_markdown(payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    if args.json_output is not None:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Showcase report written to {args.output}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
