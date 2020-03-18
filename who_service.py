from datetime import date
import os 
import pandas as pd
import requests
import csv

def get_timeline():
    return get_confirmed_cases()    


def get_confirmed_cases():
    who_file_names = ['Confirmed', 'Deaths', 'Recovered']
    who_csv_raw = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

    confirmed_cases_file = 'local_confirmed_' + str(date.today()) + '.csv'
    deaths_file = 'local_deaths_' + str(date.today()) + '.csv'
    recovered_file = 'local_recovered_' + str(date.today()) + '.csv'

    if not file_exist(confirmed_cases_file):
        df = pd.read_csv(who_csv_raw)
        df_new = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
        df_new.to_csv(confirmed_cases_file, index=False)
    
    df = pd.read_csv(confirmed_cases_file)
    cases_pers_day = df.sum(axis=0)
    dataframe = pd.DataFrame({'date':cases_pers_day.index, 'confirmed cases':cases_pers_day.values})
    dataframe.set_index('date',inplace=True)
    # dataframe.to_csv("arg.csv")
    return dataframe

# def generate_totals():
#     pass

# def get_deaths():
    # who_file_names = ['Confirmed', 'Deaths', 'Recovered']
    # who_csv_raw = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'

    # confirmed_cases_file = 'local_confirmed_' + str(date.today()) + '.csv'
    # deaths_file = 'local_deaths_' + str(date.today()) + '.csv'
    # recovered_file = 'local_recovered_' + str(date.today()) + '.csv'

    # if not file_exist(deaths_file):
    #     df = pd.read_csv(who_csv_raw)
    #     df_new = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
    #     df_new.to_csv(deaths_file, index=False)
    
    # df = pd.read_csv(deaths_file)
    # cases_pers_day = df.sum(axis=0)
    # dataframe = pd.DataFrame({'date':cases_pers_day.index, 'deaths':cases_pers_day.values})
    # dataframe.set_index('date',inplace=True)
    # # dataframe.to_csv("arg.csv")
    # return dataframe

# def get_recovered():
#     who_csv_raw = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

#     recovered_file = 'local_recovered_' + str(date.today()) + '.csv'

#     if not file_exist(recovered_file):
#         df = pd.read_csv(who_csv_raw)
#         df_new = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1)
#         df_new.to_csv(recovered_file, index=False)
    
#     df = pd.read_csv(recovered_file)
#     cases_pers_day = df.sum(axis=0)
#     dataframe = pd.DataFrame({'date':cases_pers_day.index, 'deaths':cases_pers_day.values})
#     dataframe.set_index('date',inplace=True)
#     # dataframe.to_csv("arg.csv")
#     return dataframe


    # df = pd.read_csv(recovered_file, sep='delimiter')
    # df.drop(['Province/State'], axis=1, inplace=True)
    # df.columns.name = df.index.name
    # df.index.name = None
    # print(df.columns)
    # df_new = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])
    # cases_pers_day = df_new.sum(axis=0)
    # dataframe = pd.DataFrame({'date':cases_pers_day.index, 'recovered':cases_pers_day.values})
    # dataframe.set_index('date',inplace=True)
    # dataframe.to_csv("arg.csv")
    # print(dataframe.head())

def file_exist(filename):
    if os.path.isfile(filename):
        return True
    return False

def generate_timeline_dataframe():
    # df_conf = get_confirmed_cases()
    # df_dead = get_deaths()
    # return get_recovered()
    pass
    # final_df = pd.merge(pd.merge(df_conf,df_dead,on='date'),df_recovered,on='date')
    # final_df.to_csv("arg.csv")
    # return final_df

# get_timeline()

# get_recovered()