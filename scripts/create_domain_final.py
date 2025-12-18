# WebLogic Domain Creation using WLST
# This script creates a WebLogic domain with DataSource and JMS configuration

import os
import sys

# Configuration
DOMAIN_NAME = 'base_domain'
DOMAIN_HOME = 'C:/Oracle/Middleware/user_projects/domains/base_domain'
ADMIN_USERNAME = 'weblogic'
ADMIN_PASSWORD = 'welcome1'
ADMIN_PORT = 7001

# Database configuration (multiple datasources)
DATASOURCES = [
    {
        'name': 'TestDS',
        'jndi': 'jdbc/TestDS',
        'url': 'jdbc:oracle:thin:@localhost:1521:ORCL',
        'user': 'scott',
        'password': 'tiger',
        'driver': 'oracle.jdbc.OracleDriver',
        'initial_capacity': 1,
        'max_capacity': 15,
        'min_capacity': 1
    },
    # Add more datasources here as needed
    # {
    #     'name': 'TestDS2',
    #     'jndi': 'jdbc/TestDS2',
    #     'url': 'jdbc:oracle:thin:@localhost:1521:ORCL2',
    #     'user': 'user2',
    #     'password': 'password2',
    #     'driver': 'oracle.jdbc.OracleDriver',
    #     'initial_capacity': 1,
    #     'max_capacity': 10,
    #     'min_capacity': 1
    # },
]

# JMS configuration
JMS_SERVER_NAME = 'TestJMSServer'
JMS_MODULE_NAME = 'TestJMSModule'
JMS_SUBDEPLOYMENT_NAME = 'TestSubDeployment'
JMS_CF_NAME = 'TestConnectionFactory'
JMS_CF_JNDI = 'jms/TestConnectionFactory'
JMS_QUEUE_NAME = 'TestQueue'
JMS_QUEUE_JNDI = 'jms/TestQueue'

# Server startup parameters
JVM_ARGS = {
    'memory': {
        'min_heap': '512m',      # -Xms
        'max_heap': '2048m',     # -Xmx
        'min_perm': '256m',      # -XX:PermSize (for Java 7)
        'max_perm': '512m'       # -XX:MaxPermSize (for Java 7)
    },
    'gc_options': [
        '-XX:+UseG1GC',
        '-XX:MaxGCPauseMillis=200',
        '-XX:+PrintGCDetails',
        '-XX:+PrintGCDateStamps',
        '-Xloggc:${DOMAIN_HOME}/logs/gc.log'
    ],
    'system_properties': {
        'weblogic.security.SSL.ignoreHostnameVerification': 'true',
        'java.security.egd': 'file:/dev/./urandom',
        'config.dir': '${DOMAIN_HOME}/config'  # Configuration file directory
    },
    'classpath': [
        # Add additional JAR files or directories here
        # '${DOMAIN_HOME}/lib/custom.jar',
        # '${DOMAIN_HOME}/lib/external/*'
    ]
}

print('========================================')
print('WebLogic Domain Creation Script (WLST)')
print('========================================')
print('')

# Read domain template
print('[1/5] Reading domain template...')
readTemplate('C:/Oracle/Middleware/Oracle_Home/wlserver/common/templates/wls/wls.jar')
print('  [OK] Template loaded')
print('')

# Configure Admin Server
print('[2/5] Configuring AdminServer...')
cd('/')
cd('Servers/AdminServer')
set('ListenAddress', '0.0.0.0')
set('ListenPort', ADMIN_PORT)

# Configure JVM arguments
print('  Configuring JVM arguments...')
create('AdminServer', 'ServerStart')
cd('ServerStart/AdminServer')

# Build JVM arguments string
jvm_args_list = []

# Memory settings
jvm_args_list.append('-Xms' + JVM_ARGS['memory']['min_heap'])
jvm_args_list.append('-Xmx' + JVM_ARGS['memory']['max_heap'])
# Note: PermSize is for Java 7 and earlier. Java 8+ uses MetaspaceSize
if JVM_ARGS['memory'].get('min_perm'):
    jvm_args_list.append('-XX:PermSize=' + JVM_ARGS['memory']['min_perm'])
if JVM_ARGS['memory'].get('max_perm'):
    jvm_args_list.append('-XX:MaxPermSize=' + JVM_ARGS['memory']['max_perm'])

# GC options
jvm_args_list.extend(JVM_ARGS['gc_options'])

# System properties
for key, value in JVM_ARGS['system_properties'].items():
    jvm_args_list.append('-D' + key + '=' + value)

# Set arguments
arguments = ' '.join(jvm_args_list)
set('Arguments', arguments)

# Set classpath if specified
if JVM_ARGS['classpath']:
    classpath = ';'.join(JVM_ARGS['classpath'])  # Windows uses ';', Unix uses ':'
    set('ClassPath', classpath)

print('  [OK] JVM arguments configured')

# Set admin credentials
cd('/')
cd('Security/base_domain/User/weblogic')
cmo.setPassword(ADMIN_PASSWORD)
print('  [OK] AdminServer configured')
print('')

# Set domain options
print('[3/5] Setting domain options...')
setOption('DomainName', DOMAIN_NAME)
setOption('JavaHome', 'C:/Program Files/Java/jdk-21')
setOption('ServerStartMode', 'prod')
print('  [OK] Domain options set')
print('')

# Write domain
print('[4/5] Writing domain...')
writeDomain(DOMAIN_HOME)
closeTemplate()
print('  [OK] Domain written to: ' + DOMAIN_HOME)

