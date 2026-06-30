.PHONY: setup test lint format format-check claims docs-check leaderboard check bench-smoke docs-build docs-serve clean

VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
RUFF ?= $(VENV)/bin/ruff

setup:
	python -m venv $(VENV)
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

format-check:
	$(RUFF) format --check .

claims:
	$(PYTHON) scripts/check_claims.py

docs-check:
	$(PYTHON) scripts/check_internal_links.py

leaderboard:
	$(PYTHON) scripts/render_leaderboard.py

check: leaderboard format-check lint claims docs-check test

bench-smoke:
	$(PYTHON) benchmarks/bench_aead.py --iterations 10 --sizes 64 1024

docs-build:
	$(PYTHON) -m mkdocs build --strict

docs-serve:
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf .pytest_cache .ruff_cache .hypothesis
	rm -rf site
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
