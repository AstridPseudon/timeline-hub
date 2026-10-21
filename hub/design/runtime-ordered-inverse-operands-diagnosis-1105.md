# Runtime ordered inverse operand diagnosis

```json
{
  "selector": "tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo",
  "call_count": 3,
  "calls": [
    {
      "index": 0,
      "origins": [
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_caller.py",
          "line": 197,
          "function": "__call__"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_manager.py",
          "line": 183,
          "function": "_hookexec"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_execution.py",
          "line": 147,
          "function": "_multicall"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/runner.py",
          "line": 179,
          "function": "pytest_runtest_call"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/python.py",
          "line": 1720,
          "function": "runtest"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_caller.py",
          "line": 197,
          "function": "__call__"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_manager.py",
          "line": 183,
          "function": "_hookexec"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_execution.py",
          "line": 147,
          "function": "_multicall"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/python.py",
          "line": 166,
          "function": "pytest_pyfunc_call"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/tests/test_timeline_owned_reference_integration.py",
          "line": 427,
          "function": "test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/tests/test_timeline_owned_reference_integration.py",
          "line": 249,
          "function": "_commit"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/service.py",
          "line": 2444,
          "function": "commit_timeline"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/service.py",
          "line": 2479,
          "function": "_execute_timeline_commit"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/timeline_commit_execution.py",
          "line": 87,
          "function": "execute"
        },
        {
          "filename": "/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py",
          "line": 1141,
          "function": "commit"
        },
        {
          "filename": "/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py",
          "line": 362,
          "function": "document_from_bundle"
        }
      ],
      "records_argument": {
        "type": "list",
        "entries": []
      },
      "compared_command_lists": {
        "accepted_records": [],
        "history_records": []
      },
      "first_difference": null,
      "source_hashes": {
        "records_argument": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        "records_entries": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        "records_fields": {}
      },
      "outcome": {
        "status": "returned",
        "type": "set"
      }
    },
    {
      "index": 1,
      "origins": [
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_caller.py",
          "line": 197,
          "function": "__call__"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_manager.py",
          "line": 183,
          "function": "_hookexec"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_execution.py",
          "line": 147,
          "function": "_multicall"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/runner.py",
          "line": 179,
          "function": "pytest_runtest_call"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/python.py",
          "line": 1720,
          "function": "runtest"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_caller.py",
          "line": 197,
          "function": "__call__"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_manager.py",
          "line": 183,
          "function": "_hookexec"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_execution.py",
          "line": 147,
          "function": "_multicall"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/python.py",
          "line": 166,
          "function": "pytest_pyfunc_call"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/tests/test_timeline_owned_reference_integration.py",
          "line": 439,
          "function": "test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/tests/test_timeline_owned_reference_integration.py",
          "line": 249,
          "function": "_commit"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/service.py",
          "line": 2444,
          "function": "commit_timeline"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/service.py",
          "line": 2479,
          "function": "_execute_timeline_commit"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/timeline_commit_execution.py",
          "line": 87,
          "function": "execute"
        },
        {
          "filename": "/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py",
          "line": 1141,
          "function": "commit"
        },
        {
          "filename": "/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py",
          "line": 362,
          "function": "document_from_bundle"
        }
      ],
      "records_argument": {
        "type": "list",
        "entries": []
      },
      "compared_command_lists": {
        "accepted_records": [],
        "history_records": []
      },
      "first_difference": null,
      "source_hashes": {
        "records_argument": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        "records_entries": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        "records_fields": {}
      },
      "outcome": {
        "status": "returned",
        "type": "set"
      }
    },
    {
      "index": 2,
      "origins": [
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_caller.py",
          "line": 197,
          "function": "__call__"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_manager.py",
          "line": 183,
          "function": "_hookexec"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_execution.py",
          "line": 147,
          "function": "_multicall"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/runner.py",
          "line": 179,
          "function": "pytest_runtest_call"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/python.py",
          "line": 1720,
          "function": "runtest"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_caller.py",
          "line": 197,
          "function": "__call__"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_manager.py",
          "line": 183,
          "function": "_hookexec"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/pluggy/_execution.py",
          "line": 147,
          "function": "_multicall"
        },
        {
          "filename": "/home/user/work/venv-agent/lib/python3.13/site-packages/_pytest/python.py",
          "line": 166,
          "function": "pytest_pyfunc_call"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/tests/test_timeline_owned_reference_integration.py",
          "line": 483,
          "function": "test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/tests/test_timeline_owned_reference_integration.py",
          "line": 249,
          "function": "_commit"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/service.py",
          "line": 2444,
          "function": "commit_timeline"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/service.py",
          "line": 2479,
          "function": "_execute_timeline_commit"
        },
        {
          "filename": "/home/user/work/wt/.test-rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618/runtime_protocol/timeline_commit_execution.py",
          "line": 87,
          "function": "execute"
        },
        {
          "filename": "/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py",
          "line": 1141,
          "function": "commit"
        },
        {
          "filename": "/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py",
          "line": 362,
          "function": "document_from_bundle"
        }
      ],
      "records_argument": {
        "type": "AcceptedRecords",
        "entries": [
          {
            "publication_id": "txn-2630c1a7f2914c8d95d865ac0c4c29be",
            "revision_id": "authoring-parent-revision-1f90b9bdd13fdc45cb2047a67ed0460dcf8d104391fecb57e25a882303306015",
            "previous": {
              "revision_id": "authoring-parent-revision-50e58cd168d38a9846dc48fd8bd3d2f0cfd53e01a04d1c074d49421a1a949d6d",
              "publication_id": "txn-1f9dac44417241e49f20ffb341e87b18"
            },
            "receipt": {
              "receipt_id": "txn-2630c1a7f2914c8d95d865ac0c4c29be",
              "command_kind": "timeline.commit",
              "idempotency_key": "ordered-data-remove",
              "request_hash": "83432897f99bc0ca348676e4f5532f8f380fe530dc771ff451845d4898e3290a",
              "project_id": "85f56c73ed084405baddbf0ee686cec9",
              "project_seq": [
                4,
                4
              ],
              "event_ids": [
                "4"
              ],
              "result": {
                "accepted_revision_id": "authoring-parent-revision-1f90b9bdd13fdc45cb2047a67ed0460dcf8d104391fecb57e25a882303306015",
                "base_publication_id": "txn-1f9dac44417241e49f20ffb341e87b18",
                "base_revision_id": "authoring-parent-revision-50e58cd168d38a9846dc48fd8bd3d2f0cfd53e01a04d1c074d49421a1a949d6d",
                "canonical_document": {
                  "dependency_manifest": {
                    "documents": [],
                    "internal_timelines": [],
                    "media": [],
                    "shots": []
                  },
                  "internal_timeline_revisions": [],
                  "parent_revision": {
                    "content_digest": "sha256:67f878483ea5b3d16c97570a533684471b527005b5190264e87170ae86d662d6",
                    "payload": {
                      "clips": [],
                      "config": {
                        "app": {
                          "a-before": {
                            "keep": {
                              "future": {
                                "kept": true
                              },
                              "literal": [
                                null,
                                false,
                                0
                              ]
                            }
                          },
                          "z-after": {
                            "keep": {
                              "literal": {
                                "nested": [
                                  null,
                                  "opaque"
                                ]
                              }
                            }
                          }
                        },
                        "clips": [],
                        "tracks": []
                      },
                      "occurrences": [],
                      "registry": {}
                    },
                    "revision_id": "authoring-parent-revision-1f90b9bdd13fdc45cb2047a67ed0460dcf8d104391fecb57e25a882303306015"
                  },
                  "project_id": "85f56c73ed084405baddbf0ee686cec9",
                  "schema_version": 1,
                  "shot_revisions": [],
                  "timeline_id": "main"
                },
                "commands": [
                  {
                    "args": {
                      "key": "gone",
                      "mode": "remove",
                      "target": "com.example.compiler-canary"
                    },
                    "authorship": {
                      "parent::config.app[\"com.example.compiler-canary\"]": "direct",
                      "parent::config.app[\"com.example.compiler-canary\"].gone": "direct"
                    },
                    "bindings": {},
                    "created": [],
                    "expect": {
                      "parent::config.app[\"com.example.compiler-canary\"]": {
                        "state": "present",
                        "value": {
                          "gone": null
                        }
                      },
                      "parent::config.app[\"com.example.compiler-canary\"].gone": {
                        "state": "present",
                        "value": null
                      }
                    },
                    "intent": {},
                    "op": "project-data.write",
                    "reads": [],
                    "resolved": [],
                    "schema_version": 1,
                    "select": "parent",
                    "selections": [],
                    "version": "1"
                  }
                ],
                "compiler_version": "authoring-bundle-1",
                "document_digest": "sha256:179f6ccc704747df955b9a72c44fd4be695f73e9b63db5c800e41e16c24f3278",
                "id_map": {},
                "previous_publication_id": "txn-1f9dac44417241e49f20ffb341e87b18",
                "previous_revision_id": "authoring-parent-revision-50e58cd168d38a9846dc48fd8bd3d2f0cfd53e01a04d1c074d49421a1a949d6d",
                "provider_version": "astrid-v1",
                "publisher": "rt03-native-proof",
                "rebased_onto": null,
                "source": {
                  "via": "python"
                },
                "status": "accepted"
              },
              "created_at": "2026-10-21T11:12:55.427+00:00"
            },
            "intent": "recorded",
            "records": {
              "commands": [
                {
                  "bindings": [],
                  "command": {
                    "args": {
                      "key": "gone",
                      "mode": "remove",
                      "target": "com.example.compiler-canary"
                    },
                    "authorship": {
                      "parent::config.app[\"com.example.compiler-canary\"]": "direct",
                      "parent::config.app[\"com.example.compiler-canary\"].gone": "direct"
                    },
                    "bindings": {},
                    "created": [],
                    "expect": {
                      "parent::config.app[\"com.example.compiler-canary\"]": {
                        "state": "present",
                        "value": {
                          "gone": null
                        }
                      },
                      "parent::config.app[\"com.example.compiler-canary\"].gone": {
                        "state": "present",
                        "value": null
                      }
                    },
                    "intent": {},
                    "op": "project-data.write",
                    "reads": [],
                    "resolved": [],
                    "schema_version": 1,
                    "select": "parent",
                    "selections": [],
                    "version": "1"
                  },
                  "created": [],
                  "dependencies": [],
                  "derived_writes": [],
                  "ordinal": 0,
                  "reads": [],
                  "selections": [],
                  "writes": [
                    {
                      "after": {
                        "state": "absent"
                      },
                      "before": {
                        "state": "present",
                        "value": null
                      },
                      "path": [
                        "config",
                        "app",
                        "com.example.compiler-canary",
                        "gone"
                      ],
                      "ref": "parent"
                    },
                    {
                      "after": {
                        "state": "absent"
                      },
                      "before": {
                        "state": "present",
                        "value": {}
                      },
                      "insertion_order": [
                        "a-before",
                        "com.example.compiler-canary",
                        "z-after"
                      ],
                      "path": [
                        "config",
                        "app",
                        "com.example.compiler-canary"
                      ],
                      "ref": "parent"
                    }
                  ]
                }
              ],
              "restored_from": null,
              "schema_version": 1,
              "undo_of": []
            },
            "provider_version": "astrid-v1",
            "compiler_version": "authoring-bundle-1",
            "publisher": "rt03-native-proof",
            "source": {
              "via": "python"
            }
          }
        ]
      },
      "compared_command_lists": {
        "accepted_records": [
          {
            "bindings": [],
            "command": {
              "args": {
                "key": "gone",
                "mode": "remove",
                "target": "com.example.compiler-canary"
              },
              "authorship": {
                "parent::config.app[\"com.example.compiler-canary\"]": "direct",
                "parent::config.app[\"com.example.compiler-canary\"].gone": "direct"
              },
              "bindings": {},
              "created": [],
              "expect": {
                "parent::config.app[\"com.example.compiler-canary\"]": {
                  "state": "present",
                  "value": {
                    "gone": null
                  }
                },
                "parent::config.app[\"com.example.compiler-canary\"].gone": {
                  "state": "present",
                  "value": null
                }
              },
              "intent": {},
              "op": "project-data.write",
              "reads": [],
              "resolved": [],
              "schema_version": 1,
              "select": "parent",
              "selections": [],
              "version": "1"
            },
            "created": [],
            "dependencies": [],
            "derived_writes": [],
            "ordinal": 0,
            "reads": [],
            "selections": [],
            "writes": [
              {
                "after": {
                  "state": "absent"
                },
                "before": {
                  "state": "present",
                  "value": null
                },
                "path": [
                  "config",
                  "app",
                  "com.example.compiler-canary",
                  "gone"
                ],
                "ref": "parent"
              },
              {
                "after": {
                  "state": "absent"
                },
                "before": {
                  "state": "present",
                  "value": {
                    "gone": null
                  }
                },
                "insertion_order": [
                  "a-before",
                  "com.example.compiler-canary",
                  "z-after"
                ],
                "path": [
                  "config",
                  "app",
                  "com.example.compiler-canary"
                ],
                "ref": "parent"
              }
            ]
          }
        ],
        "history_records": [
          {
            "bindings": [],
            "command": {
              "args": {
                "key": "gone",
                "mode": "remove",
                "target": "com.example.compiler-canary"
              },
              "authorship": {
                "parent::config.app[\"com.example.compiler-canary\"]": "direct",
                "parent::config.app[\"com.example.compiler-canary\"].gone": "direct"
              },
              "bindings": {},
              "created": [],
              "expect": {
                "parent::config.app[\"com.example.compiler-canary\"]": {
                  "state": "present",
                  "value": {
                    "gone": null
                  }
                },
                "parent::config.app[\"com.example.compiler-canary\"].gone": {
                  "state": "present",
                  "value": null
                }
              },
              "intent": {},
              "op": "project-data.write",
              "reads": [],
              "resolved": [],
              "schema_version": 1,
              "select": "parent",
              "selections": [],
              "version": "1"
            },
            "created": [],
            "dependencies": [],
            "derived_writes": [],
            "ordinal": 0,
            "reads": [],
            "selections": [],
            "writes": [
              {
                "after": {
                  "state": "absent"
                },
                "before": {
                  "state": "present",
                  "value": null
                },
                "path": [
                  "config",
                  "app",
                  "com.example.compiler-canary",
                  "gone"
                ],
                "ref": "parent"
              },
              {
                "after": {
                  "state": "absent"
                },
                "before": {
                  "state": "present",
                  "value": {}
                },
                "insertion_order": [
                  "a-before",
                  "com.example.compiler-canary",
                  "z-after"
                ],
                "path": [
                  "config",
                  "app",
                  "com.example.compiler-canary"
                ],
                "ref": "parent"
              }
            ]
          }
        ]
      },
      "first_difference": {
        "kind": "presence",
        "path": "$[0][\"writes\"][1][\"before\"][\"value\"][\"gone\"]",
        "left": "present",
        "right": "absent"
      },
      "source_hashes": {
        "records_argument": "sha256:5da5f1a12f1ee1a31569868e900957dc261b6372738026fe2d85ca30a37c4336",
        "records_entries": "sha256:29df32a87a1d0f84a9674172d5d6c3ae55d1d7945f15fea2eab3de685097e80e",
        "records_fields": {
          "$[0][\"receipt\"][\"request_hash\"]": "83432897f99bc0ca348676e4f5532f8f380fe530dc771ff451845d4898e3290a",
          "$[0][\"receipt\"][\"result\"][\"canonical_document\"][\"parent_revision\"][\"content_digest\"]": "sha256:67f878483ea5b3d16c97570a533684471b527005b5190264e87170ae86d662d6",
          "$[0][\"receipt\"][\"result\"][\"document_digest\"]": "sha256:179f6ccc704747df955b9a72c44fd4be695f73e9b63db5c800e41e16c24f3278"
        }
      },
      "outcome": {
        "status": "raised",
        "type": "CommandError",
        "message": "media inverse records differ from accepted history"
      }
    }
  ]
}
```
