Implemented isolated real-Player capture probes. **All backends produced captured audio, but mixed-output qualification failed.**

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome npm exec -- playwright test --config tests/e2e/timeline/player-audio.config.ts
npm exec -- eslint tests/e2e/timeline/player-audio*.ts tests/e2e/timeline/player-tab-capture.probe.ts --max-warnings 0
git diff --check
```

- Browser: **2 failed**. Mixes showed silent gaps, phase discontinuities and up to 841 ms drift. Fade duration also failed.
- Mute produced zero PCM; Player half-volume measured −6.334 dB. Planted capture gain measured −6.232 dB, but the positive baseline remains unqualified.
- ESLint and whitespace checks passed.
- Used private PulseAudio after tab capture failed, and playable WebM after MP4 failed. Product/shared configuration growth: zero.
- Processes and temporary directories cleaned; commit message written.

[Detailed evidence and launch steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/player-audio-feasibility.md).

Next: isolate Player scheduling/buffering versus capture-clock effects. M3 export/frame parity remains unverified; gate 6 stays open.