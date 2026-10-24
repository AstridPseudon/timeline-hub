#!/bin/sh
set -eu
: "${D83_STUB_COUNT:?D83_STUB_COUNT is required}"
printf '%s\n' called
exit 17
