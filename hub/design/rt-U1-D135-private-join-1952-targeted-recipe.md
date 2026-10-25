# Targeted test recipe

The local run was not submitted because available space was 4,804,920 KiB,
below the required fresh 5 GiB threshold. The exact command to run on a farm
with the existing Runtime venv is:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D135-private-join-1952/evidence/targeted.xml tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py
```

Central test-service recipe (do not duplicate locally):

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-U1-D135-private-join-1952 targeted --files "tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The farm must use the existing Runtime venv and private test/cache paths.
