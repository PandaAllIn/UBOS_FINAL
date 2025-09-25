# UBOS Workflow Integration Handoff

**Date:** 2025-09-25

## 1. High-Level Goal

The primary objective is to create a comprehensive integration test suite (`test_ubos_workflow_integration.py`) that validates the end-to-end workflow of the UBOS agent system. The plan is to test each "upstream" agent in sequence, starting with the `ResearchAgent` and `MasterLibrarianAgent`.

## 2. Current Status

-   **Phase 1, Step 1 (Research Agent): COMPLETE & SUCCESSFUL.** The test `test_1_phase1_step1_execute_real_research` successfully calls the `UBOSResearchAgent`, gets real data from the Perplexity API, and validates the structured output.
-   **Phase 1, Step 2 (Master Librarian Agent): BLOCKED.** We are attempting to implement `test_2_phase1_step2_execute_real_consultation`. This test needs to import and instantiate components from the `MasterLibrarianAgent`, but it is consistently failing due to a complex and persistent `ImportError`.

## 3. The Core Problem: Persistent `ImportError`

When the test suite attempts to import components from the `MasterLibrarianAgent` (specifically `UbosIngester`), it fails with an `ImportError`. The root cause appears to be a complex circular dependency and/or packaging issue within the `master_librarian` module.

The typical error is:
`ImportError: cannot import name 'UbosIngester' from 'master_librarian.ingestion.ubos_ingester' (...)`

This error occurs even when `sys.path` is correctly configured, indicating the problem lies with how the `master_librarian` package is internally structured and how its `__init__.py` files are resolving imports.

## 4. Unsuccessful Attempts to Resolve the Issue

I have made numerous attempts to fix this issue, all of which have failed. The next agent should **avoid repeating these exact steps**:

1.  **Modifying `sys.path` in Agent `__init__.py` files:** Added `sys.path.append()` logic to `master_librarian/__init__.py`. This led to deeper circular dependencies.
2.  **Blanking `__init__.py` files:** I systematically cleared the contents of all `__init__.py` files within the `master_librarian` directory to treat them as simple namespace packages. This still resulted in import errors.
3.  **Creating Aliases:** I identified a potential typo (`UBOSKnowledgeIngester` vs. `UbosIngester`) and tried to create an alias in `ingestion/__init__.py` to resolve it. This did not fix the underlying import resolution problem.
4.  **Correcting Typos Directly:** I tried correcting the typo in `api/app.py` directly. This also failed.
5.  **Direct File Imports:** I modified the `test_ubos_workflow_integration.py` file to use direct, file-level imports (e.g., `from master_librarian.ingestion.ubos_ingester import UbosIngester`). This was the most promising approach but still failed, indicating the problem is triggered as soon as the Python interpreter enters the `master_librarian` package.
6.  **Reverting and Retrying:** I have reverted all changes multiple times to restore the codebase to a clean state before trying a new combination of the above fixes. The error remains the same.

## 5. Key Files

-   **Test File:** `/Users/panda/Desktop/UBOS/UBOS/test_ubos_workflow_integration.py`
-   **Problematic Package Root:** `/Users/panda/Desktop/UBOS/UBOS/Agents/KnowledgeAgent/MasterLibrarianAgent/master_librarian/`
-   **Key Files in Package:**
    -   `__init__.py` (and all other `__init__.py` files in subdirectories)
    -   `api/app.py`
    -   `ingestion/ubos_ingester.py`
    -   `ingestion/yaml_parser.py`

## 6. Recommended Next Steps for the New Agent

My attempts have been focused on manipulating the codebase directly. A fresh perspective is needed.

1.  **External Research:** Use the `google_web_search` tool to investigate advanced Python import resolution strategies for complex, nested package structures with potential circular dependencies. Search for terms like: "Python circular import error in nested packages", "relative vs absolute imports __init__.py", "python namespace package import issues".
2.  **Analyze Project Structure:** Before modifying any code, perform a more thorough analysis of the entire project's import patterns. There may be a convention used in other agents that I have missed. Use `glob` and `read_many_files` to study how other agents (`AIPrimeAgent`, `AgentSummoner`) handle their internal imports.
3.  **Consider a Different Pathing Strategy:** The current strategy of adding agent roots to `sys.path` in the test file is standard, but there might be a nuance I'm missing. Investigate if an environment variable like `PYTHONPATH` or a different test runner configuration is expected.
4.  **Isolate the Problem:** Create a new, minimal test script (`minimal_import_test.py`) that does nothing but try to import `UbosIngester`. This will allow for faster iteration without running the full test suite.

I have failed to solve this problem. I am handing off this task with all the context I have gathered. Good luck.
