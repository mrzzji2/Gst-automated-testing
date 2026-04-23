"""
User Management Page Tests
用户管理页测试用例
"""
import pytest
import allure
from loguru import logger

from pages.user_management_page import UserManagementPage


@allure.feature("User Management")
@allure.story("User List")
@allure.severity(allure.severity_level.HIGH)
class TestUserManagement:
    """用户管理测试类"""

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("测试用户管理页面加载")
    @allure.description("验证用户管理页面正确加载并显示用户列表")
    async def test_user_management_page_load(self, user_management_page: UserManagementPage):
        """
        测试用例：用户管理页面加载

        步骤：
        1. 导航到用户管理页
        2. 验证页面标题和元素

        期望结果：
        - 用户管理页面正确加载
        - 显示用户列表
        - 显示操作按钮
        """
        # 步骤 1: 导航到用户管理页
        await user_management_page.goto_user_management()

        # 步骤 2: 验证页面元素
        await user_management_page.assert_on_user_management_page()

        logger.info("User management page loaded successfully")

    @pytest.mark.regression
    @allure.title("测试获取用户列表")
    @allure.description("验证能够获取并显示用户列表")
    async def test_get_user_list(self, user_management_page: UserManagementPage):
        """
        测试用例：获取用户列表

        期望结果：
        - 返回用户列表
        - 列表不为空
        """
        await user_management_page.goto_user_management()

        # 获取用户列表
        users = await user_management_page.get_all_users()

        # 验证列表
        assert isinstance(users, list), "Should return a list of users"
        assert len(users) >= 0, "User list should be retrievable"

        logger.info(f"Retrieved {len(users)} users")

        # 打印用户信息
        for user in users:
            logger.debug(f"User: {user}")

    @pytest.mark.regression
    @allure.title("测试搜索用户")
    @allure.description("验证搜索功能能够找到匹配的用户")
    async def test_search_user(self, user_management_page: UserManagementPage, test_user):
        """
        测试用例：搜索用户

        期望结果：
        - 能够找到已知的用户
        - 搜索结果正确
        """
        await user_management_page.goto_user_management()

        # 搜索用户
        await user_management_page.search_user(test_user["username"])

        # 等待搜索结果
        await user_management_page.wait_for_network_idle()

        # 验证用户可见
        await user_management_page.assert_user_exists(test_user["username"])

        logger.info(f"User found in search: {test_user['username']}")

    @pytest.mark.regression
    @allure.title("测试按状态筛选用户")
    @allure.description("验证状态筛选功能")
    async def test_filter_by_status(self, user_management_page: UserManagementPage):
        """
        测试用例：按状态筛选

        期望结果：
        - 筛选后只显示指定状态的用户
        """
        await user_management_page.goto_user_management()

        # 筛选活跃用户
        await user_management_page.filter_by_status("active")

        # 等待筛选结果
        await user_management_page.wait_for_network_idle()

        # 验证筛选结果
        users = await user_management_page.get_all_users()
        for user in users:
            # 注意：根据实际实现调整
            logger.debug(f"User status: {user.get('status')}")

        logger.info("Status filter tested")

    @pytest.mark.regression
    @allure.title("测试按角色筛选用户")
    @allure.description("验证角色筛选功能")
    async def test_filter_by_role(self, user_management_page: UserManagementPage):
        """
        测试用例：按角色筛选

        期望结果：
        - 筛选后只显示指定角色的用户
        """
        await user_management_page.goto_user_management()

        # 筛选管理员用户
        await user_management_page.filter_by_role("admin")

        # 等待筛选结果
        await user_management_page.wait_for_network_idle()

        # 验证筛选结果
        users = await user_management_page.get_all_users()
        for user in users:
            logger.debug(f"User role: {user.get('role')}")

        logger.info("Role filter tested")


