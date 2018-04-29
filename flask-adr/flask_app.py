from flask import Flask, request
from flask import jsonify
from flask import render_template

app = Flask(__name__)


import csv
import requests
import json
from math import sqrt
import csv
import datetime
from time import sleep


def do_for_user(drug_name, temp, pressure):
    """
    takes input drug name , temp and pressue
    returns list of dictionarys containing drug, reaction and prr
    """
    data = requests.get(
        "https://api.thingspeak.com/channels/428295/feeds.json?api_key=GJE5KVVNGI5893O6&results={}".format(46))
    jf = str(data.text)
    json_data = json.loads(jf)
    prr_data = json_data['feeds']

    data = requests.get(
        "https://api.thingspeak.com/channels/425709/feeds.json?api_key=78FZQAN4A3UE30NH&results={}".format(49))
    jf = str(data.text)
    json_data = json.loads(jf)
    csv_data_drug = json_data['feeds']

    drug_data = list()
    for data in csv_data_drug:
        if data['field2'] == drug_name:
              if data['field4'] > temp or data['field5'] < temp or data['field6'] > pressure or data['field7'] < pressure:
                data['prr'] = None
                drug_data.append(data)

    for data in drug_data:
        for prr in prr_data:
            if data['field2'] == prr['field1'] and data['field3'] == prr['field2']:
                data['prr'] = prr['field3']
    result = list()
    print("Drug   --   Reaction   --   PRR")
    for data in drug_data:
        if data['prr'] is not None:
            rdata = dict()
            rdata['drug'] = data['field2']
            rdata['reaction'] = data['field3']
            rdata['prr'] = data['prr']
            result.append(rdata)

    return result


@app.route("/")
def home():
    return render_template('home.html', title='Home')


@app.route("/do")
def get_do():
    try:
        drug_name = request.args['drug_name']
        temp = request.args['temp']
        pressure = request.args['pressure']
    except KeyError as err:
        d = {
            "status": "error",
            "message": "{field} parameter missing".format(
                field=err.args[0]),
        }
    else:
        result = do_for_user(
            drug_name=drug_name, temp=temp, pressure=pressure
        )
        d = {
            'status': 'SUCCESS',
            'data': result,
        }
    return jsonify(d)


if __name__ == '__main__':
    app.run()
