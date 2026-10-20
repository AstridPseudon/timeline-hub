import type { Theme, RuntimeTheme } from '@banodoco/timeline-composition/theme-api';
import own from './handoff-vw-m3-app-delivered-theme-seam-source.json';
import common from './handoff-vw-m3-resolved-theme-common-source-values.json';
const themes: Theme[] = [own.implicit, own.explicit, common.cases.implicit.theme,
  common.cases.color_override.theme, common.cases.full_visual_override.theme];
const runtimeThemes: RuntimeTheme[] = themes.map(theme => ({
  ...theme, color: theme.visual.color, type: theme.visual.type, motion: theme.visual.motion,
}));
void runtimeThemes;
