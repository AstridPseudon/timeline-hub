#!/bin/sh
# Private actual-layout fixture launcher. It models a venv's bin/python while
# keeping all package bytes in the fixture's site-packages directory.
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
site=$(find "$root/lib" -mindepth 2 -maxdepth 2 -type d -name site-packages -print -quit)
[ -n "$site" ]
if [ "${1:-}" != '-I' ]; then
  echo 'fixture-python requires the isolated -I shape' >&2
  exit 2
fi
shift
if [ "${1:-}" = '-c' ]; then
  code=${2:?missing -c code}
  shift 2
  exec "${D21B_FIXTURE_PYTHON:-python3}" -I -c \
    'import sys; site=sys.argv[1]; code=sys.argv[2]; sys.path.insert(0, site); sys.argv=["<child -c>", *sys.argv[3:]]; exec(compile(code, "<child -c>", "exec"), {"__name__": "__main__"})' \
    "$site" "$code" "$@"
fi
if [ "${1:-}" = '-' ]; then
  shift
  exec "${D21B_FIXTURE_PYTHON:-python3}" -I -c \
    'import sys; site=sys.argv[1]; sys.path.insert(0, site); sys.argv=["<child stdin>", *sys.argv[2:]]; exec(compile(sys.stdin.read(), "<child stdin>", "exec"), {"__name__": "__main__"})' \
    "$site" "$@"
fi
echo 'fixture-python supports only -I - and -I -c' >&2
exit 2
