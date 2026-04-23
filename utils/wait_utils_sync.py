"""
Wait Utilities - Synchronous Version
智能等待策略封装 - 同步版本
"""
from typing import Optional, Callable, Any
from playwright.sync_api import Page, Locator
from loguru import logger


class WaitUtils:
    """
    等待工具类 - 同步版本
    提供各种等待策略，避免硬编码 sleep
    """

    def __init__(self, default_timeout: int = 30000):
        """
        初始化等待工具

        Args:
            default_timeout: 默认超时时间（毫秒）
        """
        self.default_timeout = default_timeout

    def wait_for_element_visible(
        self,
        page: Page,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        等待元素可见

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            timeout: 超时时间（毫秒）

        Returns:
            元素定位器
        """
        timeout = timeout or self.default_timeout
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            logger.debug(f"Element visible: {selector}")
            return locator
        except Exception as e:
            logger.error(f"Element not visible: {selector} - {e}")
            raise

    def wait_for_element_hidden(
        self,
        page: Page,
        selector: str,
        timeout: Optional[int] = None
    ):
        """
        等待元素隐藏

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            locator = page.locator(selector)
            locator.wait_for(state="hidden", timeout=timeout)
            logger.debug(f"Element hidden: {selector}")
        except Exception as e:
            logger.error(f"Element still visible: {selector} - {e}")
            raise

    def wait_for_element_enabled(
        self,
        page: Page,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        等待元素可点击/启用

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            timeout: 超时时间（毫秒）

        Returns:
            元素定位器
        """
        timeout = timeout or self.default_timeout
        try:
            locator = page.locator(selector)
            locator.wait_for(state="attached", timeout=timeout)
            # 等待元素可点击
            page.wait_for_function(
                f"document.querySelector('{selector}') && !document.querySelector('{selector}').disabled",
                timeout=timeout
            )
            logger.debug(f"Element enabled: {selector}")
            return locator
        except Exception as e:
            logger.error(f"Element not enabled: {selector} - {e}")
            raise

    def wait_for_url(
        self,
        page: Page,
        url: str,
        timeout: Optional[int] = None
    ):
        """
        等待URL变化

        Args:
            page: Playwright Page 对象
            url: 期望的URL（支持正则）
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            page.wait_for_url(url, timeout=timeout)
            logger.debug(f"URL matched: {url}")
        except Exception as e:
            logger.error(f"URL not matched: {url} - {e}")
            raise

    def wait_for_navigation(
        self,
        page: Page,
        url: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """
        等待导航完成

        Args:
            page: Playwright Page 对象
            url: 期望导航到的URL（可选）
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            if url:
                page.wait_for_url(url, timeout=timeout)
            else:
                page.wait_for_load_state("networkidle", timeout=timeout)
            logger.debug("Navigation completed")
        except Exception as e:
            logger.error(f"Navigation timeout - {e}")
            raise

    def wait_for_text(
        self,
        page: Page,
        selector: str,
        text: str,
        timeout: Optional[int] = None
    ):
        """
        等待元素包含指定文本

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            text: 期望的文本
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            locator.wait_for(state="contains_text", text=text, timeout=timeout)
            logger.debug(f"Text found in element: {selector} - {text}")
        except Exception as e:
            logger.error(f"Text not found: {selector} - {text} - {e}")
            raise

    def wait_for_count(
        self,
        page: Page,
        selector: str,
        count: int,
        timeout: Optional[int] = None
    ):
        """
        等待元素数量达到指定值

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            count: 期望的元素数量
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            locator = page.locator(selector)
            locator.wait_for(state="attached", timeout=timeout)
            page.wait_for_function(
                f"document.querySelectorAll('{selector}').length >= {count}",
                timeout=timeout
            )
            logger.debug(f"Element count reached: {selector} - {count}")
        except Exception as e:
            logger.error(f"Element count not reached: {selector} - {count} - {e}")
            raise

    def wait_for_attribute(
        self,
        page: Page,
        selector: str,
        attribute: str,
        value: str,
        timeout: Optional[int] = None
    ):
        """
        等待元素属性值变化

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            attribute: 属性名
            value: 期望的属性值
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            page.wait_for_function(
                f"document.querySelector('{selector}').getAttribute('{attribute}') === '{value}'",
                timeout=timeout
            )
            logger.debug(f"Attribute matched: {selector} - {attribute}={value}")
        except Exception as e:
            logger.error(f"Attribute not matched: {selector} - {attribute}={value} - {e}")
            raise

    def wait_for_js_condition(
        self,
        page: Page,
        js_expression: str,
        timeout: Optional[int] = None
    ):
        """
        等待 JavaScript 条件为真

        Args:
            page: Playwright Page 对象
            js_expression: JavaScript 表达式
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            page.wait_for_function(js_expression, timeout=timeout)
            logger.debug(f"JS condition met: {js_expression}")
        except Exception as e:
            logger.error(f"JS condition not met: {js_expression} - {e}")
            raise

    def wait_for_selector_count_change(
        self,
        page: Page,
        selector: str,
        initial_count: int,
        timeout: Optional[int] = None
    ):
        """
        等待元素数量变化

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            initial_count: 初始数量
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.default_timeout
        try:
            page.wait_for_function(
                f"document.querySelectorAll('{selector}').length !== {initial_count}",
                timeout=timeout
            )
            logger.debug(f"Element count changed: {selector}")
        except Exception as e:
            logger.error(f"Element count did not change: {selector} - {e}")
            raise

    def polling_wait(
        self,
        condition: Callable[[], Any],
        timeout: int = 30000,
        poll_interval: int = 500
    ):
        """
        轮询等待条件满足

        Args:
            condition: 条件函数（返回 bool）
            timeout: 超时时间（毫秒）
            poll_interval: 轮询间隔（毫秒）
        """
        import time
        start_time = time.time()

        while True:
            if condition():
                logger.debug("Polling condition met")
                return

            elapsed = (time.time() - start_time) * 1000
            if elapsed >= timeout:
                raise TimeoutError(f"Polling timeout after {timeout}ms")

            time.sleep(poll_interval / 1000)

    def smart_sleep(self, seconds: float = 0.5):
        """
        智能休眠（仅在必要时使用）

        Args:
            seconds: 休眠秒数
        """
        import time
        time.sleep(seconds)
        logger.debug(f"Slept for {seconds}s")


# 全局实例
wait_utils = WaitUtils()

__all__ = ["WaitUtils", "wait_utils"]