# AGENTS.md

## Purpose

This repository is developed collaboratively by humans and coding agents. Keep changes small, reviewable and evidence-oriented.

## Product direction

ANCOVA Ops is not an "ANCOVA chatbot". The system has separate layers:

1. request understanding and feature extraction;
2. routing / human hand-off;
3. operational outcome collection;
4. statistical analysis of historical outcomes;
5. later, carefully evaluated adaptive or predictive models.

Do not implement ANCOVA as a sentiment classifier or message filter.

## Development rules

- Use English for code, documentation, issues, PRs and commit messages.
- Prefer transparent baseline logic before complex ML.
- Do not claim project performance from synthetic data.
- Label synthetic, benchmark and measured data distinctly.
- Keep personal or resident data out of the repository.
- Add tests for new routing or analytical behaviour.
- Preserve human-readable explanations for routing decisions.
- Statistical code must state the model formula and assumptions being tested.

## Near-term scope

Phase 0 and Phase 1 should remain lightweight. Do not add LSTM, agentic orchestration or large infrastructure until a baseline dataset and evaluation protocol exist.

## Commands

```bash
pip install -e ".[dev]"
pytest
python -m ancova_ops.demo
```
