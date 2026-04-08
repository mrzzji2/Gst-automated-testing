"""
User Management Page
用户管理页面对象
"""
from playwright.async_api import Page
from typing import Dict, List
from loguru import logger

from pages.base_page import BasePage
from elements.user_management_locators import UserManagementLocators


class UserManagementPage(BasePage):
    """
    用户管理页面对象
    封装用户管理相关的所有操作
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        初始化用户管理页

        Args:
            page: Playwright Page 对象
            base_url: 基础URL
        """
        super().__init__(page, base_url)
        self.locators = UserManagementLocators

    # ==================== 导航操作 ====================

    async def goto_user_management(self):
        """导航到用户管理页"""
        await self.navigate("/users")

    # ==================== 用户列表操作 ====================

    async def get_user_count(self) -> int:
        """
        获取用户列表数量

        Returns:
            用户数量
        """
        return await self.count_elements(self.locators.TABLE_ROWS)

    async def get_all_users(self) -> List[Dict[str, str]]:
        """
        获取所有用户信息

        Returns:
            用户信息列表
        """
        users = []
        row_count = await self.get_user_count()

        for i in range(row_count):
            try:
                row = f"{self.locators.TABLE_ROWS}:nth-child({i+1})"
                user = {
                    "name": await self.get_text(f"{row} {self.locators.NAME_COLUMN}"),
                    "email": await self.get_text(f"{row} {self.locators.EMAIL_COLUMN}"),
                    "role": await self.get_text(f"{row} {self.locators.ROLE_COLUMN}"),
                    "status": await self.get_text(f"{row} {self.locators.STATUS_COLUMN}")
                }
                users.append(user)
            except Exception as e:
                logger.warning(f"Failed to get user at row {i+1}: {e}")

        return users

    async def find_user_by_email(self, email: str) -> Dict[str, str]:
        """
        根据邮箱查找用户

        Args:
            email: 用户邮箱

        Returns:
            用户信息字典，未找到返回None
        """
        users = await self.get_all_users()
        for user in users:
            if user.get("email", "").lower() == email.lower():
                return user
        return None

    async def is_user_visible(self, email: str) -> bool:
        """
        检查用户是否在列表中可见

        Args:
            email: 用户邮箱

        Returns:
            用户是否可见
        """
        return await self.find_user_by_email(email) is not None

    # ==================== 搜索和筛选 ====================

    async def search_user(self, query: str):
        """
        搜索用户

        Args:
            query: 搜索关键词（邮箱或姓名）
        """
        await self.type_text(self.locators.SEARCH_INPUT, query)
        logger.info(f"Searched for user: {query}")

    async def clear_search(self):
        """清空搜索"""
        await self.clear_text(self.locators.SEARCH_INPUT)
        logger.debug("Cleared search")

    async def filter_by_status(self, status: str):
        """
        按状态筛选用户

        Args:
            status: 用户状态 (active, inactive, pending, suspended)
        """
        await self.select_option(self.locators.STATUS_FILTER, status)
        logger.info(f"Filtered by status: {status}")

    async def filter_by_role(self, role: str):
        """
        按角色筛选用户

        Args:
            role: 用户角色 (admin, user, moderator, guest)
        """
        await self.select_option(self.locators.ROLE_FILTER, role)
        logger.info(f"Filtered by role: {role}")

    async def clear_filters(self):
        """清空所有筛选"""
        await self.click(self.locators.CLEAR_SEARCH_BUTTON)
        logger.debug("Cleared filters")

    # ==================== 添加用户操作 ====================

    async def click_add_user(self):
        """点击添加用户按钮"""
        await self.click(self.locators.ADD_USER_BUTTON)
        logger.info("Clicked add user button")

    async def fill_user_form(
        self,
        username: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
        role: str = "user",
        status: str = "active",
        password: str = "",
        confirm_password: str = ""
    ):
        """
        填写用户表单

        Args:
            username: 用户名
            email: 邮箱
            first_name: 名
            last_name: 姓
            role: 角色
            status: 状态
            password: 密码
            confirm_password: 确认密码
        """
        await self.type_text(self.locators.USERNAME_INPUT, username)
        await self.type_text(self.locators.EMAIL_INPUT, email)

        if first_name:
            await self.type_text(self.locators.FIRST_NAME_INPUT, first_name)
        if last_name:
            await self.type_text(self.locators.LAST_NAME_INPUT, last_name)

        await self.select_option(self.locators.ROLE_SELECT, role)
        await self.select_option(self.locators.STATUS_SELECT, status)

        if password:
            await self.type_text(self.locators.PASSWORD_INPUT, password)
        if confirm_password:
            await self.type_text(self.locators.CONFIRM_PASSWORD_INPUT, confirm_password)

        logger.debug(f"Filled user form for: {username}")

    async def save_user(self):
        """保存用户"""
        await self.click(self.locators.SAVE_BUTTON)
        logger.info("Saved user")

    async def cancel_user_form(self):
        """取消用户表单"""
        await self.click(self.locators.CANCEL_BUTTON)
        logger.info("Cancelled user form")

    async def add_user(
        self,
        username: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
        role: str = "user",
        status: str = "active",
        password: str = ""
    ) -> str:
        """
        添加用户（完整流程）

        Args:
            username: 用户名
            email: 邮箱
            first_name: 名
            last_name: 姓
            role: 角色
            status: 状态
            password: 密码

        Returns:
            操作结果消息
        """
        await self.click_add_user()
        await self.fill_user_form(username, email, first_name, last_name, role, status, password, password)
        await self.save_user()

        # 等待操作完成
        await self.wait_for_network_idle()

        # 返回成功/错误消息
        if await self.is_visible(self.locators.SUCCESS_TOAST, timeout=5000):
            return await self.get_text(self.locators.SUCCESS_TOAST)
        elif await self.is_visible(self.locators.ERROR_TOAST, timeout=5000):
            return await self.get_text(self.locators.ERROR_TOAST)

        return "User added successfully"

    # ==================== 编辑用户操作 ====================

    async def click_edit_user(self, email: str):
        """
        点击编辑用户

        Args:
            email: 用户邮箱
        """
        # 找到包含该邮箱的行
        users = await self.get_all_users()
        for i, user in enumerate(users):
            if user.get("email", "").lower() == email.lower():
                row = f"{self.locators.TABLE_ROWS}:nth-child({i+1})"
                await self.click(f"{row} {self.locators.EDIT_USER_BUTTON}")
                logger.info(f"Clicked edit user: {email}")
                return

        raise ValueError(f"User not found: {email}")

    async def update_user(self, email: str, **kwargs):
        """
        更新用户信息

        Args:
            email: 用户邮箱
            **kwargs: 要更新的字段

        Returns:
            操作结果消息
        """
        await self.click_edit_user(email)

        # 更新字段
        if "first_name" in kwargs:
            await self.type_text(self.locators.FIRST_NAME_INPUT, kwargs["first_name"], clear=True)
        if "last_name" in kwargs:
            await self.type_text(self.locators.LAST_NAME_INPUT, kwargs["last_name"], clear=True)
        if "role" in kwargs:
            await self.select_option(self.locators.ROLE_SELECT, kwargs["role"])
        if "status" in kwargs:
            await self.select_option(self.locators.STATUS_SELECT, kwargs["status"])

        await self.save_user()
        await self.wait_for_network_idle()

        logger.info(f"Updated user: {email}")
        return "User updated successfully"

    # ==================== 删除用户操作 ====================

    async def click_delete_user(self, email: str):
        """
        点击删除用户

        Args:
            email: 用户邮箱
        """
        users = await self.get_all_users()
        for i, user in enumerate(users):
            if user.get("email", "").lower() == email.lower():
                row = f"{self.locators.TABLE_ROWS}:nth-child({i+1})"
                await self.click(f"{row} {self.locators.DELETE_USER_BUTTON}")
                logger.info(f"Clicked delete user: {email}")
                return

        raise ValueError(f"User not found: {email}")

    async def confirm_delete_user(self):
        """确认删除用户"""
        await self.click(self.locators.CONFIRM_DELETE_BUTTON)
        logger.info("Confirmed delete user")

    async def cancel_delete_user(self):
        """取消删除用户"""
        await self.click(self.locators.CANCEL_DELETE_BUTTON)
        logger.info("Cancelled delete user")

    async def delete_user(self, email: str) -> str:
        """
        删除用户（完整流程）

        Args:
            email: 用户邮箱

        Returns:
            操作结果消息
        """
        await self.click_delete_user(email)
        await self.confirm_delete_user()
        await self.wait_for_network_idle()

        logger.info(f"Deleted user: {email}")
        return "User deleted successfully"

    # ==================== 批量操作 ====================

    async def select_all_users(self):
        """选择所有用户"""
        await self.check_checkbox(self.locators.SELECT_ALL_CHECKBOX)
        logger.info("Selected all users")

    async def select_user_by_index(self, index: int):
        """
        根据索引选择用户

        Args:
            index: 行索引（从1开始）
        """
        row = f"{self.locators.TABLE_ROWS}:nth-child({index})"
        checkbox = f"{row} {self.locators.CHECKBOX_COLUMN}"
        await self.check_checkbox(checkbox)
        logger.debug(f"Selected user at index {index}")

    async def bulk_delete_users(self):
        """批量删除用户"""
        await self.click(self.locators.BULK_DELETE_BUTTON)
        await self.confirm_delete_user()
        logger.info("Bulk deleted users")

    async def bulk_activate_users(self):
        """批量激活用户"""
        await self.click(self.locators.BULK_ACTIVATE_BUTTON)
        logger.info("Bulk activated users")

    async def bulk_deactivate_users(self):
        """批量停用用户"""
        await self.click(self.locators.BULK_DEACTIVATE_BUTTON)
        logger.info("Bulk deactivated users")

    # ==================== 分页操作 ====================

    async def go_to_next_page(self):
        """跳转到下一页"""
        await self.click(self.locators.NEXT_PAGE)
        logger.debug("Navigated to next page")

    async def go_to_previous_page(self):
        """跳转到上一页"""
        await self.click(self.locators.PREVIOUS_PAGE)
        logger.debug("Navigated to previous page")

    async def get_page_info(self) -> str:
        """
        获取分页信息

        Returns:
            分页信息文本
        """
        return await self.get_text(self.locators.PAGE_INFO)

    async def set_page_size(self, size: int):
        """
        设置每页显示数量

        Args:
            size: 每页数量
        """
        await self.select_option(self.locators.PAGE_SIZE_SELECT, str(size))
        logger.info(f"Set page size to {size}")

    # ==================== 导入导出 ====================

    async def click_import_users(self):
        """点击导入用户按钮"""
        await self.click(self.locators.IMPORT_USERS_BUTTON)
        logger.info("Clicked import users button")

    async def click_export_users(self):
        """点击导出用户按钮"""
        await self.click(self.locators.EXPORT_USERS_BUTTON)
        logger.info("Clicked export users button")

    # ==================== 验证操作 ====================

    async def assert_on_user_management_page(self):
        """断言在用户管理页"""
        await self.assert_element_visible(self.locators.PAGE_TITLE)
        logger.debug("Verified on user management page")

    async def assert_user_exists(self, email: str):
        """
        断言用户存在

        Args:
            email: 用户邮箱
        """
        assert await self.is_user_visible(email), f"User not found: {email}"
        logger.debug(f"Verified user exists: {email}")

    async def assert_user_not_exists(self, email: str):
        """
        断言用户不存在

        Args:
            email: 用户邮箱
        """
        assert not await self.is_user_visible(email), f"User should not exist: {email}"
        logger.debug(f"Verified user does not exist: {email}")

    async def assert_user_status(self, email: str, status: str):
        """
        断言用户状态

        Args:
            email: 用户邮箱
            status: 期望状态
        """
        user = await self.find_user_by_email(email)
        assert user is not None, f"User not found: {email}"
        assert user.get("status", "").lower() == status.lower(), f"User status mismatch: expected {status}, got {user.get('status')}"
        logger.debug(f"Verified user status: {email} is {status}")

    async def assert_user_role(self, email: str, role: str):
        """
        断言用户角色

        Args:
            email: 用户邮箱
            role: 期望角色
        """
        user = await self.find_user_by_email(email)
        assert user is not None, f"User not found: {email}"
        assert user.get("role", "").lower() == role.lower(), f"User role mismatch: expected {role}, got {user.get('role')}"
        logger.debug(f"Verified user role: {email} is {role}")

    # ==================== 表单验证 ====================

    async def is_form_error_displayed(self) -> bool:
        """检查表单错误是否显示"""
        return await self.is_visible(self.locators.ERROR_MESSAGE)

    async def get_form_error_message(self) -> str:
        """获取表单错误消息"""
        return await self.get_text(self.locators.ERROR_MESSAGE)

    async def is_modal_open(self) -> bool:
        """检查用户模态框是否打开"""
        return await self.is_visible(self.locators.USER_MODAL)

    async def close_modal(self):
        """关闭模态框"""
        await self.click(self.locators.MODAL_CLOSE)
        logger.debug("Closed user modal")

    # ==================== 空状态 ====================

    async def is_empty_state_visible(self) -> bool:
        """检查空状态是否显示"""
        return await self.is_visible(self.locators.EMPTY_STATE)

    async def get_empty_state_message(self) -> str:
        """获取空状态消息"""
        return await self.get_text(self.locators.EMPTY_STATE_MESSAGE)
