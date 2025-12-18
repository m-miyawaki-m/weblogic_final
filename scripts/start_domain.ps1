# WebLogic ドメイン起動スクリプト
# このスクリプトは、作成されたWebLogicドメインのAdminServerを起動します。

# ==========================================
# 設定
# ==========================================

$DomainHome = "C:\Oracle\Middleware\user_projects\domains\base_domain"
$AdminServerName = "AdminServer"
$ConsoleUrl = "http://localhost:7001/console"

# ==========================================
# 前提条件チェック
# ==========================================

Write-Host "======================================"
Write-Host "WebLogic ドメイン起動スクリプト"
Write-Host "======================================"
Write-Host ""

Write-Host "ドメインをチェック中..." -ForegroundColor Cyan

if (-not (Test-Path $DomainHome)) {
    Write-Host "エラー: ドメインが見つかりません。" -ForegroundColor Red
    Write-Host "パス: $DomainHome" -ForegroundColor Red
    Write-Host ""
    Write-Host "先にドメインを作成してください:" -ForegroundColor Yellow
    Write-Host "  .\scripts\create_domain.ps1" -ForegroundColor White
    exit 1
}

Write-Host "  ✓ ドメイン確認: $DomainHome" -ForegroundColor Green

if (-not (Test-Path "$DomainHome\bin\startWebLogic.cmd")) {
    Write-Host "エラー: 起動スクリプトが見つかりません。" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ 起動スクリプト確認" -ForegroundColor Green
Write-Host ""

# ==========================================
# AdminServerの起動確認
# ==========================================

Write-Host "AdminServerの状態をチェック中..." -ForegroundColor Cyan

# ポート7001が使用中かチェック
$PortCheck = netstat -ano | findstr ":7001"

if ($PortCheck) {
    Write-Host "警告: ポート7001は既に使用されています。" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "使用中のプロセス:" -ForegroundColor Yellow

    # プロセス情報を表示
    $Processes = netstat -ano | findstr ":7001" | ForEach-Object {
        if ($_ -match '\s+(\d+)$') {
            $pid = $matches[1]
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                "  PID: $pid - $($process.ProcessName)"
            }
        }
    } | Select-Object -Unique

    $Processes | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }

    Write-Host ""
    $response = Read-Host "AdminServerは既に起動している可能性があります。続行しますか? (y/N)"

    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "処理を中止しました。" -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "  ✓ ポート7001は利用可能です。" -ForegroundColor Green
}

Write-Host ""

# ==========================================
# AdminServerの起動
# ==========================================

Write-Host "AdminServerを起動中..." -ForegroundColor Cyan
Write-Host "これには数分かかる場合があります..." -ForegroundColor Yellow
Write-Host ""

Write-Host "起動情報:" -ForegroundColor Cyan
Write-Host "  ドメイン: base_domain" -ForegroundColor White
Write-Host "  サーバー: $AdminServerName" -ForegroundColor White
Write-Host "  ポート: 7001" -ForegroundColor White
Write-Host "  管理コンソール: $ConsoleUrl" -ForegroundColor White
Write-Host ""

Write-Host "--------------------------------------" -ForegroundColor Gray
Write-Host "ログ出力:" -ForegroundColor Gray
Write-Host "--------------------------------------" -ForegroundColor Gray
Write-Host ""

# AdminServerを起動
Push-Location $DomainHome\bin

try {
    # startWebLogic.cmdを実行
    & .\startWebLogic.cmd

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "エラー: AdminServerの起動に失敗しました。" -ForegroundColor Red
        Write-Host "終了コード: $LASTEXITCODE" -ForegroundColor Red
        Write-Host ""
        Write-Host "ログを確認してください:" -ForegroundColor Yellow
        Write-Host "  $DomainHome\servers\$AdminServerName\logs\$AdminServerName.log" -ForegroundColor White
        exit 1
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "======================================"
Write-Host "AdminServerが起動しました"
Write-Host "======================================"
Write-Host ""
Write-Host "管理コンソールにアクセス:" -ForegroundColor Cyan
Write-Host "  URL: $ConsoleUrl" -ForegroundColor White
Write-Host "  ユーザー名: weblogic" -ForegroundColor White
Write-Host "  パスワード: welcome1" -ForegroundColor White
Write-Host ""
