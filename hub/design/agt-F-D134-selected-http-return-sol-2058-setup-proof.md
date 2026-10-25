# D134 HTTP bootstrap source proof

PASS_SOURCE_ENGINE_ONLY. The only source correction reads the physical parent payload for the root previous value. Every sequential guard, request envelope, and desired final parent remains as inherited.

Review2053's apply_change-only conclusion is incomplete: bundle_from_document strips occurrences into placements, while Closure.payload restores them before the root guard. The inherited root guard therefore fails first. After root replacement, Closure.install handles config removal by also removing the mirrored top-level clips; the subsequent original ABSENT clips guard is valid. Changing it to PRESENT would cause the second guarded change to fail. Both counterexamples and the corrected whole-command pass are below.

This is an in-memory source probe through the real commands.execute and Closure.install implementations using the immutable Runtime's pure empty_bootstrap_document. It does not run Runtime acceptance, HTTP, schema admission, or any test selector and gives no behavioral gate credit. No guard or producer is changed in source.

Command:
```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" /home/user/work/venv-agent/bin/python /tmp/w-fd40272e29/d134-setup-probe.py
```

Source references: commit.bundle_from_document at astrid/sdk/timeline/commit.py:154; Closure.payload at _doc_patch.py:158; Closure.install at _doc_patch.py:222 (root decomposition 237, config mirror removal 260); patch sequential loop at _doc_patch.py:479; Runtime empty_bootstrap_document at timeline_commit_baseline.py:416.

