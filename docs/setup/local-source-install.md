# Install Astrid

Astrid Runtime and the agent run on your computer. Open the app at
https://astrid.haus.

On macOS or Linux:

```sh
curl -fsSL https://astrid.haus/install | sh
```

On Windows, from PowerShell 5.1 or later:

```powershell
& ([scriptblock]::Create((Invoke-RestMethod https://astrid.haus/install.ps1)))
```

Run the same line to repair or restart an existing installation. It keeps the
installed version and your workspace. To update, pass `--update` to the script
(`sh -s -- --update` after the pipe on macOS/Linux). Updates back up the selected
workspace and keep the previous program version until the new door is verified.

The scripts get pinned uv and Python, then invoke the shared `astrid install`
core. It installs user-local tools and registers a login service. No administrator
access is needed. Without a systemd user service on Linux, run the line to restart.
Installation ends with `Open https://astrid.haus` and opens the connection page.
On failure, report the sentence and the `Details:` log path.

`astrid install uninstall` stops and unregisters the service and removes owned
program files. It keeps data unless you explicitly add `--delete-data`; locked
files are reported for removal after their processes exit.

The app is hosted; installation does not clone or build it. App developers use
`npm run dev:local` in their app checkout. Creative providers still need their
own credentials and qualified artifacts.
