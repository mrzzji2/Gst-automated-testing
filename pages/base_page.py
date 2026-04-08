"""
Base Page
基础页面类
封装通用操作
"""
from typing import Optional, List
from playwright.async_api import Page, Locator, expect
from loguru import logger

from elements.base_locators import BaseLocators
from utils.wait_utils import WaitUtils
from utils.screenshot import ScreenshotUtils


class BasePage:
    """
    基础页面类
    封装所有页面通用的操作和方法
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        初始化基础页面

        Args:
            page: Playwright Page 对象
            base_url: 基础URL
        """
        self.page = page
        self.base_url = base_url
        self.wait_utils = WaitUtils()
        self.screenshot_utils = ScreenshotUtils()

    # ==================== 导航操作 ====================

    async def navigate(self, url: str = ""):
        """
        导航到指定URL

        Args:
            url: 目标URL（相对或绝对路径）
        """
        target_url = url if url.startswith("http") else f"{self.base_url}{url}"
        await self.page.goto(target_url)
        logger.info(f"Navigated to: {target_url}")

    async def reload(self):
        """刷新页面"""
        await self.page.reload()
        logger.info("Page reloaded")

    async def go_back(self):
        """返回上一页"""
        await self.page.go_back()
        logger.info("Navigated back")

    async def go_forward(self):
        """前进到下一页"""
        await self.page.go_forward()
        logger.info("Navigated forward")

    async def wait_for_url(self, url: str, timeout: int = 30000):
        """
        等待URL变化

        Args:
            url: 期望的URL（支持正则）
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_url(self.page, url, timeout)

    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.page.url

    def get_page_title(self) -> str:
        """获取页面标题"""
        return await self.page.title()

    # ==================== 元素操作 ====================

    async def click(self, selector: str, timeout: int = 30000):
        """
        点击元素

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_enabled(self.page, selector, timeout)
        await self.page.click(selector)
        logger.debug(f"Clicked: {selector}")

    async def double_click(self, selector: str, timeout: int = 30000):
        """
        双击元素

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.dblclick(selector)
        logger.debug(f"Double clicked: {selector}")

    async def right_click(self, selector: str, timeout: int = 30000):
        """
        右键点击元素

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.click(selector, button="right")
        logger.debug(f"Right clicked: {selector}")

    async def hover(self, selector: str, timeout: int = 30000):
        """
        鼠标悬停

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.hover(selector)
        logger.debug(f"Hovered: {selector}")

    async def type_text(self, selector: str, text: str, clear: bool = True, timeout: int = 30000):
        """
        输入文本

        Args:
            selector: 元素选择器
            text: 输入的文本
            clear: 是否先清空
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)

        if clear:
            await self.page.fill(selector, "")
            logger.debug(f"Cleared: {selector}")

        await self.page.fill(selector, text)
        logger.debug(f"Typed '{text}' into: {selector}")

    async def fill(self, selector: str, value: str, timeout: int = 30000):
        """
        填充表单字段（快速输入）

        Args:
            selector: 元素选择器
            value: 填充值
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.fill(selector, value)
        logger.debug(f"Filled '{value}' into: {selector}")

    async def clear_text(self, selector: str, timeout: int = 30000):
        """
        清空文本

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.fill(selector, "")
        logger.debug(f"Cleared: {selector}")

    async def select_option(self, selector: str, value: str, timeout: int = 30000):
        """
        选择下拉框选项

        Args:
            selector: 元素选择器
            value: 选项值
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.select_option(selector, value=value)
        logger.debug(f"Selected '{value}' from: {selector}")

    async def check_checkbox(self, selector: str, timeout: int = 30000):
        """
        勾选复选框

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.check(selector)
        logger.debug(f"Checked: {selector}")

    async def uncheck_checkbox(self, selector: str, timeout: int = 30000):
        """
        取消勾选复选框

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.uncheck(selector)
        logger.debug(f"Unchecked: {selector}")

    async def upload_file(self, selector: str, file_path: str, timeout: int = 30000):
        """
        上传文件

        Args:
            selector: 元素选择器
            file_path: 文件路径
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.set_input_files(selector, file_path)
        logger.debug(f"Uploaded file to: {selector}")

    # ==================== 元素信息 ====================

    async def get_text(self, selector: str, timeout: int = 30000) -> str:
        """
        获取元素文本

        Args:
            selector: 元素选择器
            timeout: 超时时间

        Returns:
            元素文本内容
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        text = await self.page.text_content(selector)
        return text.strip() if text else ""

    async def get_attribute(self, selector: str, attribute: str, timeout: int = 30000) -> Optional[str]:
        """
        获取元素属性

        Args:
            selector: 元素选择器
            attribute: 属性名
            timeout: 超时时间

        Returns:
            属性值
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        return await self.page.get_attribute(selector, attribute)

    async def get_value(self, selector: str, timeout: int = 30000) -> Optional[str]:
        """
        获取输入框的值

        Args:
            selector: 元素选择器
            timeout: 超时时间

        Returns:
            输入框的值
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        return await self.page.input_value(selector)

    async def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        检查元素是否可见

        Args:
            selector: 元素选择器
            timeout: 超时时间

        Returns:
            是否可见
        """
        try:
            await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
            return True
        except:
            return False

    async def is_enabled(self, selector: str, timeout: int = 5000) -> bool:
        """
        检查元素是否启用

        Args:
            selector: 元素选择器
            timeout: 超时时间

        Returns:
            是否启用
        """
        try:
            await self.wait_utils.wait_for_element_enabled(self.page, selector, timeout)
            return True
        except:
            return False

    async def is_checked(self, selector: str, timeout: int = 5000) -> bool:
        """
        检查复选框是否勾选

        Args:
            selector: 元素选择器
            timeout: 超时时间

        Returns:
            是否勾选
        """
        try:
            await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
            return await self.page.is_checked(selector)
        except:
            return False

    async def count_elements(self, selector: str, timeout: int = 5000) -> int:
        """
        统计元素数量

        Args:
            selector: 元素选择器
            timeout: 超时时间

        Returns:
            元素数量
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        return await self.page.locator(selector).count()

    # ==================== 断言操作 ====================

    async def assert_element_visible(self, selector: str, timeout: int = 30000):
        """
        断言元素可见

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        logger.debug(f"Element is visible: {selector}")

    async def assert_element_hidden(self, selector: str, timeout: int = 30000):
        """
        断言元素隐藏

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_hidden(self.page, selector, timeout)
        logger.debug(f"Element is hidden: {selector}")

    async def assert_text_equals(self, selector: str, expected: str, timeout: int = 30000):
        """
        断言文本相等

        Args:
            selector: 元素选择器
            expected: 期望的文本
            timeout: 超时时间
        """
        actual = await self.get_text(selector, timeout)
        assert actual == expected, f"Text mismatch: expected '{expected}', got '{actual}'"
        logger.debug(f"Text matches: {selector} = '{expected}'")

    async def assert_text_contains(self, selector: str, expected: str, timeout: int = 30000):
        """
        断言文本包含

        Args:
            selector: 元素选择器
            expected: 期望包含的文本
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_text(self.page, selector, expected, timeout)
        logger.debug(f"Text contains: {selector} contains '{expected}'")

    async def assert_attribute_equals(self, selector: str, attribute: str, expected: str, timeout: int = 30000):
        """
        断言属性相等

        Args:
            selector: 元素选择器
            attribute: 属性名
            expected: 期望的属性值
            timeout: 超时时间
        """
        actual = await self.get_attribute(selector, attribute, timeout)
        assert actual == expected, f"Attribute mismatch: {attribute} expected '{expected}', got '{actual}'"
        logger.debug(f"Attribute matches: {selector} {attribute} = '{expected}'")

    async def assert_url_contains(self, expected: str, timeout: int = 30000):
        """
        断言URL包含

        Args:
            expected: 期望包含的URL片段
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_url(self.page, f"**/*{expected}*", timeout)
        logger.debug(f"URL contains: {expected}")

    async def assert_title_equals(self, expected: str, timeout: int = 30000):
        """
        断言页面标题相等

        Args:
            expected: 期望的标题
            timeout: 超时时间
        """
        await self.page.wait_for_timeout(timeout)
        actual = await self.get_page_title()
        assert actual == expected, f"Title mismatch: expected '{expected}', got '{actual}'"
        logger.debug(f"Title matches: '{expected}'")

    # ==================== JavaScript 执行 ====================

    async def execute_script(self, script: str) -> any:
        """
        执行 JavaScript

        Args:
            script: JavaScript 代码

        Returns:
            执行结果
        """
        return await self.page.evaluate(script)

    async def scroll_to_element(self, selector: str, timeout: int = 30000):
        """
        滚动到元素

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        await self.wait_utils.wait_for_element_visible(self.page, selector, timeout)
        await self.page.locator(selector).scroll_into_view_if_needed()
        logger.debug(f"Scrolled to: {selector}")

    async def scroll_to_top(self):
        """滚动到页面顶部"""
        await self.page.evaluate("window.scrollTo(0, 0)")
        logger.debug("Scrolled to top")

    async def scroll_to_bottom(self):
        """滚动到页面底部"""
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        logger.debug("Scrolled to bottom")

    # ==================== 截图操作 ====================

    async def take_screenshot(self, filename: str = None, full_page: bool = True) -> str:
        """
        截取页面截图

        Args:
            filename: 文件名
            full_page: 是否截取整页

        Returns:
            截图文件路径
        """
        return await self.screenshot_utils.capture_screenshot(self.page, filename, full_page)

    # ==================== 等待操作 ====================

    async def wait(self, milliseconds: int):
        """
        显式等待（慎用）

        Args:
            milliseconds: 等待毫秒数
        """
        await self.page.wait_for_timeout(milliseconds)
        logger.debug(f"Waited {milliseconds}ms")

    async def wait_for_network_idle(self, timeout: int = 30000):
        """
        等待网络空闲

        Args:
            timeout: 超时时间
        """
        await self.page.wait_for_load_state("networkidle", timeout=timeout)
        logger.debug("Network idle")

    # ==================== 弹窗操作 ====================

    async def accept_alert(self):
        """接受警告弹窗"""
        self.page.on("dialog", lambda dialog: dialog.accept())
        logger.debug("Alert accepted")

    async def dismiss_alert(self):
        """拒绝警告弹窗"""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
        logger.debug("Alert dismissed")

    async def handle_prompt(self, text: str):
        """
        处理提示弹窗

        Args:
            text: 输入的文本
        """
        async def handle(dialog):
            await dialog.accept(text)
        self.page.on("dialog", handle)
        logger.debug(f"Prompt handled with: {text}")

    # ==================== Frame 操作 ====================

    async def switch_to_frame(self, selector: str):
        """
        切换到 iframe

        Args:
            selector: iframe 选择器
        """
        frame = self.page.frame_locator(selector)
        logger.debug(f"Switched to frame: {selector}")
        return frame

    async def switch_to_main_frame(self):
        """切换回主页面"""
        # Playwright 会自动处理，这里只是占位
        logger.debug("Switched to main frame")

    # ==================== Tab 操作 ====================

    async def get_new_tab(self, url_filter: str = None) -> Optional[Page]:
        """
        获取新打开的标签页

        Args:
            url_filter: URL过滤器

        Returns:
            新标签页对象
        """
        context = self.page.context

        for page in context.pages:
            if url_filter is None or url_filter in page.url:
                return page

        return None

    async def close_tab(self, page: Page = None):
        """
        关闭标签页

        Args:
            page: 要关闭的标签页（默认当前页）
        """
        if page is None:
            page = self.page
        await page.close()
        logger.debug("Tab closed")
