import requests
from typing import Dict, Any


class AuthAPI:
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/auth/login"
    
    def login(self, username: str, password: str) -> requests.Response:
        payload = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(self.endpoint, json=payload)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса логина: {str(e)}")
    
    def login_with_missing_fields(self, username: str = None, password: str = None) -> requests.Response:
        payload = {}
        if username:
            payload["username"] = username
        if password:
            payload["password"] = password
            
        try:
            response = requests.post(self.endpoint, json=payload)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса логина: {str(e)}")