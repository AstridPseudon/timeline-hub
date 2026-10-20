from pathlib import Path
import hashlib, json, subprocess
from astrid.packs.rendering.shared.rendering_backend import _resolved_theme_for_render
root=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
source=Path('/home/user/work/wt/vw-m3-resolved-theme-common-source')
work=root/'workers/vw-m3-app-delivered-theme-seam'
config={'tracks':[{'id':'V1','kind':'visual','label':'V1'}], 'clips':[{'id':'one','track':'V1','at':0,'hold':3,'clipType':'hold'}]}
timeline=work/'source-timeline.json'
timeline.write_text(json.dumps(config))
implicit=_resolved_theme_for_render(timeline,None)
# New synthetic authored override, never an owner film or fixture rewrite.
explicit_config={**config,'theme':'banodoco-default','theme_overrides':{'visual':{'color':{'bg':'#123456','accent':'#654321'}}}}
timeline.write_text(json.dumps(explicit_config))
explicit=_resolved_theme_for_render(timeline,None)
modules=['astrid/core/theme/_schema.py','astrid/packs/rendering/shared/rendering_backend/__init__.py']
result={'implicit':implicit,'explicit':explicit,'explicitConfig':explicit_config,'source':{'agent_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),'resolver':'astrid.packs.rendering.shared.rendering_backend._resolved_theme_for_render','sha256':{p:hashlib.sha256((source/p).read_bytes()).hexdigest() for p in modules}}}
(root/'design/handoff-vw-m3-app-delivered-theme-seam-source.json').write_text(json.dumps(result,indent=2)+'\n')
(work/'offline-app/agent-theme.json').write_text(json.dumps(result,indent=2)+'\n')
print('Actual Agent resolver: implicit + authored color override; source hashes recorded')
