"""Read saved central-test/check-in text; write only this audit's JSON and table."""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
HUB = Path('/home/user/timeline-hub/hub')
OUT = Path(__file__).resolve().parent
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def read(path):
    return path.read_text(errors='replace') if path.is_file() else ''


def stamp(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec='microseconds')


def metadata(path):
    if not path.is_file():
        return {'path': str(path), 'exists': False}
    st = path.stat()
    return {'path': str(path), 'exists': True, 'mtime_utc': stamp(st.st_mtime),
            'size_bytes': st.st_size}


def fields(text):
    return dict(line.split('=', 1) for line in text.splitlines() if '=' in line)


def counts(text):
    text = ANSI.sub('', text)
    result = {'collected': None, 'passed': None, 'failed': None, 'skipped': None,
              'basis': 'unavailable'}
    tap = list(re.finditer(r'^# tests (\d+)$', text, re.M))
    running = list(re.finditer(r'^Running (\d+) tests? using', text, re.M))
    collected = list(re.finditer(r'collected (\d+) items?', text))
    if tap:
        result.update(collected=int(tap[-1][1]), basis='explicit TAP totals')
        for name, key in [('pass', 'passed'), ('fail', 'failed'), ('skipped', 'skipped')]:
            hits = re.findall(r'^# ' + name + r' (\d+)\s*$', text, re.M)
            if hits:
                result[key] = int(hits[-1])
    else:
        # Only terminal result lines; a 404 message containing "failed" is not a count.
        terminal = [line for line in text.splitlines() if re.match(
            r'^\s*(?:=+\s*)?\d+ (?:passed|failed|skipped)(?:\b)', line)]
        if terminal:
            tail = '\n'.join(terminal[-3:])
            for key in ['passed', 'failed', 'skipped']:
                hits = re.findall(r'(\d+) ' + key + r'\b', tail)
                result[key] = int(hits[-1]) if hits else 0
            result['basis'] = 'terminal outcomes; collection inferred from their sum'
            result['collected'] = sum(result[k] for k in ['passed', 'failed', 'skipped'])
        if running or collected:
            result['collected'] = int((running or collected)[-1][1])
            result['basis'] = 'explicit Running/collected line plus terminal outcomes'
        vitest = re.findall(r'Tests\s+(\d+) passed\s+\((\d+)\)', text)
        if vitest:
            result.update(collected=int(vitest[-1][1]), passed=int(vitest[-1][0]),
                          failed=0, skipped=0, basis='saved Vitest Tests totals')
        if 'SyntaxError:' in text and not running and not collected and not terminal:
            result.update(collected=0, passed=0, failed=0, skipped=0,
                          basis='setup SyntaxError before test runner/collection')
    return result


checkins = []
for directory in sorted((ORCH / 'lead/checkins').iterdir()):
    if not directory.is_dir():
        continue
    # Read every saved text file, not just directory names or request timestamps.
    saved = {f.name: read(f) for f in directory.iterdir() if f.is_file()}
    observed = re.search(r'^date=(.*)$', saved.get('facts.txt', ''), re.M)
    floor = datetime.strptime(directory.name, '%Y%m%dT%H%MZ').replace(tzinfo=timezone.utc)
    end = max(f.stat().st_mtime for f in directory.iterdir() if f.is_file())
    checkins.append({'id': directory.name,
                     'envelope_start_utc': floor.isoformat(),
                     'facts_observed_utc': observed[1] if observed else None,
                     'envelope_end_utc': stamp(end),
                     'deletion_instant': None,
                     'boundary_rule': 'minute floor through final saved file; conservative, not a deletion timestamp',
                     'files': [metadata(f) for f in sorted(directory.iterdir()) if f.is_file()],
                     'meta': saved.get('meta', ''),
                     'report': saved.get('report.md', ''),
                     'actions': saved.get('actions.txt', '')})

