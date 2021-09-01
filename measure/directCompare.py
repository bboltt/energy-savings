# TODO: 添加功能，区分节能策略运行前后数据源
import numpy as np
from numpy.linalg import norm

def direct_compare(sn, date_list:list, k):
    """
    :param sn:
    :param date_list:
    :param k: number of similar days for each comparing date
    :return:
    """
    n_days = len(date_list)
    if n_days < 1:
        return None
    else:
        similar_days = {}
        for i in range(n_days):
            similar_days[date_list[i]] = find_similarity_days(sn, date_list[i])


def find_similarity_days(sn, date):
    recall_similar_days()
    historical_data = get_data(sn, date)
    days_pool = pool(historical_data)

def compute_similarity(sn, date_1, date_2):
    """
    compute cosine similarity of two given dates
    :param sn:
    :param date_1: date_1
    :param date_2: date_2
    :return: cosine similarity
    """
    vector_1 = get_data(sn, date_1)
    vector_2 = get_data(sn, date_2)
    return np.dot(vector_1, vector_2) / (norm(vector_1) * norm(vector_2))

def recall_similar_days(sn, date):
    get_data(sn, date)
    similar_days = []









比较日 = 选取实施节能措施的m个运行日
相似日备选池 = 没有实施节能措施的运行日

相似日 = 相似日选取(比较日天气数据)

日节能量 = []
for i in range(len(相似日)):
    日节能量.append(计算节能量(相似日[i], 比较日))

def 相似日选取(比较日天气数据):
    # 对每个因素规定相应的约定值，相似日必须满足与比较日在每个因素上的差值都小于对应的约定值。根据此标准筛选出符合要求的相似日，再根据温度和湿度选择出Top K个最相似的相似日。
    相似日 = []
    for 备选相似日 in 相似日备选池:
        if 备选相似日.天气现象 == 比较日.天气现象
        and abs(备选相似日.温度 - 比较日.温度) < 约定值1
        and abs(备选相似日.相对湿度 - 比较日.相对湿度) < 约定值2
        and abs(备选相似日.风速 - 比较日.风速) < 约定值3
        and abs(备选相似日.能见度 - 比较日.能见度) < 约定值4
        and abs(备选相似日.气压 - 比较日.气压) < 约定值5
        and (备选相似日 is 运行日) and (比较日 is 运行日):
            相似日.append(备选相似日)
    return 相似日.sort(by=similarity(温度，湿度))[:k]

def 计算节能量(相似日, 比较日):
    return 根据国标上规定的以下方法，计算出节能量