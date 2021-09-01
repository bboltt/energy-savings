
#%%
import requests

url = "http://47.118.41.17:8026/api/apps-energy-manager/v1/algorithm/input/history/query?nid=vrf/vrf_0000CC111000CCM1718B134002050000/indoor/1&startTime=2021-08-20 16:32:17&endTime=2021-08-22 16:32:20&columnList=onOff"

params = {"format": "json"}
data = requests.get(url, params=params)

#%%
print(data.content)
#%%
data.json()