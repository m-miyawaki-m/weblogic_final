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

### 複数のデータソースの設定

[scripts/create_domain_final.py](../scripts/create_domain_final.py) を編集:

```python
# Database configuration (multiple datasources)
DATASOURCES = [
    {
        'name': 'ProductionDS',
        'jndi': 'jdbc/ProductionDS',
        'url': 'jdbc:oracle:thin:@prod-server:1521:PROD',
        'user': 'produser',
        'password': 'prodpass',
        'driver': 'oracle.jdbc.OracleDriver',
        'initial_capacity': 5,
        'max_capacity': 50,
        'min_capacity': 5
    },
    {
        'name': 'ReportingDS',
        'jndi': 'jdbc/ReportingDS',
        'url': 'jdbc:oracle:thin:@report-server:1521:REPORT',
        'user': 'reportuser',
        'password': 'reportpass',
        'driver': 'oracle.jdbc.OracleDriver',
        'initial_capacity': 2,
        'max_capacity': 20,
        'min_capacity': 2
    }
]
```

各データソースには以下のプロパティを設定できます:
- `name`: データソース名
- `jndi`: JNDI名
- `url`: データベース接続URL
- `user`: データベースユーザー名
- `password`: データベースパスワード
- `driver`: JDBCドライバークラス名
- `initial_capacity`: 初期接続数
- `max_capacity`: 最大接続数
- `min_capacity`: 最小接続数

### データベース接続の変更（単一データソースの場合）

```python
DATASOURCES = [
    {
        'name': 'MyDS',
        'jndi': 'jdbc/MyDS',
        'url': 'jdbc:oracle:thin:@myhost:1521:MYDB',
        'user': 'myuser',
        'password': 'mypassword',
        'driver': 'oracle.jdbc.OracleDriver',
        'initial_capacity': 1,
        'max_capacity': 15,
        'min_capacity': 1
    }
]
```

### MySQLを使用する場合

```python
DATASOURCES = [
    {
        'name': 'MySQLDS',
        'jndi': 'jdbc/MySQLDS',
        'url': 'jdbc:mysql://localhost:3306/mydb?useSSL=false',
        'user': 'root',
        'password': 'password',
        'driver': 'com.mysql.cj.jdbc.Driver',
        'initial_capacity': 1,
        'max_capacity': 15,
        'min_capacity': 1
    }
]
```

**注意:** MySQL JDBCドライバーをダウンロードして配置してください。

### PostgreSQLを使用する場合

