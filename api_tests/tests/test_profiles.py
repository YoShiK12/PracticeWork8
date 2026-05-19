import pytest
import requests
from utils.validators import (
    validate_user_profile_structure,
    validate_profile_values,
    validate_no_password_field,
    validate_error_response
)


class TestProfilesAPI:    
    def test_get_user_profile_success(self, profiles_api, user_token):
        response = profiles_api.get_my_profile(user_token)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = response.json()
        missing_fields = validate_user_profile_structure(data)
        
        assert len(missing_fields) == 0, f"Отсутствуют или некорректны поля: {missing_fields}"
    
    def test_user_profile_values_match(self, profiles_api, user_token):
        response = profiles_api.get_my_profile(user_token)
        data = response.json()
        
        mismatches = validate_profile_values(
            data,
            expected_username="user_krapivnitskiy",
            expected_email="pavel@user.ru",
            expected_role_id=3
        )
        
        assert len(mismatches) == 0, f"Несоответствия в значениях: {mismatches}"
    
    def test_user_profile_no_password(self, profiles_api, user_token):
        response = profiles_api.get_my_profile(user_token)
        data = response.json()
        
        assert validate_no_password_field(data), "Поле password обнаружено в ответе!"
    
    def test_admin_profile_success(self, profiles_api, admin_token):
        response = profiles_api.get_my_profile(admin_token)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        data = response.json()
        missing_fields = validate_user_profile_structure(data)
        assert len(missing_fields) == 0, f"Отсутствуют или некорректны поля: {missing_fields}"
    
    def test_admin_has_admin_role(self, profiles_api, admin_token):
        response = profiles_api.get_my_profile(admin_token)
        data = response.json()
        
        profile_data = data.get("profile", {})
        
        assert profile_data.get("role_id") == 1, f"Ожидалась role_id=1, получена {profile_data.get('role_id')}"
        
        if "role" in profile_data:
            role_data = profile_data["role"]
            assert role_data.get("name") == "admin", f"Ожидалась роль admin, получена {role_data.get('name')}"
    
    def test_get_profile_without_token(self, profiles_api):
        response = profiles_api.get_profile_with_invalid_token("")
        
        errors = validate_error_response(response, 403, "not authenticated")
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    def test_get_profile_with_invalid_token(self, profiles_api):
        response = profiles_api.get_profile_with_invalid_token("invalid_token_12345")
        
        errors = validate_error_response(response, 401, "could not validate credentials")
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    def test_get_profile_with_malformed_token(self, profiles_api):
        response = profiles_api.get_profile_with_invalid_token("Bearer malformed")
        
        errors = validate_error_response(response, 401)
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    def test_get_profile_with_none_token(self, profiles_api):
        response = profiles_api.get_profile_with_invalid_token(None)
        
        errors = validate_error_response(response, 401)
        assert len(errors) == 0, f"Ошибки валидации: {errors}"
    
    
    @pytest.mark.parametrize("token_fixture,expected_role_id,expected_role_name", [
        ("user_token", 3, "user"),
        ("admin_token", 1, "admin"),
    ])
    def test_different_roles_profile_structure(self, profiles_api, request, token_fixture, expected_role_id, expected_role_name):
        token = request.getfixturevalue(token_fixture)
        response = profiles_api.get_my_profile(token)
        
        assert response.status_code == 200, f"Статус не 200 для роли {expected_role_name}"
        data = response.json()
        
        missing_fields = validate_user_profile_structure(data)
        assert len(missing_fields) == 0, f"Ошибки структуры для роли {expected_role_name}: {missing_fields}"
        
        profile_data = data.get("profile", {})
        assert profile_data.get("role_id") == expected_role_id, \
            f"Для роли {expected_role_name} ожидалась role_id={expected_role_id}, получена {profile_data.get('role_id')}"
    
    
    def test_user_profile_response_contains_required_fields(self, profiles_api, user_token):
        response = profiles_api.get_my_profile(user_token)
        data = response.json()
        
        profile = data.get("profile", {})
        
        required_fields = ["id", "username", "email", "role_id", "is_active", "profile_id"]
        
        for field in required_fields:
            assert field in profile, f"Отсутствует обязательное поле '{field}' в профиле"
        
        if "role" in profile:
            role = profile["role"]
            assert "id" in role, "В объекте role отсутствует поле id"
            assert "name" in role, "В объекте role отсутствует поле name"
    
    def test_user_profile_data_types(self, profiles_api, user_token):
        response = profiles_api.get_my_profile(user_token)
        data = response.json()
        
        profile = data.get("profile", {})
        
        assert isinstance(profile.get("id"), int), "id должен быть числом"
        assert isinstance(profile.get("username"), str), "username должен быть строкой"
        assert isinstance(profile.get("email"), str), "email должен быть строкой"
        assert isinstance(profile.get("role_id"), int), "role_id должен быть числом"
        assert isinstance(profile.get("is_active"), bool), "is_active должен быть булевым значением"