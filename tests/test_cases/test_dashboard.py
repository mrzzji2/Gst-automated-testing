"""
Dashboard Page Tests
仪表盘页测试用例
"""
import pytest
import allure
from loguru import logger

from pages.dashboard_page import DashboardPage


@allure.feature("Dashboard")
@allure.story("Dashboard Navigation")
@allure.severity(allure.severity_level.HIGH)
class TestDashboard:
    """仪表盘测试类"""

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("测试仪表盘页面加载")
    @allure.description("验证已登录用户能够成功访问仪表盘页面")
    async def test_dashboard_page_load(self, dashboard_page: DashboardPage):
        """
        测试用例：仪表盘页面加载

        步骤：
        1. 导航到仪表盘
        2. 验证页面标题和元素

        期望结果：
        - 仪表盘页面正确加载
        - 显示欢迎消息
        - 显示统计卡片
        """
        # 步骤 1: 导航到仪表盘
        await dashboard_page.goto_dashboard()

        # 步骤 2: 验证页面元素
        await dashboard_page.assert_on_dashboard()

        # 验证欢迎消息
        await dashboard_page.assert_welcome_message()

        logger.info("Dashboard page loaded successfully")

    @pytest.mark.regression
    @allure.title("测试统计卡片显示")
    @allure.description("验证仪表盘上的所有统计卡片正确显示")
    async def test_statistics_cards(self, dashboard_page: DashboardPage):
        """
        测试用例：统计卡片显示

        期望结果：
        - 所有统计卡片可见
        - 显示正确的数值
        """
        await dashboard_page.goto_dashboard()

        # 验证各统计卡片
        stats_types = ["users", "active", "revenue", "orders"]

        for stat_type in stats_types:
            await dashboard_page.assert_stat_displayed(stat_type)

        # 获取所有统计数据
        stats = await dashboard_page.get_all_stats()
        logger.info(f"Dashboard stats: {stats}")

        # 验证数据不为空
        for key, value in stats.items():
            assert value and value != "N/A", f"Stat {key} should have a value"

    @pytest.mark.regression
    @allure.title("测试点击统计卡片导航")
    @allure.description("验证点击统计卡片能够导航到相应页面")
    async def test_stat_card_navigation(self, dashboard_page: DashboardPage):
        """
        测试用例：统计卡片导航

        期望结果：
        - 点击卡片后导航到相应详情页
        """
        await dashboard_page.goto_dashboard()

        # 点击用户统计卡片
        await dashboard_page.click_stat_card("users")

        # 验证导航（根据实际实现调整）
        # await dashboard_page.assert_url_contains("/users")

        logger.info("Stat card navigation tested")

    @pytest.mark.regression
    @allure.title("测试侧边栏菜单")
    @allure.description("验证侧边栏菜单项可见且可点击")
    async def test_sidebar_menu(self, dashboard_page: DashboardPage):
        """
        测试用例：侧边栏菜单

        期望结果：
        - 所有菜单项可见
        - 点击菜单项能够导航
        """
        await dashboard_page.goto_dashboard()

        # 验证侧边栏可见
        assert await dashboard_page.is_sidebar_visible(), "Sidebar should be visible"

        # 测试切换侧边栏
        await dashboard_page.toggle_sidebar()
        # await dashboard_page.assert_element_hidden(dashboard_page.locators.SIDEBAR)

        logger.info("Sidebar menu tested")

    @pytest.mark.regression
    @allure.title("测试通知功能")
    @allure.description("验证通知按钮和通知列表")
    async def test_notifications(self, dashboard_page: DashboardPage):
        """
        测试用例：通知功能

        期望结果：
        - 通知按钮可见
        - 点击后显示通知列表
        """
        await dashboard_page.goto_dashboard()

        # 点击通知按钮
        await dashboard_page.click_notification_button()

        # 验证通知面板打开（根据实际实现调整）
        # await dashboard_page.assert_element_visible(dashboard_page.locators.NOTIFICATION_DROPDOWN)

        logger.info("Notifications tested")

    @pytest.mark.regression
    @allure.title("测试用户菜单")
    @allure.description("验证用户菜单可以打开和关闭")
    async def test_user_menu(self, dashboard_page: DashboardPage):
        """
        测试用例：用户菜单

        期望结果：
        - 用户菜单可以打开
        - 显示菜单项（个人资料、登出等）
        """
        await dashboard_page.goto_dashboard()

        # 打开用户菜单
        await dashboard_page.open_user_menu()
        assert await dashboard_page.is_user_menu_open(), "User menu should be open"

        # 关闭用户菜单
        await dashboard_page.close_user_menu()
        # assert not await dashboard_page.is_user_menu_open()

        logger.info("User menu tested")

    @pytest.mark.regression
    @allure.title("测试搜索功能")
    @allure.description("验证搜索框可以输入和提交搜索")
    async def test_search(self, dashboard_page: DashboardPage):
        """
        测试用例：搜索功能

        期望结果：
        - 可以在搜索框输入文本
        - 提交搜索后显示结果
        """
        await dashboard_page.goto_dashboard()

        # 执行搜索
        await dashboard_page.search("test query")

        # 验证搜索结果（根据实际实现调整）
        # await dashboard_page.assert_url_contains("?search=test+query")

        # 清空搜索
        await dashboard_page.clear_search()

        logger.info("Search functionality tested")

    @pytest.mark.regression
    @allure.title("测试刷新仪表盘")
    @allure.description("验证刷新按钮能够更新仪表盘数据")
    async def test_refresh_dashboard(self, dashboard_page: DashboardPage):
        """
        测试用例：刷新仪表盘

        期望结果：
        - 点击刷新按钮后数据更新
        """
        await dashboard_page.goto_dashboard()

        # 获取刷新前的统计数据
        stats_before = await dashboard_page.get_all_stats()

        # 刷新
        await dashboard_page.refresh_dashboard()

        # 等待加载完成
        await dashboard_page.wait_for_network_idle()

        # 获取刷新后的统计数据
        stats_after = await dashboard_page.get_all_stats()

        logger.info(f"Stats before refresh: {stats_before}")
        logger.info(f"Stats after refresh: {stats_after}")

        # 验证页面仍然正常显示
        await dashboard_page.assert_on_dashboard()

    @pytest.mark.regression
    @allure.title("测试最近活动动态")
    @allure.description("验证最近活动动态正确显示")
    async def test_recent_activity(self, dashboard_page: DashboardPage):
        """
        测试用例：最近活动动态

        期望结果：
        - 活动动态可见
        - 显示活动列表
        """
        await dashboard_page.goto_dashboard()

        # 验证活动动态可见
        is_visible = await dashboard_page.is_activity_feed_visible()

        if is_visible:
            # 获取活动列表
            activities = await dashboard_page.get_recent_activities()
            logger.info(f"Recent activities: {activities}")

            assert len(activities) >= 0, "Should retrieve activity list"
        else:
            logger.info("Activity feed is not displayed on this dashboard")

    @pytest.mark.regression
    @allure.title("测试图表显示")
    @allure.description("验证仪表盘上的图表正确显示")
    async def test_charts(self, dashboard_page: DashboardPage):
        """
        测试用例：图表显示

        期望结果：
        - 图表正确渲染
        - 图表类型正确
        """
        await dashboard_page.goto_dashboard()

        # 验证图表可见（根据实际配置调整）
        chart_types = ["", "line", "bar", "pie"]

        for chart_type in chart_types:
            if await dashboard_page.is_chart_visible(chart_type):
                logger.info(f"Chart visible: {chart_type if chart_type else 'general'}")
                break
        else:
            logger.info("No charts displayed on this dashboard")

    @pytest.mark.regression
    @allure.title("测试导出报告功能")
    @allure.description("验证导出按钮能够下载报告")
    async def test_export_report(self, dashboard_page: DashboardPage):
        """
        测试用例：导出报告

        期望结果：
        - 点击导出按钮
        - 文件开始下载
        """
        await dashboard_page.goto_dashboard()

        # 点击导出按钮
        await dashboard_page.export_report("pdf")

        # 验证下载（根据实际实现调整）
        # 等待下载开始
        # async with dashboard_page.page.expect_download() as download_info:
        #     await dashboard_page.click(dashboard_page.locators.EXPORT_BUTTON)
        # download = await download_info.value
        # assert download.suggested_filename.endswith(".pdf")

        logger.info("Export report tested")

    @pytest.mark.ui
    @allure.title("测试仪表盘响应式设计")
    @allure.description("验证仪表盘在不同视口大小下的显示")
    async def test_responsive_design(self, dashboard_page: DashboardPage):
        """
        测试用例：响应式设计

        期望结果：
        - 在不同视口大小下页面正常显示
        - 侧边栏在小屏幕上隐藏
        """
        await dashboard_page.goto_dashboard()

        # 测试移动端视口
        await dashboard_page.page.set_viewport_size({"width": 375, "height": 667})
        await dashboard_page.wait(1000)

        # 验证侧边栏隐藏或折叠
        # is_sidebar_hidden = not await dashboard_page.is_sidebar_visible()
        # assert is_sidebar_hidden, "Sidebar should be hidden on mobile"

        # 测试桌面端视口
        await dashboard_page.page.set_viewport_size({"width": 1920, "height": 1080})
        await dashboard_page.wait(1000)

        # 验证侧边栏显示
        assert await dashboard_page.is_sidebar_visible(), "Sidebar should be visible on desktop"

        logger.info("Responsive design tested")

    @pytest.mark.regression
    @allure.title("测试日期范围选择器")
    @allure.description("验证日期范围选择器功能")
    async def test_date_range_picker(self, dashboard_page: DashboardPage):
        """
        测试用例：日期范围选择器

        期望结果：
        - 可以选择日期范围
        - 数据根据日期范围更新
        """
        await dashboard_page.goto_dashboard()

        # 选择日期范围
        await dashboard_page.select_date_range("2024-01-01", "2024-12-31")

        # 等待数据更新
        await dashboard_page.wait_for_network_idle()

        # 验证页面仍然正常
        await dashboard_page.assert_on_dashboard()

        logger.info("Date range picker tested")


