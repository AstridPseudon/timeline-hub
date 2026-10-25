#!/bin/sh
set -eu
export PYTHONPATH="/home/user/work/wt/rt-D112-acceptance-return-0850/diagnostics${PYTHONPATH:+:$PYTHONPATH}"
exec /home/user/work/venv-runtime/bin/python "$@"