runs = []
for directory in sorted((ORCH / 'tests').iterdir()):
    if not directory.is_dir() or directory.name == 'cache':
        continue
    saved = {f.name: read(f) for f in directory.iterdir() if f.is_file()}
    summary = saved.get('summary', '')
    log = ANSI.sub('', saved.get('log.txt', ''))
    req, snap = fields(saved.get('request', '')), fields(saved.get('snap', ''))
    cached = re.search(r'already tested by ([^;\s]+)', summary)
    cached_from = saved.get('cached_from', '').strip() or (cached[1] if cached else None)
    imported = not req and not log
    hub_directory = HUB / 'tests' / directory.name
    hub_matches = [name for name in ['snap', 'summary', 'ext', 'status', 'exit']
                   if (directory / name).is_file() and (hub_directory / name).is_file()
                   and read(directory / name) == read(hub_directory / name)]
    duration = re.search(r'exit=\d+ in (\d+)s', summary)
    end_path = directory / 'status'
    end = end_path.stat().st_mtime if end_path.exists() else None
    snap_time = (directory / 'snap').stat().st_mtime if (directory / 'snap').exists() else None
    start = min(snap_time, end - int(duration[1])) if snap_time and end and duration else snap_time
    physical = not imported and not cached_from
    intersections = []
    if physical and start is not None and end is not None:
        if saved.get('status', '').strip() == 'running':
            end = (directory / 'log.txt').stat().st_mtime
        for checkin in checkins:
            lo = datetime.fromisoformat(checkin['envelope_start_utc']).timestamp()
            hi = datetime.fromisoformat(checkin['envelope_end_utc']).timestamp()
            if start <= hi and end >= lo:
                intersections.append(checkin['id'])
    special_lines = []
    for number, line in enumerate(log.splitlines(), 1):
        if (re.search(r'\d{4}-\d\d-\d\d[T ]\d\d:\d\d:\d\d|Start at|Running \d+ tests?|^# (tests|pass|fail|skipped)|\d+ (passed|failed|skipped)|SyntaxError|ENOENT|snapshot', line)
                or 'epochMs' in line):
            special_lines.append({'path': str(directory / 'log.txt'), 'line': number,
                                  'text': line[:1200]})
    result_counts = counts(log or summary)
    result_counts['source'] = 'cached source log; not a new execution' if cached_from else 'actual log' if log else 'imported summary only; original log absent'
    run = {'id': directory.name,
           'origin': 'MAIN_IMPORTED_ASSET' if imported else 'LOCAL_CACHE_HIT' if cached_from else 'LOCAL_PHYSICAL_EXECUTION',
           'origin_proof': {'request_present': bool(req), 'local_log_present': bool(log),
                            'worktree': snap.get('worktree'), 'hub_identical_files': hub_matches,
                            'rule': 'hub-sync exports only status/exit/summary/ext/snap; paths alone do not identify a host'},
           'request': req, 'snapshot': snap, 'external': saved.get('ext', '').strip(),
           'status': saved.get('status', '').strip(), 'exit': saved.get('exit', '').strip() or None,
           'cached_from': cached_from, 'summary_header': summary.split('\n---')[0],
           'hub_current_status': read(hub_directory / 'status').strip() or None,
           'command': next((l[5:] for l in summary.splitlines() if l.startswith('cmd: ')), None),
           'counts': result_counts,
           'window': {'start_lower_bound_utc': stamp(start) if physical and start else None,
                      'end_upper_bound_utc': stamp(end) if physical and end and saved.get('status', '').strip() != 'running' else None,
                      'last_log_write_utc': stamp((directory / 'log.txt').stat().st_mtime) if log else None,
                      'summary_duration_seconds': int(duration[1]) if duration else None,
                      'basis': 'snap mtime and status-minus-summary-duration lower bound; final status upper bound; running uses last log mtime' if physical else 'none: imported result or cache hit is not a local physical execution',
                      'exact_process_start_end_logged': False},
           'checkin_ids': intersections,
           'classification': 'UNCERTAIN_ENVIRONMENT_AFFECTED' if intersections else 'MAIN_NOT_LOCAL' if imported else 'CACHE_TRACE_SOURCE' if cached_from else 'NO_SAVED_CHECKIN_OVERLAP',
           'files': [metadata(directory / n) for n in ['request', 'snap', 'summary', 'status', 'exit', 'log.txt', 'runner.log', 'ext', 'cached_from']],
           'log_event_lines': special_lines,
           'cited_by': [], 'acceptance': 'No exact acceptance citation established yet',
           'required_action': 'No incident rerun: complete local bounds do not intersect a saved check-in'}
    if imported:
        run['required_action'] = ('MAIN imported evidence: local logs/request unavailable; do not infer local execution '
                                  'or unaffected MAIN timing from import mtimes. Original MAIN owner retains validation responsibility.')
    if start and end and physical:
        before = [c for c in checkins if datetime.fromisoformat(c['envelope_end_utc']).timestamp() < start]
        after = [c for c in checkins if datetime.fromisoformat(c['envelope_start_utc']).timestamp() > end]
        run['unaffected_bounds'] = {'previous_checkin_end': before[-1]['envelope_end_utc'] if before else 'handover 2026-10-19T19:34:00Z',
                                    'next_checkin_start': after[0]['envelope_start_utc'] if after else 'fix 2026-10-20T03:12:00Z'}
    runs.append(run)