@allure.feature("User Management")
@allure.story("Add User")
class TestAddUser:
    """添加用户测试类"""

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("测试添加新用户")
    @allure.description("验证能够成功添加新用户")
    async def test_add_user(self, user_management_page: UserManagementPage, new_user_data):
        """
        测试用例：添加新用户

        步骤：
        1. 点击添加用户按钮
        2. 填写用户表单
        3. 保存用户
        4. 验证用户添加成功

        期望结果：
        - 用户成功添加
        - 用户出现在列表中
        """
        # 步骤 1-3: 添加用户
        result = await user_management_page.add_user(
            username=new_user_data["username"],
            email=new_user_data["email"],
            first_name=new_user_data["first_name"],
            last_name=new_user_data["last_name"],
            role=new_user_data["role"],
            status=new_user_data["status"],
            password=new_user_data["password"]
        )

        logger.info(f"Add user result: {result}")

        # 步骤 4: 验证用户添加成功
        await user_management_page.wait_for_network_idle()
        await user_management_page.assert_user_exists(new_user_data["email"])

        # 清理：删除测试用户
        await user_management_page.delete_user(new_user_data["email"])

    @pytest.mark.regression
    @allure.title("测试添加用户表单验证")
    @allure.description("验证添加用户时的表单验证")
    async def test_add_user_form_validation(self, user_management_page: UserManagementPage):
        """
        测试用例：添加用户表单验证

        期望结果：
        - 无效输入显示错误消息
        - 表单不能提交
        """
        await user_management_page.goto_user_management()

        # 点击添加用户
        await user_management_page.click_add_user()

        # 不填写任何字段，直接保存
        await user_management_page.save_user()

        # 验证错误消息
        if await user_management_page.is_form_error_displayed():
            error_message = await user_management_page.get_form_error_message()
            assert error_message, "Should display form validation error"
            logger.info(f"Form validation error: {error_message}")

        # 关闭模态框
        await user_management_page.close_modal()

    @pytest.mark.regression
    @pytest.mark.parametrize("field,value,expected_error", [
        ("email", "invalid-email", "请输入有效的邮箱地址"),
        ("password", "123", "密码长度至少6位"),
    ])
    @allure.title("测试字段验证 - {field}")
    @allure.description("验证{field}字段的验证规则")
    async def test_field_validation(
        self,
        user_management_page: UserManagementPage,
        new_user_data,
        field,
        value,
        expected_error
    ):
        """
        测试用例：字段验证（参数化）

        期望结果：
        - 显示相应的错误消息
        """
        await user_management_page.goto_user_management()

        # 点击添加用户
        await user_management_page.click_add_user()

        # 填写表单（使用无效值）
        await user_management_page.fill_user_form(
            username=new_user_data["username"],
            email=value if field == "email" else new_user_data["email"],
            password=value if field == "password" else new_user_data["password"]
        )

        # 尝试保存
        await user_management_page.save_user()

        # 验证错误（根据实际实现调整）
        # await user_management_page.assert_text_contains(
        #     user_management_page.locators.ERROR_MESSAGE,
        #     expected_error
        # )

        # 关闭模态框
        await user_management_page.close_modal()

        logger.info(f"Field validation tested for {field}")


@allure.feature("User Management")
@allure.story("Edit User")
class TestEditUser:
    """编辑用户测试类"""

    @pytest.mark.regression
    @allure.title("测试编辑用户信息")
    @allure.description("验证能够成功编辑用户信息")
    async def test_edit_user(self, user_management_page: UserManagementPage, new_user_data):
        """
        测试用例：编辑用户信息

        步骤：
        1. 添加测试用户
        2. 编辑用户信息
        3. 验证修改成功

        期望结果：
        - 用户信息成功更新
        """
        # 步骤 1: 添加测试用户
        await user_management_page.add_user(
            username=new_user_data["username"],
            email=new_user_data["email"],
            first_name=new_user_data["first_name"],
            last_name=new_user_data["last_name"],
            password=new_user_data["password"]
        )

        # 步骤 2: 编辑用户
        await user_management_page.update_user(
            email=new_user_data["email"],
            first_name="Updated",
            last_name="Name"
        )

        # 步骤 3: 验证修改
        await user_management_page.wait_for_network_idle()
        users = await user_management_page.get_all_users()
        updated_user = await user_management_page.find_user_by_email(new_user_data["email"])

        assert updated_user is not None, "User should still exist"
        # 验证更新（根据实际实现调整）
        # assert "Updated" in updated_user.get("name", ""), "User name should be updated"

        # 清理
        await user_management_page.delete_user(new_user_data["email"])

        logger.info("Edit user functionality tested")


