"""
Dashboard Page Locators
仪表盘页元素定位器
"""


class DashboardLocators:
    """仪表盘页元素定位器"""

    # 页面标题
    PAGE_TITLE = "h1:has-text('Dashboard'), h1:has-text('Overview')"
    WELCOME_MESSAGE = ".welcome, .greeting"

    # 侧边栏
    SIDEBAR = ".sidebar, aside"
    SIDEBAR_MENU = ".sidebar-menu, .nav-menu"
    SIDEBAR_TOGGLE = ".sidebar-toggle, .menu-toggle"

    # 导航菜单
    MENU_DASHBOARD = "a[href*='dashboard'], .menu-item:has-text('Dashboard')"
    MENU_USERS = "a[href*='users'], .menu-item:has-text('Users')"
    MENU_SETTINGS = "a[href*='settings'], .menu-item:has-text('Settings')"
    MENU_REPORTS = "a[href*='reports'], .menu-item:has-text('Reports')"
    MENU_PROFILE = "a[href*='profile'], .menu-item:has-text('Profile')"
    MENU_LOGOUT = "a[href*='logout'], .menu-item:has-text('Logout')"

    # 统计卡片
    STATS_CARDS = ".stats-card, .metric-card"
    TOTAL_USERS_CARD = ".stats-card:has-text('Total Users'), .metric-card:has-text('Users')"
    ACTIVE_USERS_CARD = ".stats-card:has-text('Active Users')"
    TOTAL_REVENUE_CARD = ".stats-card:has-text('Revenue')"
    TOTAL_ORDERS_CARD = ".stats-card:has-text('Orders')"

    # 统计数值
    STAT_VALUE = ".stat-value, .metric-value"
    STAT_LABEL = ".stat-label, .metric-label"
    STAT_CHANGE = ".stat-change, .metric-change"

    # 图表
    CHART = ".chart, [data-chart]"
    LINE_CHART = ".line-chart, .chart[type='line']"
    BAR_CHART = ".bar-chart, .chart[type='bar']"
    PIE_CHART = ".pie-chart, .chart[type='pie']"

    # 顶部导航
    TOP_NAV = ".top-nav, .navbar"
    USER_MENU = ".user-menu, .user-dropdown"
    USER_MENU_TOGGLE = ".user-menu-toggle, .user-avatar"
    USER_MENU_ITEMS = ".user-menu .menu-item"

    # 通知
    NOTIFICATION_BUTTON = ".notification-button, .bell-icon"
    NOTIFICATION_BADGE = ".notification-badge"
    NOTIFICATION_DROPDOWN = ".notification-dropdown"
    NOTIFICATION_ITEMS = ".notification-item"

    # 搜索
    SEARCH_INPUT = ".search-input, input[placeholder*='search' i]"
    SEARCH_BUTTON = ".search-button, button:has-text('Search')"

    # 快速操作
    QUICK_ACTIONS = ".quick-actions"
    QUICK_ACTION_BUTTON = ".quick-action-button"

    # 最近活动
    RECENT_ACTIVITY = ".recent-activity, .activity-feed"
    ACTIVITY_ITEMS = ".activity-item"
    ACTIVITY_TIMESTAMP = ".activity-time"

    # 数据表格
    DATA_TABLE = ".data-table, table"
    TABLE_ROWS = "tbody tr"
    TABLE_HEADERS = "thead th"

    # 分页
    PAGINATION = ".pagination"
    PAGE_INFO = ".page-info"

    # 加载状态
    LOADING_SPINNER = ".loading-spinner"
    EMPTY_STATE = ".empty-state, .no-data"

    # 日期选择器
    DATE_PICKER = ".date-picker, input[type='date']"
    DATE_RANGE_PICKER = ".date-range-picker"

    # 导出按钮
    EXPORT_BUTTON = "button:has-text('Export'), .export-button"

    # 刷新按钮
    REFRESH_BUTTON = "button:has-text('Refresh'), .refresh-button"
