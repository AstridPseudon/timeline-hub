from pathlib import Path
import difflib, subprocess
orch=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
work=orch/'workers/vw-m3-app-delivered-theme-seam'
app=work/'offline-app'
r=app/'src/tools/video-editor/compositions/TimelineRenderer.tsx'
s=(work/'renderer-baseline.tsx').read_text()
s=s.replace('  type RuntimeTheme,', '  type RuntimeTheme,\n  type Theme,')
s=s.replace('type TimelineRendererInput = { config:', 'type TimelineRendererInput = { resolvedTheme?: Theme; config:')
s=s.replace('memo(({ config, compiledTransitions }) => {','memo(({ config, compiledTransitions, resolvedTheme }) => {')
s=s.replace('useMemo(() => resolveTimelineRenderTheme(renderConfig), [renderConfig])','useMemo(() => resolvedTheme ?? resolveTimelineRenderTheme(renderConfig), [resolvedTheme, renderConfig])')
s=s.replace('memo(({ config, compiledTransitions, astridElementHost }) => {','memo(({ config, compiledTransitions, resolvedTheme, astridElementHost }) => {')
s=s.replace('<TimelineRendererBody config={config} compiledTransitions={compiledTransitions} />','<TimelineRendererBody config={config} compiledTransitions={compiledTransitions} resolvedTheme={resolvedTheme} />')
r.write_text(s)
p=app/'src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx'
s=(work/'preview-baseline.tsx').read_text()
s="import type { Theme } from '@banodoco/timeline-composition/theme-api';\n"+s
s=s.replace('interface RemotionPreviewProps {','interface RemotionPreviewProps {\n  /** Whole Agent result paired by the caller with this exact config. */\n  resolvedTheme?: Theme;')
s=s.replace('interface PreviewDelivery {','interface PreviewDelivery {\n  resolvedTheme?: Theme;')
s=s.replace('{ config, compiledTransitions, previewRevision =','{ config, compiledTransitions, resolvedTheme, previewRevision =')
s=s.replace('useRef({ config, compiledTransitions })','useRef({ config, compiledTransitions, resolvedTheme })')
s=s.replace('configIdentityRef.current.compiledTransitions !== compiledTransitions)', 'configIdentityRef.current.compiledTransitions !== compiledTransitions || configIdentityRef.current.resolvedTheme !== resolvedTheme)')
s=s.replace('configIdentityRef.current = { config, compiledTransitions };','configIdentityRef.current = { config, compiledTransitions, resolvedTheme };')
s=s.replace('({config, compiledTransitions, revision:', '({config, compiledTransitions, resolvedTheme, revision:')
s=s.replace('current.config === config\n', 'current.config === config\n      && current.compiledTransitions === compiledTransitions\n      && current.resolvedTheme === resolvedTheme\n')
s=s.replace('}, [config, previewRevision]);','}, [config, compiledTransitions, resolvedTheme, previewRevision]);')
s=s.replace('        compiledTransitions,\n', '        compiledTransitions,\n        resolvedTheme,\n')
s=s.replace('[config, compiledTransitions, isPlaying,', '[config, compiledTransitions, resolvedTheme, isPlaying,')
s=s.replace('    compiledTransitions: delivery.compiledTransitions,','    compiledTransitions: delivery.compiledTransitions,\n    resolvedTheme: delivery.resolvedTheme,')
s=s.replace('[delivery.revision, delivery.compiledTransitions,', '[delivery.revision, delivery.compiledTransitions, delivery.resolvedTheme,')
p.write_text(s)
patch=''
for path, baseline in [(r,'renderer-baseline.tsx'),(p,'preview-baseline.tsx')]:
    relative=str(path.relative_to(app))
    patch+=''.join(difflib.unified_diff((work/baseline).read_text().splitlines(True),path.read_text().splitlines(True),fromfile='a/'+relative,tofile='b/'+relative))
(orch/'design/handoff-vw-m3-app-delivered-theme-seam-UNAPPLIED.patch').write_text(patch)
print('External prototype: 2 product files; no data/provider/default/pin changes')
