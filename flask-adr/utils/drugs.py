import csv
import requests
import json
from math import sqrt
import csv
import datetime
from time import sleep


BASE_URL = "https://api.thingspeak.com/channels/"

# MAP prr details columns names for readability
PRR_DRUG_NAME = 'field1'
PRR_DRUG_REACTION = 'field2'
PRR_VALUE = 'field3'

# MAP drug details columns names for readability
NAME = 'field2'
REACTION = 'field3'
TEMP_MIN = 'field4'
TEMP_MAX = 'field5'
PRESSURE_MIN = 'field6'
PRESSURE_MAX = 'field7'


def fetch_data(url):
    """A utils function for requests

    return json
    """
    resp = requests.get(url)
    try:
        data = resp.json()["feeds"]
    except KeyError:
        pass
        # TODO: raise an exception
        # TODO: catch requests exceptions too
    return data


def get_drug_details(drug_name, temp, pressure):
    """
    takes input drug name , temp and pressue
    returns list of dictionarys containing drug, reaction and prr
    """
    url = BASE_URL + \
        "428295/feeds.json?api_key=GJE5KVVNGI5893O6&results={}".format(46)
    prr_data = fetch_data(url)

    url = BASE_URL + \
        "425709/feeds.json?api_key=78FZQAN4A3UE30NH & results={}".format(49)
    drug_details = fetch_data(url)

    drug_data = []

    for drug in drug_details:
        if drug[NAME] == drug_name:
            if float(drug[TEMP_MIN]) <= float(temp) <= float(drug[TEMP_MAX]) and \
                    float(drug[PRESSURE_MIN]) <= float(pressure) <= float(drug[PRESSURE_MAX]):
                drug_data.append(drug)
    # find prr value from prr data and add to result
    result = []
    for drug in drug_data:
        for prr in prr_data:
            if drug[NAME] == prr[PRR_DRUG_NAME] and drug[REACTION] == prr[PRR_DRUG_REACTION]:
                req_data = {
                    'drug': drug[NAME],
                    'reaction': drug[REACTION],
                    'prr': prr[PRR_VALUE]
                }
                result.append(req_data)
                print("drug found")
    return result
