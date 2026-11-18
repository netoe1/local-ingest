"""Command-line interface (CLI) for Gitingest."""

# pylint: disable=no-value-for-parameter
from __future__ import annotations

import asyncio
from typing import TypedDict

import click
from typing_extensions import Unpack

from config import MAX_FILE_SIZE, OUTPUT_FILE_NAME
from entrypoint import ingest_async

# Import logging configuration first to intercept all logging
from utils.logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class _CLIArgs(TypedDict):
    source: str
    max_size: int
    exclude_pattern: tuple[str, ...]
    include_pattern: tuple[str, ...]
    include_gitignored: bool
    output: str | None


@click.command()
@click.argument("source", type=str, default=".")
@click.option(
    "--max-size",
    "-s",
    default=MAX_FILE_SIZE,
    show_default=True,
    help="Maximum file size to process in bytes",
)
@click.option("--exclude-pattern", "-e", multiple=True, help="Shell-style patterns to exclude.")
@click.option(
    "--include-pattern",
    "-i",
    multiple=True,
    help="Shell-style patterns to include.",
)
@click.option(
    "--include-gitignored",
    is_flag=True,
    default=False,
    help="Include files matched by .gitignore and .gitingestignore",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output file path (default: digest.txt in current directory). Use '-' for stdout.",
)
def main(**cli_kwargs: Unpack[_CLIArgs]) -> None:
    """Run the CLI entry point to scan a local file or directory.

    Parameters
    ----------
    **cli_kwargs : Unpack[_CLIArgs]
        A dictionary of keyword arguments forwarded to ``ingest_async``.

    Notes
    -----
    See ``ingest_async`` for a detailed description of each argument.

    Examples
    --------
    Basic usage:
        $ local-ingest
        $ local-ingest /path/to/folder
        $ local-ingest /path/to/file.txt

    Output to stdout:
        $ local-ingest -o -

    With filtering:
        $ local-ingest -i "*.py" -e "*.log"
        $ local-ingest --include-pattern "*.js" --exclude-pattern "node_modules/*"

    """
    asyncio.run(_async_main(**cli_kwargs))


async def _async_main(
    source: str,
    *,
    max_size: int = MAX_FILE_SIZE,
    exclude_pattern: tuple[str, ...] | None = None,
    include_pattern: tuple[str, ...] | None = None,
    include_gitignored: bool = False,
    output: str | None = None,
) -> None:
    """Analyze a local path and create a text dump of its contents.

    This command scans the specified local file or directory,
    applies custom include and exclude patterns, and generates a text summary of
    the analysis.  The summary is written to an output file or printed to ``stdout``.

    Parameters
    ----------
    source : str
        A path to a local file or directory.
    max_size : int
        Maximum file size in bytes to ingest (default: 10 MB).
    exclude_pattern : tuple[str, ...] | None
        Glob patterns for pruning the file set.
    include_pattern : tuple[str, ...] | None
        Glob patterns for including files in the output.
    include_gitignored : bool
        If ``True``, also ingest files matched by ``.gitignore`` or ``.gitingestignore`` (default: ``False``).
    output : str | None
        The path where the output file will be written (default: ``digest.txt`` in current directory).
        Use ``"-"`` to write to ``stdout``.

    Raises
    ------
    click.Abort
        Raised if an error occurs during execution and the command must be aborted.

    """
    try:
        # Normalise pattern containers (the ingest layer expects sets)
        exclude_patterns = set(exclude_pattern) if exclude_pattern else set()
        include_patterns = set(include_pattern) if include_pattern else set()

        output_target = output if output is not None else OUTPUT_FILE_NAME

        if output_target == "-":
            click.echo("Analyzing source, preparing output for stdout...", err=True)
        else:
            click.echo(f"Analyzing source, output will be written to '{output_target}'...", err=True)

        summary, _, _ = await ingest_async(
            source,
            max_file_size=max_size,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            include_gitignored=include_gitignored,
            output=output_target,
        )
    except Exception as exc:
        # Convert any exception into Click.Abort so that exit status is non-zero
        click.echo(f"Error: {exc}", err=True)
        raise click.Abort from exc

    if output_target == "-":  # stdout
        click.echo("\n--- Summary ---", err=True)
        click.echo(summary, err=True)
        click.echo("--- End Summary ---", err=True)
        click.echo("Analysis complete! Output sent to stdout.", err=True)
    else:  # file
        click.echo(f"Analysis complete! Output written to: {output_target}")
        click.echo("\nSummary:")
        click.echo(summary)


if __name__ == "__main__":
    main()
