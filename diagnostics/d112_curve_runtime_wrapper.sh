#!/bin/sh
set -eu
export PYTHONPATH="$(dirname "$0")${PYTHONPATH:+:$PYTHONPATH}"
exec /home/user/work/venv-runtime/bin/python "$@"
