import requests
import json 
from datetime import date
import os.path
import csv

def get_all_data():
    response = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    keys = []
    values = []

    for key,value in json.loads(response.text).items():
        keys.append(key)
        values.append(value)
    return[keys, values]


def get_all_country_data():
    response = requests.get('https://corona.lmao.ninja/countries')
    response_to_list = json.loads(response.text)

    countries = []
    deaths = []

    for item in response_to_list:
        if item.get("deaths") > 0:
            countries.append(item.get("country"))
            deaths.append(item.get("deaths"))
    return[countries, deaths]


def get_all_country_data_as_json():
    response = requests.get('https://corona.lmao.ninja/countries')
    return json.loads(response.text)
  
def get_data_keys():
    response = requests.get('https://corona.lmao.ninja/countries/greece')
    return([i for i in json.loads(response.text).keys()])

def get_data_per_country():
    pass
    
def create_data_file():
    filename = 'coronavirus_data_file_' + str(date.today()) + '.csv'
    
    # Recheck
    # if os.path.isfile(filename):
    #     return
    response = requests.get('https://corona.lmao.ninja/countries')
    response_to_list = json.loads(response.text)
    keys = response_to_list[0].keys()
    # setting up encoding to avoid  UnicodeEncodeError 
    # newline = ' to avoid having blank lines between lines
    with open(filename, 'w', encoding="utf-8", newline='') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(response_to_list)