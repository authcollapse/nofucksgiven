from __future__ import annotations

from nofucksgiven.leaderboard import load_leaderboard, render_markdown, validate_leaderboard


def test_leaderboard_data_is_valid() -> None:
    payload, algorithms = load_leaderboard()

    assert validate_leaderboard(payload["criteria"], algorithms) == []


def test_leaderboard_is_sorted_by_evidence_score() -> None:
    _, algorithms = load_leaderboard()
    scores = [algorithm.evidence_score for algorithm in algorithms]

    assert scores == sorted(scores, reverse=True)


def test_legacy_algorithms_do_not_rank_as_recommended() -> None:
    _, algorithms = load_leaderboard()
    statuses = {algorithm.name: algorithm.status for algorithm in algorithms}

    assert statuses["RC4"] == "do_not_use"
    assert statuses["DES"] == "do_not_use"
    assert statuses["Triple DES / TDEA"] == "deprecated_or_withdrawn"


def test_current_local_baselines_include_local_experiments() -> None:
    _, algorithms = load_leaderboard()
    by_name = {algorithm.name: algorithm for algorithm in algorithms}

    assert "known_answer_vectors" in by_name["AES-GCM-256"].local_experiments
    assert "known_answer_vectors" in by_name["ChaCha20-Poly1305"].local_experiments


def test_rendered_leaderboard_contains_warning_and_rankings() -> None:
    payload, algorithms = load_leaderboard()
    markdown = render_markdown(payload["criteria"], algorithms)

    assert "not a proof of security" in markdown
    assert "| Rank | Algorithm |" in markdown
    assert "AES-GCM-256" in markdown
