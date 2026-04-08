"""
Dashboard Page
仪表盘页面对象
"""
from playwright.async_api import Page
from typing import Dict, List
from loguru import logger

from pages.base_page import BasePage
from elements.dashboard_locators import DashboardLocators


class DashboardPage(BasePage):
    """
    仪表盘页面对象
    封装仪表盘相关的所有操作
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        初始化仪表盘页

        Args:
            page: Playwright Page 对象
            base_url: 基础URL
        """
        super().__init__(page, base_url)
        self.locators = DashboardLocators

    # ==================== 导航操作 ====================

    async def goto_dashboard(self):
        """导航到仪表盘"""
        await self.navigate("/dashboard")

    async def click_menu_users(self):
        """点击用户管理菜单"""
        await self.click(self.locators.MENU_USERS)
        logger.info("Clicked users menu")

    async def click_menu_settings(self):
        """点击设置菜单"""
        await self.click(self.locators.MENU_SETTINGS)
        logger.info("Clicked settings menu")

    async def click_menu_reports(self):
        """点击报告菜单"""
        await self.click(self.locators.MENU_REPORTS)
        logger.info("Clicked reports menu")

    async def click_menu_profile(self):
        """点击个人资料菜单"""
        await self.click(self.locators.MENU_PROFILE)
        logger.info("Clicked profile menu")

    async def click_menu_logout(self):
        """点击登出菜单"""
        await self.click(self.locators.MENU_LOGOUT)
        logger.info("Clicked logout menu")

    # ==================== 侧边栏操作 ====================

    async def toggle_sidebar(self):
        """切换侧边栏显示/隐藏"""
        await self.click(self.locators.SIDEBAR_TOGGLE)
        logger.debug("Toggled sidebar")

    async def is_sidebar_visible(self) -> bool:
        """检查侧边栏是否可见"""
        return await self.is_visible(self.locators.SIDEBAR)

    # ==================== 统计卡片操作 ====================

    async def get_stat_value(self, stat_type: str) -> str:
        """
        获取统计数值

        Args:
            stat_type: 统计类型 (users, active, revenue, orders)

        Returns:
            统计数值
        """
        stat_cards = {
            "users": self.locators.TOTAL_USERS_CARD,
            "active": self.locators.ACTIVE_USERS_CARD,
            "revenue": self.locators.TOTAL_REVENUE_CARD,
            "orders": self.locators.TOTAL_ORDERS_CARD
        }

        selector = stat_cards.get(stat_type)
        if selector:
            await self.assert_element_visible(selector)
            return await self.get_text(f"{selector} {self.locators.STAT_VALUE}")

        return ""

    async def get_all_stats(self) -> Dict[str, str]:
        """
        获取所有统计数据

        Returns:
            统计数据字典
        """
        stats = {}
        stat_types = ["users", "active", "revenue", "orders"]

        for stat_type in stat_types:
            try:
                value = await self.get_stat_value(stat_type)
                stats[stat_type] = value
            except:
                stats[stat_type] = "N/A"

        logger.debug(f"Retrieved stats: {stats}")
        return stats

    async def click_stat_card(self, stat_type: str):
        """
        点击统计卡片

        Args:
            stat_type: 统计类型
        """
        stat_cards = {
            "users": self.locators.TOTAL_USERS_CARD,
            "active": self.locators.ACTIVE_USERS_CARD,
            "revenue": self.locators.TOTAL_REVENUE_CARD,
            "orders": self.locators.TOTAL_ORDERS_CARD
        }

        selector = stat_cards.get(stat_type)
        if selector:
            await self.click(selector)
            logger.info(f"Clicked {stat_type} stat card")

    # ==================== 通知操作 ====================

    async def click_notification_button(self):
        """点击通知按钮"""
        await self.click(self.locators.NOTIFICATION_BUTTON)
        logger.info("Clicked notification button")

    async def get_notification_count(self) -> int:
        """
        获取未读通知数量

        Returns:
            通知数量
        """
        try:
            badge_text = await self.get_text(self.locators.NOTIFICATION_BADGE)
            return int(badge_text)
        except:
            return 0

    async def is_notification_badge_visible(self) -> bool:
        """检查通知徽章是否可见"""
        return await self.is_visible(self.locators.NOTIFICATION_BADGE)

    # ==================== 搜索操作 ====================

    async def search(self, query: str):
        """
        执行搜索

        Args:
            query: 搜索关键词
        """
        await self.type_text(self.locators.SEARCH_INPUT, query)
        await self.click(self.locators.SEARCH_BUTTON)
        logger.info(f"Searched for: {query}")

    async def clear_search(self):
        """清空搜索"""
        await self.clear_text(self.locators.SEARCH_INPUT)
        logger.debug("Cleared search")

    # ==================== 用户菜单操作 ====================

    async def open_user_menu(self):
        """打开用户菜单"""
        await self.click(self.locators.USER_MENU_TOGGLE)
        logger.debug("Opened user menu")

    async def close_user_menu(self):
        """关闭用户菜单"""
        await self.click(self.locators.USER_MENU_TOGGLE)
        logger.debug("Closed user menu")

    async def is_user_menu_open(self) -> bool:
        """检查用户菜单是否打开"""
        return await self.is_visible(self.locators.USER_MENU_ITEMS)

    # ==================== 导出操作 ====================

    async def export_report(self, format: str = "pdf"):
        """
        导出报告

        Args:
            format: 导出格式 (pdf, excel, csv)
        """
        await self.click(self.locators.EXPORT_BUTTON)
        # 这里需要根据实际UI处理导出格式选择
        logger.info(f"Exported report as {format}")

    # ==================== 刷新操作 ====================

    async def refresh_dashboard(self):
        """刷新仪表盘"""
        await self.click(self.locators.REFRESH_BUTTON)
        logger.info("Refreshed dashboard")

    # ==================== 验证操作 ====================

    async def assert_on_dashboard(self):
        """断言在仪表盘页"""
        await self.assert_element_visible(self.locators.PAGE_TITLE)
        logger.debug("Verified on dashboard page")

    async def assert_welcome_message(self, username: str = ""):
        """
        断言欢迎消息

        Args:
            username: 用户名（可选）
        """
        if username:
            await self.assert_text_contains(self.locators.WELCOME_MESSAGE, username)
        else:
            await self.assert_element_visible(self.locators.WELCOME_MESSAGE)
        logger.debug("Verified welcome message")

    async def assert_stat_displayed(self, stat_type: str):
        """
        断言统计卡片显示

        Args:
            stat_type: 统计类型
        """
        stat_cards = {
            "users": self.locators.TOTAL_USERS_CARD,
            "active": self.locators.ACTIVE_USERS_CARD,
            "revenue": self.locators.TOTAL_REVENUE_CARD,
            "orders": self.locators.TOTAL_ORDERS_CARD
        }

        selector = stat_cards.get(stat_type)
        if selector:
            await self.assert_element_visible(selector)
            logger.debug(f"Verified {stat_type} stat is displayed")

    # ==================== 最近活动 ====================

    async def get_recent_activities(self) -> List[str]:
        """
        获取最近活动列表

        Returns:
            活动文本列表
        """
        activities = []
        count = await self.count_elements(self.locators.ACTIVITY_ITEMS)

        for i in range(count):
            try:
                activity_text = await self.get_text(f"{self.locators.ACTIVITY_ITEMS}:nth-child({i+1})")
                activities.append(activity_text)
            except:
                pass

        return activities

    async def is_activity_feed_visible(self) -> bool:
        """检查活动动态是否可见"""
        return await self.is_visible(self.locators.RECENT_ACTIVITY)

    # ==================== 图表操作 ====================

    async def is_chart_visible(self, chart_type: str = "") -> bool:
        """
        检查图表是否可见

        Args:
            chart_type: 图表类型 (line, bar, pie)

        Returns:
            图表是否可见
        """
        if chart_type == "line":
            return await self.is_visible(self.locators.LINE_CHART)
        elif chart_type == "bar":
            return await self.is_visible(self.locators.BAR_CHART)
        elif chart_type == "pie":
            return await self.is_visible(self.locators.PIE_CHART)
        else:
            return await self.is_visible(self.locators.CHART)

    # ==================== 日期选择器 ====================

    async def select_date_range(self, start_date: str, end_date: str):
        """
        选择日期范围

        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
        """
        await self.click(self.locators.DATE_RANGE_PICKER)
        # 这里需要根据实际日期选择器UI实现
        logger.info(f"Selected date range: {start_date} to {end_date}")

    # ==================== 空状态 ====================

    async def is_empty_state_visible(self) -> bool:
        """检查空状态是否显示"""
        return await self.is_visible(self.locators.EMPTY_STATE)

    async def get_empty_state_message(self) -> str:
        """
        获取空状态消息

        Returns:
            空状态消息文本
        """
        return await self.get_text(self.locators.EMPTY_STATE)
