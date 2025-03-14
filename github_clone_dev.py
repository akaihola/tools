# /// script
# requires-python = ">=3.7"
# dependencies = [
#     "click>=8.0.0",
#     "gitpython>=3.1.30",
# ]
# ///

import os
import sys
import click
import git
import subprocess
from pathlib import Path


@click.command()
@click.argument('repo', required=False)
def main(repo=None):
    """Clone a GitHub repository into ~/repos/python and install it in development mode."""
    # Get the repository name if not provided
    if not repo:
        repo = click.prompt("Enter GitHub repository (e.g. psf/black)")

    # Validate repo format
    if "/" not in repo:
        click.echo("Error: Repository should be in format 'owner/repo'")
        sys.exit(1)

    # Extract repo name from the full repo path
    repo_name = repo.split("/")[-1]

    # Determine target directory
    base_dir = Path.home() / "repos" / "python"
    target_dir = base_dir / repo_name

    # Create base directory if it doesn't exist
    base_dir.mkdir(parents=True, exist_ok=True)

    # Check if target directory already exists
    if target_dir.exists():
        click.echo(f"Directory {target_dir} already exists, skipping clone.")
    else:
        # Clone the repository
        click.echo(f"Cloning {repo} into {target_dir}...")
        try:
            git.Repo.clone_from(f"https://github.com/{repo}.git", target_dir)
            click.echo(f"Successfully cloned {repo}")
        except git.GitCommandError as e:
            click.echo(f"Error cloning repository: {e}")
            sys.exit(1)

    # Install in development mode using UV
    click.echo(f"Installing {repo_name} in development mode...")
    try:
        result = subprocess.run(
            ["uv", "pip", "install", "-e", str(target_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        click.echo(f"Successfully installed {repo_name} in development mode")
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error installing {repo_name}: {e}")
        click.echo(e.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
