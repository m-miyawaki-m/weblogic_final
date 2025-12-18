# WebLogic Domain Creation using WLST (PowerShell wrapper)

$OracleHome = "C:\Oracle\Middleware\Oracle_Home"
$WlstScript = "c:\dev\dev_weblogic\scripts\create_domain_final.py"
$WlstCmd = "$OracleHome\wlserver\common\bin\wlst.cmd"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "WebLogic Domain Creation (WLST)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if WLST exists
if (-not (Test-Path $WlstCmd)) {
    Write-Host "ERROR: WLST not found at: $WlstCmd" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] WLST found: $WlstCmd" -ForegroundColor Green
Write-Host "[OK] Python script: $WlstScript" -ForegroundColor Green
Write-Host ""

Write-Host "Executing WLST script..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
Write-Host ""

# Execute WLST
& $WlstCmd $WlstScript

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "SUCCESS: Domain created!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Red
    Write-Host "ERROR: Domain creation failed" -ForegroundColor Red
    Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "======================================" -ForegroundColor Red
    exit 1
}
