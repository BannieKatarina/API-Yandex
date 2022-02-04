import requests

url = input()
port = int(input())
a = int(input())
b = int(input())
adr = f'{url}:{port}?a={a}&b={b}'
request = requests.get(adr)
response = request.json()
response['result'].sort()
print(*response['result'])
print(response['check'])
