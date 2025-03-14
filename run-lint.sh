#!/usr/bin/env bash

uvx --with isort darker .

errors=0

command -v ruff >/dev/null || with_ruff="--with ruff"
uvx --with mypy --with pydocstyle ${with_ruff} graylint . || errors=$?

exit $errors
