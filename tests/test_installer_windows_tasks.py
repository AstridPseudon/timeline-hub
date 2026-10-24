"""Exercise Windows PowerShell exit semantics without touching real login tasks."""

import shutil
import subprocess

import pytest

from astrid.installer.service import Service

pytestmark = pytest.mark.windows_native


@pytest.mark.parametrize("operation", ["disable", "stop", "unregister"])
@pytest.mark.parametrize("scenario", ["absent", "present", "lookup_failure", "action_failure"])
def test_task_cleanup_preserves_powershell_success_and_failure(tmp_path, operation, scenario):
    powershell = shutil.which("powershell.exe") or shutil.which("pwsh")
    assert powershell, "Windows PowerShell is required to exercise its native exit semantics"
    invocations = []

    def run(argv):
        # Each invocation is a new PowerShell process. The polling query observes
        # the successful stop from the preceding invocation.
        state = "Running" if not invocations else "Ready"
        body = ""
        if scenario == "lookup_failure":
            body = "throw 'Task Scheduler unavailable'"
        elif scenario != "absent":
            body = f"[pscustomobject]@{{ TaskName='Astrid Runtime'; TaskPath='\\'; State='{state}' }}"
        action = "throw 'Cannot change task'" if scenario == "action_failure" else ""
        prelude = (
            "function Get-ScheduledTask { [CmdletBinding()] param([string]$TaskName); "
            # Reproduce the cmdlet's named lookup error on a fresh installation.
            + ("if ($TaskName) { $PSCmdlet.WriteError([System.Management.Automation.ErrorRecord]::new("
               "[Exception]::new('No matching task'), 'NoMatchingTask', "
               "[System.Management.Automation.ErrorCategory]::ObjectNotFound, $TaskName)); return }; "
               if scenario == "absent" else "")
            + body + " }; "
            "function Disable-ScheduledTask { process { " + action + " } }; "
            "function Stop-ScheduledTask { process { " + action + " } }; "
            "function Unregister-ScheduledTask { param([switch]$Confirm); process { " + action + " } }; "
        )
        script = argv[-1]
        invocations.append(script)
        result = subprocess.run(
            [powershell, "-NoProfile", "-NonInteractive", "-Command", prelude + script],
            capture_output=True, text=True, timeout=30, check=True,
        )
        return result.stdout

    manager = Service(tmp_path / "program", tmp_path / "log", run, home=tmp_path, system="win32")
    if scenario.endswith("failure"):
        with pytest.raises(subprocess.CalledProcessError):
            getattr(manager, operation)()
    else:
        getattr(manager, operation)()
    assert invocations
