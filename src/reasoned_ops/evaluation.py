from __future__ import annotations

import argparse
import importlib
import json
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from .intelligence import BaselineRequestIntelligence
from .models import ServiceCase
from .routing import baseline_route

DEFAULT_FIXTURE_PATH = Path("data/evaluation/hand_authored_v1.json")


@dataclass(slots=True, frozen=True)
class EvaluationCase:
    case_id: str
    message: str
    expected_department: str
    expected_human_review: bool
    previous_related_cases: int = 0
    vulnerability_flag: bool = False
    annotation_note: str = ""


@dataclass(slots=True, frozen=True)
class EvaluationDataset:
    name: str
    version: str
    provenance: str
    label_status: str
    description: str
    limitations: tuple[str, ...]
    cases: tuple[EvaluationCase, ...]


@dataclass(slots=True, frozen=True)
class EvaluationPrediction:
    department: str
    requires_human_review: bool
    reasons: tuple[str, ...]
    issue_category: str | None = None


@dataclass(slots=True, frozen=True)
class EvaluationMetrics:
    sample_count: int
    department_correct: int
    department_accuracy: float
    high_risk_count: int
    high_risk_reviewed: int
    human_review_recall: float | None
    explained_count: int
    explanation_coverage: float


@dataclass(slots=True, frozen=True)
class EvaluationReport:
    system_name: str
    dataset_name: str
    dataset_version: str
    metrics: EvaluationMetrics
    department_errors: tuple[str, ...]
    human_review_misses: tuple[str, ...]
    unexplained_cases: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class ComparisonReport:
    baseline_system: str
    candidate_system: str
    dataset_name: str
    dataset_version: str
    department_accuracy_delta: float
    human_review_recall_delta: float | None
    explanation_coverage_delta: float
    no_regressions: bool
    strict_improvement: bool
    eligible_for_improvement_claim: bool
    verdict: str


Predictor = Callable[[EvaluationCase], EvaluationPrediction]


