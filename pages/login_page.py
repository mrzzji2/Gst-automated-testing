"""
Login Page
登录页面对象
"""
from playwright.async_api import Page
from loguru import logger

from pages.base_page import BasePage
from elements.login_locators import LoginLocators


class LoginPage(BasePage):
    """
    登录页面对象
    封装登录相关的所有操作
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        初始化登录页

        Args:
            page: Playwright Page 对象
            base_url: 基础URL
        """
        super().__init__(page, base_url)
        self.locators = LoginLocators

    # ==================== 导航操作 ====================

    async def goto_login(self):
        """导航到登录页"""
        await self.navigate(self.locators.LOGIN_FORM)

    async def goto_register(self):
        """导航到注册页"""
        await self.click(self.locators.REGISTER_LINK)
        logger.info("Navigated to registration page")

    async def goto_forgot_password(self):
        """导航到忘记密码页"""
        await self.click(self.locators.FORGOT_PASSWORD_LINK)
        logger.info("Navigated to forgot password page")

    # ==================== 登录操作 ====================

    async def login(self, username: str, password: str, remember_me: bool = False):
        """
        执行登录操作

        Args:
            username: 用户名/邮箱
            password: 密码
            remember_me: 是否记住我
        """
        # 输入用户名
        await self.type_text(self.locators.USERNAME_INPUT, username)
        logger.debug(f"Entered username: {username}")

        # 输入密码
        await self.type_text(self.locators.PASSWORD_INPUT, password)
        logger.debug("Entered password")

        # 记住我
        if remember_me:
            await self.check_checkbox(self.locators.REMEMBER_ME_CHECKBOX)
            logger.debug("Remember me checked")

        # 点击登录按钮
        await self.click(self.locators.LOGIN_BUTTON)
        logger.info(f"Login attempt with username: {username}")

    async def login_with_google(self):
        """使用Google登录"""
        await self.click(self.locators.GOOGLE_LOGIN_BUTTON)
        logger.info("Clicked Google login")

    async def login_with_github(self):
        """使用GitHub登录"""
        await self.click(self.locators.GITHUB_LOGIN_BUTTON)
        logger.info("Clicked GitHub login")

    # ==================== 表单操作 ====================

    async def enter_username(self, username: str):
        """
        输入用户名

        Args:
            username: 用户名
        """
        await self.type_text(self.locators.USERNAME_INPUT, username)
        logger.debug(f"Entered username: {username}")

    async def enter_password(self, password: str):
        """
        输入密码

        Args:
            password: 密码
        """
        await self.type_text(self.locators.PASSWORD_INPUT, password)
        logger.debug("Entered password")

    async def click_login_button(self):
        """点击登录按钮"""
        await self.click(self.locators.LOGIN_BUTTON)
        logger.info("Clicked login button")

    async def toggle_remember_me(self):
        """切换记住我选项"""
        await self.click(self.locators.REMEMBER_ME_CHECKBOX)
        logger.debug("Toggled remember me")

    # ==================== 验证操作 ====================

    async def is_login_button_enabled(self) -> bool:
        """
        检查登录按钮是否可用

        Returns:
            按钮是否可用
        """
        return await self.is_enabled(self.locators.LOGIN_BUTTON)

    async def get_error_message(self) -> str:
        """
        获取错误消息

        Returns:
            错误消息文本
        """
        return await self.get_text(self.locators.ERROR_MESSAGE)

    async def is_error_displayed(self) -> bool:
        """
        检查是否显示错误消息

        Returns:
            是否显示错误
        """
        return await self.is_visible(self.locators.ERROR_MESSAGE)

    async def assert_on_login_page(self):
        """断言在登录页"""
        await self.assert_element_visible(self.locators.LOGIN_FORM)
        logger.debug("Verified on login page")

    async def assert_error_message(self, expected_message: str):
        """
        断言错误消息

        Args:
            expected_message: 期望的错误消息
        """
        await self.assert_text_contains(self.locators.ERROR_MESSAGE, expected_message)
        logger.debug(f"Verified error message: {expected_message}")

    # ==================== 页面元素状态 ====================

    async def is_username_field_visible(self) -> bool:
        """检查用户名输入框是否可见"""
        return await self.is_visible(self.locators.USERNAME_INPUT)

    async def is_password_field_visible(self) -> bool:
        """检查密码输入框是否可见"""
        return await self.is_visible(self.locators.PASSWORD_INPUT)

    async def is_login_button_visible(self) -> bool:
        """检查登录按钮是否可见"""
        return await self.is_visible(self.locators.LOGIN_BUTTON)

    async def is_forgot_password_link_visible(self) -> bool:
        """检查忘记密码链接是否可见"""
        return await self.is_visible(self.locators.FORGOT_PASSWORD_LINK)

    async def is_register_link_visible(self) -> bool:
        """检查注册链接是否可见"""
        return await self.is_visible(self.locators.REGISTER_LINK)

    # ==================== 第三方登录状态 ====================

    async def is_google_login_available(self) -> bool:
        """检查Google登录是否可用"""
        return await self.is_visible(self.locators.GOOGLE_LOGIN_BUTTON)

    async def is_github_login_available(self) -> bool:
        """检查GitHub登录是否可用"""
        return await self.is_visible(self.locators.GITHUB_LOGIN_BUTTON)

    # ==================== 清空表单 ====================

    async def clear_form(self):
        """清空登录表单"""
        await self.clear_text(self.locators.USERNAME_INPUT)
        await self.clear_text(self.locators.PASSWORD_INPUT)
        logger.debug("Cleared login form")
