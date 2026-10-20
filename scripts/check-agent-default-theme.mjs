// Opt-in cross-product check. Run after npm run build; no Agent dependency in npm test.
import assert from 'node:assert/strict';
import {execFile} from 'node:child_process';
import {resolve} from 'node:path';
import {promisify} from 'node:util';
import * as root from '@banodoco/timeline-composition';
import * as api from '@banodoco/timeline-composition/theme-api';

const [agentCheckout, python] = process.argv.slice(2);
assert.ok(agentCheckout && python,
  'Usage: node scripts/check-agent-default-theme.mjs AGENT_CHECKOUT PYTHON');
const {stdout} = await promisify(execFile)(python, ['-c', `
import json
import sys
from pathlib import Path
checkout = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(checkout))
import astrid.core.theme._schema as schema
assert Path(schema.__file__).resolve() == checkout / "astrid/core/theme/_schema.py"
theme = schema.builtin_theme()
assert theme == schema.BUILTIN_DEFAULT_THEME
assert schema.validate_theme_document(theme) == theme
print(json.dumps({"module": schema.__file__, "theme": theme}))
`, resolve(agentCheckout)], {
  encoding: 'utf8', env: {...process.env, PYTHONDONTWRITEBYTECODE: '1'},
});
const agent = JSON.parse(stdout);
assert.strictEqual(root.DEFAULT_THEME, api.DEFAULT_THEME);
assert.deepStrictEqual(root.DEFAULT_THEME, agent.theme);
console.log(JSON.stringify({result: 'PASS', agentModule: agent.module, defaultTheme: root.DEFAULT_THEME}, null, 2));
