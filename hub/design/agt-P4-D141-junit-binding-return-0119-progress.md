# P4 D141c operational first return

Status: `PASS_OPERATIONAL_SOURCE`.

1. Read the settled PLAN, AGENTS.md, and the independent result review. The review's single custody finding is accepted and corrected without relabeling receipts.
2. Prepared a new immutable manifest input and separate durable body-evidence directory under this worker's absolute evidence root.
3. Preserved Agent `28e56`, Runtime `6a011`, App `867cb273`, Composition `635f4de0`, all source guards/origins/versions, C0 fields, timeout 45, cleared addopts, cache-off, `-m integration`, and the three original selectors.
4. Bound generated manifest `junit_paths`, launcher-generated runmanifest `junit_paths`, and candidate shell `--junitxml` to the same durable path.
5. Ran the unchanged production launcher in `run` mode with a stub: positive exit 17/counter 1; agent-SHA-only poison exit 1/counter 0.
6. No suite installation, request-test, pytest, collection, product import, original body, registry mutation, or shared dependency write was performed.

The existing controller can now run the corrected actual proof once. The old 10086 JUnit and old 1347 failure remain preserved and separately identified.
