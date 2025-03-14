#!/usr/bin/env bash

errors=0

VIRTUAL_ENV=
UV_PYTHON=.venv
uv venv
uv pip install click GitPython pytest
uv run pytest . || errors=$?

exit $errors
