from datetime import date
import os 
import pandas as pd
import requests
import csv
from functools import reduce


def get_who_data(filetype):
    who_csv_raw_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{file_name}_global.csv'.format(file_name=filetype.lower())
    file_to_generate = 'local_' +filetype.lower() + '_' + str(date.today()) + '.csv'

    if not file_exist(file_to_generate):
        transform_who_data_to_file(file_to_generate, who_csv_raw_url)

    return generate_totals_dataframe(file_to_generate, filetype.lower())


def file_exist(filename):

    if os.path.isfile(filename):
        return True
    return False


def generate_totals_dataframe(file_to_process, dataframe_column_name):
    
    df = pd.read_csv(file_to_process)
    
    cases_pers_day = df.sum(axis=0)
    dataframe = pd.DataFrame({'date':cases_pers_day.index, dataframe_column_name:cases_pers_day.values})
    dataframe["date"] = pd.to_datetime(dataframe["date"]).dt.strftime('%Y-%m-%d')
    dataframe.set_index('date',inplace=True)
    return dataframe

def transform_who_data_to_file(local_filename, file_url):

    df = pd.read_csv(file_url)
    df_new = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
    df_new.to_csv(local_filename, index=False)
        

def generate_timeline_dataframe():

    df_conf = get_who_data("confirmed")
    df_dead = get_who_data("deaths")
    df_recovered = get_who_data("recovered")
    final_df = pd.merge(pd.merge(df_conf,df_dead,on='date'),df_recovered,on='date')

    return final_df
