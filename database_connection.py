import pymysql
import requests
from config import connection_info
import pandas as pd


conn = pymysql.connect(
    host=connection_info[0],
    unix_socket=connection_info[1],
    user="root",
    passwd=connection_info[2],
    db=connection_info[3],
    charset="utf8",
)
cur = conn.cursor()
cur.execute("USE data")
# This is a very crude way of maintaining the database. I will fix in the near future
cur.execute("TRUNCATE TABLE uk_data")


def store(date, daily_cases, total_cases, daily_deaths, total_deaths):

    cur.execute(
        "INSERT INTO uk_data (date, daily_cases, total_cases, daily_deaths, total_deaths) VALUES (%s, %s, %s, %s, %s)",
        (date, daily_cases, total_cases, daily_deaths, total_deaths),
    )
    cur.connection.commit()
    print(
        f"DATE: {date}, DAILY_CASES: {daily_cases}, TOTAL_CASES: {total_cases}, DAILY_DEATHS: {daily_deaths}, TOTAL_DEATHS: {total_deaths}"
    )


def get_data(cases_data, death_data, world_data):
    res_cases = requests.get(cases_data)
    res_deaths = requests.get(death_data)
    res_world_data = requests.get(world_data)
    with open("data/world_data.csv", "wb") as f:
        f.write(res_world_data.content)
    with open("data/data_cases.csv", "wb") as f:
        f.write(res_cases.content)
    with open("data/data_deaths.csv", "wb") as f:
        f.write(res_deaths.content)
    clean_data("data/data_cases.csv", "data/data_deaths.csv")


def clean_data(cases_data, death_data):
    with open(cases_data, "r") as fc, open(death_data, "r") as fd:
        file_cases = fc.readlines()[1:]
        file_deaths = fd.readlines()[1:]
        for line_cases, line_deaths in zip(file_cases, file_deaths):
            # cases data lines
            lines_c = line_cases.split(",")
            date = lines_c[3]
            daily_cases = lines_c[4]
            total_cases = lines_c[5].replace("\n", "")
            # death data lines
            line_d = line_deaths.split(",")
            daily_deaths = line_d[4]
            total_deaths = line_d[5].replace("\n", "")
            store(date, daily_cases, total_cases, daily_deaths, total_deaths)


def write_to_new_csv_file(cases, deaths):
    data_cases, death_cases = pd.read_csv(cases), pd.read_csv(deaths)
    data_cases["rollingNewCases"] = data_cases["newCasesBySpecimenDate"].rolling(window=7, min_periods=7, center=True).mean().round()
    data_cases = data_cases.rename(columns={"newCasesBySpecimenDate": "New Cases"})

    death_cases["rollingNewDeaths"] = death_cases["newDeaths28DaysByDeathDate"].rolling(window=7, min_periods=7, center=True).mean().round()
    death_cases = death_cases.rename(columns={"newDeaths28DaysByDeathDate": "New Deaths"})
    
    data_cases.to_csv("data/data_cases.csv"), death_cases.to_csv("data/data_deaths.csv")


internet_data = get_data(
    "https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newCasesBySpecimenDate%22:%22newCasesBySpecimenDate%22,%22cumCasesBySpecimenDate%22:%22cumCasesBySpecimenDate%22%7D&format=csv",
    "https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newDeaths28DaysByDeathDate%22:%22newDeaths28DaysByDeathDate%22,%22cumDeaths28DaysByDeathDate%22:%22cumDeaths28DaysByDeathDate%22%7D&format=csv",
    "https://covid.ourworldindata.org/data/owid-covid-data.csv"
)

write_to_new_csv_file("data/data_cases.csv", "data/data_deaths.csv")

conn.close()
