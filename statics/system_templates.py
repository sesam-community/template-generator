def system_configs(system, config_group):
  if config_group != "Default":
    systems = [{"microservice": {
      "_id": None,
      "type": "system:microservice",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "docker": None,
      "verify_ssl": True
    }, "kafka":
    {
      "_id": None,
      "type": "system:kafka",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "bootstrap_servers": None
    }, "rest": 
    {
      "_id": None,
      "type": "system:rest",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "operations": None,
      "url_pattern": "",
      "verify_ssl": True
    }, "url":
    {
      "_id": None,
      "type": "system:url",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "url_pattern": "",
      "verify_ssl": True
    }, "twilio":
    {
      "_id": None,
      "type": "system:twilio",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "account": None,
      "token": None
    }, "elasticsearch": 
    {
      "_id": None,
      "type": "system:elasticsearch",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "hosts": None
    }, "solr": 
    {
      "_id": None,
      "type": "system:solr",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "url": None
    }, "smtp": 
    {
      "_id": None,
      "type": "system:smtp",
      "metadata": {
        "$config-group": f"{config_group}"
      },
    }, "sqlite":
    {
      "_id": None,
      "type": "system:sqlite",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None
    }, "postgresql": 
    {
      "_id": None,
      "type": "system:postgresql",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "oracle_tns":
    {
      "_id": None,
      "type": "system:oracle_tns",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "password": None,
      "tns_name": None,
      "username": None
    }, "sqlserver": 
    {
      "_id": None,
      "type": "system:sqlserver",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "mssql-azure-dw": 
    {
      "_id": None,
      "type": "system:mssql-azure-dw",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "mssql": 
    {
      "_id": None,
      "type": "system:mssql",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "mysql": 
    {
      "_id": None,
      "type": "system:mysql",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "oracle": 
    {
      "_id": None,
      "type": "system:oracle",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "ldap": 
    {
      "_id": None,
      "type": "system:ldap",
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "host": None,
      "password": None,
      "username": None
    }}]
  else:
    systems = [{"microservice": {
      "_id": None,
      "type": "system:microservice",
      "docker": None,
      "verify_ssl": True
    }, "kafka":
    {
      "_id": None,
      "type": "system:kafka",
      "bootstrap_servers": None
    }, "rest": 
    {
      "_id": None,
      "type": "system:rest",
      "operations": None,
      "url_pattern": "",
      "verify_ssl": True
    }, "url":
    {
      "_id": None,
      "type": "system:url",
      "url_pattern": "",
      "verify_ssl": True
    }, "twilio":
    {
      "_id": None,
      "type": "system:twilio",
      "account": None,
      "token": None
    }, "elasticsearch": 
    {
      "_id": None,
      "type": "system:elasticsearch",
      "hosts": None
    }, "solr": 
    {
      "_id": None,
      "type": "system:solr",
      "url": None
    }, "smtp": 
    {
      "_id": None,
      "type": "system:smtp"
    }, "sqlite":
    {
      "_id": None,
      "type": "system:sqlite",
      "database": None
    }, "postgresql": 
    {
      "_id": None,
      "type": "system:postgresql",
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "oracle_tns":
    {
      "_id": None,
      "type": "system:oracle_tns",
      "password": None,
      "tns_name": None,
      "username": None
    }, "sqlserver": 
    {
      "_id": None,
      "type": "system:sqlserver",
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "mssql-azure-dw": 
    {
      "_id": None,
      "type": "system:mssql-azure-dw",
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "mssql": 
    {
      "_id": None,
      "type": "system:mssql",
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "mysql": 
    {
      "_id": None,
      "type": "system:mysql",
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "oracle": 
    {
      "_id": None,
      "type": "system:oracle",
      "database": None,
      "host": None,
      "password": None,
      "username": None
    }, "ldap": 
    {
      "_id": None,
      "type": "system:ldap",
      "host": None,
      "password": None,
      "username": None
    }}]

  for system_type in systems:
    for key, value in system_type.items():
      if key == system:
        return value