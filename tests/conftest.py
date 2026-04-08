"""
Pytest Configuration File
核心配置：fixture、钩子、失败截图
"""
import os
import sys
import asyncio
import pytest
import allure
from pathlib import Path
from typing import AsyncGenerator, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from loguru import logger

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.config import config
from utils.logger import setup_logger, logger as test_logger
from utils.screenshot import screenshot_utils
from utils.webdriver import WebDriverManager


# ==================== 日志配置 ====================
setup_logger(
    log_level=config.log_level,
    log_path="logs/auto",
    console_output=True,
    file_output=True
)


# ==================== Pytest Fixtures ====================

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def browser_type():
    """启动 Playwright"""
    async with async_playwright() as p:
        yield p


@pytest.fixture(scope="function")
async def browser(browser_type) -> AsyncGenerator[Browser, None]:
    """
    启动浏览器

    支持命令行参数：
    --browser: chromium, firefox, webkit
    --headed: 有头模式
    --channel: 浏览器通道
    """
    # 获取命令行参数
    browser_name = pytest.config.getoption("--browser", default=config.browser_type)
    headed = pytest.config.getoption("--headed", default=not config.browser_headless)
    channel = pytest.config.getoption("--channel", default=config.browser_channel)

    # 启动浏览器
    browser = await browser_type[browser_name].launch(
        headless=not headed,
        channel=channel if browser_name == "chromium" else None,
        args=["--start-maximized"],
        slow_mo=config.get_int("browser.slow_mo", 0)
    )

    test_logger.info(f"Browser started: {browser_name} (headed={headed})")

    yield browser

    # 清理
    await browser.close()
    test_logger.info("Browser closed")


@pytest.fixture(scope="function")
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    """
    创建浏览器上下文

    支持命令行参数：
    --viewport: 视口大小 (1920x1080)
    """
    # 获取视口配置
    viewport = config.get_dict("browser.viewport", {"width": 1920, "height": 1080})

    # 创建上下文
    context = await browser.new_context(
        viewport=viewport,
        locale="en-US",
        timezone_id="America/New_York",
        ignore_https_errors=True,
        accept_downloads=True,
        record_video_dir="reports/videos" if config.video_enabled else None,
        record_video_size={"width": 1920, "height": 1080} if config.video_enabled else None
    )

    test_logger.info(f"Browser context created")

    yield context

    # 清理
    await context.close()
    test_logger.info("Browser context closed")


@pytest.fixture(scope="function")
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """
    创建页面

    这是测试中最常用的 fixture
    """
    # 创建页面
    page = await context.new_page()

    # 设置默认超时
    page.set_default_timeout(config.timeout_default)
    page.set_default_navigation_timeout(config.timeout_navigation)

    test_logger.info(f"New page created")

    yield page

    # 清理
    await page.close()
    test_logger.info("Page closed")


@pytest.fixture(scope="function")
async def base_url() -> str:
    """
    获取基础URL

    支持命令行参数：
    --base-url: 基础URL
    """
    return pytest.config.getoption("--base-url", default=config.base_url)


# ==================== Page Object Fixtures ====================

@pytest.fixture(scope="function")
async def login_page(page: Page, base_url: str):
    """登录页面对象"""
    from pages.login_page import LoginPage
    return LoginPage(page, base_url)


@pytest.fixture(scope="function")
async def dashboard_page(page: Page, base_url: str):
    """仪表盘页面对象"""
    from pages.dashboard_page import DashboardPage
    return DashboardPage(page, base_url)


@pytest.fixture(scope="function")
async def user_management_page(page: Page, base_url: str):
    """用户管理页面对象"""
    from pages.user_management_page import UserManagementPage
    return UserManagementPage(page, base_url)


# ==================== 认证 Fixtures ====================

@pytest.fixture(scope="function")
async def authenticated_page(page: Page, base_url: str) -> AsyncGenerator[Page, None]:
    """
    已认证的页面

    自动登录并返回已认证的页面
    """
    from pages.login_page import LoginPage

    # 获取测试账号
    username = os.getenv("TEST_USER_USERNAME", "test@example.com")
    password = os.getenv("TEST_USER_PASSWORD", "password")

    # 执行登录
    login_page = LoginPage(page, base_url)
    await login_page.goto_login()
    await login_page.login(username, password)

    # 等待导航完成
    await page.wait_for_url("**/dashboard", timeout=10000)

    test_logger.info(f"User authenticated: {username}")

    yield page

    # 登出（可选）
    # await page.click("//a[contains(text(), 'Logout')]")


@pytest.fixture(scope="function")
async def admin_page(page: Page, base_url: str) -> AsyncGenerator[Page, None]:
    """
    管理员认证的页面

    使用管理员账号登录
    """
    from pages.login_page import LoginPage

    # 获取管理员账号
    username = os.getenv("TEST_ADMIN_USERNAME", "admin@example.com")
    password = os.getenv("TEST_ADMIN_PASSWORD", "admin_password")

    # 执行登录
    login_page = LoginPage(page, base_url)
    await login_page.goto_login()
    await login_page.login(username, password)

    # 等待导航完成
    await page.wait_for_url("**/dashboard", timeout=10000)

    test_logger.info(f"Admin authenticated: {username}")

    yield page


