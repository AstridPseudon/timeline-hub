# Validation

- Restored the upstream per-model `New chat` action and `· <level>` copy in `NewChatModels`.
- Preserved NewChatMenu's remembered selection behavior and AgentChatMenu's existing row-start behavior.
- Added explicit source variants so NewChatMenu keeps compact selector classes while AgentChatMenu keeps its aligned selector classes and accessible option names.
- Changed only the three authorized source files. Test sources remain byte-identical to `e9041a2621`.
- No full suite, browser suite, build, ZIP, pins, or external writes were run.
