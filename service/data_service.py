import requests
import json
from datetime import date, datetime
import os.path
import csv
import pandas as pd
import numpy as np


def get_all_data():

    keys = []
    values = []
    updated_at = 'N/A'
    try:
        response = requests.get("https://corona.lmao.ninja/v2/all")

        for key, value in json.loads(response.text).items():

            if key in ["cases", "deaths", "recovered", "active"]:

                keys.append(key)
                values.append(add_thousand_separator(value))

            elif key == "updated":

                updated_at = datetime.fromtimestamp(value / 1000).strftime(
                    "%Y-%m-%d %H:%M:%S GMT"
                )
                continue

            else:
                continue
                # excluded keys : ['population', 'activePerOneMillion', 'continent','affectedCountries', 'casesPerOneMillion', 'testsPerOneMillion', 'tests', 'deathsPerOneMillion', 'todayDeaths', 'todayCases', 'critical']
        return [keys, values, updated_at]
    except Exception:

        updated_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S GMT"
        )
        return [["N/A"], ["/NA"], updated_at]


def create_bar_chart_data():
    pass
    # data = [keys, values]
    # df = pd.DataFrame.from_records(data[1:], columns=data[0])
    # print(df.head())


def create_data_file():
    filename = "coronavirus_data_file_" + str(date.today()) + ".csv"

    # Recheck
    # if os.path.isfile(filename):
    #     return
    response = requests.get("https://corona.lmao.ninja/v2/countries")
    # Check if we got valid response and if not then do nothing and just use previous file
    if response.status_code != 200:
        return

    response_to_list = json.loads(response.text)

    # Check if we get empty response and then do nothing and just use previous file
    if len(response_to_list) == 0:
        return

    keys = response_to_list[0].keys()
    # setting up encoding to avoid  UnicodeEncodeError
    # newline = ' to avoid having blank lines between lines
    with open(filename, "w", encoding="utf-8", newline="") as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(response_to_list)


def modify_data_frame():
    df = pd.read_csv("coronavirus_data_file_" + str(date.today()) + ".csv")

    # Rename columns
    df_new = rename_columns(df)

    normalize_country_names(df_new)
    # Remove extra columns
    df_new.drop(["active", "countryInfo", "deathsPerOneMillion"], axis=1, inplace=True)

    df_new["Mortality Rate"] = round((df_new["Deaths"] / df_new["Cases"]) * 100, 2)

    # Keeping only columns that we want to show in data table
    df_final = df_new.filter(
        [
            "Country",
            "Cases",
            "Deaths",
            "Today Cases",
            "Today Deaths",
            "Recovered",
            "Critical",
            "Cases per million",
            "Mortality Rate",
        ]
    )

    # Sort by cases
    df_final.sort_values(by=["Cases"], ascending=False, inplace=True)

    df_final.insert(loc=0, column="Index", value=(np.arange(len(df))) + 1)

    # Save to csv
    df_final.to_csv("coronavirus_data_file_" + str(date.today()) + ".csv", index=False)


def get_data():
    create_data_file()
    modify_data_frame()
    return pd.read_csv("coronavirus_data_file_" + str(date.today()) + ".csv")


def normalize_country_names(dataframe):

    dataframe["Country"].replace(
        ["Congo, the Democratic Republic of the"], "Congo", inplace=True
    )
    dataframe["Country"].replace(
        ["Tanzania, United Republic of"], "Tanzania", inplace=True
    )
    dataframe["Country"].replace(
        ["Venezuela, Bolivarian Republic of"], "Venezuela", inplace=True
    )
    dataframe["Country"].replace(
        ["Lao People's Democratic Republic"], "Laos", inplace=True
    )
    dataframe["Country"].replace(
        ["Saint Vincent and the Grenadines"],
        "St Vincent and the Grenadines",
        inplace=True,
    )


def rename_columns(dataframe):
    return dataframe.rename(
        columns={
            "country": "Country",
            "cases": "Cases",
            "deaths": "Deaths",
            "todayCases": "Today Cases",
            "todayDeaths": "Today Deaths",
            "recovered": "Recovered",
            "critical": "Critical",
            "casesPerOneMillion": "Cases per million",
        }
    )


def add_thousand_separator(value):
    return format(value, ",d")