# ==================== 测试数据 Fixtures ====================

@pytest.fixture(scope="session")
def test_user() -> Dict[str, str]:
    """测试用户数据"""
    return {
        "username": os.getenv("TEST_USER_USERNAME", "test@example.com"),
        "password": os.getenv("TEST_USER_PASSWORD", "password123"),
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture(scope="session")
def test_admin() -> Dict[str, str]:
    """测试管理员数据"""
    return {
        "username": os.getenv("TEST_ADMIN_USERNAME", "admin@example.com"),
        "password": os.getenv("TEST_ADMIN_PASSWORD", "admin123"),
        "first_name": "Admin",
        "last_name": "User"
    }


@pytest.fixture(scope="function")
def new_user_data():
    """新用户数据（每次生成不同的）"""
    import random
    import string

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "username": f"testuser_{random_suffix}",
        "email": f"testuser_{random_suffix}@example.com",
        "first_name": "New",
        "last_name": f"User {random_suffix}",
        "password": "Password123!",
        "role": "user",
        "status": "active"
    }


# ==================== Pytest Hooks ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试报告钩子
    失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()

    # 只在测试调用阶段处理
    if report.when == "call":
        # 获取 page fixture（如果存在）
        page = None
        if "page" in item.fixturenames:
            page = item.funcargs.get("page")

        # 测试失败时截图
        if report.failed and page is not None and config.screenshot_on_failure:
            try:
                # 获取测试名称
                test_name = item.nodeid.replace("::", "_").replace("/", "_")

                # 截图
                asyncio.run(screenshot_utils.capture_on_failure(
                    page,
                    test_name,
                    str(call.excinfo.value) if call.excinfo else None
                ))

                # 添加到 Allure 报告
                screenshot_path = f"reports/screenshots/failure_{test_name}_*.png"
                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                test_logger.warning(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """
    Pytest 配置钩子
    注册自定义标记和命令行选项
    """
    # 注册自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "sanity: 精简测试")
    config.addinivalue_line("markers", "api: API测试")
    config.addinivalue_line("markers", "ui: UI测试")
    config.addinivalue_line("markers", "slow: 慢速测试")
    config.addinivalue_line("markers", "flaky: 不稳定测试")
    config.addinivalue_line("markers", "critical: 关键业务流程")

    # 添加命令行选项
    config.addoption("--browser", action="store", default="chromium", help="浏览器类型")
    config.addoption("--headed", action="store_true", default=False, help="有头模式")
    config.addoption("--channel", action="store", default="chrome", help="浏览器通道")


def pytest_collection_modifyitems(config, items):
    """
    修改收集到的测试项

    添加默认标记、排序等
    """
    for item in items:
        # 为所有测试添加默认标记
        if not any(item.get_closest_marker(name) for name in ["smoke", "regression", "sanity", "api", "ui"]):
            item.add_marker(pytest.mark.regression)


# ==================== Allure Hooks ====================

@pytest.hookimpl(tryfirst=True)
def pytest_collection_finish(session):
    """
    测试收集完成后的钩子
    添加环境信息到 Allure 报告
    """
    try:
        # 创建环境信息文件
        environment_properties = {
            "Environment": config.environment,
            "Base URL": config.base_url,
            "Browser": config.browser_type,
            "Headless": str(config.browser_headless),
            "Python Version": sys.version,
            "Platform": sys.platform,
        }

        # 写入 Allure 环境文件
        allure_dir = Path("reports/allure")
        allure_dir.mkdir(parents=True, exist_ok=True)

        env_file = allure_dir / "environment.properties"
        with open(env_file, "w") as f:
            for key, value in environment_properties.items():
                f.write(f"{key}={value}\n")
    except Exception as e:
        test_logger.warning(f"Failed to write allure environment: {e}")


# ==================== 辅助函数 ====================

def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="包含慢速测试"
    )
    parser.addoption(
        "--flaky",
        action="store_true",
        default=False,
        help="包含不稳定测试"
    )


def pytest_collection_modifyitems(config, items):
    """根据命令行选项过滤测试"""
    run_slow = config.getoption("--slow")
    run_flaky = config.getoption("--flaky")

    for item in items:
        # 跳过慢速测试（除非指定 --slow）
        if item.get_closest_marker("slow") and not run_slow:
            item.add_marker(pytest.mark.skip(reason="Skipping slow test (use --slow to include)"))

        # 跳过不稳定测试（除非指定 --flaky）
        if item.get_closest_marker("flaky") and not run_flaky:
            item.add_marker(pytest.mark.skip(reason="Skipping flaky test (use --flaky to include)"))
