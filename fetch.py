import requests

url = "https://jsonplaceholder.typicode.com/todos/1"
resp = requests.get(url, timeout=10)
resp.raise_for_status()
print(resp.json())