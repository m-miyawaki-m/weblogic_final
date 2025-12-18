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
print('')
print('Next Steps:')
print('  1. Start AdminServer:')
print('     cd ' + DOMAIN_HOME)
print('     .\\bin\\startWebLogic.cmd')
print('')
print('  2. Access admin console:')
print('     URL: http://localhost:' + str(ADMIN_PORT) + '/console')
print('     Username: ' + ADMIN_USERNAME)
print('     Password: ' + ADMIN_PASSWORD)
print('')

exit()
