# Testing Astrid on your computer

You're testing the path a new person takes: one line installs Astrid on this computer, and the page at
https://astrid.haus connects to it. Work through the journeys below in order; together they take 30–45 minutes per
OS. When a step fails, write down what you did and what you saw (the exact words, or a screenshot), and attach a
doctor bundle (see [Reporting](#reporting)). The bundle is a small zip with Astrid's status, its versions and the
last part of its logs. Passwords, tokens, keys and credentials are removed before anything is written. File paths
in the logs and tool details stay, so they can show your user name.

## Before you start

- Use Chrome or Edge. Safari and Firefox are untested (see [Known gaps](#known-gaps)).
- macOS and Linux: use Terminal. Windows: use **Windows PowerShell** (not Command Prompt).
- You don't need administrator rights. Don't run the line with `sudo` or "Run as administrator".
- Use a computer where Astrid holds nothing you need. The uninstall journey deletes Astrid's data at the end.

### Where things live

| | macOS | Linux | Windows |
|---|---|---|---|
| Program files | `~/.local/share/astrid` | `${XDG_DATA_HOME:-$HOME/.local/share}/astrid` | `%LOCALAPPDATA%\Astrid` |
| Your workspace (projects, media) | `~/Library/Application Support/Astrid Runtime` | `${XDG_DATA_HOME:-$HOME/.local/share}/astrid-runtime` | `%LOCALAPPDATA%\Astrid Runtime` |
| The log (install and running Astrid) | `~/Library/Logs/Astrid Runtime/install.log` | `${XDG_STATE_HOME:-$HOME/.local/state}/astrid-runtime/logs/install.log` | `%LOCALAPPDATA%\Astrid Runtime\logs\install.log` |
| What keeps Astrid running | LaunchAgent `haus.astrid.runtime` | systemd user unit `astrid.service` | Task Scheduler task `Astrid Runtime` |
| Optional service settings | `~/.local/share/astrid/service-env.json` | `${XDG_DATA_HOME:-$HOME/.local/share}/astrid/service-env.json` | `%LOCALAPPDATA%\Astrid\service-env.json` |

On Linux, `XDG_DATA_HOME` sets the program and workspace roots, and `XDG_STATE_HOME` sets the log root.

The optional service settings file is private JSON. It starts as `{}`. To change the engine idle timeout or allow a GPU
pack that is not qualified yet, edit it with string values, for example:

```json
{
  "ASTRID_WARM_IDLE_SECONDS": "600",
  "ASTRID_ALLOW_UNQUALIFIED_GPU": "1"
}
```

Only those two keys are accepted. After saving, run the install line again or use `--repair` to restart Astrid; the
service reads the file when it starts. Shell profile changes do not reach the login service.

### Two checks you'll use often

**Is Astrid answering?**

macOS and Linux:

```sh
curl -s -H "Origin: https://astrid.haus" http://127.0.0.1:17340/api/runtime/v1/health
```

Windows:

```powershell
curl.exe -s -H "Origin: https://astrid.haus" http://127.0.0.1:17340/api/runtime/v1/health
```

Good: a line of JSON where `status` is `ok`. Nothing at all means Astrid isn't answering.

**Is the login service running?**

macOS:

```sh
launchctl print "gui/$(id -u)/haus.astrid.runtime" | grep -E 'state =|pid ='
```

Good: `state = running` and a `pid`.

Linux:

```sh
systemctl --user status astrid.service --no-pager
```

Good: `active (running)`.

Windows:

```powershell
Get-ScheduledTask -TaskName 'Astrid Runtime' | Select-Object TaskName, State
```

Good: `State` is `Running`.

## 1. Install with the one line

**Steps**

1. Open https://astrid.haus in Chrome or Edge. Click **Set up Astrid**, then **Copy install command**.
2. Paste it into Terminal (macOS, Linux) or PowerShell (Windows) and press Enter. These are the lines:

   macOS and Linux:

   ```sh
   curl -fsSL https://astrid.haus/install | sh
   ```

   Windows:

   ```powershell
   irm https://astrid.haus/install.ps1 | iex
   ```

3. Wait. The first install prepares Python, Bun, Node and Astrid itself, so it can take 10 minutes or more. This build
   pins uv 0.11.32, Bun 1.3.14 and Node 20.19.4. It checks for FFmpeg and FFprobe on `PATH` first. If that build
   passes Astrid’s required encoder and filter probe, it uses it; otherwise it downloads the pinned FFmpeg build.
4. When the browser opens, choose **Allow** when the browser asks about devices on your network.
5. Run the same line a second time.

**You should see**

- The line prints, in order: `Using your workspace at …`, `Installing the pinned Astrid version.`,
  `Starting Astrid at sign-in.`, `Open https://astrid.haus`.
- Your default browser opens astrid.haus. If it isn't Chrome or Edge, open https://astrid.haus in Chrome or Edge yourself.
- The page says **Choose Allow in Chrome** (or Edge). After you allow, it opens the editor by itself. A new workspace
  shows **No projects yet**.
- macOS may show a notice that a background item was added. That's the login service. Note the name it shows.
- The second run prints `Restarting Astrid with the installed version.` and `Open https://astrid.haus`, and the page
  connects again. It doesn't download everything again.
- The two checks above both pass.
- The install record and doctor bundle identify the FFmpeg source as `path` or `download`, along with its version.

**It's a failure if**

- The line prints `Astrid could not get ready.` or `Astrid could not finish; …`. Copy the whole message, including
  the `Details:` line.
- On Windows, the PowerShell window closes by itself. Open the log from the table above and attach it.
- The page stays on a connection screen after you chose Allow.
- The second run installs a new version or changes your workspace.
- Linux only: the line prints `There is no systemd user service; …`. Note it. Astrid runs, but it won't come back after
  a reboot or a crash (see Known gaps).

## 2. A cleared browser or a new browser profile

**Steps**

1. With Astrid running, open a new Chrome profile or an incognito window (Edge: InPrivate). Go directly to
   https://astrid.haus/tools/video-editor.
2. Before clicking anything, confirm the page says **Set up Astrid on this computer** and shows the install line.
   There should be no local-network permission prompt and the page should not try to connect yet.
3. In that profile, open `https://astrid.haus/?connect=1#continue`. When the browser asks about devices on your
   network, choose **Block**. The page should show **Allow Astrid in Chrome** with two Site settings steps. Follow
   them to set Local network access to Allow, then return to the tab; it should open the editor once Astrid is found.
4. Stop Astrid:

   macOS:

   ```sh
   launchctl bootout "gui/$(id -u)/haus.astrid.runtime"
   ```

   Linux:

   ```sh
   systemctl --user stop astrid.service
   ```

   Windows:

   ```powershell
   Stop-ScheduledTask -TaskName 'Astrid Runtime'
   ```

5. While Astrid is stopped, open another fresh profile or incognito window and go directly to
   https://astrid.haus/tools/video-editor. Confirm it shows setup before any permission instructions. Then open
   `https://astrid.haus/?connect=1#continue` and choose **Allow** when the browser asks.
6. Look at your first browser (the one from journey 1) too. Reload it if it hasn't changed. Click **Copy** on that
   page and run the line it gives you.

**You should see**

- Step 2: **Set up Astrid on this computer** appears before any permission instructions.
- Step 3: after you block the browser prompt, **Allow Astrid in Chrome** shows the two Site settings steps. After
  Local network access is allowed, the editor opens with your workspace.
- Step 5: the fresh profile shows setup before the prompt. After you allow it while Astrid is stopped, it still says
  **Set up Astrid on this computer**; this profile has not connected to Astrid before.
- Step 6: the browser that connected before says **Astrid isn't running**, with the same line.
- Step 6: the line prints `Restarting Astrid with the installed version.` Both pages open the editor by themselves.

**It's a failure if**

- A page asks for the browser's permission before you clicked anything (except right after the install line opened it).
- A browser that has connected before says "Set up" instead of "isn't running", or the other way round.
- The line on the screen is for the wrong OS.
- A page doesn't open by itself once Astrid is back (wait 30 seconds before you count it).

## 3. Chat with each agent

**Steps**

1. In the editor, click **New project**, then open its timeline. Open the chat panel.
2. Click the small arrow next to **New** ("New chat with…"). Note what each agent says: Astrid, Claude Code, Codex.
3. For each agent marked Ready (or with a model name), start a chat and send: `Reply with the word hello.`
4. If you have Claude Code or Codex signed in, sign out of one:

   ```sh
   claude auth logout
   ```

   ```sh
   codex logout
   ```

   Then close and reopen the menu (reload the page if it hasn't changed). Click the agent you signed out of.
5. Sign back in, then reopen the menu:

   ```sh
   claude auth login
   ```

   ```sh
   codex login
   ```

**You should see**

- Each agent shows one state: Ready (or its model name), **Sign in** or **Not installed**, with one line underneath
  when it isn't ready.
- A ready agent answers within about 30 seconds.
- A signed-out Claude Code or Codex shows **Sign in** and its matching `claude auth login` or `codex login` command. A signed-out Astrid
  agent shows `Run astrid, then /login`. Clicking a sign-in line copies it and shows **Copied**; it doesn't start a chat.
- An agent you haven't installed shows **Not installed** and an install line.
- After you sign back in, the agent shows Ready again.

**It's a failure if**

- An agent you've installed and signed in shows **Not installed** or **Sign in**. Write down how you installed it
  (for example npm, Homebrew or the official installer).
- The chat panel says `Chat isn't running on this computer right now.` while the page is connected.
- You see a raw error, an error code or "404" anywhere in chat.
- A known signed-in provider or available model catalog does not show **Ready**; a known signed-out provider with no
  usable models does not show **Sign in** with `Run astrid, then /login`; or an unknown/unavailable catalog shows
  **Sign in** instead of remaining **Ready**.

## 4. A GPU task, then idle

Do this only if the person who sent you this kit set up a generation engine (Wan2GP or ComfyUI) on your computer.
The install line doesn't set one up (see Known gaps). Skip it otherwise. Keep the engine checkout and its environment
outside Astrid's program folder; uninstall removes that folder. On Windows, installer-managed GPU environments live
under `%LOCALAPPDATA%\Astrid GPU`.

Astrid keeps an engine loaded for **10 minutes** after its last task, so the next task starts fast. Then it stops
the engine, which frees the GPU memory. The window defaults to 600 seconds; set `ASTRID_WARM_IDLE_SECONDS` in the
service settings file under [Where things live](#where-things-live) if you need to test another value, then run the
installer line again to restart the service.

**Steps**

1. Note the GPU memory in use before you start (NVIDIA, on Linux or Windows):

   ```sh
   nvidia-smi
   ```

   On macOS, open Activity Monitor and find the engine's `python` process instead. On Windows, if the GPU is not yet
   qualified, set `ASTRID_ALLOW_UNQUALIFIED_GPU` to `"1"` in the service settings file before starting the task.

2. Run a short generation the way the kit's sender told you, for example by asking Astrid in chat.
3. Run `nvidia-smi` again while it runs, and again right after it finishes.
4. Leave Astrid idle. Don't start other tasks, and don't restart Astrid. After 12 minutes, run `nvidia-smi` again.

**You should see**

- While it runs, and right after it finishes: the engine process is listed and holds GPU memory. That's the warm hold.
- After 12 minutes: the engine process is gone, and the memory in use is back near where it started.

**It's a failure if**

- The memory is still held after 15 minutes of idle.
- The engine stops while a task is still running.
- Windows: after opting in for an unqualified GPU as described above, a task still refuses with "not qualified yet".
  Report the GPU model and driver version from `nvidia-smi`.

## 5. Kill the Runtime, and it comes back

**Steps**

1. Have the editor open on a project.
2. Kill Astrid's Runtime:

   macOS:

   ```sh
   launchctl kill SIGKILL "gui/$(id -u)/haus.astrid.runtime"
   ```

   Linux:

   ```sh
   systemctl --user kill --signal=SIGKILL astrid.service
   ```

   Windows:

   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" | Where-Object { $_.CommandLine -like '*astrid_runtime*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
   ```

3. Watch the page. Run the two checks.
4. Once it's back, send a chat message to a ready agent.

**You should see**

- The page shows **Astrid stopped**, then **Astrid restarted** with a **Reload** button. After Reload, your project is there.
- macOS restarts it within about 20 seconds (launchd's KeepAlive). Linux restarts it after about 5 seconds
  (systemd's Restart=on-failure). Windows retries after 1 minute (Task Scheduler's restart on failure).
- Chat answers again.

**It's a failure if**

- Astrid isn't back after 1 minute (macOS, Linux) or 3 minutes (Windows). Then run the install line: it should print
  `Restarting Astrid with the installed version.` and bring it back. Report both.
- Your project or recent changes are missing after Reload.
- Chat doesn't answer after the restart.

## 6. Reboot, or sign out and back in

**Steps**

1. Sign out of your computer's account and sign back in. Don't run anything.
2. Wait 1 minute, then open astrid.haus in the browser you used in journey 1.
3. Restart the computer, and do step 2 again.

**You should see**

- The two checks pass without you running anything.
- The page opens the editor by itself, with your project. It doesn't ask for permission again.

**It's a failure if**

- Astrid isn't running after sign-in. Note it, then run the install line to bring it back.
- Windows: the Task Scheduler task exists but isn't `Running`, or a console window shows up at sign-in.
- Linux: systemd user services start only once you sign in. Not running before sign-in isn't a failure.

## 7. Update

Before updating, leave a recognizable conversation in each agent you configured in journey 3.
Record its title and a sentence you can find again.

**Steps**

1. Run the update line:

   macOS and Linux:

   ```sh
   curl -fsSL https://astrid.haus/install | sh -s -- --update
   ```

   Windows:

   ```powershell
   & ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update
   ```

2. Watch the page while it runs, and reload it if it asks.
3. List the program versions and backups:

   macOS:

   ```sh
   ls ~/.local/share/astrid/versions ~/.local/share/astrid/backups
   ```

   Linux:

   ```sh
   ls "${XDG_DATA_HOME:-$HOME/.local/share}/astrid/versions" "${XDG_DATA_HOME:-$HOME/.local/share}/astrid/backups"
   ```

   Windows:

   ```powershell
   Get-ChildItem "$env:LOCALAPPDATA\Astrid\versions", "$env:LOCALAPPDATA\Astrid\backups"
   ```

**You should see**

- The line prints, in order: `Stopping Astrid before the update.`, `Backing up your workspace.`,
  `Installing the pinned Astrid version.`, `Updating the workspace with Astrid Runtime.`, `Starting Astrid at sign-in.`,
  `Open https://astrid.haus`.
- The page shows **Astrid stopped**, then **Astrid restarted**. After Reload, the same projects are there.
- Two folders under `versions` (the new one and the previous one) and one under `backups`.
- Your earlier conversations still appear once in the session list and reopen with their messages.
  If you selected a custom chat folder or session directory, that selection is retained.

**The "Update Astrid" screen.** The page shows **Update Astrid** only when your Astrid is older than the page. You
can't bring it up on purpose. If you see it, click **Copy**, run that line, and check the same things as above.
Note which OS line it gave you.

**Rollback (optional).** This checks that a failed update puts everything back.

1. Run the update line again. When it prints `Installing the pinned Astrid version.`, press Ctrl+C.
2. Wait until the line stops printing. On Windows this can take a minute after the prompt comes back.
3. Run the two checks and open the page.

You should see a short failure message with a `Details:` line, saying your workspace and the update backup were
kept. Astrid then runs the previous version, on the same workspace, with the same projects. It's a failure if Astrid
isn't running afterwards, a project is missing, or the log says `recovery also failed`. If it isn't running, run the
plain install line and report what it prints.

## 8. Uninstall

Make a doctor bundle first (see [Reporting](#reporting)); there is no installed version for doctor after uninstall.

**Steps**

1. Run the uninstall line:

   macOS and Linux:

   ```sh
   curl -fsSL https://astrid.haus/install | sh -s -- --uninstall
   ```

   Windows:

   ```powershell
   & ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall
   ```

2. Check that the login service is gone:

   macOS:

   ```sh
   launchctl print "gui/$(id -u)/haus.astrid.runtime"; ls ~/Library/LaunchAgents/haus.astrid.runtime.plist
   ```

   Linux:

   ```sh
   systemctl --user status astrid.service --no-pager
   ```

   Windows:

   ```powershell
   Get-ScheduledTask -TaskName 'Astrid Runtime'
   ```

3. Check that the managed program folder is gone. On Windows, the running bootstrap may leave its directory behind.
   If the line prints a manual cleanup instruction, follow it after the installer exits, then check that the folder is gone:

   macOS:

   ```sh
   ls ~/.local/share/astrid
   ```

   Linux:

   ```sh
   ls "${XDG_DATA_HOME:-$HOME/.local/share}/astrid"
   ```

   Windows:

   ```powershell
   Test-Path "$env:LOCALAPPDATA\Astrid"
   ```

4. Run the plain install line once more (journey 1) to reinstall. The installer should adopt the kept workspace; check
   that `Using your workspace at …` names the same path, then open astrid.haus and confirm your projects and earlier
   conversations are still there.
5. Run the uninstall line a second time. It should complete safely.
6. Remove the workspace at the end of testing with the delete-data line below. Run it twice; both runs should complete
   safely, and the workspace should be gone.

**You should see**

- The line prints `Astrid was uninstalled.` and `Workspace kept at …`.
- Step 2: the service isn't found (macOS: "Could not find service" and no such file; Linux: the unit "could not be
  found"; Windows: no scheduled task found).
- Step 3: no such folder (Windows: `False` after any printed cleanup instruction is followed).
- After the first uninstall, the page says **Astrid isn't running**. After reinstalling in step 4, the page opens the same workspace.

**What's left behind, on purpose:**

- your workspace folder (projects and media), from the table above;
- the log folder on macOS and Linux (on Windows it sits inside the workspace folder);
- the `astrid-install.lock` file and `astrid-install.json` selection record next to the program folder; the selection
  record supports repeat uninstall and reinstall;
- installer-managed Windows GPU environments under `%LOCALAPPDATA%\Astrid GPU`, if you have any;
- uv's download cache (macOS: `~/Library/Caches/uv`; Linux: `${XDG_CACHE_HOME:-$HOME/.cache}/uv`;
  Windows: `%LOCALAPPDATA%\uv\cache`);
- your sign-ins for Claude Code, Codex and Astrid's model provider;
- the browser's permission for astrid.haus.

**It's a failure if**

- Astrid still runs, or comes back after a reboot.
- The workspace folder is gone (you didn't ask for that).
- The line prints `Astrid was unregistered; some files remain.` Copy each `Remaining:` line. On Windows, run the
  uninstall line again and say whether the list got shorter.

**Delete the workspace after testing.** This removes Astrid's workspace and projects. Run the uninstall line with
`--delete-data` twice to check that the command is safe to repeat.

macOS and Linux:

```sh
curl -fsSL https://astrid.haus/install | sh -s -- --uninstall --delete-data
```

Windows PowerShell:

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall --delete-data
```

After the first run, confirm the workspace path from the table above is gone. Keep the doctor bundle and install log
for your report.

## Reporting

For each failure, send:

- the journey and step number;
- your OS and version, CPU (Intel, Apple silicon, AMD, ARM), and GPU with its driver version if you have one;
- the browser and its version;
- what you did and what you saw: exact words or a screenshot, and the time;
- a doctor bundle, made right after the failure.

Make a bundle at the end of a run too, even if everything passed.

**Make a doctor bundle.** The installer line runs the doctor from the installed version, supplies the selected workspace
root, and saves the bundle in the log folder. It works while Astrid is down.

macOS and Linux:

```sh
curl -fsSL https://astrid.haus/install | sh -s -- --doctor
```

Windows PowerShell:

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --doctor
```

Look for `Astrid doctor bundle: <path>` and attach that ZIP. By default it writes `doctor.zip` in the log folder; the
line can also take an explicit bundle path after `--doctor`. An unhealthy Runtime still produces a bundle, and the
installer line succeeds when the bundle is written. If no installed version exists (for example, the install never
finished or Astrid was uninstalled), attach the install log from the table above instead.

**What the bundle holds:** `status.json` (Astrid's health check, with secrets and most paths removed), `versions.json`,
`install-manifest.json` (version numbers, source revisions, and selected FFmpeg/FFprobe paths and provenance), and `logs/` (the last 256 KB of each Astrid log,
1 MB at most). Passwords, tokens, keys and credentials are removed from the logs. File paths in the logs stay.

## Known gaps

These are known. Report what you see, but don't stop testing for them.

**Windows**

- Native Windows has never run end to end. Unit tests run in Windows CI. The install line, the sign-in task,
  Chrome on Windows and GPUs are first exercised by you.
- GPU packs (Wan2GP, ComfyUI) say "not qualified yet" until a tester confirms them on a real NVIDIA computer. GPU
  setup needs an engine checkout and is beyond this short installer run. To pass settings to the login service, use
  the service environment file described in [Where things live](#where-things-live); shell profile changes do not
  reach the service.
- The installer has not been run natively on Windows. Windows PowerShell 5.1 in particular remains unverified; if
  the line fails or its window closes, report the exact message and attach the install log.
- Coming back after the Runtime is killed relies on Task Scheduler's restart on failure. It hasn't been confirmed.
- Windows may retain the bootstrap directory while an Astrid terminal is open. If uninstall prints
  `After this line returns, run: Remove-Item …`, wait for the installer to exit, close Astrid terminals, run each
  printed cleanup command, and check that those paths are gone.
- Windows on ARM can't install: the pinned downloads have no Bun or FFmpeg build for it. The log says
  `There is no qualified bun build for windows-arm64.`
- A PC whose execution policy is set by the organization stops with a message asking the administrator to allow the installer.
- OneDrive: Astrid's own folders are in `AppData\Local`, which OneDrive doesn't sync. Media you add from a
  OneDrive-redirected Desktop or Documents, especially online-only files, is untested.

**Every OS**

- Chrome's local-network permission is the browser's own prompt, and its wording varies by Chrome version. If you
  block it, only the two steps in site settings undo that. Only Chrome and Edge are expected to work; Safari and
  Firefox are untested.
- The install line doesn't set up a GPU engine.
- The engine idle window defaults to 10 minutes. It can be changed in the service settings file under [Where things
  live](#where-things-live).
- Reinstalling after an uninstall that kept the workspace is part of journey 8: the installer should adopt the kept
  workspace and start Astrid on it. Repeating uninstall, including `--uninstall --delete-data`, should be safe.
- If the installer never completed, or Astrid has already been uninstalled, the installer’s `--doctor` command is
  unavailable; attach the install log instead.
- "Making new images isn't on this page yet." next to the compose controls is expected.
- macOS service and installer behavior has not been tested natively; report what happens with the LaunchAgent and
  include the install log and doctor bundle.

**Linux**

- Without a systemd user session (some minimal or container setups), nothing restarts Astrid after a crash or at
  sign-in. The line is the restart.
- Astrid restarts by itself only after a crash. If it's stopped normally (for example `kill` without `-9`), it stays
  stopped until the line runs or you sign in again. macOS always restarts it.