```python
DATASOURCES = [
    {
        'name': 'PostgreSQLDS',
        'jndi': 'jdbc/PostgreSQLDS',
        'url': 'jdbc:postgresql://localhost:5432/mydb',
        'user': 'postgres',
        'password': 'password',
        'driver': 'org.postgresql.Driver',
        'initial_capacity': 1,
        'max_capacity': 15,
        'min_capacity': 1
    }
]
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

### JVM起動パラメータの設定

#### メモリ設定の変更

```python
JVM_ARGS = {
    'memory': {
        'min_heap': '1024m',     # 最小ヒープサイズ (-Xms)
        'max_heap': '4096m',     # 最大ヒープサイズ (-Xmx)
        'min_perm': '512m',      # 最小PermGenサイズ (-XX:PermSize) ※Java 7以前
        'max_perm': '1024m'      # 最大PermGenサイズ (-XX:MaxPermSize) ※Java 7以前
    },
    # 他の設定は省略...
}
```

**推奨設定:**
- 開発環境: Xms=512m, Xmx=2048m
- 本番環境（小規模）: Xms=2048m, Xmx=4096m
- 本番環境（大規模）: Xms=4096m, Xmx=8192m

**注意:** Java 8以降では、PermSizeの代わりにMetaspaceSize/MaxMetaspaceSizeを使用します。

#### GC（ガベージコレクション）オプションの変更

```python
JVM_ARGS = {
    # memory設定は省略...
    'gc_options': [
        '-XX:+UseG1GC',                          # G1GCを使用
        '-XX:MaxGCPauseMillis=200',              # GC停止時間の目標
        '-XX:+PrintGCDetails',                   # GC詳細ログ出力
        '-XX:+PrintGCDateStamps',                # GCログにタイムスタンプ追加
        '-Xloggc:${DOMAIN_HOME}/logs/gc.log',    # GCログファイル
        '-XX:+UseGCLogFileRotation',             # GCログローテーション
        '-XX:NumberOfGCLogFiles=5',              # ログファイル数
        '-XX:GCLogFileSize=10M'                  # ログファイルサイズ
    ],
    # 他の設定は省略...
}
```

**GCアルゴリズムの選択:**

**G1GC（推奨 - Java 8以降）:**
```python
'-XX:+UseG1GC',
'-XX:MaxGCPauseMillis=200',
```

**ParallelGC（スループット重視）:**
```python
'-XX:+UseParallelGC',
'-XX:ParallelGCThreads=4',
```

**CMS GC（低レイテンシ重視 - Java 8）:**
```python
'-XX:+UseConcMarkSweepGC',
'-XX:+CMSParallelRemarkEnabled',
```

#### システムプロパティの追加

```python
JVM_ARGS = {
    # memory, gc_optionsは省略...
    'system_properties': {
        # SSL検証をスキップ（開発環境のみ）
        'weblogic.security.SSL.ignoreHostnameVerification': 'true',

        # ランダム数生成の高速化
        'java.security.egd': 'file:/dev/./urandom',

        # 設定ファイルディレクトリ
        'config.dir': '${DOMAIN_HOME}/config',

        # カスタムプロパティの例
        'app.environment': 'production',
        'app.log.level': 'INFO',
        'file.encoding': 'UTF-8',

        # タイムゾーン設定
        'user.timezone': 'Asia/Tokyo'
    },
    # 他の設定は省略...
}
```

**よく使用されるシステムプロパティ:**
- `file.encoding`: ファイルエンコーディング（UTF-8推奨）
- `user.timezone`: タイムゾーン設定
- `java.net.preferIPv4Stack`: IPv4を優先（true/false）
- `weblogic.security.SSL.*`: SSL/TLS関連設定

#### クラスパスの追加

```python
JVM_ARGS = {
    # memory, gc_options, system_propertiesは省略...
    'classpath': [
        '${DOMAIN_HOME}/lib/custom.jar',        # カスタムJARファイル
        '${DOMAIN_HOME}/lib/external/*',        # 外部ライブラリディレクトリ
        'C:/shared/lib/common.jar',             # 共有ライブラリ
    ]
}
```

**使用例:**
1. カスタムライブラリの配置:
   ```powershell
   mkdir C:\Oracle\Middleware\user_projects\domains\base_domain\lib
   Copy-Item my-library.jar C:\Oracle\Middleware\user_projects\domains\base_domain\lib\
   ```

2. クラスパスに追加:
   ```python
   'classpath': [
       '${DOMAIN_HOME}/lib/my-library.jar'
   ]
   ```

#### 完全な設定例

```python
# Server startup parameters
JVM_ARGS = {
    'memory': {
        'min_heap': '2048m',
        'max_heap': '4096m',
        # Java 8以降ではPermSizeは不要
    },
    'gc_options': [
        '-XX:+UseG1GC',
        '-XX:MaxGCPauseMillis=200',
        '-XX:+PrintGCDetails',
        '-XX:+PrintGCDateStamps',
        '-Xloggc:${DOMAIN_HOME}/logs/gc.log',
        '-XX:+UseGCLogFileRotation',
        '-XX:NumberOfGCLogFiles=5',
        '-XX:GCLogFileSize=10M'
    ],
    'system_properties': {
        'file.encoding': 'UTF-8',
        'user.timezone': 'Asia/Tokyo',
        'config.dir': '${DOMAIN_HOME}/config',
        'app.environment': 'production'
    },
    'classpath': [
        '${DOMAIN_HOME}/lib/custom.jar'
    ]
}
```

### 設定ファイルディレクトリの使用

スクリプト実行時に自動的に `${DOMAIN_HOME}/config` ディレクトリが作成されます。

**設定ファイルの配置例:**

1. アプリケーション設定ファイル:
   ```powershell
   # application.propertiesを配置
   Copy-Item application.properties C:\Oracle\Middleware\user_projects\domains\base_domain\config\
   ```

2. アプリケーションから参照:
   ```java
   String configDir = System.getProperty("config.dir");
   String configFile = configDir + "/application.properties";
   Properties props = new Properties();
   props.load(new FileInputStream(configFile));
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
