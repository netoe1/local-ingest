# local-ingest

`local-ingest` is an offline command-line tool and Python library that turns a local file or directory into a readable text digest for use as context with language models. It works with ordinary folders and files; the source does not need to be a Git repository.

It scans the local filesystem only. It does not clone remote repositories or run a web server. It can apply include/exclude glob patterns, respect `.gitignore`, `.gitingestignore`, and `.ignore` rules, skip large or binary files, estimate token counts, and convert Jupyter notebooks into readable Python text.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Command line

```bash
local-ingest .                         # scan the current directory
local-ingest /path/to/folder           # scan any local folder
local-ingest /path/to/file.py          # scan one file
local-ingest . -i '*.py' -i '*.md'     # include matching files
local-ingest . -e 'build/*' -e '*.log' # exclude matching files
local-ingest . --include-gitignored    # ignore-file rules are bypassed
local-ingest . -s 512000               # maximum individual file size
local-ingest . -o - | xclip -selection clipboard
```

By default, output is written to `digest.txt` in the current directory. Use `-o -` to write the digest to standard output.

## Python API

```python
from local_ingest import ingest

summary, tree, content = ingest("/path/to/any/folder")
summary, tree, content = ingest(
    "/path/to/file.py",
    include_patterns={"*.py"},
    output="digest.txt",
)
```

The returned values are a short summary, a tree view, and the collected text. Ingestion runs locally and does not require network access.

## Origin

This project began as a lightweight local adaptation of [Gitingest](https://github.com/coderamp-labs/gitingest). Its purpose here is general local file and folder ingestion, not remote Git repository processing.

## License

MIT. See [LICENSE](./LICENSE).
