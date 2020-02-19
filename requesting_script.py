import requests
dictToSend = {'description':'Salary'}
res = requests.get('http://localhost:5000/')
print('response from server:',res.text)
# dictFromServer = res.json()
# , json=dictToSend