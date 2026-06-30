"""Evidence leaderboard helpers.

Scores here are transparent confidence indicators for comparison and triage.
They are not proofs of cryptographic security.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


DEFAULT_LEADERBOARD_PATH = Path(__file__).resolve().parents[2] / "data/security_leaderboard.json"


@dataclass(frozen=True)
class AlgorithmEvidence:
    name: str
    family: str
    status: str
    score_components: dict[str, int]
    local_experiments: tuple[str, ...]
    strengths: tuple[str, ...]
    cautions: tuple[str, ...]
    sources: tuple[str, ...]

    @property
    def evidence_score(self) -> int:
        return sum(self.score_components.values())


def load_leaderboard(
    path: Path = DEFAULT_LEADERBOARD_PATH,
) -> tuple[dict[str, Any], list[AlgorithmEvidence]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    algorithms = [
        AlgorithmEvidence(
            name=item["name"],
            family=item["family"],
            status=item["status"],
            score_components=dict(item["score_components"]),
            local_experiments=tuple(item["local_experiments"]),
            strengths=tuple(item["strengths"]),
            cautions=tuple(item["cautions"]),
            sources=tuple(item["sources"]),
        )
        for item in payload["algorithms"]
    ]
    return payload, sorted(algorithms, key=lambda item: (-item.evidence_score, item.name))


def validate_leaderboard(
    criteria: dict[str, int],
    algorithms: list[AlgorithmEvidence],
) -> list[str]:
    findings: list[str] = []
    criteria_names = set(criteria)
    seen_names: set[str] = set()

    for algorithm in algorithms:
        if algorithm.name in seen_names:
            findings.append(f"duplicate algorithm: {algorithm.name}")
        seen_names.add(algorithm.name)

        component_names = set(algorithm.score_components)
        if component_names != criteria_names:
            findings.append(
                f"{algorithm.name}: score components {sorted(component_names)} "
                f"do not match criteria {sorted(criteria_names)}"
            )
        for name, value in algorithm.score_components.items():
            max_value = criteria.get(name)
            if max_value is None:
                continue
            if value < 0 or value > max_value:
                findings.append(f"{algorithm.name}: {name} score {value} outside 0..{max_value}")
        if not algorithm.sources:
            findings.append(f"{algorithm.name}: missing sources")
        if algorithm.evidence_score > sum(criteria.values()):
            findings.append(f"{algorithm.name}: total score exceeds rubric maximum")
    return findings


def render_markdown(criteria: dict[str, int], algorithms: list[AlgorithmEvidence]) -> str:
    lines = [
        "# Encryption Evidence Leaderboard",
        "",
        "This is an evidence-confidence leaderboard, not a proof of security. "
        "Use it to compare what we know, what we have tested locally, and what still needs evidence.",
        "",
        "## Rubric",
        "",
        "| Criterion | Max |",
        "| --- | ---: |",
    ]
    for name, max_value in criteria.items():
        lines.append(f"| {name.replace('_', ' ').title()} | {max_value} |")

    lines.extend(
        [
            "",
            "## Leaderboard",
            "",
            "| Rank | Algorithm | Family | Status | Evidence Score | Local Experiments | Main Caution |",
            "| ---: | --- | --- | --- | ---: | --- | --- |",
        ]
    )

    for rank, algorithm in enumerate(algorithms, start=1):
        experiments = (
            ", ".join(algorithm.local_experiments) if algorithm.local_experiments else "none yet"
        )
        caution = algorithm.cautions[0] if algorithm.cautions else ""
        lines.append(
            f"| {rank} | {algorithm.name} | {algorithm.family} | {algorithm.status} | "
            f"{algorithm.evidence_score} | {experiments} | {caution} |"
        )

    lines.extend(
        [
            "",
            "## Source Tags",
            "",
        ]
    )
    for algorithm in algorithms:
        lines.append(f"- {algorithm.name}: {', '.join(algorithm.sources)}")

    lines.extend(
        [
            "",
            "## How To Read This",
            "",
            "- A high score means stronger public evidence and safer default shape, not guaranteed safety.",
            "- Local experiments currently cover only algorithms implemented in `src/nofucksgiven/baselines.py`.",
            "- Performance benchmarks belong beside environment metadata; they do not increase security.",
            "- Legacy algorithms stay on the board so we can test that our tooling rejects or warns on them.",
            "",
        ]
    )
    return "\n".join(lines)
