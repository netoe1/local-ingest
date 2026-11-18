# File reference

This reference describes every maintained project file tracked in the repository, except this document itself. Generated files such as `__pycache__`, `.pytest_cache`, build output, and virtual environments are excluded.

## Project root

| File | Purpose |
| --- | --- |
| [`.gitignore`](../.gitignore) | Lists local, generated, and editor files Git should ignore while keeping the shared VS Code settings and launch configuration trackable. |
| [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) | Defines code-quality hooks run before commits, including whitespace, syntax, import ordering, and lint checks. |
| [`LICENSE`](../LICENSE) | Contains the project's MIT license and attribution. |
| [`README.md`](../README.md) | Introduces the project, installation, CLI and Python API usage, and links to the detailed guides. |
| [`pyproject.toml`](../pyproject.toml) | Declares package metadata, runtime and development dependencies, the `local-ingest` command, build configuration, lint settings, and pytest configuration. |

## VS Code workspace files

| File | Purpose |
| --- | --- |
| [`.vscode/settings.json`](../.vscode/settings.json) | Adds `src/` to Pylance's import search paths so editor diagnostics can resolve the project's flat source layout. |
| [`.vscode/launch.json`](../.vscode/launch.json) | Defines a debugger launch configuration for `cli` with the project root as its working directory and `src/` on `PYTHONPATH`. |

## Application modules

| File | Purpose |
| --- | --- |
| [`src/cli.py`](../src/cli.py) | Defines the Click command, parses user options, invokes the ingestion API, and reports completion or errors. |
| [`src/config.py`](../src/config.py) | Holds default file, traversal, total-size, timeout, and output-name settings. |
| [`src/entrypoint.py`](../src/entrypoint.py) | Coordinates path resolution, filters, ignore files, ingestion, and optional output writing. Exposes synchronous and asynchronous APIs. |
| [`src/ingestion.py`](../src/ingestion.py) | Traverses directories, applies filters and safety limits, handles files and links, and passes the resulting tree to the formatter. |
| [`src/local_ingest.py`](../src/local_ingest.py) | Exposes `ingest` and `ingest_async` as the public Python API. |
| [`src/output_formatter.py`](../src/output_formatter.py) | Builds the human-readable summary, directory tree, file-content sections, and approximate token estimate. |
| [`src/query_parser.py`](../src/query_parser.py) | Expands and validates a local source path and creates the scan query. |

## Data models

| File | Purpose |
| --- | --- |
| [`src/schemas/__init__.py`](../src/schemas/__init__.py) | Re-exports the query and filesystem model types for internal imports. |
| [`src/schemas/filesystem.py`](../src/schemas/filesystem.py) | Defines filesystem node types, traversal statistics, tree nodes, child sorting, and lazy content reading. |
| [`src/schemas/ingestion.py`](../src/schemas/ingestion.py) | Defines `IngestionQuery`, the data object carrying the source path and scan options. |

## Utility modules

| File | Purpose |
| --- | --- |
| [`src/utils/__init__.py`](../src/utils/__init__.py) | Marks the utility directory as an importable Python package. |
| [`src/utils/compat_func.py`](../src/utils/compat_func.py) | Provides small cross-platform or cross-version helpers, including suffix removal and link reading. |
| [`src/utils/compat_typing.py`](../src/utils/compat_typing.py) | Re-exports typing constructs with fallbacks for older supported Python versions. |
| [`src/utils/exceptions.py`](../src/utils/exceptions.py) | Defines custom exceptions for notebook errors and legacy timeout or GitHub token cases. |
| [`src/utils/file_utils.py`](../src/utils/file_utils.py) | Reads file samples, selects likely text encodings, and checks whether bytes decode as text. |
| [`src/utils/ignore_patterns.py`](../src/utils/ignore_patterns.py) | Defines the default exclusions and loads patterns from `.gitignore`, `.gitingestignore`, and other ignore files. |
| [`src/utils/ingestion_utils.py`](../src/utils/ingestion_utils.py) | Matches paths relative to the scan root against include and exclude patterns. |
| [`src/utils/logging_config.py`](../src/utils/logging_config.py) | Configures standard-library logging, terminal colors, log levels, and the `LOG_COLOR` override. |
| [`src/utils/notebook.py`](../src/utils/notebook.py) | Reads notebook JSON and renders cells and outputs as text. |
| [`src/utils/pattern_utils.py`](../src/utils/pattern_utils.py) | Splits and normalizes include/exclude patterns and combines user exclusions with defaults. |

## Test files

| File | Purpose |
| --- | --- |
| [`tests/__init__.py`](../tests/__init__.py) | Marks the test directory as an importable package. |
| [`tests/conftest.py`](../tests/conftest.py) | Provides shared fixtures for sample queries, filesystem trees, and notebook files. |
| [`tests/.pylintrc`](../tests/.pylintrc) | Configures Pylint for the test suite. |
| [`tests/query_parser/__init__.py`](../tests/query_parser/__init__.py) | Marks the query-parser test directory as a package. |
| [`tests/query_parser/test_query_parser.py`](../tests/query_parser/test_query_parser.py) | Tests local path resolution, missing paths, and unique query identifiers. |
| [`tests/test_cli.py`](../tests/test_cli.py) | Tests command-line output, file creation, filtering options, and stdout behavior. |
| [`tests/test_gitignore_feature.py`](../tests/test_gitignore_feature.py) | Tests loading ignore patterns and applying them during ingestion. |
| [`tests/test_ingestion.py`](../tests/test_ingestion.py) | Tests recursive scanning, tree output, content gathering, and include/exclude filters. |
| [`tests/test_notebook_utils.py`](../tests/test_notebook_utils.py) | Tests notebook parsing, cell formatting, and output extraction. |
| [`tests/test_pattern_utils.py`](../tests/test_pattern_utils.py) | Tests normalization and combination of include/exclude patterns. |

## Documentation files

| File | Purpose |
| --- | --- |
| [`docs/workflow.md`](workflow.md) | Explains the runtime flow from CLI input through scanning and digest output. |
| [`docs/file-reference.md`](file-reference.md) | This file-by-file project index. |
