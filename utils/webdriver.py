"""
Playwright WebDriver Manager
单例模式管理浏览器实例
"""
import asyncio
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from loguru import logger


class WebDriverManager:
    """
    Playwright 浏览器管理器（单例模式）
    支持多浏览器、并行执行、独立上下文
    """
    _instance: Optional['WebDriverManager'] = None
    _playwright: Optional[Playwright] = None
    _browsers: Dict[str, Browser] = {}
    _contexts: Dict[str, BrowserContext] = {}
    _pages: Dict[str, Page] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.config = {}
            logger.info("WebDriverManager initialized")

    @classmethod
    async def start_playwright(cls) -> Playwright:
        """启动 Playwright"""
        if cls._playwright is None:
            playwright_obj = await async_playwright().start()
            cls._playwright = playwright_obj
            logger.info("Playwright started")
        return cls._playwright

    @classmethod
    async def get_browser(
        cls,
        browser_type: str = "chromium",
        headless: bool = True,
        channel: Optional[str] = None,
        **kwargs
    ) -> Browser:
        """
        获取或创建浏览器实例

        Args:
            browser_type: chromium, firefox, webkit
            headless: 是否无头模式
            channel: 浏览器通道 (chrome, msedge, etc.)
            **kwargs: 其他浏览器参数

        Returns:
            Browser: 浏览器实例
        """
        browser_key = f"{browser_type}_{channel if channel else 'default'}_{headless}"

        if browser_key not in cls._browsers or cls._browsers[browser_key] is None:
            playwright = await cls.start_playwright()

            # 根据浏览器类型获取启动器
            browser_launcher = getattr(playwright, browser_type)

            # 启动浏览器
            browser = await browser_launcher.launch(
                headless=headless,
                channel=channel,
                **kwargs
            )

            cls._browsers[browser_key] = browser
            logger.info(f"Browser launched: {browser_type} (headless={headless}, channel={channel})")

        return cls._browsers[browser_key]

    @classmethod
    async def get_context(
        cls,
        browser: Optional[Browser] = None,
        browser_type: str = "chromium",
        headless: bool = True,
        channel: Optional[str] = None,
        context_options: Optional[Dict[str, Any]] = None
    ) -> BrowserContext:
        """
        获取或创建浏览器上下文

        Args:
            browser: 浏览器实例（可选）
            browser_type: 浏览器类型
            headless: 是否无头模式
            channel: 浏览器通道
            context_options: 上下文选项

        Returns:
            BrowserContext: 浏览器上下文
        """
        if browser is None:
            browser = await cls.get_browser(browser_type, headless, channel)

        # 生成上下文键
        context_key = f"{browser_type}_{id(browser)}"

        if context_key not in cls._contexts or cls._contexts[context_key] is None:
            # 默认上下文选项
            default_options = {
                "viewport": {"width": 1920, "height": 1080},
                "locale": "en-US",
                "timezone_id": "America/New_York",
                "ignore_https_errors": True,
                "accept_downloads": True,
                "bypass_csp": True,
            }

            # 合并自定义选项
            if context_options:
                default_options.update(context_options)

            context = await browser.new_context(**default_options)
            cls._contexts[context_key] = context
            logger.info(f"Browser context created: {context_key}")

        return cls._contexts[context_key]

    @classmethod
    async def get_page(
        cls,
        context: Optional[BrowserContext] = None,
        browser: Optional[Browser] = None,
        browser_type: str = "chromium",
        headless: bool = True,
        channel: Optional[str] = None
    ) -> Page:
        """
        获取或创建页面

        Args:
            context: 浏览器上下文
            browser: 浏览器实例
            browser_type: 浏览器类型
            headless: 是否无头模式
            channel: 浏览器通道

        Returns:
            Page: 页面实例
        """
        if context is None:
            context = await cls.get_context(browser, browser_type, headless, channel)

        page = await context.new_page()
        page_key = f"{id(context)}_{len(cls._pages)}"
        cls._pages[page_key] = page

        # 设置默认超时
        page.set_default_timeout(30000)
        page.set_default_navigation_timeout(60000)

        logger.info(f"New page created: {page_key}")
        return page

    @classmethod
    async def close_page(cls, page: Page):
        """关闭页面"""
        try:
            await page.close()
            logger.debug(f"Page closed: {id(page)}")
        except Exception as e:
            logger.warning(f"Error closing page: {e}")

    @classmethod
    async def close_context(cls, context: BrowserContext):
        """关闭上下文"""
        try:
            await context.close()
            logger.debug(f"Context closed: {id(context)}")
        except Exception as e:
            logger.warning(f"Error closing context: {e}")

    @classmethod
    async def close_browser(cls, browser: Browser):
        """关闭浏览器"""
        try:
            await browser.close()
            logger.debug(f"Browser closed: {id(browser)}")
        except Exception as e:
            logger.warning(f"Error closing browser: {e}")

    @classmethod
    async def close_all(cls):
        """关闭所有资源"""
        # 关闭所有页面
        for page_key, page in list(cls._pages.items()):
            await cls.close_page(page)
        cls._pages.clear()

        # 关闭所有上下文
        for context_key, context in list(cls._contexts.items()):
            await cls.close_context(context)
        cls._contexts.clear()

        # 关闭所有浏览器
        for browser_key, browser in list(cls._browsers.items()):
            await cls.close_browser(browser)
        cls._browsers.clear()

        # 关闭 Playwright
        if cls._playwright:
            await cls._playwright.stop()
            cls._playwright = None
            logger.info("Playwright stopped")

    @classmethod
    def set_config(cls, config: Dict[str, Any]):
        """设置配置"""
        cls.config = config