def load_dataset(path: str | Path = DEFAULT_FIXTURE_PATH) -> EvaluationDataset:
    fixture_path = Path(path)
    raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    metadata = raw["metadata"]

    cases = tuple(
        EvaluationCase(
            case_id=item["case_id"],
            message=item["message"],
            expected_department=item["expected_department"],
            expected_human_review=item["expected_human_review"],
            previous_related_cases=item.get("previous_related_cases", 0),
            vulnerability_flag=item.get("vulnerability_flag", False),
            annotation_note=item.get("annotation_note", ""),
        )
        for item in raw["cases"]
    )

    if not cases:
        raise ValueError("evaluation dataset must contain at least one case")

    case_ids = [case.case_id for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("evaluation case_id values must be unique")

    for case in cases:
        if not case.case_id.strip() or not case.message.strip():
            raise ValueError("evaluation cases require non-blank case_id and message")
        if not case.expected_department.strip():
            raise ValueError("evaluation cases require expected_department")
        if case.previous_related_cases < 0:
            raise ValueError("previous_related_cases must be non-negative")

    return EvaluationDataset(
        name=metadata["name"],
        version=metadata["version"],
        provenance=metadata["provenance"],
        label_status=metadata["label_status"],
        description=metadata["description"],
        limitations=tuple(metadata.get("limitations", [])),
        cases=cases,
    )


def baseline_predict(case: EvaluationCase) -> EvaluationPrediction:
    intelligence = BaselineRequestIntelligence()
    features = intelligence.analyze(
        case.message,
        previous_related_cases=case.previous_related_cases,
        vulnerability_flag=case.vulnerability_flag,
    )
    service_case = ServiceCase(
        case_id=case.case_id,
        message=case.message,
        issue_category=features.issue_category,
        urgency=features.urgency,
        frustration=features.frustration,
        complexity=features.complexity,
        previous_related_cases=case.previous_related_cases,
        vulnerability_flag=case.vulnerability_flag,
    )
    decision = baseline_route(service_case)
    reasons = tuple(dict.fromkeys((*features.reasons, *decision.reasons)))
    return EvaluationPrediction(
        department=decision.department,
        requires_human_review=decision.requires_human_review,
        reasons=reasons,
        issue_category=features.issue_category,
    )


def evaluate_predictor(
    dataset: EvaluationDataset,
    predictor: Predictor,
    *,
    system_name: str,
) -> EvaluationReport:
    department_correct = 0
    high_risk_count = 0
    high_risk_reviewed = 0
    explained_count = 0
    department_errors: list[str] = []
    human_review_misses: list[str] = []
    unexplained_cases: list[str] = []

    for case in dataset.cases:
        prediction = predictor(case)
        if not isinstance(prediction, EvaluationPrediction):
            raise TypeError(
                "predictor must return ancova_ops.evaluation.EvaluationPrediction"
            )

        if prediction.department == case.expected_department:
            department_correct += 1
        else:
            department_errors.append(case.case_id)

        if case.expected_human_review:
            high_risk_count += 1
            if prediction.requires_human_review:
                high_risk_reviewed += 1
            else:
                human_review_misses.append(case.case_id)

        if any(reason.strip() for reason in prediction.reasons):
            explained_count += 1
        else:
            unexplained_cases.append(case.case_id)

    sample_count = len(dataset.cases)
    human_review_recall = (
        high_risk_reviewed / high_risk_count if high_risk_count else None
    )
    metrics = EvaluationMetrics(
        sample_count=sample_count,
        department_correct=department_correct,
        department_accuracy=department_correct / sample_count,
        high_risk_count=high_risk_count,
        high_risk_reviewed=high_risk_reviewed,
        human_review_recall=human_review_recall,
        explained_count=explained_count,
        explanation_coverage=explained_count / sample_count,
    )
    return EvaluationReport(
        system_name=system_name,
        dataset_name=dataset.name,
        dataset_version=dataset.version,
        metrics=metrics,
        department_errors=tuple(department_errors),
        human_review_misses=tuple(human_review_misses),
        unexplained_cases=tuple(unexplained_cases),
    )


def compare_reports(
    baseline: EvaluationReport,
    candidate: EvaluationReport,
) -> ComparisonReport:
    if (
        baseline.dataset_name != candidate.dataset_name
        or baseline.dataset_version != candidate.dataset_version
        or baseline.metrics.sample_count != candidate.metrics.sample_count
    ):
        raise ValueError("baseline and candidate must use the same evaluation dataset")

    department_delta = (
        candidate.metrics.department_accuracy - baseline.metrics.department_accuracy
    )
    explanation_delta = (
        candidate.metrics.explanation_coverage - baseline.metrics.explanation_coverage
    )

    baseline_recall = baseline.metrics.human_review_recall
    candidate_recall = candidate.metrics.human_review_recall
    if baseline_recall is None or candidate_recall is None:
        recall_delta = None
        comparable_deltas = [department_delta, explanation_delta]
    else:
        recall_delta = candidate_recall - baseline_recall
        comparable_deltas = [department_delta, recall_delta, explanation_delta]

    tolerance = 1e-12
    no_regressions = all(delta >= -tolerance for delta in comparable_deltas)
    strict_improvement = any(delta > tolerance for delta in comparable_deltas)

    if no_regressions and strict_improvement:
        verdict = "improved"
    elif no_regressions:
        verdict = "tied"
    elif any(delta > tolerance for delta in comparable_deltas):
        verdict = "mixed"
    else:
        verdict = "regressed"

    return ComparisonReport(
        baseline_system=baseline.system_name,
        candidate_system=candidate.system_name,
        dataset_name=baseline.dataset_name,
        dataset_version=baseline.dataset_version,
        department_accuracy_delta=department_delta,
        human_review_recall_delta=recall_delta,
        explanation_coverage_delta=explanation_delta,
        no_regressions=no_regressions,
        strict_improvement=strict_improvement,
        eligible_for_improvement_claim=verdict == "improved",
        verdict=verdict,
    )


def load_predictor(spec: str) -> Predictor:
    try:
        module_name, attribute = spec.split(":", 1)
    except ValueError as exc:
        raise ValueError("candidate must use module:function syntax") from exc

    module = importlib.import_module(module_name)
    predictor = getattr(module, attribute)
    if not callable(predictor):
        raise TypeError(f"{spec} is not callable")
    return predictor


def _report_dict(report: EvaluationReport) -> dict[str, object]:
    return asdict(report)


def _format_percentage(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"


def _print_text_report(report: EvaluationReport) -> None:
    metrics = report.metrics
    print(f"System: {report.system_name}")
    print(f"Dataset: {report.dataset_name} v{report.dataset_version}")
    print(
        "Department accuracy: "
        f"{_format_percentage(metrics.department_accuracy)} "
        f"({metrics.department_correct}/{metrics.sample_count})"
    )
    print(
        "High-risk human-review recall: "
        f"{_format_percentage(metrics.human_review_recall)} "
        f"({metrics.high_risk_reviewed}/{metrics.high_risk_count})"
    )
    print(
        "Explanation coverage: "
        f"{_format_percentage(metrics.explanation_coverage)} "
        f"({metrics.explained_count}/{metrics.sample_count})"
    )
    if report.department_errors:
        print("Department errors: " + ", ".join(report.department_errors))
    if report.human_review_misses:
        print("Human-review misses: " + ", ".join(report.human_review_misses))
    if report.unexplained_cases:
        print("Unexplained cases: " + ", ".join(report.unexplained_cases))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate ANCOVA Ops routing systems on the same labelled fixture set."
    )
    parser.add_argument(
        "--fixture",
        default=str(DEFAULT_FIXTURE_PATH),
        help="Path to a labelled evaluation JSON fixture.",
    )
    parser.add_argument(
        "--candidate",
        help=(
            "Optional candidate predictor using module:function syntax. The callable must accept "
            "EvaluationCase and return EvaluationPrediction."
        ),
    )
    parser.add_argument("--candidate-name", help="Display name for the candidate system.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    dataset = load_dataset(args.fixture)
    baseline = evaluate_predictor(
        dataset,
        baseline_predict,
        system_name="transparent-baseline-v1",
    )

    candidate = None
    comparison = None
    if args.candidate:
        predictor = load_predictor(args.candidate)
        candidate = evaluate_predictor(
            dataset,
            predictor,
            system_name=args.candidate_name or args.candidate,
        )
        comparison = compare_reports(baseline, candidate)

    if args.json:
        payload: dict[str, object] = {
            "dataset": {
                "name": dataset.name,
                "version": dataset.version,
                "provenance": dataset.provenance,
                "label_status": dataset.label_status,
                "limitations": list(dataset.limitations),
            },
            "baseline": _report_dict(baseline),
        }
        if candidate is not None and comparison is not None:
            payload["candidate"] = _report_dict(candidate)
            payload["comparison"] = asdict(comparison)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    _print_text_report(baseline)
    if candidate is not None and comparison is not None:
        print()
        _print_text_report(candidate)
        print()
        print(f"Comparison verdict: {comparison.verdict}")
        print(
            "Eligible for improvement claim: "
            f"{comparison.eligible_for_improvement_claim}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
