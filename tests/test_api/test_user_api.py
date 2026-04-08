"""
User API Tests
用户API测试用例
"""
import pytest
import allure
import requests
from loguru import logger


@allure.feature("User API")
@allure.story("User CRUD Operations")
@allure.severity(allure.severity_level.HIGH)
class TestUserAPI:
    """用户API测试类"""

    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.api
    @allure.title("API测试 - 获取用户列表")
    @allure.description("验证GET /api/users接口返回正确的用户列表")
    def test_get_users_list(self):
        """
        测试用例：获取用户列表

        期望结果：
        - 状态码为200
        - 返回用户列表
        """
        # API基础URL（从配置或环境变量获取）
        base_url = "https://api.example.com"
        endpoint = "/users"

        # 发送请求
        response = requests.get(f"{base_url}{endpoint}")

        # 验证响应
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # 验证响应体
        data = response.json()
        assert "users" in data or isinstance(data, list), "Response should contain users list"

        logger.info(f"Retrieved {len(data) if isinstance(data, list) else len(data.get('users', []))} users")

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("API测试 - 创建新用户")
    @allure.description("验证POST /api/users接口能够创建新用户")
    def test_create_user(self):
        """
        测试用例：创建新用户

        期望结果：
        - 状态码为201
        - 返回创建的用户信息
        """
        base_url = "https://api.example.com"
        endpoint = "/users"

        # 请求数据
        user_data = {
            "username": "testuser_api",
            "email": "testuser_api@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "user"
        }

        # 发送请求
        response = requests.post(f"{base_url}{endpoint}", json=user_data)

        # 验证响应
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        # 验证返回数据
        data = response.json()
        assert data["email"] == user_data["email"], "Created user email should match"

        logger.info(f"Created user: {data['email']}")

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("API测试 - 获取单个用户")
    @allure.description("验证GET /api/users/{id}接口返回正确的用户信息")
    def test_get_user_by_id(self):
        """
        测试用例：获取单个用户

        期望结果：
        - 状态码为200
        - 返回正确的用户信息
        """
        base_url = "https://api.example.com"
        user_id = 1  # 假设存在ID为1的用户
        endpoint = f"/users/{user_id}"

        # 发送请求
        response = requests.get(f"{base_url}{endpoint}")

        # 验证响应
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # 验证返回数据
        data = response.json()
        assert data["id"] == user_id, "User ID should match"

        logger.info(f"Retrieved user: {data['email']}")

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("API测试 - 更新用户信息")
    @allure.description("验证PUT /api/users/{id}接口能够更新用户信息")
    def test_update_user(self):
        """
        测试用例：更新用户信息

        期望结果：
        - 状态码为200
        - 返回更新后的用户信息
        """
        base_url = "https://api.example.com"
        user_id = 1
        endpoint = f"/users/{user_id}"

        # 更新数据
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }

        # 发送请求
        response = requests.put(f"{base_url}{endpoint}", json=update_data)

        # 验证响应
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # 验证返回数据
        data = response.json()
        assert data["first_name"] == update_data["first_name"], "First name should be updated"

        logger.info(f"Updated user: {user_id}")

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("API测试 - 删除用户")
    @allure.description("验证DELETE /api/users/{id}接口能够删除用户")
    def test_delete_user(self):
        """
        测试用例：删除用户

        期望结果：
        - 状态码为204或200
        - 用户被删除
        """
        base_url = "https://api.example.com"
        user_id = 999  # 测试用户ID
        endpoint = f"/users/{user_id}"

        # 发送请求
        response = requests.delete(f"{base_url}{endpoint}")

        # 验证响应
        assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"

        logger.info(f"Deleted user: {user_id}")


@allure.feature("User API")
@allure.story("API Authentication")
class TestUserAPIAuth:
    """用户API认证测试类"""

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("API测试 - 未授权访问")
    @allure.description("验证未授权访问API返回401")
    def test_unauthorized_access(self):
        """
        测试用例：未授权访问

        期望结果：
        - 状态码为401
        """
        base_url = "https://api.example.com"
        endpoint = "/users"

        # 不提供认证信息
        response = requests.get(f"{base_url}{endpoint}")

        # 验证响应
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

        logger.info("Unauthorized access correctly blocked")

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("API测试 - Bearer Token认证")
    @allure.description("验证Bearer Token认证正常工作")
    def test_bearer_token_auth(self):
        """
        测试用例：Bearer Token认证

        期望结果：
        - 使用有效token能够访问
        - 状态码为200
        """
        base_url = "https://api.example.com"
        endpoint = "/users"
        token = "valid_token_here"  # 应该从配置获取

        # 添加认证头
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 发送请求
        response = requests.get(f"{base_url}{endpoint}", headers=headers)

        # 验证响应
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        logger.info("Bearer token authentication successful")


@allure.feature("User API")
@allure.story("API Validation")
class TestUserAPIValidation:
    """用户API验证测试类"""

    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize("field,value,expected_status", [
        ("email", "invalid-email", 400),
        ("username", "", 400),
        ("password", "123", 400),
    ])
    @allure.title("API测试 - 字段验证 - {field}")
    @allure.description("验证API对无效输入返回400错误")
    def test_field_validation(self, field, value, expected_status):
        """
        测试用例：字段验证（参数化）

        期望结果：
        - 返回400状态码
        - 返回错误消息
        """
        base_url = "https://api.example.com"
        endpoint = "/users"

        # 无效数据
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        user_data[field] = value

        # 发送请求
        response = requests.post(f"{base_url}{endpoint}", json=user_data)

        # 验证响应
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

        logger.info(f"Field validation for {field} returned {expected_status}")
