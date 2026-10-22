"""Every declared skip names CI jobs that exist, so no skip is invisible (UR skip rule)."""

from __future__ import annotations

import re
from pathlib import Path

from tests.lanes import SKIP_REGISTRY

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"


def _jobs() -> set[str]:
    jobs: set[str] = set()
    for workflow in WORKFLOWS.glob("*.yml"):
        text = workflow.read_text(encoding="utf-8")
        body = text.split("\njobs:\n", 1)[1]
        jobs.update(re.findall(r"^  ([a-z][a-z0-9-]*):\s*$", body, flags=re.M))
    return jobs


def test_every_declared_skip_names_ci_jobs_that_run_it() -> None:
    jobs = _jobs()
    problems = []
    for declared in SKIP_REGISTRY.values():
        if not declared.ci:
            problems.append(f"{declared.name}: no CI job runs it where the condition is false")
        problems.extend(f"{declared.name}: no such CI job {job!r}" for job in declared.ci if job not in jobs)
    assert not problems, "\n".join(problems)


def test_darwin_native_job_runs_the_marked_lane() -> None:
    ci = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")
    assert "-m darwin_native" in ci
