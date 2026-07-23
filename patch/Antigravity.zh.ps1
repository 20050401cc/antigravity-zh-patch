$ErrorActionPreference = 'SilentlyContinue'

$appDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe = Join-Path $appDir 'Antigravity.exe'
$injector = Join-Path $appDir 'antigravity_zh_inject.py'

$mainProcess = Get-CimInstance Win32_Process -Filter "name='Antigravity.exe'" |
  Where-Object { $_.CommandLine -notmatch '--type=' } |
  Select-Object -First 1

if (-not $mainProcess) {
  Start-Process -FilePath $exe -ArgumentList '--lang=zh-CN', '--remote-debugging-port=0' -WorkingDirectory $appDir -RedirectStandardOutput "$env:TEMP\ag_out.log" -RedirectStandardError "$env:TEMP\ag_err.log" -WindowStyle Hidden
} elseif ($mainProcess.CommandLine -notmatch '--lang=zh-CN') {
  Start-Process -FilePath $exe -ArgumentList '--lang=zh-CN', '--remote-debugging-port=0' -WorkingDirectory $appDir -RedirectStandardOutput "$env:TEMP\ag_out.log" -RedirectStandardError "$env:TEMP\ag_err.log" -WindowStyle Hidden
}

Start-Sleep -Seconds 5
python $injector | Out-Null
