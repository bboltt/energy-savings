import pickle
from sklearn import set_config
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_transformer
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
    df = pandas_feature_data(data)
    #model


if __name__ == '__main__':
    print(load_model("../model/reg.pickle"))




def predict_baseline(sn):
    #
    sql = """
    with energy as (
    select *,
    (master_device_electricity - electricity_lag)/(timeStamp - timeStamp_lag)*3600 as hourly_consumption
    from
    (
    SELECT p.sn as sn, create_time, date, hour(create_time) as hour,
    weekday(create_time) as weekday,unix_timestamp(create_time) as timeStamp,
    unix_timestamp(lag(create_time) over (partition by p.sn order by create_time asc)) as timeStamp_lag,
    master_device_electricity, lag(master_device_electricity) over (partition by p.sn order by create_time asc) as electricity_lag,
    project_name, address, project_type, province, city, district, location
    from vrf.silver_device_power p, vrf.bronze_project_info i
    where p.sn = i.SN
    and (city is not null or district is not null)
    and master_device_electricity is not null)
    ),

    weather as (
    select *, hour(datetime) as hour
    from qingxin.bronze_spi_weather)


    select sn,create_time,e.date,e.hour,weekday,timeStamp,timeStamp_lag,e.city,e.district,hourly_consumption,
    temperature,precipitation,wind_speed,visibility,relative_humidity,pressure,weather
    from energy e
    inner join weather w
    on e.date=w.date and e.hour=w.hour and e.province=w.prov and e.city=w.city and e.district=w.district
    union all
    select sn,create_time,e.date,e.hour,weekday,timeStamp,timeStamp_lag,e.city,e.district,hourly_consumption,
    temperature,precipitation,wind_speed,visibility,relative_humidity,pressure,weather
    from energy e
    left join weather w
    on e.date=w.date and e.hour=w.hour and e.city=w.city and e.district!=w.district
    where temperature is not null
    """

    data = spark.sql(sql)

    stringIndexer = StringIndexer(inputCols=['city', 'weather'], outputCols=['city_encoded', 'weather_encoded'])
    model = stringIndexer.fit(train)
    indexed = model.transform(train)
    encoder = OneHotEncoder(dropLast=False, inputCols=['city_encoded', 'weather_encoded'],
                            outputCols=['city_encoded_vec', 'weather_encoded_vec'])
    encoded = encoder.transform(indexed)

    from pyspark.ml import Pipeline
    from pyspark.ml.feature import OneHotEncoder

    CATE_FEATURES = ['city', 'weather']
    INT_CATE_FEATURES = ['hour', 'weekday']
    CONTI_FEATURES = ['temperature', 'wind_speed', 'visibility', 'relative_humidity', 'pressure']
    stages = []  # stages in Pipeline

    for categoricalCol in CATE_FEATURES:
        stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol + "Index")
        encoder = OneHotEncoder(inputCols=[stringIndexer.getOutputCol()],
                                outputCols=[categoricalCol + "classVec"])
        stages += [stringIndexer, encoder]

    for categoricalCol in INT_CATE_FEATURES:
        encoder = OneHotEncoder(inputCol=categoricalCol,
                                outputCol=categoricalCol + "classVec")
        stages += [encoder]

    assemblerInputs = [c + "classVec" for c in CATE_FEATURES] + [c + "classVec" for c in INT_CATE_FEATURES] + CONTI_FEATURES

    assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
    stages += [assembler]

    pipeline = Pipeline(stages=stages)
    pipelineModel = pipeline.fit(train)
    model = pipelineModel.transform(train)
    return model