# Create configuration directory
config_dir = DOMAIN_HOME + '/config'
if not os.path.exists(config_dir):
    os.makedirs(config_dir)
    print('  [OK] Configuration directory created: ' + config_dir)
else:
    print('  [OK] Configuration directory exists: ' + config_dir)
print('')

# Configure DataSource and JMS
print('[5/5] Configuring DataSource and JMS...')
readDomain(DOMAIN_HOME)

# Create DataSources
for ds in DATASOURCES:
    print('  Creating DataSource: ' + ds['name'] + '...')
    cd('/')
    create(ds['name'], 'JDBCSystemResource')
    cd('/JDBCSystemResource/' + ds['name'] + '/JdbcResource/' + ds['name'])
    create('myJdbcDataSourceParams','JDBCDataSourceParams')
    cd('JDBCDataSourceParams/NO_NAME_0')
    set('JNDIName', ds['jndi'])
    set('GlobalTransactionsProtocol', 'TwoPhaseCommit')

    cd('/JDBCSystemResource/' + ds['name'] + '/JdbcResource/' + ds['name'])
    create('myJdbcDriverParams','JDBCDriverParams')
    cd('JDBCDriverParams/NO_NAME_0')
    set('DriverName', ds['driver'])
    set('URL', ds['url'])
    set('PasswordEncrypted', ds['password'])
    set('UseXADataSourceInterface', 'false')

    print('    Setting Properties')
    create('myProperties','Properties')
    cd('Properties/NO_NAME_0')
    create('user', 'Property')
    cd('Property/user')
    set('Value', ds['user'])

    cd('/JDBCSystemResource/' + ds['name'] + '/JdbcResource/' + ds['name'])
    create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
    cd('JDBCConnectionPoolParams/NO_NAME_0')
    set('InitialCapacity', ds['initial_capacity'])
    set('MaxCapacity', ds['max_capacity'])
    set('MinCapacity', ds['min_capacity'])
    set('TestTableName', 'SQL SELECT 1 FROM DUAL')
    set('TestConnectionsOnReserve', 1)

    cd('/JDBCSystemResource/' + ds['name'])
    set('Target', 'AdminServer')
    print('  [OK] DataSource ' + ds['name'] + ' created')

print('  [OK] All DataSources created (' + str(len(DATASOURCES)) + ' total)')

# Create JMS Server
print('  Creating JMS Server: ' + JMS_SERVER_NAME + '...')
cd('/')
create(JMS_SERVER_NAME, 'JMSServer')
cd('/JMSServer/' + JMS_SERVER_NAME)
set('Target', 'AdminServer')
print('  [OK] JMS Server created')

# Create JMS Module
print('  Creating JMS Module: ' + JMS_MODULE_NAME + '...')
cd('/')
create(JMS_MODULE_NAME, 'JMSSystemResource')
cd('/JMSSystemResource/' + JMS_MODULE_NAME)
set('Target', 'AdminServer')

# Create SubDeployment
create(JMS_SUBDEPLOYMENT_NAME, 'SubDeployment')
cd('/JMSSystemResource/' + JMS_MODULE_NAME + '/SubDeployment/' + JMS_SUBDEPLOYMENT_NAME)
set('Target', JMS_SERVER_NAME)

# Create Connection Factory
cd('/JMSSystemResource/' + JMS_MODULE_NAME + '/JmsResource/NO_NAME_0')
create(JMS_CF_NAME, 'ConnectionFactory')
cd('ConnectionFactory/' + JMS_CF_NAME)
set('JNDIName', JMS_CF_JNDI)
set('SubDeploymentName', JMS_SUBDEPLOYMENT_NAME)

# Create Queue
cd('/JMSSystemResource/' + JMS_MODULE_NAME + '/JmsResource/NO_NAME_0')
create(JMS_QUEUE_NAME, 'Queue')
cd('Queue/' + JMS_QUEUE_NAME)
set('JNDIName', JMS_QUEUE_JNDI)
set('SubDeploymentName', JMS_SUBDEPLOYMENT_NAME)
print('  [OK] JMS Module created')

# Update domain
updateDomain()
closeDomain()
print('  [OK] Domain configuration updated')
print('')

print('========================================')
print('Domain Creation Complete!')
print('========================================')
print('')
print('Domain Information:')
print('  Domain Name: ' + DOMAIN_NAME)
print('  Domain Path: ' + DOMAIN_HOME)
print('  AdminServer Port: ' + str(ADMIN_PORT))
print('  Console URL: http://localhost:' + str(ADMIN_PORT) + '/console')
print('  Config Directory: ' + DOMAIN_HOME + '/config')
print('')
print('JVM Configuration:')
print('  Min Heap: ' + JVM_ARGS['memory']['min_heap'])
print('  Max Heap: ' + JVM_ARGS['memory']['max_heap'])
print('  GC Type: G1GC')
print('  GC Log: ' + DOMAIN_HOME + '/logs/gc.log')
print('')
print('DataSources Created: ' + str(len(DATASOURCES)))
for ds in DATASOURCES:
    print('  - ' + ds['name'] + ' (' + ds['jndi'] + ')')
print('')
print('Next Steps:')
print('  1. Place configuration files in: ' + DOMAIN_HOME + '/config')
print('')
print('  2. Start AdminServer:')
print('     cd ' + DOMAIN_HOME)
print('     .\\bin\\startWebLogic.cmd')
print('')
print('  3. Access admin console:')
print('     URL: http://localhost:' + str(ADMIN_PORT) + '/console')
print('     Username: ' + ADMIN_USERNAME)
print('     Password: ' + ADMIN_PASSWORD)
print('')

exit()
