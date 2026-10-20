exec(open('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-review-tests.py').read().split("run('native-controls'",1)[0].replace("'-results.json'", "'-neighbors-results.json'"))
E['REVIEW_SOURCE_ROOT']=str(copy)
run('live-scene-neighbors',args+['tests/packs/rendering/test_live_scene_composition.py','-k','not real_render'],0 if phase=='baseline' else 1)
run('independent-corrected',args+[str(P)+'-probe.py'],0 if phase=='candidate' else 1)
tailargs=args+[str(P)+'-held-tail-test.py']
if phase=='baseline':tailargs+=['-k','controls or old_covered']
run('held-tail',tailargs,0 if phase=='baseline' else 1)
Path(str(P)+'-'+phase+'-neighbors-results.json').write_text(json.dumps(rows,indent=2)+'\n')
