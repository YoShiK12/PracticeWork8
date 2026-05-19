from typing import Dict, Any, List


def validate_user_profile_structure(data: Dict[str, Any]) -> List[str]:
    missing_fields = []
    
    # Проверка наличия основных полей
    if "message" not in data:
        missing_fields.append("message")
    elif data["message"] != "User profile":
        missing_fields.append(f"message value (expected 'User profile', got '{data['message']}')")
    
    if "profile" not in data:
        missing_fields.append("profile")
        return missing_fields
    
    profile = data["profile"]
    required_profile_fields = ["id", "username", "email", "role_id", "is_active", "profile_id"]
    
    for field in required_profile_fields:
        if field not in profile:
            missing_fields.append(f"profile.{field}")
    
    # Проверка вложенного профиля
    if "profile" in profile:
        nested_profile = profile["profile"]
        nested_required = ["name", "surname", "birthdate"]
        for field in nested_required:
            if field not in nested_profile:
                missing_fields.append(f"profile.profile.{field}")
    
    return missing_fields


def validate_profile_values(data: Dict[str, Any], expected_username: str, expected_email: str, expected_role_id: int) -> List[str]:
    mismatches = []
    
    if "profile" not in data:
        mismatches.append("profile field missing")
        return mismatches
    
    profile = data["profile"]
    
    if profile.get("username") != expected_username:
        mismatches.append(f"username: expected '{expected_username}', got '{profile.get('username')}'")
    
    if profile.get("email") != expected_email:
        mismatches.append(f"email: expected '{expected_email}', got '{profile.get('email')}'")
    
    if profile.get("role_id") != expected_role_id:
        mismatches.append(f"role_id: expected {expected_role_id}, got {profile.get('role_id')}")
    
    # Проверка роли
    if "role" in profile:
        role = profile["role"]
        if role_id := role.get("id"):
            if role_id != expected_role_id:
                mismatches.append(f"role.id: expected {expected_role_id}, got {role_id}")
    
    return mismatches


def validate_no_password_field(data: Dict[str, Any]) -> bool:
    data_str = str(data).lower()
    return "password" not in data_str


def validate_error_response(response, expected_status: int, expected_message_substring: str = None) -> List[str]:
    errors = []
    
    if response.status_code != expected_status:
        errors.append(f"status_code: expected {expected_status}, got {response.status_code}")
    
    if expected_message_substring:
        try:
            response_data = response.json()
            response_str = str(response_data).lower()
            
            # Проверяем разные возможные варианты сообщений об ошибках
            error_messages = []
            if isinstance(response_data, dict):
                # Извлекаем все возможные сообщения об ошибках
                if "detail" in response_data:
                    error_messages.append(str(response_data["detail"]).lower())
                if "message" in response_data:
                    error_messages.append(str(response_data["message"]).lower())
                if "error" in response_data:
                    error_messages.append(str(response_data["error"]).lower())
                
                if "detail" in response_data and isinstance(response_data["detail"], list):
                    for detail in response_data["detail"]:
                        if isinstance(detail, dict):
                            if "msg" in detail:
                                error_messages.append(detail["msg"].lower())
                            if "message" in detail:
                                error_messages.append(detail["message"].lower())
            
            if not error_messages:
                error_messages = [response_str]
            
            found = any(expected_message_substring.lower() in msg for msg in error_messages)
            
            if not found:
                errors.append(f"error message does not contain '{expected_message_substring}'. Got: {error_messages}")
                
        except Exception as e:
            if expected_message_substring.lower() not in response.text.lower():
                errors.append(f"error message does not contain '{expected_message_substring}'. Got: {response.text[:200]}")
    
    return errors