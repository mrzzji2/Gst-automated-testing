"""
Base Locators
通用元素定位器
"""
from typing import Dict


class BaseLocators:
    """基础定位器类"""

    # 通用定位器
    LOADING_SPINNER = ".loading-spinner"
    SUCCESS_MESSAGE = ".success-message"
    ERROR_MESSAGE = ".error-message"
    WARNING_MESSAGE = ".warning-message"
    INFO_MESSAGE = ".info-message"

    # 按钮定位器
    SUBMIT_BUTTON = "button[type='submit']"
    CANCEL_BUTTON = "button[type='button']:has-text('Cancel')"
    CONFIRM_BUTTON = "button[type='button']:has-text('Confirm')"
    SAVE_BUTTON = "button:has-text('Save')"
    DELETE_BUTTON = "button:has-text('Delete')"
    EDIT_BUTTON = "button:has-text('Edit')"

    # 输入框定位器
    TEXT_INPUT = "input[type='text']"
    EMAIL_INPUT = "input[type='email']"
    PASSWORD_INPUT = "input[type='password']"
    NUMBER_INPUT = "input[type='number']"
    SEARCH_INPUT = "input[placeholder*='search' i], input[placeholder*='Search' i]"

    # 下拉框定位器
    SELECT_DROPDOWN = "select"
    MULTI_SELECT = "select[multiple]"

    # 复选框和单选框
    CHECKBOX = "input[type='checkbox']"
    RADIO_BUTTON = "input[type='radio']"

    # 表格定位器
    TABLE = "table"
    TABLE_ROW = "tr"
    TABLE_CELL = "td"
    TABLE_HEADER = "th"

    # 模态框定位器
    MODAL = ".modal, .dialog, [role='dialog']"
    MODAL_TITLE = ".modal-title, .dialog-title"
    MODAL_BODY = ".modal-body, .dialog-body"
    MODAL_FOOTER = ".modal-footer, .dialog-footer"
    MODAL_CLOSE = ".modal-close, .dialog-close, button[aria-label='Close']"

    # 通知定位器
    TOAST = ".toast, .notification"
    TOAST_SUCCESS = ".toast.success, .notification.success"
    TOAST_ERROR = ".toast.error, .notification.error"
    TOAST_WARNING = ".toast.warning, .notification.warning"

    # 导航定位器
    NAVIGATION = "nav, .navbar, .navigation"
    MENU_ITEM = ".menu-item, .nav-item"
    DROPDOWN_MENU = ".dropdown-menu"
    BREADCRUMB = ".breadcrumb"

    # 表单定位器
    FORM = "form"
    FORM_GROUP = ".form-group"
    FORM_LABEL = "label"
    FORM_ERROR = ".error-message, .validation-error"

    # 列表定位器
    LIST = "ul, ol"
    LIST_ITEM = "li"
    CARD = ".card"

    # 标签页定位器
    TAB = "[role='tab']"
    TAB_PANEL = "[role='tabpanel']"
    TAB_ACTIVE = "[role='tab'][aria-selected='true']"

    # 分页定位器
    PAGINATION = ".pagination"
    PAGE_ITEM = ".page-item"
    PAGE_LINK = ".page-link"
    NEXT_PAGE = ".page-item.next, [aria-label='Next']"
    PREV_PAGE = ".page-item.previous, [aria-label='Previous']"

    # 加载状态
    LOADING = "[data-loading='true'], .loading, .spinner"
    DISABLED = "[disabled], [aria-disabled='true']"

    # 链接定位器
    LINK = "a"
    EXTERNAL_LINK = "a[target='_blank']"

    # 图片定位器
    IMAGE = "img"
    AVATAR = ".avatar, img[alt*='avatar' i]"

    # 徽章和标签
    BADGE = ".badge"
    TAG = ".tag"
    LABEL = ".label"

    # 进度条
    PROGRESS_BAR = ".progress-bar, progress"

    # 工具提示
    TOOLTIP = "[role='tooltip'], .tooltip"

    # 侧边栏
    SIDEBAR = ".sidebar, aside"
    SIDEBAR_TOGGLE = ".sidebar-toggle"

    # 页脚
    FOOTER = "footer"

    # 数据属性定位器（常用）
    DATA_TEST = (lambda value: f"[data-test='{value}']")
    DATA_CY = (lambda value: f"[data-cy='{value}']")
    DATA_QA = (lambda value: f"[data-qa='{value}']")
    DATA_ID = (lambda value: f"[data-id='{value}']")

    # ARIA 定位器
    ARIA_LABEL = (lambda value: f"[aria-label='{value}']")
    ARIA_LABELEDBY = (lambda value: f"[aria-labelledby='{value}']")

    @classmethod
    def get_by_text(cls, text: str, exact: bool = False) -> str:
        """根据文本获取定位器"""
        if exact:
            return f"text={text}"
        return f"text={text}"

    @classmethod
    def get_by_role(cls, role: str, name: str = "") -> str:
        """根据角色获取定位器"""
        if name:
            return f"[role='{role}']:has-text('{name}')"
        return f"[role='{role}']"

    @classmethod
    def get_by_placeholder(cls, placeholder: str) -> str:
        """根据占位符获取定位器"""
        return f"[placeholder='{placeholder}']"
