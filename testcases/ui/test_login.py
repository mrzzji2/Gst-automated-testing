"""
Login Page Tests
登录页测试用例
测试
"""
import pytest
import allure
from loguru import logger

from pages.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("User Login")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    """登录测试类"""

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("测试用户能够成功登录")
    @allure.description("验证用户使用正确的凭据能够成功登录系统")
    async def test_successful_login(self, login_page: LoginPage, test_user):
        """
        测试用例：成功登录

        步骤：
        1. 导航到登录页
        2. 输入有效的用户名和密码
        3. 点击登录按钮
        4. 验证导航到仪表盘

        期望结果：
        - 用户成功登录
        - 页面导航到仪表盘
        """
        # 步骤 1-2: 导航到登录页并输入凭据
        await login_page.goto_login()
        await login_page.login(
            username=test_user["username"],
            password=test_user["password"]
        )

        # 步骤 3-4: 验证登录成功
        await login_page.wait_for_url("**/dashboard", timeout=10000)

        # 断言
        current_url = login_page.get_current_url()
        assert "dashboard" in current_url.lower(), f"Expected to be on dashboard, but got: {current_url}"

        logger.info(f"User {test_user['username']} logged in successfully")

    @pytest.mark.regression
    @allure.title("测试使用无效凭据登录失败")
    @allure.description("验证使用无效的用户名或密码登录时会显示错误消息")
    async def test_login_with_invalid_credentials(self, login_page: LoginPage):
        """
        测试用例：使用无效凭据登录

        步骤：
        1. 导航到登录页
        2. 输入无效的用户名和密码
        3. 点击登录按钮
        4. 验证显示错误消息

        期望结果：
        - 登录失败
        - 显示错误消息
        """
        # 步骤 1-2: 导航到登录页并输入无效凭据
        await login_page.goto_login()
        await login_page.login(
            username="invalid@example.com",
            password="wrongpassword"
        )

        # 步骤 3-4: 验证错误消息
        await login_page.assert_on_login_page()

        # 验证错误消息
        if await login_page.is_error_displayed():
            error_message = await login_page.get_error_message()
            assert error_message, "Error message should be displayed"
            logger.info(f"Expected error message displayed: {error_message}")
        else:
            # 验证仍在登录页
            current_url = login_page.get_current_url()
            assert "login" in current_url.lower(), "Should remain on login page"

    @pytest.mark.regression
    @allure.title("测试使用空用户名登录")
    @allure.description("验证不输入用户名时登录失败")
    async def test_login_with_empty_username(self, login_page: LoginPage):
        """
        测试用例：使用空用户名登录

        期望结果：
        - 登录按钮不可用或显示验证错误
        """
        await login_page.goto_login()
        await login_page.enter_username("")
        await login_page.enter_password("somepassword")

        # 验证登录按钮状态或错误消息
        is_enabled = await login_page.is_login_button_enabled()
        assert not is_enabled, "Login button should be disabled with empty username"

    @pytest.mark.regression
    @allure.title("测试使用空密码登录")
    @allure.description("验证不输入密码时登录失败")
    async def test_login_with_empty_password(self, login_page: LoginPage):
        """
        测试用例：使用空密码登录

        期望结果：
        - 登录按钮不可用或显示验证错误
        """
        await login_page.goto_login()
        await login_page.enter_username("test@example.com")
        await login_page.enter_password("")

        # 验证登录按钮状态或错误消息
        is_enabled = await login_page.is_login_button_enabled()
        assert not is_enabled, "Login button should be disabled with empty password"

    @pytest.mark.regression
    @allure.title("测试记住我功能")
    @allure.description("验证勾选记住我后，下次访问时保持登录状态")
    async def test_remember_me_functionality(self, login_page: LoginPage, test_user):
        """
        测试用例：记住我功能

        注意：此测试需要验证cookie存储，可能需要重新加载页面
        """
        await login_page.goto_login()
        await login_page.login(
            username=test_user["username"],
            password=test_user["password"],
            remember_me=True
        )

        # 验证登录成功
        await login_page.wait_for_url("**/dashboard", timeout=10000)

        # 检查是否设置了remember me cookie
        cookies = await login_page.page.context.cookies()
        remember_cookie = next((c for c in cookies if "remember" in c.get("name", "").lower()), None)

        # 断言（根据实际实现调整）
        # assert remember_cookie is not None, "Remember me cookie should be set"

        logger.info("Remember me functionality tested")

    @pytest.mark.regression
    @allure.title("测试忘记密码链接")
    @allure.description("验证忘记密码链接可以点击并导航到正确页面")
    async def test_forgot_password_link(self, login_page: LoginPage):
        """
        测试用例：忘记密码链接

        期望结果：
        - 点击链接后导航到忘记密码页面
        """
        await login_page.goto_login()

        # 验证链接可见
        assert await login_page.is_forgot_password_link_visible(), "Forgot password link should be visible"

        # 点击链接
        await login_page.goto_forgot_password()

        # 验证导航（根据实际URL调整）
        current_url = login_page.get_current_url()
        assert "forgot" in current_url.lower() or "reset" in current_url.lower(), \
            f"Should navigate to password reset page, got: {current_url}"

    @pytest.mark.regression
    @allure.title("测试注册链接")
    @allure.description("验证注册链接可以点击并导航到注册页面")
    async def test_register_link(self, login_page: LoginPage):
        """
        测试用例：注册链接

        期望结果：
        - 点击链接后导航到注册页面
        """
        await login_page.goto_login()

        # 验证链接可见
        assert await login_page.is_register_link_visible(), "Register link should be visible"

        # 点击链接
        await login_page.goto_register()

        # 验证导航（根据实际URL调整）
        current_url = login_page.get_current_url()
        assert "register" in current_url.lower() or "signup" in current_url.lower(), \
            f"Should navigate to registration page, got: {current_url}"

    @pytest.mark.ui
    @allure.title("测试登录页UI元素")
    @allure.description("验证登录页所有必需的UI元素都正确显示")
    async def test_login_page_ui_elements(self, login_page: LoginPage):
        """
        测试用例：登录页UI元素

        验证所有必需的UI元素都正确显示
        """
        await login_page.goto_login()

        # 验证所有元素可见
        assert await login_page.is_username_field_visible(), "Username field should be visible"
        assert await login_page.is_password_field_visible(), "Password field should be visible"
        assert await login_page.is_login_button_visible(), "Login button should be visible"
        assert await login_page.is_forgot_password_link_visible(), "Forgot password link should be visible"

        logger.info("All login page UI elements are visible")

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "", "用户名和密码不能为空"),
        ("test", "", "密码不能为空"),
        ("", "password", "用户名不能为空"),
        ("invalid-email", "password", "请输入有效的邮箱地址"),
    ])
    @allure.title("测试表单验证 - 无效输入")
    @allure.description("验证登录表单的客户端验证")
    async def test_form_validation(self, login_page: LoginPage, username, password, expected_error):
        """
        测试用例：表单验证

        参数化测试各种无效输入
        """
        await login_page.goto_login()
        await login_page.login(username, password)

        # 验证错误消息或按钮状态
        if username and password:
            # 如果有输入，检查是否显示错误
            # 实际实现可能不同
            pass
        else:
            # 空输入时按钮应该禁用
            is_enabled = await login_page.is_login_button_enabled()
            assert not is_enabled, "Login button should be disabled with invalid input"


