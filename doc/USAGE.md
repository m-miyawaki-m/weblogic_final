# WebLogic ドメイン作成ツール - 使用方法

このドキュメントでは、WebLogicドメイン作成ツールの詳細な使用方法を説明します。

---

## 📋 目次

1. [基本的な使い方](#基本的な使い方)
2. [設定のカスタマイズ](#設定のカスタマイズ)
3. [トラブルシューティング](#トラブルシューティング)
4. [応用例](#応用例)

---

## 基本的な使い方

### 1. ドメインの作成

```powershell
cd c:\dev\weblogic_final
.\scripts\create_domain_final.ps1
```

**実行結果:**

```
======================================
WebLogic Domain Creation Script (WLST)
======================================

[1/5] Reading domain template...
  [OK] Template loaded

[2/5] Configuring AdminServer...
  [OK] AdminServer configured

[3/5] Setting domain options...
  [OK] Domain options set

[4/5] Writing domain...
  [OK] Domain written to: C:/Oracle/Middleware/user_projects/domains/base_domain

[5/5] Configuring DataSource and JMS...
  Creating DataSource: TestDS...
  [OK] DataSource created
  Creating JMS Server: TestJMSServer...
  [OK] JMS Server created
  Creating JMS Module: TestJMSModule...
  [OK] JMS Module created

========================================
Domain Creation Complete!
========================================
```

### 2. ドメインの起動

**方法A: スクリプトを使用**

```powershell
.\scripts\start_domain.ps1
```

**方法B: 手動で起動**

```powershell
cd C:\Oracle\Middleware\user_projects\domains\base_domain
.\startWebLogic.cmd
```

初回起動時は、ユーザー名とパスワードを入力:
```
Enter username to boot WebLogic server: weblogic
Enter password to boot WebLogic server: welcome1
```

### 3. 管理コンソールへのアクセス

ブラウザで以下にアクセス:

```
http://localhost:7001/console
```

**ログイン:**
- ユーザー名: `weblogic`
- パスワード: `welcome1`

### 4. 設定の確認

#### データソースの確認

1. 管理コンソールにログイン
2. 左メニュー: **サービス** → **データ・ソース**
3. `TestDS` をクリック
4. **監視** → **テスト** タブでデータベース接続をテスト

#### JMS設定の確認

1. 管理コンソールにログイン
2. 左メニュー: **サービス** → **メッセージング** → **JMS モジュール**
3. `TestJMSModule` をクリック
4. キュー `TestQueue` を確認

### 5. ドメインの停止

**方法A: スクリプトを使用**

```powershell
.\scripts\stop_domain.ps1
```

**方法B: 手動で停止**

AdminServerのコンソールで `Ctrl+C` を押す

---

## 設定のカスタマイズ

### データベース接続の変更

[scripts/create_domain_final.py](../scripts/create_domain_final.py) を編集:

```python
# Database configuration
JDBC_NAME = 'MyDS'                 # データソース名
JDBC_JNDI = 'jdbc/MyDS'           # JNDI名
JDBC_URL = 'jdbc:oracle:thin:@myhost:1521:MYDB'  # 接続URL
JDBC_USER = 'myuser'              # ユーザー名
JDBC_PASSWORD = 'mypassword'      # パスワード
JDBC_DRIVER = 'oracle.jdbc.OracleDriver'
```

### MySQLを使用する場合

```python
JDBC_URL = 'jdbc:mysql://localhost:3306/mydb?useSSL=false'
JDBC_USER = 'root'
JDBC_PASSWORD = 'password'
JDBC_DRIVER = 'com.mysql.cj.jdbc.Driver'
```

**注意:** MySQL JDBCドライバーをダウンロードして配置してください。

### PostgreSQLを使用する場合

```python
JDBC_URL = 'jdbc:postgresql://localhost:5432/mydb'
JDBC_USER = 'postgres'
JDBC_PASSWORD = 'password'
JDBC_DRIVER = 'org.postgresql.Driver'
```

### ポート番号の変更

```python
ADMIN_PORT = 8001  # 7001から8001に変更
```

### ドメイン名とパスの変更

```python
DOMAIN_NAME = 'my_domain'
DOMAIN_HOME = 'C:/Oracle/Middleware/user_projects/domains/my_domain'
```

### 管理ユーザーの変更

```python
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'MySecurePassword123!'
```

### JMS設定の変更

```python
JMS_SERVER_NAME = 'MyJMSServer'
JMS_MODULE_NAME = 'MyJMSModule'
JMS_CF_NAME = 'MyConnectionFactory'
JMS_CF_JNDI = 'jms/MyConnectionFactory'
JMS_QUEUE_NAME = 'MyQueue'
JMS_QUEUE_JNDI = 'jms/MyQueue'
```

---

## トラブルシューティング

### ドメイン作成が失敗する

**症状:** スクリプトがエラーで終了する

**確認事項:**

1. **WebLogicがインストールされているか:**
   ```powershell
   Test-Path "C:\Oracle\Middleware\Oracle_Home\wlserver"
   ```

2. **WLSTが存在するか:**
   ```powershell
   Test-Path "C:\Oracle\Middleware\Oracle_Home\wlserver\common\bin\wlst.cmd"
   ```

3. **ドメインディレクトリが既に存在していないか:**
   ```powershell
   Test-Path "C:\Oracle\Middleware\user_projects\domains\base_domain"
   ```

**対処:**

既存のドメインを削除:
```powershell
Remove-Item -Recurse -Force C:\Oracle\Middleware\user_projects\domains\base_domain
```

### AdminServerが起動しない

**症状:** `startWebLogic.cmd` を実行してもサーバーが起動しない

**確認事項:**

1. **ポート7001が使用中でないか:**
   ```powershell
   netstat -ano | findstr :7001
   ```

2. **Java_HOMEが設定されているか:**
   ```powershell
   $env:JAVA_HOME
   ```

**対処:**

ポートを使用中のプロセスを終了:
```powershell
taskkill /PID <PID> /F
```

### 管理コンソールにアクセスできない

**症状:** `http://localhost:7001/console` にアクセスできない

**確認事項:**

1. **AdminServerが起動しているか:**
   ```powershell
   netstat -ano | findstr :7001
   ```

2. **ファイアウォールでブロックされていないか**

**対処:**

ログを確認:
```powershell
Get-Content "C:\Oracle\Middleware\user_projects\domains\base_domain\servers\AdminServer\logs\AdminServer.log" -Tail 50
```

### データソース接続テストが失敗

**症状:** 管理コンソールでデータソースのテストが失敗する

**確認事項:**

1. **データベースが起動しているか**
2. **接続情報が正しいか**
3. **JDBCドライバーが配置されているか**

**対処:**

1. データベースを起動
2. `create_domain_final.py` の接続情報を確認
3. JDBCドライバーをダウンロードして配置:
   ```powershell
   # ドライバーを配置
   Copy-Item "ojdbc8.jar" "C:\Oracle\Middleware\user_projects\domains\base_domain\lib\"

   # AdminServerを再起動
   ```

---

## 応用例

### 複数のデータソースを作成

`create_domain_final.py` に以下を追加:

```python
# Create second DataSource
print('  Creating DataSource: TestDS2...')
cd('/')
create('TestDS2', 'JDBCSystemResource')
cd('/JDBCSystemResource/TestDS2/JdbcResource/TestDS2')
create('myJdbcDataSourceParams','JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', 'jdbc/TestDS2')

cd('/JDBCSystemResource/TestDS2/JdbcResource/TestDS2')
create('myJdbcDriverParams','JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('DriverName', 'oracle.jdbc.OracleDriver')
set('URL', 'jdbc:oracle:thin:@localhost:1521:ORCL2')
set('PasswordEncrypted', 'tiger')

create('myProperties','Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
set('Value', 'scott')

cd('/JDBCSystemResource/TestDS2')
set('Target', 'AdminServer')
print('  [OK] DataSource created')
```

### 複数のJMSキューを作成

`create_domain_final.py` に以下を追加:

```python
# Create additional queues
cd('/JMSSystemResource/' + JMS_MODULE_NAME + '/JmsResource/NO_NAME_0')

# Priority Queue
create('PriorityQueue', 'Queue')
cd('Queue/PriorityQueue')
set('JNDIName', 'jms/PriorityQueue')
set('SubDeploymentName', JMS_SUBDEPLOYMENT_NAME)

# Dead Letter Queue
cd('/JMSSystemResource/' + JMS_MODULE_NAME + '/JmsResource/NO_NAME_0')
create('DeadLetterQueue', 'Queue')
cd('Queue/DeadLetterQueue')
set('JNDIName', 'jms/DeadLetterQueue')
set('SubDeploymentName', JMS_SUBDEPLOYMENT_NAME)
```

### JMSトピックを作成

```python
# Create Topic
cd('/JMSSystemResource/' + JMS_MODULE_NAME + '/JmsResource/NO_NAME_0')
create('TestTopic', 'Topic')
cd('Topic/TestTopic')
set('JNDIName', 'jms/TestTopic')
set('SubDeploymentName', JMS_SUBDEPLOYMENT_NAME)
```

---

## スクリプトの再実行

ドメインを再作成する場合:

```powershell
# 1. ドメインを停止
.\scripts\stop_domain.ps1

# 2. 既存のドメインを削除
Remove-Item -Recurse -Force C:\Oracle\Middleware\user_projects\domains\base_domain

# 3. ドメインを再作成
.\scripts\create_domain_final.ps1

# 4. ドメインを起動
.\scripts\start_domain.ps1
```

---

## まとめ

このツールを使用すると、WebLogicドメインの作成が簡単に自動化できます。

**ポイント:**
- ✅ WLST (WebLogic標準ツール) を使用
- ✅ データソースとJMS設定を自動作成
- ✅ カスタマイズが簡単
- ✅ 再現性が高い

詳細な情報は [README.md](../README.md) を参照してください。
