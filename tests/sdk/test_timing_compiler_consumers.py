"""Compiler ownership at authored edit and consumer boundaries (synthetic inputs)."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline_checkout import Checkout


FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures/timeline_editing'


def checkout():
    return Checkout(json.loads((FIXTURES / 'tiny_publishable.json').read_text()))


def author(tl, operation):
    if operation == 'on':
        tl.clip('c1.rocket').on('"went"')
    elif operation == 'nudge':
        # The fixture's moment is retained, and the authored nudge becomes its offset.
        tl.clip('c1.rocket').nudge(frames=3)
    elif operation == 'nudge-literal':
        # An unanchored narration clip writes its literal placement before resolution.
        tl.clip('a-vo').nudge(frames=3)
    elif operation == 'duplicate':
        tl.cut('c1').duplicate(0.0)
    elif operation == 'move':
        tl.cut('c2').move(4.2)
    else:
        raise AssertionError(operation)


@pytest.mark.parametrize('operation', ['on', 'nudge', 'nudge-literal', 'duplicate', 'move'])
def test_authored_placement_edits_adopt_the_final_compiler_result(monkeypatch, operation):
    from astrid.sdk.timeline import compiler

    tl = checkout()
    before = copy.deepcopy(tl.bundle)
    results = []
    original = compiler.compile_timing

    def recorded(inputs, commands=()):
        declared = copy.deepcopy((inputs.bundle, inputs.state))
        result = original(inputs, commands)
        assert (inputs.bundle, inputs.state) == declared
        results.append(copy.deepcopy(result.bundle))
        return result

    monkeypatch.setattr(compiler, 'compile_timing', recorded)
    author(tl, operation)
    assert tl.bundle != before
    assert results, 'the authored edit must reach the timing compiler'
    assert tl.bundle == results[-1], 'no later placement writer may replace the compiled result'
    assert original(tl.document()).bundle == tl.document()


@pytest.mark.parametrize('operation', ['on', 'nudge', 'nudge-literal', 'duplicate', 'move'])
def test_compiler_refusal_cannot_expose_a_final_authored_placement(monkeypatch, operation):
    from astrid.sdk.timeline import compiler

    tl = checkout()
    clip = tl.clip('c1.rocket')
    handle = clip.data
    before = copy.deepcopy(tl.bundle)

    def refuse(*args, **kwargs):
        raise RuntimeError('compiler refused')

    monkeypatch.setattr(compiler, 'compile_timing', refuse)
    with pytest.raises(RuntimeError, match='compiler refused'):
        author(tl, operation)
    assert tl.bundle == before
    assert clip.data is handle is tl.clip('c1.rocket').data
    assert not tl._pending_calls


@pytest.mark.parametrize('flags,materializer', [
    (['--retime'], 'retime'),
    (['--gap-after', 's1=0.5'], 'reflow'),
])
def test_cli_timing_edits_save_compiler_output(monkeypatch, tmp_path, flags, materializer):
    from astrid.packs.timeline import cli
    from astrid.sdk.timeline import compiler

    path = tmp_path / 'timeline.checkout.json'
    checkout().save(path, quiet=True)
    calls, results = [], []
    original = compiler.compile_timing

    def recorded(inputs, commands=()):
        calls.extend(command[0] for command in commands)
        result = original(inputs, commands)
        results.append(copy.deepcopy(result.bundle))
        return result

    monkeypatch.setattr(compiler, 'compile_timing', recorded)
    parsed = cli.build_parser(None).parse_args(['edit', '--file', str(path), *flags])
    assert parsed.handler(parsed) in (0, 3)  # retime may already be resolved
    assert materializer in calls
    assert Checkout.load(path).document() == Checkout(results[-1]).document()


def test_render_admission_freezes_compiled_timing_without_another_timing_writer(monkeypatch):
    from astrid.sdk.authoring_render_preview import render_authoring_candidate_preview
    from astrid.sdk.timeline import compiler

    tl = checkout()
    tl.clip('c1.rocket').on('"went"')
    candidate = tl.document()
    before = copy.deepcopy(candidate)

    def unexpected(*args, **kwargs):
        raise AssertionError('render projection must consume the compiled candidate as frozen')

    monkeypatch.setattr(compiler, 'compile_timing', unexpected)

    class Client:
        def invoke_result(self, capability, **kwargs):
            assert capability == 'rendering.render'
            return kwargs['inputs']['authoring_preview']

    preview = render_authoring_candidate_preview(candidate, Client(), project='p', timeline_ref='t')
    assert candidate == before
    assert preview['candidate'] == candidate
    assert preview['candidate'] is not candidate
    published = next(row for row in preview['publication']['internal_timeline_revisions']
                     if any(c.get('id') == 'a-rocket' for c in row['payload']['clips']))
    rocket = next(c for c in published['payload']['clips'] if c['id'] == 'a-rocket')
    assert rocket['at'] == tl.clip('c1.rocket').at
    preview['candidate']['shots']['A']['internal_timeline']['clips'].clear()
    assert candidate == before
