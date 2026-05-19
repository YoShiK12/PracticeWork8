import pytest
from utils.validators import validate_error_response


class TestAuthAPI:
    
    def test_valid_login_returns_200(self, auth_api, user_credentials):
        response = auth_api.login(user_credentials["username"], user_credentials["password"])
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        response_data = response.json()
        assert "access_token" in response_data, "В ответе отсутствует поле access_token"
        if "token_type" in response_data:
            assert response_data.get("token_type") == "bearer", "Неверный тип токена"
    
    def test_valid_login_returns_token(self, auth_api, user_credentials):
        response = auth_api.login(user_credentials["username"], user_credentials["password"])
        
        assert response.status_code == 200
        token = response.json().get("access_token")
        
        assert token is not None, "Токен отсутствует в ответе"
        assert len(token) > 0, "Токен пустой"
    
    def test_invalid_login_returns_401(self, auth_api):
        response = auth_api.login("invalid_user", "invalid_pass")
        errors = validate_error_response(response, 401, "incorrect username or password")
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    def test_missing_password_returns_422(self, auth_api, user_credentials):
        response = auth_api.login_with_missing_fields(
            username=user_credentials["username"],
            password=None
        )
        errors = validate_error_response(response, 422)
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    def test_missing_username_returns_422(self, auth_api, user_credentials):
        response = auth_api.login_with_missing_fields(
            username=None,
            password=user_credentials["password"]
        )
        
        errors = validate_error_response(response, 422)
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    def test_empty_credentials_returns_422(self, auth_api):
        response = auth_api.login_with_missing_fields()
        
        errors = validate_error_response(response, 422)
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    @pytest.mark.parametrize("username,password,expected_status,expected_message", [
        ("", "q12345!", 401, None),           
        ("user_krapivnitskiy", "", 401, None), 
        ("", "", 401, None),                   
        ("user_krapivnitskiy", "wrong", 401, "incorrect username or password"),  
        ("wrong_user", "q12345!", 401, "incorrect username or password"),       
    ])
    def test_various_invalid_credentials(self, auth_api, username, password, expected_status, expected_message):
        response = auth_api.login(username, password)
        
        errors = validate_error_response(response, expected_status, expected_message)
        assert len(errors) == 0, f"Ошибки валидации для username='{username}', password='{password}': {errors}"