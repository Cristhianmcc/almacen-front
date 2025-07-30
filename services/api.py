import requests

BASE_URL = "http://localhost:3003/api"  # Cambia el puerto si tu backend usa otro


class ApiResponse:
    def __init__(self, response_json):
        self.success = response_json.get('success', False)
        self.data = response_json.get('data', None)
        self.message = response_json.get('message', '')

def get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    resp_json = response.json()
    return ApiResponse(resp_json)

def post(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, json=data)
    response.raise_for_status()
    resp_json = response.json()
    return ApiResponse(resp_json)

def put(endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.put(url, json=data)
    response.raise_for_status()
    resp_json = response.json()
    return ApiResponse(resp_json)

def delete(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.delete(url)
    response.raise_for_status()
    resp_json = response.json()
    return ApiResponse(resp_json)
