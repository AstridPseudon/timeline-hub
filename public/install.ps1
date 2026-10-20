# Astrid's bootstrap, PowerShell 5.1+. Run with -NoProfile -ExecutionPolicy Bypass.
# A child scope keeps irm | iex from changing the caller's error preference.
& {
    param([bool]$FileInvocation)
    $InstallerArgs = @($args)
    $ErrorActionPreference = 'Stop'
    $UvVersion = '0.11.32'
    $PythonVersion = '3.11.13'
    $Bootstrap = Join-Path $env:LOCALAPPDATA 'Astrid\bootstrap'
    $LogDir = Join-Path $env:LOCALAPPDATA 'Astrid Runtime\logs'
    $Log = Join-Path $LogDir 'install.log'
    $Temp = Join-Path ([IO.Path]::GetTempPath()) ('astrid-install-' + [Guid]::NewGuid().ToString('N'))
    $CoreFailure = $null
    $NativeExitCode = 1

    # The readers run in .NET so stderr never becomes a PS 5.1 terminating
    # error, and progress bypasses the function's captured success output.
    function Invoke-InstallerCommand([string]$FilePath, [string[]]$Arguments, [switch]$LogOutput, [switch]$StreamOutput) {
        $Quoted = foreach ($Argument in $Arguments) {
            '"' + ([regex]::Replace($Argument, '(\\*)"', '$1$1\"') -replace '(\\+)$', '$1$1') + '"'
        }
        $Info = New-Object Diagnostics.ProcessStartInfo
        $Info.FileName = $FilePath
        $Info.Arguments = $Quoted -join ' '
        $Info.UseShellExecute = $false
        # A detached child would miss the console's Ctrl+C event on Windows.
        $Info.CreateNoWindow = $false
        $Info.RedirectStandardOutput = $true
        $Info.RedirectStandardError = $true
        return [AstridInstallerProcessV2]::Run($Info, $Log, $LogOutput.IsPresent, $StreamOutput.IsPresent)
    }

    try {
        New-Item -ItemType Directory -Force -Path $Bootstrap, $LogDir, $Temp | Out-Null
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $Policy = Get-ExecutionPolicy -List
        $Enforced = $Policy | Where-Object { $_.Scope -in @('MachinePolicy','UserPolicy') -and $_.ExecutionPolicy -in @('Restricted','AllSigned') }
        if ($Enforced) {
            throw 'An organization execution policy may block setup. Process-level Bypass cannot override Group Policy; ask your administrator to allow the Astrid installer.'
        }
        if (-not ('AstridInstallerProcessV2' -as [type])) {
            Add-Type -TypeDefinition @'
using System;
using System.Diagnostics;
using System.IO;
using System.Text;
public sealed class AstridInstallerProcessV2 {
    private static readonly string[] FailureMarkers = new string[] {
        "Astrid could not finish; your workspace and any update backup have been kept.",
        "There is not enough free disk space to back up your workspace."
    };
    public int ExitCode;
    public string Output;
    public bool FailureDisplayed;
    public static int FindFailureStart(string text) {
        int found = -1;
        foreach (string marker in FailureMarkers) {
            int index = text.IndexOf(marker, StringComparison.Ordinal);
            if (index >= 0 && (found < 0 || index < found)) found = index;
        }
        return found;
    }
    private static void AppendLog(string log, string text) {
        using (var stream = new FileStream(log, FileMode.Append, FileAccess.Write, FileShare.ReadWrite | FileShare.Delete))
        using (var writer = new StreamWriter(stream, new UTF8Encoding(false))) {
            writer.Write(text);
        }
    }
    public static AstridInstallerProcessV2 Run(ProcessStartInfo info, string log, bool logOutput, bool streamOutput) {
        var output = new StringBuilder();
        var errors = new StringBuilder();
        var gate = new object();
        bool failurePending = false, interrupted = false, failureDisplayed = false;
        ConsoleCancelEventHandler onCancel = (sender, args) => { lock (gate) interrupted = true; };
        using (var process = new Process()) {
            process.StartInfo = info;
            process.OutputDataReceived += (sender, data) => {
                if (data.Data == null) return;
                lock (gate) {
                    output.AppendLine(data.Data);
                    if (Array.IndexOf(FailureMarkers, data.Data) >= 0) failurePending = true;
                    // The final failure paragraph is thrown once by the caller.
                    if (streamOutput && !failurePending) Console.WriteLine(data.Data);
                }
            };
            process.ErrorDataReceived += (sender, data) => {
                if (data.Data != null) lock (gate) errors.AppendLine(data.Data);
            };
            Console.CancelKeyPress += onCancel;
            try {
                process.Start();
                try {
                    process.BeginOutputReadLine();
                    process.BeginErrorReadLine();
                } finally {
                    // The child shares our console and receives Ctrl+C itself.
                    // Keep its readers alive until cooperative recovery completes.
                    process.WaitForExit();
                    // The core opens this same log. Append only after it exits,
                    // so Windows sharing and independent file offsets cannot clash.
                    if (errors.Length > 0) AppendLog(log, errors.ToString());
                    if (logOutput) AppendLog(log, output.ToString());
                    // Ctrl+C can stop the PS pipeline before its catch can run.
                    if (streamOutput && interrupted && failurePending) {
                        string text = output.ToString();
                        Console.WriteLine(text.Substring(FindFailureStart(text)).TrimEnd());
                        failureDisplayed = true;
                    }
                }
                return new AstridInstallerProcessV2 { ExitCode = process.ExitCode, Output = output.ToString(), FailureDisplayed = failureDisplayed };
            } finally {
                Console.CancelKeyPress -= onCancel;
            }
        }
    }
}
'@
        }
        $Manifest = Join-Path $Temp 'manifest.json'
        $ManifestUrl = if ($env:ASTRID_INSTALL_MANIFEST_URL) { $env:ASTRID_INSTALL_MANIFEST_URL } else { 'https://astrid.haus/install-manifest.json' }
        Invoke-WebRequest -UseBasicParsing $ManifestUrl -OutFile $Manifest
        $Pins = Get-Content -Raw -Encoding UTF8 $Manifest | ConvertFrom-Json
        if ($Pins.tools.uv.version -ne $UvVersion -or $Pins.tools.python.version -ne $PythonVersion) {
            throw 'The bootstrap and manifest tool pins disagree.'
        }
        $Uv = Join-Path $Bootstrap 'uv.exe'
        $InstallUv = -not (Test-Path $Uv)
        if (-not $InstallUv) {
            $FoundVersion = Invoke-InstallerCommand $Uv @('--version')
            if ($FoundVersion.ExitCode -ne 0) { throw 'The installed uv could not run.' }
            $VersionParts = $FoundVersion.Output.Trim() -split '\s+'
            $InstallUv = $VersionParts.Count -lt 2 -or $VersionParts[0] -ne 'uv' -or $VersionParts[1] -ne $UvVersion
        }
        if ($InstallUv) {
            $UvScript = Join-Path $Temp 'uv.ps1'
            Invoke-WebRequest -UseBasicParsing "https://astral.sh/uv/$UvVersion/install.ps1" -OutFile $UvScript
            $env:UV_UNMANAGED_INSTALL = $Bootstrap
            $env:UV_NO_MODIFY_PATH = '1'
            $PowerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
            $Result = Invoke-InstallerCommand $PowerShell @('-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',$UvScript) -LogOutput
            if ($Result.ExitCode -ne 0) { throw 'uv setup failed. Group Policy can override process-level execution-policy Bypass; see the log.' }
        }
        $env:UV_PYTHON_INSTALL_DIR = Join-Path $Bootstrap 'python'
        $env:ASTRID_INSTALL_UV = $Uv
        $Result = Invoke-InstallerCommand $Uv @('python','install',$PythonVersion,'--no-bin','--no-registry') -LogOutput
        if ($Result.ExitCode -ne 0) { throw 'uv could not prepare Python.' }
        function Get-GitRequirement([string]$Name) {
            $Pin = $Pins.$Name
            $Sha = $Pin.sha
            if ($Sha -isnot [string] -or $Sha -cnotmatch '^[0-9a-f]{40}$') { throw "Invalid $Name source pin." }
            if ($null -eq $Pin.PSObject.Properties['repo']) {
                return "https://github.com/banodoco/astrid-$Name/archive/$Sha.tar.gz"
            }
            if ($Pin.repo -isnot [string] -or -not $Pin.repo) { throw 'Source repo must be an absolute local path or file:// URL.' }
            if ($Pin.repo.StartsWith('file://')) {
                $RepoAuthority = ($Pin.repo.Substring(7) -split '/', 2)[0]
                $RepoUrl = [Uri]$Pin.repo
                if (-not $RepoUrl.IsFile -or $RepoAuthority -cnotin @('', 'localhost') -or $RepoUrl.Query -or $RepoUrl.Fragment -or $Pin.repo.IndexOf('/', 7) -lt 0) {
                    throw 'Source file URL must refer to this computer.'
                }
                # .NET treats even localhost as UNC. Strip the validated local
                # authority before converting to this computer's native path.
                $LocalRepoUrl = [UriBuilder]::new($RepoUrl)
                $LocalRepoUrl.Host = ''
                $RepoPath = $LocalRepoUrl.Uri.LocalPath
            } else {
                $RepoPath = $Pin.repo
            }
            # Reject drive-relative paths, UNC shares and rooted paths without a
            # drive on Windows; only an absolute path on this computer is local.
            if (-not [IO.Path]::IsPathRooted($RepoPath) -or $RepoPath.StartsWith('\\')) { throw 'Source repo must be absolute and local.' }
            if ([IO.Path]::DirectorySeparatorChar -eq '\' -and $RepoPath -notmatch '^[A-Za-z]:[\\/]') { throw 'Source repo must include its drive.' }
            $RepoUrl = [Uri]::new([IO.Path]::GetFullPath($RepoPath))
            return 'git+' + $RepoUrl.AbsoluteUri + '@' + $Sha
        }
        $AgentRequirement = Get-GitRequirement 'agent'
        $Lock = Join-Path $Temp 'runtime.lock'
        if ($null -ne $Pins.agent.PSObject.Properties['repo']) {
            $RepoValue = $Pins.agent.repo
            if ($RepoValue.StartsWith('file://')) {
                $RepoUrl = [Uri]$RepoValue
                $RepoAuthority = ($RepoValue.Substring(7) -split '/', 2)[0]
                if (-not $RepoUrl.IsFile -or $RepoAuthority -cnotin @('', 'localhost') -or $RepoUrl.Query -or $RepoUrl.Fragment -or $RepoValue.IndexOf('/', 7) -lt 0) {
                    throw 'Source file URL must refer to this computer.'
                }
                $LocalRepoUrl = [UriBuilder]::new($RepoUrl)
                $LocalRepoUrl.Host = ''
                $AgentRepoPath = $LocalRepoUrl.Uri.LocalPath
            } else {
                $AgentRepoPath = $RepoValue
            }
            $LockResult = Invoke-InstallerCommand 'git' @('-C',$AgentRepoPath,'show',"$($Pins.agent.sha):requirements/runtime.lock")
            if ($LockResult.ExitCode -ne 0) { throw 'The pinned agent has no requirements/runtime.lock.' }
            [IO.File]::WriteAllText($Lock, $LockResult.Output, [Text.UTF8Encoding]::new($false))
        } else {
            $LockUrl = "https://raw.githubusercontent.com/banodoco/astrid-agent/$($Pins.agent.sha)/requirements/runtime.lock"
            Invoke-WebRequest -UseBasicParsing $LockUrl -OutFile $Lock
        }
        $Venv = Join-Path $Temp 'venv'
        $Result = Invoke-InstallerCommand $Uv @('venv',$Venv,'--python',$PythonVersion) -LogOutput
        if ($Result.ExitCode -ne 0) { throw 'The installer environment could not be prepared.' }
        $VenvPython = Join-Path $Venv 'Scripts/python.exe'
        $Result = Invoke-InstallerCommand $Uv @('pip','install','--python',$VenvPython,'--require-hashes','-r',$Lock) -LogOutput
        if ($Result.ExitCode -ne 0) { throw 'The pinned dependency lock could not be installed.' }
        $RuntimeRequirement = Get-GitRequirement 'runtime'
        $ClientRequirement = $RuntimeRequirement + '#subdirectory=packages/python'
        $Result = Invoke-InstallerCommand $Uv @('pip','install','--python',$VenvPython,'--no-deps',$RuntimeRequirement,$ClientRequirement,$AgentRequirement) -LogOutput
        if ($Result.ExitCode -ne 0) { throw 'The pinned Astrid packages could not be installed.' }
        $RunArgs = @('run', '--no-project', '--python', $VenvPython, 'python','-u','-I','-m','astrid','install','--manifest',$Manifest)
        $RunArgs += $InstallerArgs
        $Result = Invoke-InstallerCommand $Uv $RunArgs -StreamOutput
        $NativeExitCode = $Result.ExitCode
        $global:LASTEXITCODE = $NativeExitCode
        if ($Result.ExitCode -ne 0) {
            $FailureStart = [AstridInstallerProcessV2]::FindFailureStart($Result.Output)
            if ($FailureStart -ge 0) {
                $CoreFailure = $Result.Output.Substring($FailureStart).TrimEnd()
            }
            if ($Result.FailureDisplayed) {
                if ($FileInvocation) { exit $NativeExitCode }
                return
            }
            throw 'The Astrid installer did not finish; see the log.'
        }
    } catch {
        try {
            $ErrorText = ($_ | Out-String) + [Environment]::NewLine
            $ErrorBytes = [Text.UTF8Encoding]::new($false).GetBytes($ErrorText)
            $ErrorStream = [IO.FileStream]::new($Log, [IO.FileMode]::Append, [IO.FileAccess]::Write, [IO.FileShare]::ReadWrite -bor [IO.FileShare]::Delete)
            try { $ErrorStream.Write($ErrorBytes, 0, $ErrorBytes.Length) } finally { $ErrorStream.Dispose() }
        } catch { }
        $Message = if ($CoreFailure) { $CoreFailure } else { "Astrid could not get ready.`nDetails: $Log" }
        $global:LASTEXITCODE = $NativeExitCode
        if ($FileInvocation) {
            [Console]::Error.WriteLine($Message)
            exit $NativeExitCode
        }
        # Throw instead of exit: irm | iex must never close the user's shell.
        throw $Message
    } finally {
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $Temp
    }
} ([bool]$PSCommandPath -and $MyInvocation.MyCommand -is [Management.Automation.ExternalScriptInfo]) @args
