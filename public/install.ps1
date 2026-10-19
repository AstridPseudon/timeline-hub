# Astrid's bootstrap, PowerShell 5.1+. Run with -NoProfile -ExecutionPolicy Bypass.
# A child scope keeps irm | iex from changing the caller's error preference.
& {
    $InstallerArgs = @($args)
    $ErrorActionPreference = 'Stop'
    $UvVersion = '0.11.32'
    $PythonVersion = '3.11.13'
    $Bootstrap = Join-Path $env:LOCALAPPDATA 'Astrid\bootstrap'
    $LogDir = Join-Path $env:LOCALAPPDATA 'Astrid Runtime\logs'
    $Log = Join-Path $LogDir 'install.log'
    $Temp = Join-Path ([IO.Path]::GetTempPath()) ('astrid-install-' + [Guid]::NewGuid().ToString('N'))
    $CoreFailure = $null

    # Read native streams through .NET: PS 5.1 otherwise turns stderr progress
    # into terminating errors under ErrorActionPreference Stop, even on exit 0.
    function Invoke-InstallerCommand([string]$FilePath, [string[]]$Arguments, [switch]$LogOutput) {
        $Quoted = foreach ($Argument in $Arguments) {
            '"' + ([regex]::Replace($Argument, '(\\*)"', '$1$1\"') -replace '(\\+)$', '$1$1') + '"'
        }
        $Process = New-Object Diagnostics.Process
        try {
            $Process.StartInfo.FileName = $FilePath
            $Process.StartInfo.Arguments = $Quoted -join ' '
            $Process.StartInfo.UseShellExecute = $false
            $Process.StartInfo.CreateNoWindow = $true
            $Process.StartInfo.RedirectStandardOutput = $true
            $Process.StartInfo.RedirectStandardError = $true
            $Process.Start() | Out-Null
            $OutputTask = $Process.StandardOutput.ReadToEndAsync()
            $ErrorTask = $Process.StandardError.ReadToEndAsync()
            $Process.WaitForExit()
            $OutputText = $OutputTask.GetAwaiter().GetResult()
            $ErrorText = $ErrorTask.GetAwaiter().GetResult()
            if ($ErrorText) { Add-Content -Encoding UTF8 -Path $Log -Value $ErrorText }
            if ($LogOutput -and $OutputText) { Add-Content -Encoding UTF8 -Path $Log -Value $OutputText }
            return [pscustomobject]@{ ExitCode = $Process.ExitCode; Output = $OutputText }
        } finally {
            $Process.Dispose()
        }
    }

    try {
        New-Item -ItemType Directory -Force -Path $Bootstrap, $LogDir, $Temp | Out-Null
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $Policy = Get-ExecutionPolicy -List
        $Enforced = $Policy | Where-Object { $_.Scope -in @('MachinePolicy','UserPolicy') -and $_.ExecutionPolicy -in @('Restricted','AllSigned') }
        if ($Enforced) {
            throw 'An organization execution policy may block setup. Process-level Bypass cannot override Group Policy; ask your administrator to allow the Astrid installer.'
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
        $RunArgs = @('run', '--no-project', '--python', $PythonVersion)
        foreach ($Name in @('runtime','agent')) {
            $RunArgs += @('--with', (Get-GitRequirement $Name))
        }
        $RunArgs += @('python','-I','-m','astrid','install','--manifest',$Manifest)
        $RunArgs += $InstallerArgs
        $Result = Invoke-InstallerCommand $Uv $RunArgs
        if ($Result.ExitCode -ne 0) {
            if ($Result.Output.Contains('Astrid could not finish; your workspace and any update backup have been kept.')) {
                $CoreFailure = $Result.Output.TrimEnd()
            }
            throw 'The Astrid installer did not finish; see the log.'
        }
        if ($Result.Output) { Write-Output $Result.Output.TrimEnd() }
    } catch {
        $_ | Out-String | Add-Content -Encoding UTF8 -Path $Log -ErrorAction SilentlyContinue
        # Throw instead of exit: irm | iex must never close the user's shell.
        if ($CoreFailure) { throw $CoreFailure }
        throw "Astrid could not get ready.`nDetails: $Log"
    } finally {
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $Temp
    }
} @args
