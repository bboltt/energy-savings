import pickle
from sklearn.linear_model import Ridge
#from pyspark.ml import Pipeline
#from pyspark.ml.feature import OneHotEncoder

from ..data.load_data import load_from_json_file, pandas_feature_data


def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def calculate_energy_base(url):
    """
    compute energy base by given json url
    :param url: api url
    :return:
    """
    data = load_from_json_file(url)
    model_path = data["data"][0]["file_path"]["mlModel"]
    df = pandas_feature_data(data)
    model = load_model(model_path)
    print("hourly consumption is: \t", model.predict(df)[0])
    return model.predict(df)[0]


if __name__ == '__main__':
    print(load_model("../../model/reg.pickle"))