# Exact-ID citations across current/historical design, status, escalation and reports.
# Manager round logs preserve historical STATUS bodies after STATUS was overwritten.
reference_files = set()
for root in [ORCH / 'design', ORCH / 'escalations', ORCH / 'managers', HUB / 'design', HUB / 'escalations', HUB / 'status']:
    for path in root.rglob('*'):
        if path.is_file() and path.suffix in ['.md', '.log']:
            reference_files.add(path)
for path in (ORCH / 'workers').glob('*/*'):
    if path.parent.name == 'vw-m3-central-deletion-evidence-audit':
        continue
    if path.is_file() and ('report' in path.name.lower() or path.name == 'REVIEW.md'):
        reference_files.add(path)
needle = re.compile('|'.join(re.escape(r['id']) for r in runs))
by_id = {r['id']: r for r in runs}
for path in sorted(reference_files):
    for number, line in enumerate(read(path).splitlines(), 1):
        for match in needle.finditer(line):
            by_id[match[0]]['cited_by'].append({'path': str(path), 'line': number, 'text': line[:1800],
                                             'kind': 'exact ID reference; not automatically approval'})


def cite(run, relative, needle_text, meaning):
    path = ORCH / relative
    for number, line in enumerate(read(path).splitlines(), 1):
        if needle_text in line:
            run['cited_by'].append({'path': str(path), 'line': number, 'text': line,
                                    'kind': meaning})
            return
    raise ValueError(f'Missing reviewed citation: {relative}: {needle_text}')


