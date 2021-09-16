#%%
import json
import os
import pandas as pd

url = "../docs/inSamples.json"
#%%


def load_from_json_file(path):
    with open(url, encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_from_url(path):
    pass

#%%


def load_stats(sn, weekday, hour, month):
    df = pd.read_csv('../stats/avgHourlyEnergyByWeekday.csv')
    avg_energy_weekday = df[(df["sn"] == sn) & (df["weekday"] == weekday)].iloc[0, 2]
    df = pd.read_csv('../stats/avgHourlyEnergyByHour.csv')
    avg_energy_hour = df[(df["sn"] == sn) & (df["hour"] == hour)].iloc[0, 2]
    df = pd.read_csv('../stats/avgHourlyEnergyByMonth.csv')
    avg_energy_month = df[(df["sn"] == sn) & (df["month"] == month)].iloc[0, 2]
    return avg_energy_weekday, avg_energy_hour, avg_energy_month


def pandas_feature_data(data):
    """
    prepare features as pandas dataframe by given json dict.
    :param data: json dict
    :return: df
    """
    df = pd.DataFrame()
    sn = data["sn"]
    weekday = pd.Timestamp(data["data"][0]["time"]).dayofweek
    hour = int(data["data"][0]["time"][11:13])
    month = int(data["data"][0]["time"][5:7])
    df["hour"] = [hour]
    df["weekday"] = [weekday]
    df['month'] = [month]
    df["city"] = [data["data"][0]["info"]["city"]]
    df["temperature"] = [data["data"][0]["weather"]["temperature"]]
    df["relative_humidity"] = [data["data"][0]["weather"]["relative_humidity"]]
    df["wind_scale"] = [data["data"][0]["weather"]["wind_power"]]
    df["weather"] = [data["data"][0]["weather"]["weather"]]
    avg_energy_x, avg_energy_y, avg_energy = load_stats(sn, weekday, hour, month)
    df["avg_energy_x"] = [avg_energy_x]
    df["avg_energy_y"] = [avg_energy_y]
    df["avg_energy"] = [avg_energy]
    print(df)
    return df
    #["hour", "weekday", "month", "city", "temperature", "relative_humidity", "wind_scale", "weather", "avg_energy_x"
    # (avg_weekday), "avg_energy_y" (avg_hour), "avg_energy" (avg_month)]

if __name__ == "__main__":
    features = pandas_feature_data(load_from_json_file(url))


"""
#params = {"format": "json"}
#data = requests.get(url, params=params)
#%%
inputs = load_from_json_file(url)

print(inputs)
#%%
print(inputs["data"])


#%%
import test

test.print_test()

"""
#%%
a = pd.DataFrame()
a["B"] = 5

