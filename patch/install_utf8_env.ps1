# ==============================================================================
# Windows UTF-8 Anti-Mojibake Environment Installer
# Designed for Antigravity & General Development
# ==============================================================================

Write-Host "Starting UTF-8 Environment Configuration..." -ForegroundColor Cyan

# 1. Update PowerShell Profile
$profilePath = $PROFILE
if (-not (Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force | Out-Null
}

$profileContent = Get-Content $profilePath -Raw
$configBlock = @"

# === Comprehensive UTF-8 Anti-Garble Block ===
# 1. Console Host Encoding (fixes output from native apps to the console)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 2. Pipeline Encoding (fixes sending text to native apps via pipeline)
`$OutputEncoding = [System.Text.Encoding]::UTF8

# 3. Active Code Page (forces legacy tools like ping/git to output UTF-8)
chcp 65001 > `$null

# 4. Default File Encoding (prevents PowerShell from generating UTF-16 LE files by default)
`$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
`$PSDefaultParameterValues['Out-String:Encoding'] = 'utf8'
`$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'
`$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'

# 5. Global Environment Variables for Node/Python/Git
`$env:PYTHONIOENCODING = "utf-8"
`$env:PYTHONUTF8 = "1"
`$env:LESSCHARSET = "utf-8"

# 6. Remove Dummy GitHub Token (Antigravity Specific)
if (`$env:GITHUB_TOKEN -eq 'github_pat_antigravitydummytoken') {
    Remove-Item Env:\GITHUB_TOKEN -ErrorAction SilentlyContinue
}
# ===============================================
"@

if ($profileContent -match "Comprehensive UTF-8 Anti-Garble Block") {
    Write-Host "[SKIP] PowerShell profile already contains the UTF-8 configuration." -ForegroundColor Yellow
} else {
    Add-Content -Path $profilePath -Value $configBlock
    Write-Host "[OK] Injected UTF-8 configuration into PowerShell profile: $profilePath" -ForegroundColor Green
}

# 2. Update CMD AutoRun
Write-Host "Configuring cmd.exe AutoRun..." -ForegroundColor Cyan
$regPath = "HKCU:\SOFTWARE\Microsoft\Command Processor"
if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}
Set-ItemProperty -Path $regPath -Name "AutoRun" -Value "chcp 65001 > nul"
Write-Host "[OK] cmd.exe now defaults to code page 65001 (UTF-8)" -ForegroundColor Green

# 3. Set Global Environment Variables
Write-Host "Setting global environment variables..." -ForegroundColor Cyan
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
[Environment]::SetEnvironmentVariable("LESSCHARSET", "utf-8", "User")
Write-Host "[OK] Global variables set (PYTHONIOENCODING, PYTHONUTF8, LESSCHARSET)" -ForegroundColor Green

# 4. Configure Git
Write-Host "Configuring Git encoding..." -ForegroundColor Cyan
if (Get-Command git -ErrorAction SilentlyContinue) {
    git config --global core.quotepath false
    git config --global gui.encoding utf-8
    git config --global i18n.commitencoding utf-8
    git config --global i18n.logoutputencoding utf-8
    Write-Host "[OK] Git UTF-8 configuration applied" -ForegroundColor Green
} else {
    Write-Host "[WARN] Git is not installed, skipped git config" -ForegroundColor Yellow
}

Write-Host "`nAll done! Please restart your terminal for all changes to take effect." -ForegroundColor Cyan