Reproducer (SHA-256: 5bdd7da3042f135364b1b71929b241cd10fd97228d9d0e4ac9a66b35aeb22801):
```python
import ast
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import astrid
import runtime_protocol
from astrid.sdk.timeline import _doc_patch, commands, commit
from runtime_protocol.timeline_commit_baseline import empty_bootstrap_document

ROOT = Path('/home/user/work/wt/agt-F-D134-selected-http-return-sol-2058')
FILE = 'tests/sdk/test_timeline_selected_schema_runtime.py'
EVIDENCE = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-selected-http-return-sol-2058/evidence')
fixture = next(n for n in ast.parse((ROOT / FILE).read_text()).body
               if isinstance(n, ast.FunctionDef) and n.name == 'http_retained_pack')
original = subprocess.check_output(['git', 'show', 'a30e74e901:' + FILE], cwd=ROOT, text=True)
original_payload = next(ast.literal_eval(value) for node in ast.walk(ast.parse(original))
                        if isinstance(node, ast.Dict) for key, value in zip(node.keys, node.values)
                        if isinstance(key, ast.Constant) and key.value == 'parent_composition')
document = empty_bootstrap_document('project', 'film', 'bootstrap-parent')
bundle = commit.bundle_from_document(document)
physical_baseline = document['parent_revision']['payload']


def fixture_inputs(baseline):
    namespace = {'copy': copy, 'baseline': copy.deepcopy(baseline), 'project': 'project',
                 'base': {'revision_id': 'bootstrap-parent', 'publication_id': 'bootstrap-publication'}}
    for node in fixture.body:
        if (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ('original_parent', 'changes')):
            exec(compile(ast.Module(body=[node], type_ignores=[]), '<fixture-data>', 'exec'), namespace)
    seeded = next(node for node in fixture.body if isinstance(node, ast.Assign)
                  and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'seeded')
    request = eval(compile(ast.Expression(seeded.value.args[2]), '<fixture-request>', 'eval'), namespace)
    return namespace['original_parent'], request


def run(baseline, *, second_present=False):
    expected, request = fixture_inputs(baseline)
    assert expected == original_payload
    if second_present:
        request['commands'][0]['args']['changes'][1]['before'] = {'state': 'present', 'value': []}
    untouched = copy.deepcopy(request)
    trace = []
    original_apply = _doc_patch.apply_change

    def observed(root, change, **kwargs):
        trace.append({'path': change['path'], 'observed_root': copy.deepcopy(root),
                      'guard': copy.deepcopy(change['before'])})
        return original_apply(root, change, **kwargs)

    try:
        with patch.object(_doc_patch, 'apply_change', observed):
            plan = commands.execute(bundle, request['commands'], commit_request=request)
        final = commit.document_from_bundle(plan.bundle)['parent_revision']['payload']
        assert final == original_payload
        assert 'clips' not in final['config']
        outcome = {'status': 'PASS_SOURCE_ENGINE', 'final_parent': final,
                   'steps': plan.steps, 'final_parent_exact': True}
    except commands.CommandError as exc:
        outcome = {'status': 'EXPECTED_SOURCE_ERROR', 'kind': exc.kind, 'path': exc.path,
                   'claimed': exc.base, 'observed': exc.theirs}
    assert request == untouched
    return {**outcome, 'trace': trace, 'request_unchanged_by_engine': True}


cases = {'inherited': run(bundle['parent']),
         'naive_present_guard_only': run(bundle['parent'], second_present=True),
         'physical_root_but_present_second_guard': run(physical_baseline, second_present=True),
         'corrected_physical_root_original_absent_second_guard': run(physical_baseline)}
assert cases['inherited']['path'] == []
assert cases['inherited']['kind'] == 'previous_value_mismatch'
assert cases['naive_present_guard_only']['path'] == []
assert cases['physical_root_but_present_second_guard']['path'] == ['clips']
assert cases['physical_root_but_present_second_guard']['observed'] == {'state': 'absent'}
passing = cases['corrected_physical_root_original_absent_second_guard']
assert passing['status'] == 'PASS_SOURCE_ENGINE'
assert passing['trace'][0]['guard']['value'] == passing['trace'][0]['observed_root']
assert passing['trace'][1]['guard'] == {'state': 'absent'}
assert 'clips' not in passing['trace'][1]['observed_root']
assert 'clips' not in passing['trace'][1]['observed_root']['config']
assert bundle == commit.bundle_from_document(document)
data = {'classification': 'SOURCE_ENGINE_ONLY_NOT_RUNTIME_ACCEPTANCE',
        'origins': {'astrid': str(Path(astrid.__file__).resolve()),
                    'runtime_protocol': str(Path(runtime_protocol.__file__).resolve())},
        'bootstrap_document_producer': 'immutable Runtime empty_bootstrap_document; no service, realm, admission, socket or provider created',
        'original_parent': original_payload,
        'physical_baseline': physical_baseline, 'authoring_baseline': bundle['parent'], 'cases': cases}
assert Path(astrid.__file__).resolve() == ROOT / 'astrid/__init__.py'
assert Path(runtime_protocol.__file__).resolve() == Path('/home/user/work/wt/rt-pin-ab1e4f61/runtime_protocol/__init__.py')
script = Path(__file__).read_text()
report = '''# D134 HTTP bootstrap source proof

PASS_SOURCE_ENGINE_ONLY. The only source correction reads the physical parent payload for the root previous value. Every sequential guard, request envelope, and desired final parent remains as inherited.

Review2053's apply_change-only conclusion is incomplete: bundle_from_document strips occurrences into placements, while Closure.payload restores them before the root guard. The inherited root guard therefore fails first. After root replacement, Closure.install handles config removal by also removing the mirrored top-level clips; the subsequent original ABSENT clips guard is valid. Changing it to PRESENT would cause the second guarded change to fail. Both counterexamples and the corrected whole-command pass are below.

This is an in-memory source probe through the real commands.execute and Closure.install implementations using the immutable Runtime's pure empty_bootstrap_document. It does not run Runtime acceptance, HTTP, schema admission, or any test selector and gives no behavioral gate credit. No guard or producer is changed in source.

Command:
```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" /home/user/work/venv-agent/bin/python /tmp/w-fd40272e29/d134-setup-probe.py
```

Source references: commit.bundle_from_document at astrid/sdk/timeline/commit.py:154; Closure.payload at _doc_patch.py:158; Closure.install at _doc_patch.py:222 (root decomposition 237, config mirror removal 260); patch sequential loop at _doc_patch.py:479; Runtime empty_bootstrap_document at timeline_commit_baseline.py:416.

Reproducer (SHA-256: SCRIPT_HASH):
```python
SCRIPT
```

Observed results:
```json
{
  "classification": "SOURCE_ENGINE_ONLY_NOT_RUNTIME_ACCEPTANCE",
  "origins": {
    "astrid": "/home/user/work/wt/agt-F-D134-selected-http-return-sol-2058/astrid/__init__.py",
    "runtime_protocol": "/home/user/work/wt/rt-pin-ab1e4f61/runtime_protocol/__init__.py"
  },
  "bootstrap_document_producer": "immutable Runtime empty_bootstrap_document; no service, realm, admission, socket or provider created",
  "original_parent": {
    "config": {
      "tracks": []
    },
    "registry": {},
    "clips": [],
    "occurrences": []
  },
  "physical_baseline": {
    "config": {
      "clips": [],
      "tracks": []
    },
    "registry": {},
    "clips": [],
    "occurrences": []
  },
  "authoring_baseline": {
    "config": {
      "clips": [],
      "tracks": []
    },
    "registry": {},
    "clips": []
  },
  "cases": {
    "inherited": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [],
      "claimed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": []
        }
      },
      "observed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": [],
          "occurrences": []
        }
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": []
            }
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "naive_present_guard_only": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [],
      "claimed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": []
        }
      },
      "observed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": [],
          "occurrences": []
        }
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": []
            }
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "physical_root_but_present_second_guard": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [
        "clips"
      ],
      "claimed": {
        "state": "present",
        "value": []
      },
      "observed": {
        "state": "absent"
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": [],
              "occurrences": []
            }
          }
        },
        {
          "path": [
            "clips"
          ],
          "observed_root": {
            "config": {
              "tracks": []
            },
            "registry": {},
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": []
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "corrected_physical_root_original_absent_second_guard": {
      "status": "PASS_SOURCE_ENGINE",
      "final_parent": {
        "config": {
          "tracks": []
        },
        "registry": {},
        "clips": [],
        "occurrences": []
      },
      "steps": [
        {
          "id": "edit",
          "label": "Timeline edit",
          "intent": "",
          "tags": [],
          "command_ordinals": [
            0
          ],
          "patch": [
            {
              "op": "set",
              "ref": "parent",
              "path": [],
              "before": {
                "state": "present",
                "value": {
                  "config": {
                    "clips": [],
                    "tracks": []
                  },
                  "registry": {},
                  "clips": [],
                  "occurrences": []
                }
              },
              "value": {
                "config": {
                  "tracks": []
                },
                "registry": {},
                "clips": [],
                "occurrences": []
              }
            }
          ],
          "dependencies": [
            {
              "kind": "field",
              "ref": "parent",
              "path": [],
              "state": {
                "state": "present",
                "value": {
                  "config": {
                    "clips": [],
                    "tracks": []
                  },
                  "registry": {},
                  "clips": [],
                  "occurrences": []
                }
              }
            },
            {
              "kind": "field",
              "ref": "parent",
              "path": [
                "config",
                "clips"
              ],
              "state": {
                "state": "absent"
              }
            },
            {
              "kind": "scope",
              "ref": "parent",
              "path": []
            },
            {
              "kind": "scope",
              "ref": "timeline",
              "path": []
            }
          ]
        }
      ],
      "final_parent_exact": true,
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": [],
              "occurrences": []
            }
          }
        },
        {
          "path": [
            "clips"
          ],
          "observed_root": {
            "config": {
              "tracks": []
            },
            "registry": {},
            "occurrences": []
          },
          "guard": {
            "state": "absent"
          }
        }
      ],
      "request_unchanged_by_engine": true
    }
  }
}
```
'''
report = report.replace('SCRIPT_HASH', hashlib.sha256(script.encode()).hexdigest()).replace('SCRIPT\n', script + '\n').replace('{
  "classification": "SOURCE_ENGINE_ONLY_NOT_RUNTIME_ACCEPTANCE",
  "origins": {
    "astrid": "/home/user/work/wt/agt-F-D134-selected-http-return-sol-2058/astrid/__init__.py",
    "runtime_protocol": "/home/user/work/wt/rt-pin-ab1e4f61/runtime_protocol/__init__.py"
  },
  "bootstrap_document_producer": "immutable Runtime empty_bootstrap_document; no service, realm, admission, socket or provider created",
  "original_parent": {
    "config": {
      "tracks": []
    },
    "registry": {},
    "clips": [],
    "occurrences": []
  },
  "physical_baseline": {
    "config": {
      "clips": [],
      "tracks": []
    },
    "registry": {},
    "clips": [],
    "occurrences": []
  },
  "authoring_baseline": {
    "config": {
      "clips": [],
      "tracks": []
    },
    "registry": {},
    "clips": []
  },
  "cases": {
    "inherited": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [],
      "claimed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": []
        }
      },
      "observed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": [],
          "occurrences": []
        }
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": []
            }
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "naive_present_guard_only": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [],
      "claimed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": []
        }
      },
      "observed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": [],
          "occurrences": []
        }
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": []
            }
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "physical_root_but_present_second_guard": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [
        "clips"
      ],
      "claimed": {
        "state": "present",
        "value": []
      },
      "observed": {
        "state": "absent"
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": [],
              "occurrences": []
            }
          }
        },
        {
          "path": [
            "clips"
          ],
          "observed_root": {
            "config": {
              "tracks": []
            },
            "registry": {},
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": []
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "corrected_physical_root_original_absent_second_guard": {
      "status": "PASS_SOURCE_ENGINE",
      "final_parent": {
        "config": {
          "tracks": []
        },
        "registry": {},
        "clips": [],
        "occurrences": []
      },
      "steps": [
        {
          "id": "edit",
          "label": "Timeline edit",
          "intent": "",
          "tags": [],
          "command_ordinals": [
            0
          ],
          "patch": [
            {
              "op": "set",
              "ref": "parent",
              "path": [],
              "before": {
                "state": "present",
                "value": {
                  "config": {
                    "clips": [],
                    "tracks": []
                  },
                  "registry": {},
                  "clips": [],
                  "occurrences": []
                }
              },
              "value": {
                "config": {
                  "tracks": []
                },
                "registry": {},
                "clips": [],
                "occurrences": []
              }
            }
          ],
          "dependencies": [
            {
              "kind": "field",
              "ref": "parent",
              "path": [],
              "state": {
                "state": "present",
                "value": {
                  "config": {
                    "clips": [],
                    "tracks": []
                  },
                  "registry": {},
                  "clips": [],
                  "occurrences": []
                }
              }
            },
            {
              "kind": "field",
              "ref": "parent",
              "path": [
                "config",
                "clips"
              ],
              "state": {
                "state": "absent"
              }
            },
            {
              "kind": "scope",
              "ref": "parent",
              "path": []
            },
            {
              "kind": "scope",
              "ref": "timeline",
              "path": []
            }
          ]
        }
      ],
      "final_parent_exact": true,
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": [],
              "occurrences": []
            }
          }
        },
        {
          "path": [
            "clips"
          ],
          "observed_root": {
            "config": {
              "tracks": []
            },
            "registry": {},
            "occurrences": []
          },
          "guard": {
            "state": "absent"
          }
        }
      ],
      "request_unchanged_by_engine": true
    }
  }
}', json.dumps(data, indent=2))
(EVIDENCE / 'setup-proof.md').write_text(report)
print('PASS: corrected full command engine; inherited and naive-guard counterexamples; exact original physical final parent; input conservation; source origins. No live bodies.')

```