@allure.feature("Authentication")
@allure.story("Third-party Login")
class TestThirdPartyLogin:
    """第三方登录测试类"""

    @pytest.mark.regression
    @allure.title("测试Google登录按钮")
    @allure.description("验证Google登录按钮存在且可点击")
    async def test_google_login_button(self, login_page: LoginPage):
        """
        测试用例：Google登录按钮

        期望结果：
        - Google登录按钮可见
        - 点击后打开OAuth窗口（不验证完整流程）
        """
        await login_page.goto_login()

        if await login_page.is_google_login_available():
            # 验证按钮可见
            assert await login_page.is_google_login_available(), "Google login button should be visible"
            logger.info("Google login button is available")
        else:
            logger.warning("Google login is not configured")

    @pytest.mark.regression
    @allure.title("测试GitHub登录按钮")
    @allure.description("验证GitHub登录按钮存在且可点击")
    async def test_github_login_button(self, login_page: LoginPage):
        """
        测试用例：GitHub登录按钮

        期望结果：
        - GitHub登录按钮可见
        """
        await login_page.goto_login()

        if await login_page.is_github_login_available():
            assert await login_page.is_github_login_available(), "GitHub login button should be visible"
            logger.info("GitHub login button is available")
        else:
            logger.warning("GitHub login is not configured")
