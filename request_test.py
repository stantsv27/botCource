import requests


res = requests.get('http://numbersapi.com/43')
print(res.text)