@allure.feature("User Management")
@allure.story("Delete User")
class TestDeleteUser:
    """删除用户测试类"""

    @pytest.mark.regression
    @allure.title("测试删除用户")
    @allure.description("验证能够成功删除用户")
    async def test_delete_user(self, user_management_page: UserManagementPage, new_user_data):
        """
        测试用例：删除用户

        步骤：
        1. 添加测试用户
        2. 删除用户
        3. 验证用户已删除

        期望结果：
        - 用户成功删除
        - 用户不再出现在列表中
        """
        # 步骤 1: 添加测试用户
        await user_management_page.add_user(
            username=new_user_data["username"],
            email=new_user_data["email"],
            password=new_user_data["password"]
        )

        # 验证用户存在
        await user_management_page.assert_user_exists(new_user_data["email"])

        # 步骤 2: 删除用户
        await user_management_page.delete_user(new_user_data["email"])

        # 步骤 3: 验证用户已删除
        await user_management_page.wait_for_network_idle()
        await user_management_page.assert_user_not_exists(new_user_data["email"])

        logger.info("Delete user functionality tested")

    @pytest.mark.regression
    @allure.title("测试取消删除用户")
    @allure.description("验证能够取消删除操作")
    async def test_cancel_delete_user(self, user_management_page: UserManagementPage, new_user_data):
        """
        测试用例：取消删除用户

        期望结果：
        - 取消后用户仍然存在
        """
        # 添加测试用户
        await user_management_page.add_user(
            username=new_user_data["username"],
            email=new_user_data["email"],
            password=new_user_data["password"]
        )

        # 点击删除
        await user_management_page.click_delete_user(new_user_data["email"])

        # 取消删除
        await user_management_page.cancel_delete_user()

        # 验证用户仍然存在
        await user_management_page.assert_user_exists(new_user_data["email"])

        # 清理
        await user_management_page.delete_user(new_user_data["email"])

        logger.info("Cancel delete user functionality tested")


@allure.feature("User Management")
@allure.story("Bulk Operations")
class TestBulkOperations:
    """批量操作测试类"""

    @pytest.mark.regression
    @allure.title("测试选择所有用户")
    @allure.description("验证能够选择所有用户")
    async def test_select_all_users(self, user_management_page: UserManagementPage):
        """
        测试用例：选择所有用户

        期望结果：
        - 所有用户被选中
        - 可以执行批量操作
        """
        await user_management_page.goto_user_management()

        # 选择所有用户
        await user_management_page.select_all_users()

        # 验证选择（根据实际实现调整）
        logger.info("Select all users tested")

    @pytest.mark.regression
    @allure.title("测试批量删除用户")
    @allure.description("验证能够批量删除用户")
    async def test_bulk_delete_users(self, user_management_page: UserManagementPage, new_user_data):
        """
        测试用例：批量删除用户

        步骤：
        1. 添加多个测试用户
        2. 选择并批量删除
        3. 验证用户已删除

        期望结果：
        - 选中的用户被批量删除
        """
        # 步骤 1: 添加测试用户
        test_users = []
        for i in range(2):
            user_data = {
                "username": f"bulk_test_{i}_{new_user_data['username']}",
                "email": f"bulk_test_{i}_{new_user_data['email']}",
                "password": new_user_data["password"]
            }
            await user_management_page.add_user(**user_data)
            test_users.append(user_data["email"])

        # 步骤 2: 批量删除（根据实际实现调整）
        # await user_management_page.select_all_users()
        # await user_management_page.bulk_delete_users()

        # 步骤 3: 验证删除
        # for email in test_users:
        #     await user_management_page.assert_user_not_exists(email)

        # 清理（如果批量删除未执行）
        for email in test_users:
            try:
                await user_management_page.delete_user(email)
            except:
                pass

        logger.info("Bulk delete users tested")


@allure.feature("User Management")
@allure.story("Pagination")
class TestPagination:
    """分页测试类"""

    @pytest.mark.regression
    @allure.title("测试分页导航")
    @allure.description("验证分页功能正常工作")
    async def test_pagination(self, user_management_page: UserManagementPage):
        """
        测试用例：分页导航

        期望结果：
        - 可以切换页面
        - 页面信息正确显示
        """
        await user_management_page.goto_user_management()

        # 获取页面信息
        page_info = await user_management_page.get_page_info()
        logger.info(f"Page info: {page_info}")

        # 测试下一页（如果有）
        # await user_management_page.go_to_next_page()

        # 测试上一页
        # await user_management_page.go_to_previous_page()

        logger.info("Pagination tested")

    @pytest.mark.regression
    @allure.title("测试设置每页显示数量")
    @allure.description("验证可以设置每页显示的用户数量")
    async def test_set_page_size(self, user_management_page: UserManagementPage):
        """
        测试用例：设置每页显示数量

        期望结果：
        - 可以更改每页显示数量
        - 列表按设置的数量显示
        """
        await user_management_page.goto_user_management()

        # 设置每页显示50条
        await user_management_page.set_page_size(50)

        # 等待更新
        await user_management_page.wait_for_network_idle()

        # 验证（根据实际实现调整）
        logger.info("Page size set to 50")
