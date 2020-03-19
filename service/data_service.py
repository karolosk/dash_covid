import requests
import json 
from datetime import date,datetime
import os.path
import csv
import pandas as pd

def get_all_data():
    response = requests.get('https://corona.lmao.ninja/all')
    keys = []
    values = []

    for key,value in json.loads(response.text).items():
        if key == 'updated':
            updated_at = datetime.fromtimestamp(value/1000).strftime('%Y-%m-%d %H:%M:%S GMT')
            continue
        else:
            updated_at = date.today()
        keys.append(key)
        values.append(add_thousand_separator(value))
    
    return[keys, values, updated_at]



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


def modify_data_frame():
    df = pd.read_csv('coronavirus_data_file_' + str(date.today()) + '.csv')
    
    # Rename columns
    df_new = rename_columns(df)

    # Remove extra columns
    df_new.drop(['active', 'casesPerOneMillion'], axis=1, inplace=True)

    # Save to csv
    df_new.to_csv('coronavirus_data_file_' + str(date.today()) + '.csv', index=False)

def get_data():
    create_data_file()
    modify_data_frame()
    return pd.read_csv('coronavirus_data_file_' + str(date.today()) + '.csv')


def rename_columns(dataframe):
    return dataframe.rename(columns={
        'country': 'Country',
        'cases': 'Cases',
        'deaths': 'Deaths',
        'todayCases': 'Today Cases',
        'todayDeaths': 'Today Deaths',
        'recovered': 'Recovered',
        'critical': 'Critical'
    })



def add_thousand_separator(value):
    return format(value, ',d')


