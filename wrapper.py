import cfClient as cf
from flask import Flask
from flask import request

import utils as ut

app = Flask(__name__)


####### rest api wrapper ##########

@app.route("/broker/update", methods=['POST'])
def updateBrokerWhoseNameIsApi():
    if request.json:
        broker_name = request.json['broker_name']
        space_guid = request.json['space_guid']
        broker_password = request.json['broker_password']

    return cfclient.updateBrokerWhoseNameIs(broker_name, space_guid, broker_password)


@app.route("/broker/list")
def listBrokerApi():
    spaceGuid = '32b16966-045b-4890-8f4d-9f6f0c0d7462'

    return cfclient.listBrokers(spaceGuid)


if __name__ == "__main__":
    # Read settings
    targetEndpoint, userName, userPassword = ut.readSettings()

    # create instance cf client
    cfclient = cf.CfClient(targetEndpoint, userName, userPassword)

    # Start flask
    app.run(host= '0.0.0.0')

