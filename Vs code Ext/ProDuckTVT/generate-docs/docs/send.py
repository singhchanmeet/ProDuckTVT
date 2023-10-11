import requests
import json

url = 'http://127.0.0.0:8000/generate-docs/'
python_code = """
x = 10
y = 'Hello'

def add(a, b):
    return a + b

class MyClass:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
    """
data = {'python_code': python_code}

response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    documentation = response.json()['documentation']
    print(documentation)
else:
    print(f'Error: {response.status_code}')
