#!/usr/bin/env python3
"""Command-line utility to list and run tools from the package.

Usage:
  tools                           # List all available tools
  tools [uv_options] tool_name [tool_arguments]  # Run a specific tool

Examples:
  tools                           # List all available tools
  tools github_clone_dev          # Run the github_clone_dev tool
  tools --python 3.9 github_clone_dev repo  # Run with Python 3.9

"""
from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path


def get_package():
    """Find the package by importing it."""
    try:
        import akaihola_tools

        return akaihola_tools
    except ImportError:
        print("Error: Could not find the akaihola_tools package.")
        sys.exit(1)


def get_tools():
    """Discover all Python modules in the package."""
    package = get_package()
    package_name = package.__name__
    package_path = Path(package.__file__).parent
    tools = []

    for file in package_path.glob("*.py"):
        if file.name == "__init__.py" or file.name == "tools.py":
            continue

        # Get the module name
        module_name = file.stem

        # Try to import the module to get its docstring
        try:
            module = importlib.import_module(f"{package_name}.{module_name}")
            description = (
                module.__doc__.strip().split("\n")[0]
                if module.__doc__
                else "No description available"
            )
        except (ImportError, AttributeError):
            description = "No description available"

        tools.append((module_name, description))

    return tools, package_name


def list_tools():
    """Print out names and descriptions of each Python script in the package."""
    tools, _ = get_tools()

    print("Available tools:")
    for name, description in sorted(tools):
        print(f"  {name}: {description}")


def parse_command_line(args):
    """Parse command line to extract tool name, options for uv run, and arguments for the tool."""
    for i, arg in enumerate(args):
        if not arg.startswith("-"):
            # Found the tool name
            return arg, args[:i], args[i + 1 :]

    # No tool name found
    return None, args, []


def run_tool(args):
    """Run the specified tool using uv run."""
    tool_name, uv_options, tool_args = parse_command_line(args)

    if tool_name is None:
        print("Error: No tool name provided.")
        sys.exit(1)

    tools, package_name = get_tools()
    tool_names = [name for name, _ in tools]

    if tool_name not in tool_names:
        print(f"Error: Tool '{tool_name}' not found.")
        sys.exit(1)

    # Get the package path
    package = get_package()
    package_path = Path(package.__file__).parent
    tool_path = package_path / f"{tool_name}.py"

    # Construct the command
    cmd = ["uv", "run"] + uv_options + [str(tool_path)] + tool_args

    # Execute the command
    subprocess.run(cmd, check=False)


def main(args: list[str] | None = None) -> None:
    """Execute the tools command.

    Args:
        args: Command line arguments. If None, sys.argv[1:] is used.

    """
    if args is None:
        args = sys.argv[1:]

    if len(args) == 0 or "--list" in args:
        # No arguments or --list flag, list available tools
        list_tools()
    else:
        # Run the specified tool
        run_tool(args)


if __name__ == "__main__":
    main()
