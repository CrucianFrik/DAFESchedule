import requests
import time

ti = time.time()
dictToSend = {"teachers": [{"name": "", "surname": "Бурмистров"}],
              "weekdays": []}
R = requests.post('http://crucianfrik.pythonanywhere.com/request/', json=dictToSend).json()
print(R)
print(requests.get('http://crucianfrik.pythonanywhere.com/req/').json())
for t in R['lessons_list']:
    print(t)
print(time.time() - ti)
