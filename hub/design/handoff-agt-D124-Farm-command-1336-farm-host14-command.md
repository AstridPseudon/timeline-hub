# D124 Farm input: separate host14 original-14 command

This derivative preserves the original host14 light proof as a separate route.
It must not be merged into or retargeted to the corrected 0b586e core tuple,
and it must not consume the core D73 manifest.

## Exact host14 tuple and pending receipts

| role | Farm checkout binding | commit | tree | parent guard |
| --- | --- | --- | --- | --- |
| Agent | <FARM_NORMAL_CHECKOUT_AGENT_9EA67534> | 9ea67534f61d3604c9cb136de449803c4cbe51c2 | ded3451dca1546b971d512cc97f5d83181490d93 | 9ea67534f61d3604c9cb136de449803c4cbe51c2 369ffa7c00bd3d45c610fac7651ff79e7a283a1a |
| Runtime | <FARM_NORMAL_CHECKOUT_RUNTIME_369FFA7C> | 369ffa7c00bd3d45c610fac7651ff79e7a283a1a | 9bf331d68df8c966e8927a3f083ba03687803c99 | 369ffa7c00bd3d45c610fac7651ff79e7a283a1a e65422348314084a1a3cb6687fcdc520c73347e8 |

The normal profile and child venv remain Farm-lead inputs keyed to this
Agent/Runtime pair, not to the core 0b/42aad pair and not to the old
9cd3dbe8/1d9ddba5 near-match:

~~~text
HOST14_PYTHON=<NORMAL_CHILD_VENV_PYTHON_RECEIPT_FOR_9EA67534_AND_369FFA7C>
HOST14_NODE=<NORMAL_PROFILE_NODE_RECEIPT_FOR_V20.19.4>
HOST14_PROFILE=<NORMAL_RUNTIME_PROFILE_RECEIPT_FOR_9EA67534_AND_369FFA7C>
HOST14_EVIDENCE=<FARM_OWNED_D124_HOST14_EVIDENCE_DIRECTORY>
HOST14_POSITIVE_CONTROL=<LEAD_EXISTING_PARSED_POSITIVE_CONTROL>
HOST14_POSITIVE_COUNTER=<LEAD_FRESH_HOST14_POSITIVE_COUNTER>
HOST14_POISON_CONTROL=<LEAD_EXISTING_PARSED_POISON_CONTROL>
HOST14_POISON_COUNTER=<LEAD_FRESH_HOST14_POISON_COUNTER>
~~~

ABI targets are Node v20.19.4, Composition 0.0.14, archive
819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234, lock
f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d, registry
d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96, and
schema sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b.
They are validation targets only.

## Exact selector command

The launcher remains the existing qualified blob, SHA-256
cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1. The
source hash of tests/sdk/test_host_bootstrap_source_identity.py is
08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b.

~~~sh
set -eu
: "${AGENT_CHECKOUT_HOST14:?Farm must bind the normal Agent 9ea checkout}"
: "${RUNTIME_CHECKOUT_HOST14:?Farm must bind the normal Runtime 369 checkout}"
: "${HOST14_PYTHON:?Farm must bind the normal child-venv Python receipt}"
: "${HOST14_NODE:?Farm must bind the normal Node receipt}"
: "${HOST14_PROFILE:?Farm must bind the normal profile receipt}"
: "${HOST14_EVIDENCE:?Farm must bind host14 evidence}"
test "$(git -C "$AGENT_CHECKOUT_HOST14" rev-parse HEAD)" = 9ea67534f61d3604c9cb136de449803c4cbe51c2
test "$(git -C "$AGENT_CHECKOUT_HOST14" rev-parse HEAD^{tree})" = ded3451dca1546b971d512cc97f5d83181490d93
test "$(git -C "$RUNTIME_CHECKOUT_HOST14" rev-parse HEAD)" = 369ffa7c00bd3d45c610fac7651ff79e7a283a1a
test "$(git -C "$RUNTIME_CHECKOUT_HOST14" rev-parse HEAD^{tree})" = 9bf331d68df8c966e8927a3f083ba03687803c99
test "$(sha256sum "$AGENT_CHECKOUT_HOST14/tests/sdk/test_host_bootstrap_source_identity.py" | awk '{print $1}')" = 08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b
exec env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT_HOST14:$RUNTIME_CHECKOUT_HOST14" \
  PATH="$(dirname "$HOST14_NODE"):/usr/local/bin:/usr/bin:/bin" \
  VIRTUAL_ENV="$(dirname "$(dirname "$HOST14_PYTHON")")" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT_HOST14" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT_HOST14" \
  ASTRID_REMOTION_PROJECT_DIR="$HOST14_PROFILE" ASTRID_TEST_NODE_MODULES="$HOST14_PROFILE/node_modules" \
  "$HOST14_PYTHON" -P -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$HOST14_EVIDENCE/host14.xml" \
  tests/sdk/test_host_bootstrap_source_identity.py -k 'bootstrap_stops_on_correlated_terminal_registration_failure or startup_budget_polling_preserves_identity_and_original_cleanup'
~~~

Run the existing parsed-once positive and poison-zero controls first, with
fresh host14 counters. Expected body accounting is 14 passed, 0 failed,
0 errors, 0 skipped; it is not an observed result here. Farm owns admission
and footprint, and may order host14 before the heavy corrected core when its
resource guard permits.
