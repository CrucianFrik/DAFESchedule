import requests
import time

t = time.time()
dictToSend = {"request": {'weekdays': [('weekday', 'Среда')]}}
R = requests.get('http://crucianfrik.pythonanywhere.com/response/', json=dictToSend).json()
for t in R.items():
    for i in t[1].items():
        print(t[0], i)
print(time.time() - t)