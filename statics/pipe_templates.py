def collect_pipe(system, pipeNameAndDatatype, config_group):
  if config_group != "Default":
    config = {
      "_id": f"{config_group}-{pipeNameAndDatatype}-collect",
      "type": "pipe",
      "source": {
        "type": f"{system['type']}",
        "system": f"{system['_id']}"
      },
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "add_namespaces": False
    }
  else:
    config = {
      "_id": f"{pipeNameAndDatatype}-collect",
      "type": "pipe",
      "source": {
        "type": f"{system['type']}",
        "system": f"{system['_id']}"
      },
      "add_namespaces": False
    }
  return config

def enrich_pipe(pipeNameAndDatatype, config_group):
  if config_group != "Default":
    config = {
      "_id": f"{config_group}-{pipeNameAndDatatype}-enrich",
      "type": "pipe",
      "source": {
        "type": "dataset",
        "dataset": f"{pipeNameAndDatatype}-collect"
      },
      "transform": {
        "type": "dtl",
        "rules": {
          "default": [
            ["copy", "*"],
            ["comment", "*** convention here is to add namespaced identifiers ***"],
            ["make-ni", "system-datatype", "datatype"],
            ["comment", "*** convention here is to add the property rdf:type ***"],
            ["add", "rdf:type",
              ["ni", "template:Example"]
            ]
          ]
        }
      },
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "add_namespaces": True,
      "namespaces": {
        "identity": f"{pipeNameAndDatatype}",
        "property": f"{pipeNameAndDatatype}"
      }
    }
  else:
    config = {
      "_id": f"{pipeNameAndDatatype}-enrich",
      "type": "pipe",
      "source": {
        "type": "dataset",
        "dataset": f"{pipeNameAndDatatype}-collect"
      },
      "transform": {
        "type": "dtl",
        "rules": {
          "default": [
            ["copy", "*"],
            ["comment", "*** convention here is to add namespaced identifiers ***"],
            ["make-ni", "system-datatype", "datatype"],
            ["comment", "*** convention here is to add the property rdf:type ***"],
            ["add", "rdf:type",
              ["ni", "template:Example"]
            ]
          ]
        }
      },
      "add_namespaces": True,
      "namespaces": {
        "identity": f"{pipeNameAndDatatype}",
        "property": f"{pipeNameAndDatatype}"
      }
    }
  return config

def global_pipe(pipeNameAndDatatype, config_group):
  if config_group != "Default":
    config = {
      "_id": f"{config_group}-template",
      "type": "pipe",
      "source": {
        "type": "merge",
        "datasets": [f"{config_group}-{pipeNameAndDatatype}-enrich"],
        "equality": [],
        "identity": "first",
        "strategy": "compact",
        "version": 2
      },
      "metadata": {
        "global": True,
        "$config-group": f"{config_group}",
        "tags": ["add your logical grouping here"]
      }
    }
  else:
    config = {
      "_id": "global-template",
      "type": "pipe",
      "source": {
        "type": "merge",
        "datasets": [f"{pipeNameAndDatatype}-enrich"],
        "equality": [],
        "identity": "first",
        "strategy": "compact",
        "version": 2
      },
      "metadata": {
        "global": True,
        "tags": ["add your logical grouping here"]
      }
    }
  return config

def transform_pipe(pipeNameAndDatatype, config_group):
  if config_group != "Default":
    config = {
      "_id": f"{config_group}-{pipeNameAndDatatype}-transform",
      "type": "pipe",
      "source": {
        "type": "dataset",
        "dataset": "global-template"
      },
      "transform": {
        "type": "dtl",
        "rules": {
          "default": [
            ["comment", "*** convention to filter data on rdf:type ***"],
            ["filter",
              ["in",
                ["ni", "template:Example"], "_S.rdf:type"]
            ],
            ["comment", "*** Add target system properties ***"],
            ["add", "someNameForTargetSystem",
              "_S.pick_a_global_property"
            ]
          ]
        }
      },
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "remove_namespaces": True
    }
  else:
    config = {
      "_id": f"{pipeNameAndDatatype}-transform",
      "type": "pipe",
      "source": {
        "type": "dataset",
        "dataset": "global-template"
      },
      "transform": {
        "type": "dtl",
        "rules": {
          "default": [
            ["comment", "*** convention to filter data on rdf:type ***"],
            ["filter",
              ["in",
                ["ni", "template:Example"], "_S.rdf:type"]
            ],
            ["comment", "*** Add target system properties ***"],
            ["add", "someNameForTargetSystem",
              "_S.pick_a_global_property"
            ]
          ]
        }
      },
      "remove_namespaces": True
    }
  return config