for run in runs:
    name = run['id']
    run['rerun_plan'] = None
    if name.startswith('vw-m1-ssr-snapshot-'):
        run['acceptance'] = 'ACCEPTED: f8164bef Viewing M1 items closed; final portable result is 21654, not a browser/parity gate'
        cite(run, 'managers/viewing/INBOX.md', 'Good: f816 merged and central 4 PASS', 'explicit orchestrator acceptance')
    elif name == 'composition-full-1020032729-7262':
        run['acceptance'] = 'AFTER-FIX P1 rerun: actual physical 63/63/0/0 on same c04 tree; all original 22 names retained'
        run['rerun_plan'] = 'P1'
        run['required_action'] = 'P1 complete once; compare 22 original names and 63/63 counts in after_fix_mappings. No further Composition incident rerun.'
    elif name == 'composition-full-1020014116-11460':
        run['acceptance'] = 'ACCEPTED: c04ada57/0.0.10 and D12 cleanup evidence; 0122 direction approved, consumer adoption still held'
        cite(run, 'managers/viewing/INBOX.md', 'Composition c04ada5 (0.0.10 opacity export)', 'explicit direction approval')
        cite(run, 'managers/viewing/STATUS.md', 'Integrated: Composition c04ada57', 'integrated status / 63-pass evidence')
        cite(run, 'design/deletion-ledger.viewing.md', '| D12 |', 'accepted deletion item citation')
    elif name == 'composition-full-1020001557-12697':
        run['acceptance'] = 'ACCEPTED source package 0.0.9 / 59 tests; consumers remain 0.0.8 and held'
        cite(run, 'design/viewing-coordination.md', 'ONE central integration npm test59PASS', 'source package evidence; no consumer adoption')
    elif name == 'composition-full-1019202023-13230':
        run['acceptance'] = 'CITED PASS: integrated Composition 0.0.8 baseline, 22 tests; superseded source suite retains all 22 names'
        cite(run, 'escalations/closed/viewing-20261019T2036Z-theme-source-and-consumer-ready.md', 'Composition actual full22pass', 'reported integrated baseline evidence')
        run['rerun_plan'] = 'P1'
    elif name.endswith('1019223448-19007'):
        run['acceptance'] = 'CITED PASS: accepted CPU H264/AAC backend qualification only; App-route and gate6 parity remain open'
        cite(run, 'design/viewing-final-route.md', 'Separately inspected central result:', 'reviewed 8-test backend qualification citation')
        cite(run, 'design/viewing-coordination.md', 'backendqualified8PASS137.83s', 'accepted backend qualification, limited scope')
        run['rerun_plan'] = 'P2'
    elif name.endswith('1019204228-2884'):
        run['acceptance'] = 'CITED PASS: manager accepted native fixture/capture readiness only; frame/export harness and gate6 remained held'
        cite(run, 'managers/viewing/rounds/20261019T2032Z.log', 'The recovered frame-readiness test passed:', 'manager reviewed and accepted limited readiness evidence')
        cite(run, 'managers/viewing/rounds/20261019T2032Z.log', "s=s.replace('Frame34865727b HELD;", 'historical STATUS update; parity explicitly held')
        run['rerun_plan'] = 'P3'
    elif name.endswith('1019201859-32356'):
        run['acceptance'] = 'HELD RED diagnostic: 1/3 passed does not establish audio baseline, M1 closure or parity'
        run['rerun_plan'] = 'P4'
    elif name.endswith('1019204228-3208'):
        run['acceptance'] = 'HELD RED corrected direct-CDP audio baseline, 0/6 passed; not accepted product evidence'
        cite(run, 'workers/vw-m3-player-clock-restart/report.md', '| `vw-m3-player-clock-restart-e2e-viewing-audio-fade-1019204228-3208`', 'explicit failed diagnostic classification')
        run['rerun_plan'] = 'P4'
    elif name.endswith('1020020422-26386') or name.endswith('1020021844-21023'):
        run['acceptance'] = 'HELD RED four-case fixture/render/parity attempts; no accepted MP4/comparator evidence'
        cite(run, 'workers/vw-m3-frame-fixture-schema/REPORT.md', '4 tests / 4 failures', 'fixture-muted schema fix justification; no passing gate')
        run['rerun_plan'] = 'P3'
        if name.endswith('21023'):
            run['classification'] = 'REPORTED_LIVE_DELETION_ENVIRONMENT_INVALID'
            cite(run, 'escalations/closed/viewing-20261020T0302Z-snapshot-postflight.md', 'ENOENT', 'actual missing tracked artifact plus four failed cases')
    elif name.endswith('1019223409-31492'):
        run['acceptance'] = 'NO PHYSICAL RUN: cache hit of 24853 pre-collection syntax failure; not a product finding'
        run['rerun_plan'] = 'P2'
        run['required_action'] = 'Trace to physical 24853; corrected 19007 executed all 8 later but overlaps check-in envelope. One safe P2 rerun covers the corrected CPU test family; never rerun obsolete SyntaxError.'
    elif name.endswith('1019223330-24853'):
        run['acceptance'] = 'Setup SyntaxError, no test collection; source of cached 31492. Corrected 19007 is separate physical evidence'
    elif name.endswith('1020012754-17587'):
        run['acceptance'] = 'ACCEPTED limited live-host lifecycle / cleanup qualification, 1 test; no browser/render/parity claim'
        cite(run, 'design/viewing-coordination.md', 'integration-viewing-host-live-1020012754-17587 PASS1', 'limited host wrapper qualification')
    elif name.endswith('1020011556-27355'):
        run['acceptance'] = 'CITED U1 diagnostic 1 PASS only; original 5/6 RED baseline and gate6 remain open'
        cite(run, 'workers/vw-m3-player-anchor-cause/REPORT.md', 'This single traced PASS is NOT stable6/6 or gate6', 'explicit diagnostic limit')
    elif name.endswith('1020015144-17020'):
        run['acceptance'] = 'HELD RED T1 instrumentation-invalid; not a product fix or valid PCM timing proof'
        cite(run, 'workers/vw-m3-player-anchor-cause/REPORT.md', 'Actual central T1 qualification', 'explicit failed instrumentation classification')
    elif name.endswith('1020002626-14698'):
        run['acceptance'] = 'HELD RED no-primer baseline: 5 PASS / 1 FAIL; all six WAV comparators passing is not six test passes'
        cite(run, 'design/viewing-coordination.md', 'Audio baseline8a315eb6 no-primer', 'explicit baseline red / WAV distinction')
    elif name.endswith('1019225904-10161'):
        run['acceptance'] = 'CITED 3-PASS active monitor-control diagnostic; not untouched first-cold baseline or parity'
        cite(run, 'workers/vw-m3-audio-monitor-control/REPORT.md', 'QUIET_DONE was written immediately', 'three-control diagnostic evidence')
    elif name.endswith('1020031108-18739'):
        run['acceptance'] = 'COMPLETED P3 successor: 4 collected / 1 PASS / 3 FAIL; readiness case PASS after fix, source postflight passed. Render/parity remain RED'
        run['required_action'] = 'P3 completed once: map exact 1/1 readiness and 13 captures; old four-failure families rerun with 4 collected/1 passed/3 failed. No duplicate submission. Keep render/parity failures for separate reviewed follow-up.'
        run['rerun_plan'] = 'P3'
    elif run['status'] == 'pass':
        run['acceptance'] = 'Recorded passing supporting test result; exact-ID references attached where present; no separate gate closure established by this audit'
    elif run['status'] in ['fail', 'error', 'timeout']:
        run['acceptance'] = 'Failed/setup diagnostic; not an accepted PASS or gate closure'
    else:
        run['acceptance'] = 'No completed local result; imported/queued status is not physical execution evidence'
    if run['checkin_ids']:
        run['required_action'] = f"Environment-invalid for acceptance pending one safe rerun ({run['rerun_plan']}); compare collected/pass/fail/skip counts and test identity; no deletion-causal product finding."
    if run['cached_from']:
        source = by_id.get(run['cached_from'])
        run['cached_source_checkin_ids'] = source['checkin_ids'] if source else None
        cache_snap = ORCH / 'tests' / name / 'snap'
        run['cache_service_checkin_ids'] = [c['id'] for c in checkins if cache_snap.is_file()
            and datetime.fromisoformat(c['envelope_start_utc']).timestamp()
            <= cache_snap.stat().st_mtime
            <= datetime.fromisoformat(c['envelope_end_utc']).timestamp()]

