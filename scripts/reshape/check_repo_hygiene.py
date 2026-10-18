"""Guard against generated root artifacts and tracked ignored outputs.

Detection is name-only / path-pattern based: this checker classifies tracked
paths by their *names* and never reads or prints the contents of any file.
"""

from __future__ import annotations

import fnmatch
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Approved top-level files. Anything else tracked at the repo root is flagged
# as an unknown root entry.
ROOT_FILE_ALLOWLIST = {
    "AGENTS.md",
    "SECURITY.md",
    ".env.example",
    ".gitattributes",
    ".gitignore",
    ".node-version",
    "LICENSE",
    "Makefile",
    "README.md",
    "package.json",
    # Generated, checked contracts: scripts/artifact_manifest.py and
    # scripts/gen_cli_surface.py write them; tests/test_artifact_manifest.py
    # checks them. candidate-dependencies.json is pinned by the pack
    # requirements.txt files under astrid/packs/{comfy_wrap,vibecomfy}.
    "artifacts.json",
    "candidate-dependencies.json",
    "cli-surface.json",
    "pyproject.toml",
}

# Legacy scratch notes the owner committed at the repo root. They are not
# product or source content, but they are the owner's to move or delete, so
# this checker tolerates exactly these names and nothing else.
# SHRINK-ONLY: the owner moves or deletes entries; never add one. A new root
# file belongs in ROOT_FILE_ALLOWLIST only if it is product content, and an
# entry that is no longer tracked must be removed (find_stale_legacy_root_clutter).
LEGACY_ROOT_CLUTTER = {
    "discord_solution_check.md",
    "eval_100_stratified.json",
    "eval_100_stratified.md",
    "eval_run_results.md",
    "failure_taxonomy.md",
    "gh_workflow_issues_shortlist.md",
    "judged_assessment_summary.md",
    "pitfall_analysis.json",
    "pitfall_report.md",
    "sense_check_v2_report.md",
    "vibecomfy_scenario_assessment.json",
    "vibecomfy_scenario_quality.md",
    "workflow_provided_shortlist.md",
    "workflow_questions_shortlist.md",
    "workflow_scenarios_100.json",
    "workflow_scenarios_100.md",
    "workflow_scenarios_FINAL.md",
    "workflow_scenarios_master.json",
}

# Approved top-level directories.
ROOT_DIR_ALLOWLIST = {
    # Stage 1 acceptance output; runtime state remains classified below.
    ".astrid-convergence",
    ".github",
    ".megaplan",
    ".vscode",
    "astrid",
    "artifacts",
    # Product configuration and contracts read by code and tests:
    # config/ (capability ledger, runtime, hivemind contract),
    # schemas/ (JSON schemas validated by tests/schemas),
    # astrid_runtime_client/ (vendored generated client, imported by
    # scripts and astrid), evals/ (timeline eval harness imported by tests/evals).
    "astrid_runtime_client",
    "config",
    "docs",
    "evals",
    "examples",
    "planning",
    "remotion",
    "requirements",
    "schemas",
    "scripts",
    # Authored storyboard provenance (not generated render output).
    "storyboards",
    "tests",
    "tools",
    # Authored operator source and records, committed deliberately:
    # workflows/ (H3 workflow scripts and READMEs referenced by guides and
    # scripts/watch_h3_5090_storage.py), projects/ (H3 continuation recipe
    # exercised by tests/test_h3_continuation_runner_contract.py), guides/
    # (operator guides linked from README and checked by check_doc_references),
    # receipts/ and findings/ (durable review evidence, like
    # .astrid-convergence; nothing in code reads them), output/ (one tracked
    # imagegen prompt source; generated output elsewhere stays untracked).
    "findings",
    "guides",
    "output",
    "projects",
    "receipts",
    "workflows",
}

ROOT_GENERATED_PATTERNS = (
    "agentic-*.report.md",
    "chain.yaml",
    "dry_run_map.json",
    "idea.md",
    "M5_TEST_STATUS.md",
    "plan_revision.json",
    "plan_v1.revised.md",
    "report-*.md",
    "scorecard.png",
)

# Legitimate tracked files/sources that look output-ish but must be kept.
# The classifier consults this allowlist before applying any rule so that
# fixtures, example env files, and the secrets *source module* are never
# flagged. We match by path/name only; contents are never inspected.
TRACKED_PATH_ALLOWLISTS = (
    ".env.example",
    "astrid/core/util/credentials_scope.py",
    "astrid/core/util/secrets.py",
    "docs/assets/astrid-orchestration.png",
    "tests/core/test_credentials_scope.py",
    "tests/core/test_dataset_build_credentials_parity.py",
    "tests/core/util/test_secrets.py",
    "tests/sdk/test_zero_secret_smoke.py",
    "tests/v10/test_m6_secret_sink.py",
    "tests/**/fixtures/**",
    "tests/fixtures/**",
    # Element/workflow assets that are authored pack content, not runtime
    # output: render-element plates and cards, and the h3_av inpaint masks.
    "astrid/packs/*/rendering/elements/**/assets/*",
    "astrid/packs/h3_av/workflows/**/mask_*.png",
    # Docs *about* credentials (setup/reference prose), never credential values.
    "docs/**/*credentials*.md",
)

