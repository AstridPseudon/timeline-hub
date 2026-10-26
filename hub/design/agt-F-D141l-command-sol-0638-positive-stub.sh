#!/bin/sh
set -eu
printf '%s\n' called >> "$P4_STUB_COUNT"
exit 17