old_names = re.findall(r'^# Subtest: (.+)$', read(ORCH / 'tests/composition-full-1019202023-13230/log.txt'), re.M)
new_names = re.findall(r'^# Subtest: (.+)$', read(ORCH / 'tests/composition-full-1020014116-11460/log.txt'), re.M)
after_fix_mappings = []
composition_repeat = by_id.get('composition-full-1020032729-7262')
if composition_repeat and composition_repeat['status'] == 'pass':
    repeat_names = re.findall(r'^# Subtest: (.+)$', read(ORCH / 'tests' / composition_repeat['id'] / 'log.txt'), re.M)
    assert len(repeat_names) == 63 and not (set(old_names) - set(repeat_names))
    assert composition_repeat['snapshot']['tree'] == by_id['composition-full-1020014116-11460']['snapshot']['tree']
    after_fix_mappings.append({'plan': 'P1', 'original': 'composition-full-1019202023-13230',
                              'replacement': composition_repeat['id'], 'status': 'COMPLETE_ONCE',
                              'old_collected_passed': [22, 22], 'new_collected_passed': [63, 63],
                              'retained_old_tests': len(old_names), 'missing_old_names': sorted(set(old_names) - set(repeat_names)),
                              'same_current_c04_tree': True, 'cache_hit': bool(composition_repeat['cached_from'])})
