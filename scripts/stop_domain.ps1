# WebLogic ドメイン停止スクリプト
# このスクリプトは、WebLogicドメインのAdminServerを停止します。

# ==========================================
# 設定
# ==========================================

$DomainHome = "C:\Oracle\Middleware\user_projects\domains\base_domain"
$OracleHome = "C:\Oracle\Middleware"
$AdminUrl = "t3://localhost:7001"
$AdminUser = "weblogic"
$AdminPassword = "welcome1"

# ==========================================
# 前提条件チェック
# ==========================================

Write-Host "======================================"
Write-Host "WebLogic ドメイン停止スクリプト"
Write-Host "======================================"
Write-Host ""

Write-Host "ドメインをチェック中..." -ForegroundColor Cyan

if (-not (Test-Path $DomainHome)) {
    Write-Host "エラー: ドメインが見つかりません。" -ForegroundColor Red
    Write-Host "パス: $DomainHome" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ ドメイン確認: $DomainHome" -ForegroundColor Green
Write-Host ""

# ==========================================
# AdminServerの停止
# ==========================================

Write-Host "AdminServerを停止中..." -ForegroundColor Cyan
Write-Host ""

# WLSTスクリプトを作成
$WlstScript = @"
# WLST スクリプト - AdminServerの停止

try:
    print('AdminServerに接続中...')
    connect('$AdminUser', '$AdminPassword', '$AdminUrl')

    print('AdminServerを停止中...')
    shutdown('AdminServer', 'Server', force='true')

    print('AdminServerが正常に停止しました。')

except Exception, e:
    print('エラー: ' + str(e))
    exit(exitcode=1)
"@

# 一時ファイルに保存
$TempScript = "$env:TEMP\stop_weblogic.py"
Set-Content -Path $TempScript -Value $WlstScript -Encoding UTF8

try {
    # WLSTを実行
    Push-Location "$OracleHome\wlserver\common\bin"

    & .\wlst.cmd $TempScript

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "エラー: AdminServerの停止に失敗しました。" -ForegroundColor Red
        Write-Host ""
        Write-Host "手動で停止する方法:" -ForegroundColor Yellow
        Write-Host "  1. タスクマネージャーでjava.exeプロセスを確認" -ForegroundColor White
        Write-Host "  2. WebLogicのプロセスを終了" -ForegroundColor White
        exit 1
    }
}
finally {
    Pop-Location

    # 一時ファイルを削除
    if (Test-Path $TempScript) {
        Remove-Item $TempScript -Force
    }
}

Write-Host ""
Write-Host "======================================"
Write-Host "AdminServerが停止しました"
Write-Host "======================================"
Write-Host ""
