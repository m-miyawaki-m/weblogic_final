# WebLogic ドメイン作成ツール

このプロジェクトは、WebLogic Serverのドメインを自動作成するためのスクリプトを提供します。

---

## 📋 概要

WebLogic Scripting Tool (WLST) を使用して、以下を自動的に作成します:

- ✅ WebLogicドメイン (`base_domain`)
- ✅ AdminServer (ポート 7001)
- ✅ データソース (`TestDS`)
- ✅ JMSサーバー (`TestJMSServer`)
- ✅ JMS接続ファクトリとキュー

---

## 📁 ファイル構成

```
weblogic_final/
├── scripts/
│   ├── create_domain_final.ps1    # ドメイン作成スクリプト
│   ├── create_domain_final.py     # WLSTのPythonスクリプト
│   ├── start_domain.ps1           # ドメイン起動スクリプト
│   └── stop_domain.ps1            # ドメイン停止スクリプト
├── doc/
│   └── USAGE.md                   # 使用方法
└── README.md                      # このファイル
```

---

## 🚀 クイックスタート

### 前提条件

- WebLogic Server 14.1.1.0.0 がインストール済み
- インストールパス: `C:\Oracle\Middleware\Oracle_Home`
- Java 11 以上

### ステップ1: ドメインの作成

```powershell
cd c:\dev\weblogic_final
.\scripts\create_domain_final.ps1
```

### ステップ2: AdminServerの起動

```powershell
.\scripts\start_domain.ps1
```

または手動で:

```powershell
cd C:\Oracle\Middleware\user_projects\domains\base_domain
.\startWebLogic.cmd
```

### ステップ3: 管理コンソールへのアクセス

ブラウザで以下にアクセス:

```
http://localhost:7001/console
```

**ログイン情報:**
- ユーザー名: `weblogic`
- パスワード: `welcome1`

---

## 🎯 作成される設定

### ドメイン構成

| 項目 | 設定値 |
|------|--------|
| ドメイン名 | `base_domain` |
| ドメインパス | `C:\Oracle\Middleware\user_projects\domains\base_domain` |
| AdminServerポート | 7001 |
| 管理ユーザー | `weblogic` / `welcome1` |

### データソース

| 項目 | 設定値 |
|------|--------|
| 名前 | `TestDS` |
| JNDI名 | `jdbc/TestDS` |
| URL | `jdbc:oracle:thin:@localhost:1521:ORCL` |
| ユーザー | `scott` |
| パスワード | `tiger` |
| ドライバー | `oracle.jdbc.OracleDriver` |
| 接続プール | 初期1、最小1、最大15 |

### JMS構成

| リソース | 名前 | JNDI名 |
|---------|------|--------|
| JMSサーバー | `TestJMSServer` | - |
| JMSモジュール | `TestJMSModule` | - |
| 接続ファクトリ | `TestConnectionFactory` | `jms/TestConnectionFactory` |
| キュー | `TestQueue` | `jms/TestQueue` |

---

## ⚙️ カスタマイズ

設定を変更する場合は、[scripts/create_domain_final.py](scripts/create_domain_final.py) を編集してください。

### データベース接続の変更

```python
# Database configuration
JDBC_URL = 'jdbc:oracle:thin:@localhost:1521:ORCL'
JDBC_USER = 'scott'
JDBC_PASSWORD = 'tiger'
JDBC_DRIVER = 'oracle.jdbc.OracleDriver'
```

### ポート番号の変更

```python
# Configuration
ADMIN_PORT = 7001
```

### ドメイン名の変更

```python
# Configuration
DOMAIN_NAME = 'base_domain'
DOMAIN_HOME = 'C:/Oracle/Middleware/user_projects/domains/base_domain'
```

---

## 🔧 スクリプトの詳細

### create_domain_final.ps1

WLSTを呼び出してドメインを作成するPowerShellラッパースクリプト。

**実行:**
```powershell
.\scripts\create_domain_final.ps1
```

### create_domain_final.py

WLSTのPythonスクリプト。ドメイン、データソース、JMS設定を作成します。

**このスクリプトは create_domain_final.ps1 から自動的に呼び出されます。**

### start_domain.ps1

ドメインを起動するスクリプト。

**実行:**
```powershell
.\scripts\start_domain.ps1
```

### stop_domain.ps1

ドメインを停止するスクリプト。

**実行:**
```powershell
.\scripts\stop_domain.ps1
```

---

## ❓ トラブルシューティング

### ドメインが既に存在する

**エラー:** "Domain directory already exists"

**対処:**
```powershell
Remove-Item -Recurse -Force C:\Oracle\Middleware\user_projects\domains\base_domain
.\scripts\create_domain_final.ps1
```

### WLSTが見つからない

**エラー:** "WLST not found at: ..."

**対処:**

1. WebLogicのインストールパスを確認:
   ```powershell
   Get-ChildItem -Path "C:\Oracle\Middleware" -Filter "wlst.cmd" -Recurse
   ```

2. `scripts\create_domain_final.ps1` の `$OracleHome` を修正:
   ```powershell
   $OracleHome = "C:\Oracle\Middleware\Oracle_Home"
   ```

### ポート7001が使用中

**エラー:** "Address already in use"

**対処:**
```powershell
# 使用中のプロセスを確認
netstat -ano | findstr :7001

# プロセスを終了
taskkill /PID <PID> /F
```

### データソースのテストが失敗

**原因:**
- データベースが起動していない
- 接続情報が間違っている
- JDBCドライバーがない

**対処:**
1. データベースが起動しているか確認
2. `scripts\create_domain_final.py` の接続情報を確認
3. Oracle JDBCドライバーをダウンロード
4. ドライバーを `C:\Oracle\Middleware\user_projects\domains\base_domain\lib` にコピー

---

## 📚 参考情報

### WebLogic Server

- **バージョン:** 14.1.1.0.0
- **公式ドキュメント:** https://docs.oracle.com/en/middleware/fusion-middleware/weblogic-server/14.1.1/

### WLST (WebLogic Scripting Tool)

- **公式ドキュメント:** https://docs.oracle.com/en/middleware/fusion-middleware/weblogic-server/14.1.1/wlstc/

---

## 📝 注意事項

### セキュリティ

- デフォルトのパスワード (`welcome1`) は本番環境で使用しないでください
- 本番環境では強固なパスワードに変更してください

### データベース

- このスクリプトはOracleデータベースを想定しています
- 他のデータベースを使用する場合は、JDBCドライバーとURLを変更してください

### JMSの永続化

- JMSメッセージはファイルストアに永続化されます
- パス: `C:\Oracle\Middleware\user_projects\domains\base_domain\jms\filestore`

---

## 🎉 完成!

これで以下が利用可能になりました:

✅ WebLogicドメイン
✅ 管理コンソール (http://localhost:7001/console)
✅ データソース (JNDI: `jdbc/TestDS`)
✅ JMSキュー (JNDI: `jms/TestQueue`)

ドメインの作成から起動まで、すべて自動化されています!
