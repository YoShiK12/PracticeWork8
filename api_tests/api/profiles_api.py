import requests
from typing import Dict, Optional


class ProfilesAPI:
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.me_endpoint = f"{base_url}/api/profiles/me"
    
    def get_headers(self, token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}
    
    def get_my_profile(self, token: str) -> requests.Response:
        try:
            headers = self.get_headers(token)
            response = requests.get(self.me_endpoint, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса профиля: {str(e)}")
    
    def get_profile_with_invalid_token(self, token: str) -> requests.Response:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(self.me_endpoint, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса профиля: {str(e)}")