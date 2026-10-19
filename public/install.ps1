# Astrid's bootstrap, PowerShell 5.1+. Run with -NoProfile -ExecutionPolicy Bypass.
$InstallerArgs = @($args)
$ErrorActionPreference = 'Stop'
$UvVersion = '0.8.22'
$PythonVersion = '3.11.13'
$Bootstrap = Join-Path $env:LOCALAPPDATA 'Astrid\bootstrap'
New-Item -ItemType Directory -Force -Path $Bootstrap | Out-Null
$LogDir = Join-Path $env:LOCALAPPDATA 'Astrid Runtime\logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Log = Join-Path $LogDir 'install.log'
$Temp = Join-Path $Bootstrap ([Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $Temp | Out-Null
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $Policy = Get-ExecutionPolicy -List
    $Enforced = $Policy | Where-Object { $_.Scope -in @('MachinePolicy','UserPolicy') -and $_.ExecutionPolicy -in @('Restricted','AllSigned') }
    if ($Enforced) {
        throw 'An organization execution policy may block setup. Process-level Bypass cannot override Group Policy; ask your administrator to allow the Astrid installer.'
    }
    $Manifest = Join-Path $Temp 'manifest.json'
    Invoke-WebRequest -UseBasicParsing 'https://astrid.haus/install-manifest.json' -OutFile $Manifest
    $Pins = Get-Content -Raw -Encoding UTF8 $Manifest | ConvertFrom-Json
    if ($Pins.tools.uv.version -ne $UvVersion -or $Pins.tools.python.version -ne $PythonVersion) {
        throw 'The bootstrap and manifest tool pins disagree.'
    }
    $Uv = Join-Path $Bootstrap 'uv.exe'
    $InstallUv = -not (Test-Path $Uv)
    if (-not $InstallUv) {
        $FoundVersion = & $Uv --version
        if ($LASTEXITCODE -ne 0) { throw 'The installed uv could not run.' }
        $InstallUv = $FoundVersion -ne "uv $UvVersion"
    }
    if ($InstallUv) {
        $UvScript = Join-Path $Temp 'uv.ps1'
        Invoke-WebRequest -UseBasicParsing "https://astral.sh/uv/$UvVersion/install.ps1" -OutFile $UvScript
        $env:UV_UNMANAGED_INSTALL = $Bootstrap
        $env:UV_NO_MODIFY_PATH = '1'
        $PowerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
        & $PowerShell -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $UvScript *>> $Log
        if ($LASTEXITCODE -ne 0) { throw 'uv setup failed. Group Policy can override process-level execution-policy Bypass; see the log.' }
    }
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $Bootstrap 'python'
    $env:ASTRID_INSTALL_UV = $Uv
    & $Uv python install $PythonVersion *>> $Log
    if ($LASTEXITCODE -ne 0) { throw 'uv could not prepare Python.' }
    $RunArgs = @('run', '--no-project', '--python', $PythonVersion)
    foreach ($Name in @('runtime','agent')) {
        $Sha = $Pins.$Name.sha
        if ($Sha -notmatch '^[0-9a-f]{40}$') { throw "Invalid $Name source pin." }
        $RunArgs += @('--with', "https://github.com/banodoco/astrid-$Name/archive/$Sha.tar.gz")
    }
    $RunArgs += @('python','-I','-m','astrid','install','--manifest',$Manifest)
    $RunArgs += $InstallerArgs
    & $Uv @RunArgs 2>> $Log
    if ($LASTEXITCODE -ne 0) { throw 'The Astrid installer did not finish; see the log.' }
} catch {
    $_ | Out-String | Add-Content -Encoding UTF8 $Log
    Write-Host ('Astrid could not get ready: ' + $_.Exception.Message)
    Write-Host "Details: $Log"
    exit 1
} finally {
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $Temp
}
