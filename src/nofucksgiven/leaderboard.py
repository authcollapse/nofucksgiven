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


def _status_badge(status: str) -> str:
    label_by_status = {
        "recommended_baseline": ("baseline", "go"),
        "recommended_misuse_resistant": ("misuse-resistant", "go"),
        "recommended_constrained_devices": ("constrained devices", "lab"),
        "recommended_when_available": ("extended nonce", "lab"),
        "acceptable_when_composed_correctly": ("compose carefully", "lab"),
        "experimental_lab": ("lab build", "lab"),
        "avoid_for_new_work": ("avoid", "avoid"),
        "do_not_use_for_secret_data": ("do not use", "avoid"),
        "deprecated_or_withdrawn": ("withdrawn", "avoid"),
        "do_not_use": ("do not use", "avoid"),
    }
    label, kind = label_by_status.get(status, (status.replace("_", " "), "lab"))
    return f'<span class="nfg-status nfg-status--{kind}">{label}</span>'


def _experiment_label(experiments: tuple[str, ...]) -> str:
    if not experiments:
        return "none yet"
    short_names = {
        "known_answer_vectors": "vectors",
        "round_trip_property_tests": "round trips",
        "tamper_rejection_tests": "tamper rejection",
        "benchmark_smoke": "benchmark smoke",
        "deterministic_datasets": "deterministic datasets",
        "nonce_reuse_failure_demos": "nonce-reuse failure demos",
    }
    return ", ".join(short_names.get(item, item.replace("_", " ")) for item in experiments)


def _podium_card(algorithm: AlgorithmEvidence, rank: int) -> list[str]:
    rank_labels = {
        1: "#1 | belt holder",
        2: "#2 | mistake-resistant challenger",
        3: "#3 | software-speed favorite",
    }
    score_colors = {1: "gold", 2: "silver", 3: "bronze"}
    tagline_by_name = {
        "AES-GCM-256": (
            "The default heavyweight. Standardized, widely deployed, locally tested here. "
            "Still gets folded by nonce reuse."
        ),
        "AES-GCM-SIV": (
            "Built for a better nonce-mistake posture. Winning on public evidence while it waits "
            "for local reps."
        ),
        "ChaCha20-Poly1305": (
            "The software-speed favorite. Clean modern AEAD shape, no freestyle nonce nonsense."
        ),
    }
    card_class = "nfg-card nfg-card--champ" if rank == 1 else "nfg-card"
    tagline = tagline_by_name.get(
        algorithm.name,
        algorithm.cautions[0] if algorithm.cautions else "Bring evidence before bragging.",
    )
    return [
        f'<div class="{card_class}" markdown>',
        f'<div class="nfg-rank">{rank_labels[rank]}</div>',
        f'<div class="nfg-score nfg-score--{score_colors[rank]}">{algorithm.evidence_score}</div>',
        f"### {algorithm.name}",
        f'<p class="nfg-tagline">{tagline}</p>',
        "</div>",
        "",
    ]


def _score_breakdown(algorithm: AlgorithmEvidence, criteria: dict[str, int]) -> list[str]:
    labels = {
        "standard_status": "Standard",
        "security_margin": "Margin",
        "auth_integrity": "Auth",
        "misuse_resistance": "Misuse",
        "review_maturity": "Review",
    }
    lines = ['  <div class="nfg-score-breakdown" aria-label="Score breakdown">']
    for name, max_value in criteria.items():
        value = algorithm.score_components[name]
        label = labels.get(name, name.replace("_", " ").title())
        lines.extend(
            [
                '    <div class="nfg-score-chip">',
                f"      <span>{label}</span>",
                f"      <strong>{value}/{max_value}</strong>",
                "    </div>",
            ]
        )
    lines.append("  </div>")
    return lines


def _standings_card(algorithm: AlgorithmEvidence, rank: int, criteria: dict[str, int]) -> list[str]:
    top_class = " nfg-competitor--top" if rank <= 3 else ""
    nfg_class = " nfg-competitor--nfg" if algorithm.name == "NFG-v0" else ""
    experiments = _experiment_label(algorithm.local_experiments)
    caution = algorithm.cautions[0] if algorithm.cautions else "Bring evidence before bragging."
    lines = [
        f'<article class="nfg-competitor{top_class}{nfg_class}">',
        f'  <div class="nfg-competitor__rank">#{rank}</div>',
        '  <div class="nfg-competitor__main">',
        f"    <h3>{algorithm.name}</h3>",
        f"    <p>{algorithm.family}</p>",
        "  </div>",
        f"  <div>{_status_badge(algorithm.status)}</div>",
        f'  <div class="nfg-competitor__score">{algorithm.evidence_score}</div>',
    ]
    lines.extend(_score_breakdown(algorithm, criteria))
    lines.extend(
        [
            f'  <div class="nfg-competitor__detail"><strong>Local reps:</strong> {experiments}</div>',
            f'  <div class="nfg-competitor__detail"><strong>Caution:</strong> {caution}</div>',
        ]
    )
    lines.extend(
        [
            "</article>",
            "",
        ]
    )
    return lines


def render_markdown(criteria: dict[str, int], algorithms: list[AlgorithmEvidence]) -> str:
    lines = [
        "# Encryption Evidence Leaderboard",
        "",
        '<section class="nfg-hero" markdown>',
        '<div class="nfg-hero__kicker">Season one standings</div>',
        '<div class="nfg-hero__title">Authenticated encryption cage match.</div>',
        "",
        '<p class="nfg-hero__subtitle">',
        "The score is evidence confidence: standards, review maturity, misuse shape, "
        "auth integrity, and what this repo has actually tested. It is not a magical "
        "security number.",
        "</p>",
        "</section>",
        "",
        '<div class="nfg-podium" markdown>',
    ]
    for rank, algorithm in enumerate(algorithms[:3], start=1):
        lines.extend(_podium_card(algorithm, rank))
    lines.extend(
        [
            "</div>",
            "",
            '<p class="nfg-callout">',
            'High score means "stronger public evidence and safer default shape." '
            'It is not a proof of security, and it is not "go encrypt production '
            'data with random code from a GitHub repo."',
            "</p>",
            "",
        ]
    )

    lines.extend(
        [
            "",
            "## Rubric",
            "",
            "| Criterion | Max |",
            "| --- | ---: |",
        ]
    )
    for name, max_value in criteria.items():
        lines.append(f"| {name.replace('_', ' ').title()} | {max_value} |")

    lines.extend(
        [
            "",
            "## Leaderboard",
            "",
            '<div class="nfg-standings">',
        ]
    )

    for rank, algorithm in enumerate(algorithms, start=1):
        lines.extend(_standings_card(algorithm, rank, criteria))

    lines.extend(
        [
            "</div>",
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
            "- Local experiments currently cover algorithms implemented in `src/nofucksgiven/baselines.py` and the NFG-v0 scaffold under `experiments/nfg/`.",
            "- Performance benchmarks belong beside environment metadata; they do not increase security.",
            "- Legacy algorithms stay on the board so we can test that our tooling rejects or warns on them.",
            "",
        ]
    )
    return "\n".join(lines)