def share_pipe(pipeNameAndDatatype, config_group):
  if config_group != "Default":
    config = {
      "_id": f"{config_group}-{pipeNameAndDatatype}-share-operation",
      "type": "pipe",
      "source": {
        "type": "dataset",
        "dataset": f"{config_group}-{pipeNameAndDatatype}-transform"
      },
      "sink": {
        "type": "temporary",
        "system": "temporary",
        "operation": "temporary"
      },
      "transform": [{
        "type": "dtl",
        "rules": {
          "default": [
            ["comment", "*** add discard or filter here to only expose curated data ***"],
            ["discard",
              ["is-not-empty", "_S.critial_property"]
            ],
            ["comment", "filter",
              ["eq", "_S._deleted", False]
            ],
            ["copy", "*"]
          ]
        }
      }, {
        "type": "template",
        "system": "template",
        "operation": "get",
        "replace_entity": False
      }, {
        "type": "dtl",
        "rules": {
          "default": [
            ["comment", "*** the above external transform is only required when checking for optimistic locking in updates ***"],
            ["comment", "*** optimistic locking ***"],
            ["add", "_old",
              ["first",
                ["hops", {
                  "datasets": ["you-collect-dataflow-pipe a"],
                  "where": [
                    ["eq", "_S._id", "a._id"]
                  ]
                }]
              ]
            ],
            ["add", "_json_old",
              ["json-transit",
                ["apply", "remove-under", "_T._old"]
              ]
            ],
            ["add", "_json_new",
              ["first",
                ["json-transit",
                  ["apply", "remove-under",
                    ["first", "_S."]
                  ]
                ]
              ]
            ],
            ["add", "_hash_old",
              ["hash128", "murmur3", "_T._json_old"]
            ],
            ["add", "_hash_new",
              ["hash128", "murmur3", "_T._json_new"]
            ],
            ["if",
              ["eq", "_T._hash_old", "_T._hash_new"],
              [
                ["comment", "*** same data in system as in sesam collect ***"],
                ["comment", "*** expose your data ***"],
                ["comment", "*** example for a rest system is provided below ***"],
                ["add", "::payload",
                  ["apply", "remove-under", "_S."]
                ],
                ["add", "::properties",
                  ["dict", "url",
                    ["concat", "your-endpoint-ressource/", "_S.entity.id"]
                  ]
                ]
              ],
              [
                ["comment", "**** different data in system than in sesam collect ****"],
                ["discard"]
              ]
            ]
          ],
          "remove-under": [
            ["copy", "*", "_*"]
          ]
        }
      }],
      "metadata": {
        "$config-group": f"{config_group}"
      },
      "batch_size": 1
    }
  else:
    config = {
      "_id": f"{pipeNameAndDatatype}-share-operation",
      "type": "pipe",
      "source": {
        "type": "dataset",
        "dataset": f"{pipeNameAndDatatype}-transform"
      },
      "sink": {
        "type": "temporary",
        "system": "temporary",
        "operation": "temporary"
      },
      "transform": [{
        "type": "dtl",
        "rules": {
          "default": [
            ["comment", "*** add discard or filter here to only expose curated data ***"],
            ["discard",
              ["is-not-empty", "_S.critial_property"]
            ],
            ["comment", "filter",
              ["eq", "_S._deleted", False]
            ],
            ["copy", "*"]
          ]
        }
      }, {
        "type": "template",
        "system": "template",
        "operation": "get",
        "replace_entity": False
      }, {
        "type": "dtl",
        "rules": {
          "default": [
            ["comment", "*** the above external transform is only required when checking for optimistic locking in updates ***"],
            ["comment", "*** optimistic locking ***"],
            ["add", "_old",
              ["first",
                ["hops", {
                  "datasets": ["you-collect-dataflow-pipe a"],
                  "where": [
                    ["eq", "_S._id", "a._id"]
                  ]
                }]
              ]
            ],
            ["add", "_json_old",
              ["json-transit",
                ["apply", "remove-under", "_T._old"]
              ]
            ],
            ["add", "_json_new",
              ["first",
                ["json-transit",
                  ["apply", "remove-under",
                    ["first", "_S."]
                  ]
                ]
              ]
            ],
            ["add", "_hash_old",
              ["hash128", "murmur3", "_T._json_old"]
            ],
            ["add", "_hash_new",
              ["hash128", "murmur3", "_T._json_new"]
            ],
            ["if",
              ["eq", "_T._hash_old", "_T._hash_new"],
              [
                ["comment", "*** same data in system as in sesam collect ***"],
                ["comment", "*** expose your data ***"],
                ["comment", "*** example for a rest system is provided below ***"],
                ["add", "::payload",
                  ["apply", "remove-under", "_S."]
                ],
                ["add", "::properties",
                  ["dict", "url",
                    ["concat", "your-endpoint-ressource/", "_S.entity.id"]
                  ]
                ]
              ],
              [
                ["comment", "**** different data in system than in sesam collect ****"],
                ["discard"]
              ]
            ]
          ],
          "remove-under": [
            ["copy", "*", "_*"]
          ]
        }
      }],
      "batch_size": 1
    }
  return config