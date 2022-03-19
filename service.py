from flask import Flask, request, jsonify
import os
import json
from statics.pipe_templates import collect_pipe, enrich_pipe, global_pipe, transform_pipe, share_pipe
from statics.system_templates import system_configs
from sesamutils import sesam_logger

app = Flask(__name__)

###
# Helpers
###
logger = sesam_logger("Steve the logger", app=app)

@app.route('/')
def index():
    output = {
        'service': 'Template generator up and running',
        'remote_addr': request.remote_addr
    }
    return jsonify(output)

###
# Do the magic.
###
@app.route('/create_node_template', methods=['GET','POST'])
def create_dataflow():
    if request.args.get('config_group'):
        config_group = request.args.get('config_group')
        system_type = request.args.get('system_type')
        system_name = request.args.get('system_name')
        datatype = request.args.get('datatype')
    else:
        config_group = "Default"
        system_type = request.args.get('system_type')
        system_name = request.args.get('system_name')
        datatype = request.args.get('datatype')

    ###
    # node .zip related stuff
    ###
    path = "/local/path/to/repository/template-generator/"
    try:
        os.mkdir(f"{path}/node")
        os.mkdir(f"{path}/node/systems")
        os.mkdir(f"{path}/node/pipes")
    except Exception:
        logger.error("folders already created")
    
    for type in [system_type]:
        json_string = system_configs(type, config_group)
        if config_group != "Default":
            json_string["_id"] = f"{config_group}-{system_name}"
        else:
            json_string["_id"] = system_name

        with open(f"{path}/node/systems/{json_string['_id']}.conf.json", "w") as outfile:
            json.dump(json_string, outfile)
        
        pipes_to_create = []
        pipeNameAndDatatype = f"{system_name}-{datatype}"
        pipes_to_create.append(collect_pipe(json_string, pipeNameAndDatatype, config_group))
        pipes_to_create.append(enrich_pipe(pipeNameAndDatatype, config_group))
        pipes_to_create.append(global_pipe(pipeNameAndDatatype, config_group))
        pipes_to_create.append(transform_pipe(pipeNameAndDatatype, config_group))
        pipes_to_create.append(share_pipe(pipeNameAndDatatype, config_group))

        for pipe in pipes_to_create:
            with open(f"{path}/node/pipes/{pipe['_id']}.conf.json", "w") as outfile:
                json.dump(pipe, outfile)

    return {"status": "your config has been created!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)