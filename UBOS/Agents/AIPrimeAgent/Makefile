# UBOS AI Prime Agent Makefile

PY ?= python3
PORT ?= 5035
QUERY ?= How to orchestrate agents under UBOS?
DEPTH ?= medium
LIB_TIMEOUT ?= 90
RESEARCH_TIMEOUT ?= 120
RESEARCH_CLI ?=

# Paths (relative to this Makefile location)
PRIME_PYTHONPATH := .
LIBRARIAN_PYTHONPATH := ../../KnowledgeAgent/MasterLibrarianAgent
BOOKS_DIR := ../../SystemFundamentals/Books

.PHONY: help install test test-e2e run-librarian run-librarian-bg stop-librarian run-prime-stub run-prime-real clean-artifacts

help:
	@echo "Targets:"
	@echo "  install             - install AI Prime requirements"
	@echo "  test                - run unit/integration tests (no network)"
	@echo "  test-e2e            - run E2E tests (requires RUN_UBOS_E2E=1 and API keys)"
	@echo "  run-librarian       - run Librarian REST (foreground) on PORT=$(PORT)"
	@echo "  run-librarian-bg    - run Librarian REST (background) on PORT=$(PORT)"
	@echo "  stop-librarian      - stop background Librarian on PORT=$(PORT)"
	@echo "  run-prime-stub      - run Prime with stub adapters (writes artifacts/)"
	@echo "  run-prime-real      - run Prime with Librarian REST and optional Research CLI"
	@echo "  clean-artifacts     - prune reports older than 14 days"
	@echo "Variables: PORT, QUERY, DEPTH, LIB_TIMEOUT, RESEARCH_CLI, RESEARCH_TIMEOUT"

install:
	$(PY) -m pip install -r requirements.txt

test:
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $(PY) -m pytest -q

test-e2e:
	RUN_UBOS_E2E=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $(PY) -m pytest -q -k e2e

run-librarian:
	UBOS_BOOKS_PATH=$$(pwd)/$(BOOKS_DIR) \
	PYTHONPATH=$(LIBRARIAN_PYTHONPATH) \
	$(PY) -c "from master_librarian.api.app import create_app; create_app().run(host='127.0.0.1', port=$(PORT))"

run-librarian-bg:
	UBOS_BOOKS_PATH=$$(pwd)/$(BOOKS_DIR) \
	PYTHONPATH=$(LIBRARIAN_PYTHONPATH) \
	nohup $(PY) -c "from master_librarian.api.app import create_app; create_app().run(host='127.0.0.1', port=$(PORT))" \
	  > /tmp/ml_server_$(PORT).log 2>&1 & echo $$! > /tmp/ml_pid_$(PORT)
	@echo "Librarian started on http://127.0.0.1:$(PORT) (PID: $$(cat /tmp/ml_pid_$(PORT)))"

stop-librarian:
	-kill $$(cat /tmp/ml_pid_$(PORT)) 2>/dev/null || true
	@rm -f /tmp/ml_pid_$(PORT)

run-prime-stub:
	PYTHONPATH=$(PRIME_PYTHONPATH) \
	$(PY) -m ai_prime_agent.cli research-synthesize \
	  --query "$(QUERY)" --depth $(DEPTH) \
	  --report-dir artifacts \
	  --transcript /tmp/prime_transcript.jsonl
	@echo "Cleaning up old artifacts..."
	@bash scripts/clean_artifacts.sh 7

run-prime-real:
	PYTHONPATH=$(PRIME_PYTHONPATH) \
	$(PY) -m ai_prime_agent.cli research-synthesize \
	  --query "$(QUERY)" --depth $(DEPTH) \
	  --librarian-url "http://127.0.0.1:$(PORT)" \
	  --librarian-timeout $(LIB_TIMEOUT) \
	  $(if $(LIBRARIAN_AUTH),--librarian-auth $(LIBRARIAN_AUTH),) \
	  $(if $(RESEARCH_CLI),--research-cli $(RESEARCH_CLI) --research-timeout $(RESEARCH_TIMEOUT),) \
	  --report-dir artifacts \
	  --transcript /tmp/prime_transcript.jsonl
	@echo "Cleaning up old artifacts..."
	@bash scripts/clean_artifacts.sh 7

clean-artifacts:
	bash scripts/clean_artifacts.sh 14