proof_root = ORCH / 'workers/vw-m3-render-route-qualified-prep2'
proof = json.loads(read(proof_root / 'render-door-route-source-result.json'))
tests = json.loads(read(proof_root / 'render-door-route-tests.json'))
readiness_results = []


def test_results(suites):
    for suite in suites:
        for spec in suite.get('specs', []):
            for test in spec['tests']:
                for result in test['results']:
                    yield {'title': spec['title'], 'status': result['status'],
                           'start_utc': result.get('startTime'), 'duration_ms': result.get('duration')}
        yield from test_results(suite.get('suites', []))


results = list(test_results(tests['suites']))
readiness_results = [r for r in results if r['title'].startswith('fixture readiness')]
readiness_artifacts = list(Path('/tmp/viewing-render-door-route-gYm3M3').glob('*/viewing-parity/fixture-readiness.json'))
captures = json.loads(read(readiness_artifacts[0]))['captures'] if len(readiness_artifacts) == 1 else []
assert proof['postflight'] == 'passed' and proof['before'] == proof['after']
assert len(readiness_results) == 1 and readiness_results[0]['status'] == 'passed'
assert len(captures) == 13
assert [(c['frame'], c.get('marker')) for c in captures if c.get('marker') is not None] == [(120, 0), (121, 1), (135, 15), (143, 23), (164, 44), (135, 15)]
after_fix_mappings.append({'plan': 'P3', 'original_pass': 'vw-m3-frame-fixture-restart-e2e-viewing-frame-fixture-1019204228-2884',
                          'replacement': 'vw-m3-render-route-qualified-prep2-e2e-viewing-render-route-qualified-1020031108-18739',
                          'status': 'READINESS_REPRODUCED_ONCE; FOUR_CASE_RERUN_COMPLETE_STILL_RED',
                          'old_readiness_collected_passed': [1, 1], 'new_readiness_collected_passed': [1, 1],
                          'new_all_counts': {'collected': 4, 'passed': 1, 'failed': 3, 'skipped': 0},
                          'per_case_results': results, 'source_postflight': proof['postflight'],
                          'before_after_exact_equal': proof['before'] == proof['after'],
                          'captures': [{'frame': c['frame'], 'marker': c.get('marker')} for c in captures],
                          'actual_readiness_start_after_fix': readiness_results[0]['start_utc'] > '2026-10-20T03:12:00Z',
                          'proof_path': str(proof_root / 'render-door-route-source-result.json'),
                          'test_results_path': str(proof_root / 'render-door-route-tests.json'),
                          'readiness_artifact_path': str(readiness_artifacts[0])})
for run in runs:
    if run['rerun_plan'] == 'P1':
        run['required_action'] = 'COMPLETE_ONCE by physical after-fix 1020032729-7262: 63/63/0/0, original22/22 names retained. No duplicate rerun.'
    elif run['rerun_plan'] == 'P3':
        run['required_action'] = 'COMPLETE_ONCE by terminal 18739: readiness1/1 and13 captures reproduced afterfix; both old four-failure families rerun with4 collected/1 pass/3 fail, postflight passed. Keep render/parity RED; no incident duplicate.'

