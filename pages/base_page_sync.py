"""
Base Page - Synchronous Version
基础页面对象 - 同步版本
"""
from typing import Optional
from playwright.sync_api import Page
from loguru import logger

from utils.wait_utils_sync import WaitUtils
from utils.screenshot_sync import ScreenshotUtils


class BasePage:
    """基础页面对象 - 同步版本"""

    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url
        self.wait_utils = WaitUtils()
        self.screenshot_utils = ScreenshotUtils()

    # ==================== 导航操作 ====================

    def navigate(self, url: str = ""):
        """导航到指定URL"""
        target_url = url if url.startswith("http") else f"{self.base_url}{url}"
        self.page.goto(target_url)
        logger.info(f"Navigated to: {target_url}")

    def reload(self):
        """刷新页面"""
        self.page.reload()
        logger.info("Page reloaded")

    def go_back(self):
        """返回上一页"""
        self.page.go_back()
        logger.info("Navigated back")

    def go_forward(self):
        """前进到下一页"""
        self.page.go_forward()
        logger.info("Navigated forward")

    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.page.url

    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.page.title()

    # ==================== 元素操作 ====================

    def click(self, selector: str, timeout: int = 30000):
        """点击元素"""
        self.page.wait_for_selector(selector, timeout=timeout)
        self.page.click(selector)
        logger.debug(f"Clicked: {selector}")

    def double_click(self, selector: str, timeout: int = 30000):
        """双击元素"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.dblclick(selector)
        logger.debug(f"Double clicked: {selector}")

    def right_click(self, selector: str, timeout: int = 30000):
        """右键点击元素"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.click(selector, button="right")
        logger.debug(f"Right clicked: {selector}")

    def hover(self, selector: str, timeout: int = 30000):
        """鼠标悬停"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.hover(selector)
        logger.debug(f"Hovered: {selector}")

    def type_text(self, selector: str, text: str, clear: bool = True, timeout: int = 30000):
        """输入文本"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        if clear:
            self.page.fill(selector, "")
        self.page.fill(selector, text)
        logger.debug(f"Typed '{text}' into: {selector}")

    def fill(self, selector: str, value: str, timeout: int = 30000):
        """填充表单字段"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.fill(selector, value)
        logger.debug(f"Filled '{value}' into: {selector}")

    def clear_text(self, selector: str, timeout: int = 30000):
        """清空文本"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.fill(selector, "")
        logger.debug(f"Cleared: {selector}")

    def select_option(self, selector: str, value: str, timeout: int = 30000):
        """选择下拉框选项"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.select_option(selector, value=value)
        logger.debug(f"Selected '{value}' from: {selector}")

    def check_checkbox(self, selector: str, timeout: int = 30000):
        """勾选复选框"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.check(selector)
        logger.debug(f"Checked: {selector}")

    def uncheck_checkbox(self, selector: str, timeout: int = 30000):
        """取消勾选复选框"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.uncheck(selector)
        logger.debug(f"Unchecked: {selector}")

    def upload_file(self, selector: str, file_path: str, timeout: int = 30000):
        """上传文件"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.set_input_files(selector, file_path)
        logger.debug(f"Uploaded file to: {selector}")

    # ==================== 元素信息 ====================

    def get_text(self, selector: str, timeout: int = 30000) -> str:
        """获取元素文本"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        text = self.page.text_content(selector)
        return text.strip() if text else ""

    def get_attribute(self, selector: str, attribute: str, timeout: int = 30000) -> Optional[str]:
        """获取元素属性"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return self.page.get_attribute(selector, attribute)

    def get_value(self, selector: str, timeout: int = 30000) -> Optional[str]:
        """获取输入框的值"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return self.page.input_value(selector)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否可见"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False

    def is_enabled(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否启用"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return self.page.is_enabled(selector)
        except:
            return False

    def is_checked(self, selector: str, timeout: int = 5000) -> bool:
        """检查复选框是否勾选"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return self.page.is_checked(selector)
        except:
            return False

    def count_elements(self, selector: str, timeout: int = 5000) -> int:
        """统计元素数量"""
        try:
            self.page.wait_for_selector(selector, state="attached", timeout=timeout)
        except:
            pass
        return self.page.locator(selector).count()

    # ==================== 断言操作 ====================

    def assert_element_visible(self, selector: str, timeout: int = 30000):
        """断言元素可见"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        logger.debug(f"Element is visible: {selector}")

    def assert_element_hidden(self, selector: str, timeout: int = 30000):
        """断言元素隐藏"""
        self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
        logger.debug(f"Element is hidden: {selector}")

    def assert_text_equals(self, selector: str, expected: str, timeout: int = 30000):
        """断言文本相等"""
        actual = self.get_text(selector, timeout)
        assert actual == expected, f"Text mismatch: expected '{expected}', got '{actual}'"
        logger.debug(f"Text matches: {selector} = '{expected}'")

    def assert_text_contains(self, selector: str, expected: str, timeout: int = 30000):
        """断言文本包含"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        text = self.page.text_content(selector)
        assert expected in text, f"Text should contain '{expected}', got: {text}"
        logger.debug(f"Text contains: {selector} contains '{expected}'")

    def assert_attribute_equals(self, selector: str, attribute: str, expected: str, timeout: int = 30000):
        """断言属性相等"""
        actual = self.get_attribute(selector, attribute, timeout)
        assert actual == expected, f"Attribute mismatch: {attribute} expected '{expected}', got '{actual}'"
        logger.debug(f"Attribute matches: {selector} {attribute} = '{expected}'")

    def assert_url_contains(self, expected: str, timeout: int = 30000):
        """断言URL包含"""
        self.page.wait_for_url(f"**/*{expected}*", timeout=timeout)
        logger.debug(f"URL contains: {expected}")

    def assert_title_equals(self, expected: str, timeout: int = 30000):
        """断言页面标题相等"""
        self.page.wait_for_timeout(timeout)
        actual = self.get_page_title()
        assert actual == expected, f"Title mismatch: expected '{expected}', got '{actual}'"
        logger.debug(f"Title matches: '{expected}'")

    # ==================== JavaScript 执行 ====================

    def execute_script(self, script: str):
        """执行 JavaScript"""
        return self.page.evaluate(script)

    def scroll_to_element(self, selector: str, timeout: int = 30000):
        """滚动到元素"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.locator(selector).scroll_into_view_if_needed()
        logger.debug(f"Scrolled to: {selector}")

    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.page.evaluate("window.scrollTo(0, 0)")
        logger.debug("Scrolled to top")

    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        logger.debug("Scrolled to bottom")

    # ==================== 等待操作 ====================

    def wait(self, milliseconds: int):
        """显式等待（慎用）"""
        self.page.wait_for_timeout(milliseconds)
        logger.debug(f"Waited {milliseconds}ms")

    def wait_for_network_idle(self, timeout: int = 30000):
        """等待网络空闲"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        logger.debug("Network idle")

    # ==================== 弹窗操作 ====================

    def accept_alert(self):
        """接受警告弹窗"""
        def accept_dialog(dialog):
            dialog.accept()
        self.page.on("dialog", accept_dialog)
        logger.debug("Alert accepted")

    def dismiss_alert(self):
        """拒绝警告弹窗"""
        def dismiss_dialog(dialog):
            dialog.dismiss()
        self.page.on("dialog", dismiss_dialog)
        logger.debug("Alert dismissed")

    def handle_prompt(self, text: str):
        """处理提示弹窗"""
        def handle(dialog):
            dialog.accept(text)
        self.page.on("dialog", handle)
        logger.debug(f"Prompt handled with: {text}")