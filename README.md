# local-ingest

> **Notice:** This project is a lightweight, modified fork of [coderamp-labs/gitingest](https://github.com), adapted to work **exclusively locally and offline**, without web server, Docker, or remote repository cloning dependencies.

A command-line interface (CLI) tool and Python library to turn any local file or directory into a prompt-friendly text digest for Large Language Models (LLMs).

---

## 🚀 Features

* **100% Local & Offline:** Reads entire directories or individual files directly from your local filesystem.
* **Respects `.gitignore`:** Automatically skips files matched by `.gitignore` and `.gitingestignore` (with an option to include them).
* **Flexible Filtering:** Supports shell-style glob patterns to include (`-i`) or exclude (`-e`) specific files and directories.
* **Token Estimation:** Built-in token counting (`tiktoken`) to help with LLM context window planning.
* **Notebook Support:** Automatically converts `.ipynb` Jupyter notebooks into clean, readable Python scripts.

---

## 📦 Local Installation

To install the `local-ingest` command globally in an isolated environment using `pipx` (recommended) or `pip`:

```bash
# Clone your fork
git clone <YOUR_REPOSITORY_URL>
cd local-ingest

# Recommended installation (isolated via pipx in editable mode)
pipx install -e .

# Or via pip inside a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 💡 Command Line Usage (CLI)

By default, `local-ingest` writes the output to a file named `digest.txt` in your current working directory.

```bash
# Analyze the current directory
local-ingest

# Analyze a specific directory
local-ingest /path/to/your/project

# Analyze a single file
local-ingest /path/to/your/file.py

# Stream output directly to STDOUT or pipe to clipboard
local-ingest . -o -
local-ingest . -o - | xclip -selection clipboard

# Save to a custom output file
local-ingest ./src -o src_context.txt

# Filter by file extensions (include only Python and Markdown files)
local-ingest . -i "*.py" -i "*.md"

# Exclude specific folders or file types
local-ingest . -e "tests/*" -e "*.log"

# Include files normally ignored by .gitignore
local-ingest . --include-gitignored

# Set maximum file size in bytes (e.g., 500 KB)
local-ingest . -s 512000
```

---

## 🐍 Python Package Usage

You can also import the ingestion engine directly into your Python scripts:

```python
from gitingest import ingest

# Ingest a local directory
summary, tree, content = ingest("/path/to/project")

print(summary)
print(tree)

# Filter patterns and save directly to a file
summary, tree, content = ingest(
    "/path/to/project",
    include_patterns={"*.py", "*.c", "*.h"},
    exclude_patterns={"build/*"},
    output="output.txt",
)
```

---

## 🛠️ Refactoring Status (Temporary)

This repository is currently undergoing cleanup to strip out all legacy network and web server code:

* [X] Removed FastAPI server, HTML templates, frontend JS, and Docker/S3 configurations.
* [X] Removed upstream CI/CD workflows and deployment metadata.
* [ ] Final cleanup of internal `git clone` and remote authentication modules (`entrypoint.py`, `query_parser.py`).
* [ ] Update unit tests to cover purely local filesystem scenarios.

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](./LICENSE) for more details.

* Original project by **Romain Courtois** and **Filip Christiansen** ([gitingest](https://github.com)).
* Local modifications by **Ely Torres Neto**.