plans = {
    'P1': {'target': 'integration:composition', 'suite': 'full',
           'proposed_request_not_executed': '$ORCH/bin/request-test integration:composition full --no-cache',
           'inner_command': 'npm test',
           'expected': '63 collected / 63 passed / 0 failed / 0 skipped on frozen c04ada57; separately compare original 22 names, all 22 retained and passing',
           'reason': '22-test cited baseline intersects uncertain 20:20 envelope. Old/current TAP-name set comparison is 22/63 with zero missing. No completed after-fix replacement exists in saved inventory.',
           'manager_only': True},
    'P2': {'target': 'reviewed corrected CPU test source (blob 70f6dc9c021f0b2888e9281f83bdc7b4ab35c576)',
           'suite': 'e2e-viewing-cpu-profile after manager rebinds its obsolete hard-coded runtime path',
           'proposed_request_not_executed': 'BLOCKED until manager reviews existing source/runtime binding; do not run the old setup-run.sh as-is',
           'inner_command': '/home/user/work/venv-agent/bin/python -m pytest -q -m integration -o tmp_path_retention_policy=all --basetemp=<new retained evidence directory> tests/packs/rendering/test_viewing_cpu_export.py',
           'expected': '8 collected / 8 passed / 0 skipped: 5 environment cases plus media-only, text-card, transition-windows exports',
           'reason': 'Cited 19007 overlaps conservative 22:34 check-in envelope. 31492 is cache from pre-check-in SyntaxError 24853, not physical deletion proof; one corrected 8-test rerun covers this family.',
           'runtime_requirements': 'Existing admitted runtime only; Node20.19.4/npm10.8.2, Composition0.0.8/93bc, React18.3.1, Remotion4.0.509, 1194 headless_shell; original source-equality and all77 package hashes before/after. Old /home/user/work/wt/vw-m3-cpu-profile-proof is absent. No install/copy in this audit.',
           'manager_only': True},
    'P3': {'target': 'vw-m3-render-route-qualified-prep2', 'suite': 'e2e-viewing-render-route-qualified',
           'existing_run': 'vw-m3-render-route-qualified-prep2-e2e-viewing-render-route-qualified-1020031108-18739',
           'proposed_request_not_executed': 'NONE: manager waits existing ID; do not duplicate or mutate frozen source',
           'inner_command': 'Existing foreground setup-render-door-route.sh / run-render-door-route.mjs controller, browser flock, Runtime source lease2',
           'expected': '4 collected, no skip: normal Render MP4; managed Player readiness; positive frame comparison; planted picture mismatch control. Compare old readiness subcase 1 collected/1 passed and all 13 captures/0,1,15,23,44 markers/backseek; compare both failed 4-case runs to four individual outcomes.',
           'reason': 'Covers old readiness PASS 2884 plus obsolete fixture failures 26386/21023 on current reviewed muted-schema/routes descendant. Current run began 03:11 (before announced 03:12 fix), still running in saved metadata; cannot credit after-fix completion or passing counts yet.',
           'source_requirements': 'Frozen Agent b70, Runtime9f9 lease2, Composition source c04, installed8/77 bytes/6 hashes, f816 runtime donor; snapshot identity/content pre/post. No original bad-schema replay.',
           'mapping_status': 'PENDING terminal result and exact test/assertion retention comparison; no completed after-fix mapping claimed',
           'manager_only': True},
    'P4': {'target': 'vw-m3-observed-player-baseline', 'suite': 'e2e-viewing-audio-observed-baseline',
           'proposed_request_not_executed': '$ORCH/bin/request-test vw-m3-observed-player-baseline e2e-viewing-audio-observed-baseline --no-cache',
           'inner_command': 'npm exec -- playwright test --config tests/e2e/timeline/player-audio.config.ts --grep "amplified fade timing" --repeat-each=3 --workers=1',
           'expected': '6 collected = 3 warm + 3 first-cold, no skips; report pass/fail split honestly. Old 32356 was only 3 collected/1 passed/2 failed; old 3208 was 6 collected/0 passed/6 failed; current pre-fix baseline14698 is 6 collected/5 passed/1 failed.',
           'reason': 'One current unchanged-graph no-primer rerun for both failed audio antecedents. Existing later6-case baseline is before fix, so does not discharge post-fix rerun. No obsolete keepalive/primer or retired T1 tap.',
           'prerequisites': 'Manager source review/fresh quiet grant and peer acknowledgements, browser flock, BEFORE-gesture external observation, verify-source pre/post and all6 hashes/all77 bytes; no new threshold/gain/codec/clock changes. Preserve original expectations and raw WAVs.',
           'manager_only': True},
}
for mapping in after_fix_mappings:
    plans[mapping['plan']]['resolution'] = mapping['status']
