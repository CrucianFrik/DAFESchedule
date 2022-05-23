import requests
dictToSend = {"teachers": [("surname", "Свечников")]}
res = requests.post('http://crucianfrik.pythonanywhere.com/request/', json=dictToSend)
print('response from server:',res.text)
dictFromServer = res.json()


print(requests.get('http://crucianfrik.pythonanywhere.com/response/').json())