# Astrid

Tools and knowledge for agents and humans to make art with open models.

### Give this to your agent

```text
╭────────────────────────────────── ◇ ───────────────────────────────────╮
│                                                                        │
│                         A   S   T   R   I   D                          │
│                                                                        │
│                    agents harnessed, humans free —                     │
│                     open tools for what could be:                      │
│                    moving image, voice, and frame,                     │
│                  clone it, shape it, share the flame.                  │
│                                                                        │
│                                ·  ·  ·                                 │
│                                                                        │
│  https://github.com/banodoco/astrid-agent/blob/main/docs/setup/SKILL.md  │
│                                                                        │
│                                ·  ·  ·                                 │
│                                                                        │
│                     Set up Astrid on this machine;                     │
│              check what’s there, keep its work pristine.               │
│                  Follow the skill and see what’s new;                  │
│                test every step, then guide me through.                 │
│                                                                        │
╰────────────────────────────────── ◇ ───────────────────────────────────╯
```

**Want to set it up yourself?** [Get started →](docs/setup/README.md)

The CI default lane uses the committed `tests/.test_durations` file to balance its eight pytest shards. After a full default-lane run, refresh it with `python -m pytest -q --store-durations --durations-path tests/.test_durations`, then commit the updated file.

### More info

- [How Astrid works](docs/guides/how-it-works.md)
- [When and how to create a pack](docs/guides/create-a-pack.md)
- [Contributing knowledge](docs/guides/contributing-knowledge.md)
- [Get help](docs/setup/troubleshooting.md)

---

_[License](LICENSE)_