# Each rule is (category-label, name/path globs). A tracked path is flagged
# under every category whose globs it matches (after the allowlist check).
TRACKED_PATH_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "local env filename",
        (
            ".env",
            ".env.*",
            "this.env",
            "*/.env",
            "*/.env.*",
            "*/this.env",
        ),
    ),
    (
        "credential-like filename",
        (
            "*.pem",
            "*.key",
            "*.p12",
            "*.pfx",
            "*credentials*",
            "*secret*",
        ),
    ),
    (
        "generated runtime directory",
        (
            "runs",
            "runs/*",
            "runs/**",
            "*/runs/*",
            "out",
            "out/*",
            "out/**",
            "*/out/*",
            "cache/*",
            "*/cache/*",
            ".astrid",
            ".astrid/*",
            ".astrid/**",
            "*/.astrid/*",
            "tests/agentic/reports/*",
            "astrid/packs/*/build/*",
            "examples/packs/*/build/*",
        ),
    ),
    (
        "generated project worktree",
        (
            "mgt-*",
            "mgt-*/**",
        ),
    ),
    (
        "tracked runtime media output",
        (
            "*.mp4",
            "*.mov",
            "*.wav",
            "*.mp3",
            "*.jpg",
            "*.jpeg",
            "*.png",
        ),
    ),
    (
        "preview/temp artifact",
        (
            "*.preview.*",
            "*tmp_*",
        ),
    ),
    (
        "local tool state",
        (
            ".DS_Store",
            "*/.DS_Store",
            ".compactify",
            ".compactify/*",
            ".compactify/**",
            ".desloppify",
            ".desloppify/*",
            ".desloppify/**",
            "*/.desloppify",
            "*/.desloppify/*",
            "*/.desloppify/**",
            ".venv",
            ".venv/*",
            ".venv/**",
            "node_modules",
            "node_modules/*",
            "node_modules/**",
            "*.bak",
        ),
    ),
    (
        "megaplan local state",
        (
            # docs/megaplan/ is the source-of-truth directory and is
            # intentionally NOT matched here; only local state roots are.
            ".megaplan",
            ".megaplan/*",
            ".megaplan/**",
            ".megaplan-agentic",
            ".megaplan-agentic/*",
            ".megaplan-agentic/**",
        ),
    ),
)

def _tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def _matches_any(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def _is_allowlisted(path: str) -> bool:
    return _matches_any(path, TRACKED_PATH_ALLOWLISTS)


def find_stale_legacy_root_clutter(tracked: list[str] | None = None) -> list[str]:
    """LEGACY_ROOT_CLUTTER entries that are no longer tracked (must be removed)."""
    present = set(tracked if tracked is not None else _tracked_files())
    return sorted(name for name in LEGACY_ROOT_CLUTTER if name not in present)


def find_root_generated_artifacts() -> list[str]:
    findings: list[str] = []
    for pattern in ROOT_GENERATED_PATTERNS:
        findings.extend(path.name for path in REPO_ROOT.glob(pattern) if path.is_file())
    return sorted(set(findings))


def find_unknown_root_entries(tracked: list[str] | None = None) -> list[str]:
    findings: list[str] = []
    for path in tracked if tracked is not None else _tracked_files():
        if "/" in path:
            root = path.split("/", 1)[0]
            if root not in ROOT_DIR_ALLOWLIST and (REPO_ROOT / path).exists():
                findings.append(root + "/")
            continue
        if (
            path not in ROOT_FILE_ALLOWLIST
            and path not in LEGACY_ROOT_CLUTTER
            and (REPO_ROOT / path).exists()
        ):
            findings.append(path)
    return sorted(set(findings))


def classify_tracked_path(path: str) -> list[str]:
    if _is_allowlisted(path):
        return []
    return [label for label, patterns in TRACKED_PATH_RULES if _matches_any(path, patterns)]


def find_tracked_ignored_artifacts(
    tracked: list[str] | None = None,
) -> list[tuple[str, str]]:
    findings: set[tuple[str, str]] = set()
    for path in tracked if tracked is not None else _tracked_files():
        if not (REPO_ROOT / path).exists():
            continue
        for category in classify_tracked_path(path):
            findings.add((category, path))
    return sorted(findings, key=lambda item: (item[1], item[0]))


def main() -> int:
    failed = False

    unknown_root = find_unknown_root_entries()
    if unknown_root:
        failed = True
        print("unknown root entries must not be committed or kept at repository root:", file=sys.stderr)
        for path in unknown_root:
            print(f"  {path}", file=sys.stderr)

    stale_clutter = find_stale_legacy_root_clutter()
    if stale_clutter:
        failed = True
        print("LEGACY_ROOT_CLUTTER is shrink-only; remove entries that are no longer tracked:", file=sys.stderr)
        for path in stale_clutter:
            print(f"  {path}", file=sys.stderr)

    root_findings = find_root_generated_artifacts()
    if root_findings:
        failed = True
        print("root generated artifacts must not be committed or kept at repository root:", file=sys.stderr)
        for path in root_findings:
            print(f"  [root generated artifact] {path}", file=sys.stderr)

    tracked_findings = find_tracked_ignored_artifacts()
    if tracked_findings:
        failed = True
        print("tracked ignored artifacts must not be committed:", file=sys.stderr)
        for category, path in tracked_findings:
            print(f"  [{category}] {path}", file=sys.stderr)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