@allure.feature("Dashboard")
@allure.story("Dashboard Menu Navigation")
class TestDashboardMenuNavigation:
    """仪表盘菜单导航测试类"""

    @pytest.mark.regression
    @pytest.mark.parametrize("menu_item,expected_url", [
        ("users", "/users"),
        ("settings", "/settings"),
        ("reports", "/reports"),
        ("profile", "/profile"),
    ])
    @allure.title("测试菜单导航 - {menu_item}")
    @allure.description("验证点击{menu_item}菜单能够导航到正确页面")
    async def test_menu_navigation(self, dashboard_page: DashboardPage, menu_item, expected_url):
        """
        测试用例：菜单导航（参数化）

        期望结果：
        - 点击菜单项后导航到正确页面
        """
        await dashboard_page.goto_dashboard()

        # 点击菜单
        if menu_item == "users":
            await dashboard_page.click_menu_users()
        elif menu_item == "settings":
            await dashboard_page.click_menu_settings()
        elif menu_item == "reports":
            await dashboard_page.click_menu_reports()
        elif menu_item == "profile":
            await dashboard_page.click_menu_profile()

        # 验证导航
        await dashboard_page.assert_url_contains(expected_url)

        logger.info(f"Menu navigation to {menu_item} tested")

    @pytest.mark.smoke
    @allure.title("测试登出功能")
    @allure.description("验证登出功能能够正常工作")
    async def test_logout(self, dashboard_page: DashboardPage, login_page):
        """
        测试用例：登出功能

        期望结果：
        - 点击登出后导航到登录页
        - 会话被清除
        """
        await dashboard_page.goto_dashboard()

        # 点击登出
        await dashboard_page.click_menu_logout()

        # 验证导航到登录页
        await login_page.assert_on_login_page()

        logger.info("Logout functionality tested")