plans['P1']['proposed_request_not_executed'] = 'NONE now: manager submitted 1020032729-7262; after-fix physical 63-pass result maps original22 once'
plans['P1']['reason'] = 'Original22 uncertain boundary; after-fix physical same-current-tree63 PASS retains all22 names. Complete, no duplicate.'
plans['P3']['proposed_request_not_executed'] = 'NONE: existing18739 completed, 1 PASS/3 FAIL; no duplicate incident replay'
plans['P3']['mapping_status'] = 'COMPLETE: readiness1/1 and13 captures, afterfix03:16:52 start; full4-case rerun stays RED1/3 with exact source postflight PASS'
plans['P3']['reason'] = 'Reviewed muted/routes descendant completed; see after_fix_mappings for exact case timestamps, counts and guard proof.'

inventory = {'generated_at_utc': datetime.now(timezone.utc).isoformat(),
             'scope': {'from_utc': '2026-10-19T19:34:00Z', 'fix_utc': '2026-10-20T03:12:00Z',
                        'source_only': True, 'quiet_path': metadata(ORCH / 'QUIET.md'),
                        'quiet_symlink_target': str((ORCH / 'QUIET.md').readlink()) if (ORCH / 'QUIET.md').is_symlink() else None,
                        'no_worker_test_submissions': True,
                        'limitations': ['No saved syscall/deletion timestamp; overlapping conservative envelope is uncertain, not causal proof.',
                                        'No precise collection count is invented when no count line exists.',
                                        'Imported MAIN logs are absent locally; preserved import mtimes are not execution times.']},
             'checkins': checkins, 'runs': runs,
             'rerun_plans': plans,
             'after_fix_mappings': after_fix_mappings,
             'composition_retention': {'old_collected': 22, 'current_collected': 63,
                                       'old_test_names': old_names, 'missing_in_current': sorted(set(old_names) - set(new_names)),
                                       'note': 'All original names retained, but both saved runs precede the fix; this is source/count mapping, not an after-fix rerun.'},
             'reference_search': {'file_count': len(reference_files), 'paths': [str(p) for p in sorted(reference_files)]}}
(OUT / 'central-deletion-evidence-audit.json').write_text(json.dumps(inventory, indent=2) + '\n')


def short_time(value):
    return datetime.fromisoformat(value).strftime('%m-%d %H:%M:%S') if value else '—'


table = ['<!-- BEGIN INVENTORY TABLE -->', '',
         f'The table includes **every one of the {len(runs)} saved result directories**, including observed after-fix replacements. Times are UTC conservative execution bounds, not request times. `C/P/F/S` means collected/passed/failed/skipped; `?` is unavailable. Pytest C is inferred from terminal totals unless explicitly logged. Every nonoverlap row also has its nearest preceding/following check-in bounds in `central-deletion-evidence-audit.json`. Imported rows have no defensible local execution window.', '',
         '| Full run ID | UTC bounds | Status; C/P/F/S | Check-in / disposition |',
         '|---|---|---|---|']
for run in runs:
    window = run['window']
    bounds = f"{short_time(window['start_lower_bound_utc'])}–{short_time(window['end_upper_bound_utc'])}"
    if run['status'] == 'running':
        bounds = f"{short_time(window['start_lower_bound_utc'])}–running (last log {short_time(window['last_log_write_utc'])})"
    count_text = '/'.join(str(run['counts'][k]) if run['counts'][k] is not None else '?' for k in ['collected', 'passed', 'failed', 'skipped'])
    disposition = ', '.join(run['checkin_ids']) or ('MAIN import' if run['origin'] == 'MAIN_IMPORTED_ASSET' else 'cache; trace ' + run['cached_from'] if run['cached_from'] else 'between saved check-ins')
    if run['rerun_plan']:
        disposition += '; ' + run['rerun_plan']
    table.append(f"| `{run['id']}` | {bounds} | {run['status']}; {count_text} | {disposition} |")
report = OUT / 'central-deletion-evidence-audit.md'
body = read(report).split('<!-- BEGIN INVENTORY TABLE -->')[0].rstrip()
report.write_text(body + '\n\n' + '\n'.join(table) + '\n')
print(f'Inventoried {len(checkins)} check-ins, {len(runs)} result directories, {len(reference_files)} reference files')
for run in runs:
    if run['checkin_ids'] or run['cached_from']:
        print(run['id'], run['classification'], run['checkin_ids'], run['counts'], run['cached_from'])
