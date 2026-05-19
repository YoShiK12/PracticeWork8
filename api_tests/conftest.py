import pytest
import requests
from api.auth_api import AuthAPI
from api.profiles_api import ProfilesAPI

BASE_URL = 'https://secby.ru'


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_api(base_url):
    return AuthAPI(base_url)


@pytest.fixture(scope="session")
def profiles_api(base_url):
    return ProfilesAPI(base_url)


@pytest.fixture(scope="session")
def user_credentials():
    return {
        "username": "user_krapivnitskiy",
        "password": "q12345!"
    }


@pytest.fixture(scope="session")
def admin_credentials():
    return {
        "username": "admin",
        "password": "admin123"
    }


@pytest.fixture(scope="session")
def moderator_credentials():
    return {
        "username": "moderator",
        "password": "moderator123"
    }


@pytest.fixture(scope="session")
def user_token(auth_api, user_credentials):
    response = auth_api.login(user_credentials["username"], user_credentials["password"])
    return response.json().get("access_token")


@pytest.fixture(scope="session")
def admin_token(auth_api, admin_credentials):
    response = auth_api.login(admin_credentials["username"], admin_credentials["password"])
    return response.json().get("access_token")


@pytest.fixture(scope="session")
def moderator_token(auth_api, moderator_credentials):
    response = auth_api.login(moderator_credentials["username"], moderator_credentials["password"])
    return response.json().get("access_token")


# Параметризация для различных ролей
@pytest.fixture(params=[
    ("user_krapivnitskiy", "q12345!", "user"),
    ("admin", "admin123", "admin"),
    ("moderator", "moderator123", "moderator")
])
def role_credentials(request):
    return {
        "username": request.param[0],
        "password": request.param[1],
        "role": request.param[2]
    }