Observed results:
```json
{
  "classification": "SOURCE_ENGINE_ONLY_NOT_RUNTIME_ACCEPTANCE",
  "origins": {
    "astrid": "/home/user/work/wt/agt-F-D134-selected-http-return-sol-2058/astrid/__init__.py",
    "runtime_protocol": "/home/user/work/wt/rt-pin-ab1e4f61/runtime_protocol/__init__.py"
  },
  "bootstrap_document_producer": "immutable Runtime empty_bootstrap_document; no service, realm, admission, socket or provider created",
  "original_parent": {
    "config": {
      "tracks": []
    },
    "registry": {},
    "clips": [],
    "occurrences": []
  },
  "physical_baseline": {
    "config": {
      "clips": [],
      "tracks": []
    },
    "registry": {},
    "clips": [],
    "occurrences": []
  },
  "authoring_baseline": {
    "config": {
      "clips": [],
      "tracks": []
    },
    "registry": {},
    "clips": []
  },
  "cases": {
    "inherited": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [],
      "claimed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": []
        }
      },
      "observed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": [],
          "occurrences": []
        }
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": []
            }
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "naive_present_guard_only": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [],
      "claimed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": []
        }
      },
      "observed": {
        "state": "present",
        "value": {
          "config": {
            "clips": [],
            "tracks": []
          },
          "registry": {},
          "clips": [],
          "occurrences": []
        }
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": []
            }
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "physical_root_but_present_second_guard": {
      "status": "EXPECTED_SOURCE_ERROR",
      "kind": "previous_value_mismatch",
      "path": [
        "clips"
      ],
      "claimed": {
        "state": "present",
        "value": []
      },
      "observed": {
        "state": "absent"
      },
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": [],
              "occurrences": []
            }
          }
        },
        {
          "path": [
            "clips"
          ],
          "observed_root": {
            "config": {
              "tracks": []
            },
            "registry": {},
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": []
          }
        }
      ],
      "request_unchanged_by_engine": true
    },
    "corrected_physical_root_original_absent_second_guard": {
      "status": "PASS_SOURCE_ENGINE",
      "final_parent": {
        "config": {
          "tracks": []
        },
        "registry": {},
        "clips": [],
        "occurrences": []
      },
      "steps": [
        {
          "id": "edit",
          "label": "Timeline edit",
          "intent": "",
          "tags": [],
          "command_ordinals": [
            0
          ],
          "patch": [
            {
              "op": "set",
              "ref": "parent",
              "path": [],
              "before": {
                "state": "present",
                "value": {
                  "config": {
                    "clips": [],
                    "tracks": []
                  },
                  "registry": {},
                  "clips": [],
                  "occurrences": []
                }
              },
              "value": {
                "config": {
                  "tracks": []
                },
                "registry": {},
                "clips": [],
                "occurrences": []
              }
            }
          ],
          "dependencies": [
            {
              "kind": "field",
              "ref": "parent",
              "path": [],
              "state": {
                "state": "present",
                "value": {
                  "config": {
                    "clips": [],
                    "tracks": []
                  },
                  "registry": {},
                  "clips": [],
                  "occurrences": []
                }
              }
            },
            {
              "kind": "field",
              "ref": "parent",
              "path": [
                "config",
                "clips"
              ],
              "state": {
                "state": "absent"
              }
            },
            {
              "kind": "scope",
              "ref": "parent",
              "path": []
            },
            {
              "kind": "scope",
              "ref": "timeline",
              "path": []
            }
          ]
        }
      ],
      "final_parent_exact": true,
      "trace": [
        {
          "path": [],
          "observed_root": {
            "config": {
              "clips": [],
              "tracks": []
            },
            "registry": {},
            "clips": [],
            "occurrences": []
          },
          "guard": {
            "state": "present",
            "value": {
              "config": {
                "clips": [],
                "tracks": []
              },
              "registry": {},
              "clips": [],
              "occurrences": []
            }
          }
        },
        {
          "path": [
            "clips"
          ],
          "observed_root": {
            "config": {
              "tracks": []
            },
            "registry": {},
            "occurrences": []
          },
          "guard": {
            "state": "absent"
          }
        }
      ],
      "request_unchanged_by_engine": true
    }
  }
}
```
