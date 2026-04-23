"""
Pytest Configuration File - Simplified
Core fixtures for GST Online Consultation testing
"""
import os
import sys
import asyncio
import pytest
import allure
from pathlib import Path
from typing import AsyncGenerator
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Logger
from loguru import logger as test_logger

# ==================== Pytest Fixtures ====================

@pytest.fixture(scope="function")
async def browser_type():
    """Start Playwright"""
    async with async_playwright() as p:
        yield p


@pytest.fixture(scope="function")
async def browser(browser_type) -> AsyncGenerator[Browser, None]:
    """Launch browser"""
    browser = await browser_type.chromium.launch(
        headless=False,
        channel="chrome",
        args=["--start-maximized"],
        slow_mo=0
    )
    test_logger.info("Browser started: chromium (headed=True)")
    yield browser
    await browser.close()
    test_logger.info("Browser closed")


@pytest.fixture(scope="function")
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    """Create browser context with saved login state"""
    viewport = {"width": 1920, "height": 1080}
    storage_state_file = project_root / "tests" / "storage_state.json"

    # 如果存在保存的登录状态，直接使用；否则创建新的 context
    if storage_state_file.exists():
        context = await browser.new_context(
            viewport=viewport,
            locale="zh-CN",
            ignore_https_errors=True,
            accept_downloads=True,
            storage_state=str(storage_state_file)  # 加载保存的登录状态
        )
        test_logger.info("Browser context created with saved login state")
    else:
        context = await browser.new_context(
            viewport=viewport,
            locale="zh-CN",
            ignore_https_errors=True,
            accept_downloads=True
        )
        test_logger.info("Browser context created (no saved state)")

    yield context
    await context.close()
    test_logger.info("Browser context closed")


@pytest.fixture(scope="function")
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """Create page"""
    page = await context.new_page()
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    test_logger.info("New page created")
    yield page
    await page.close()
    test_logger.info("Page closed")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Get base URL"""
    return os.getenv("GST_BASE_URL", "https://doc-online-test.gstyun.cn/webClinic/index.html")


# ==================== Page Object Fixtures ====================
# 所有页面对象 fixture（除 login_page 外）都会自动执行登录
# 使用 authenticated_page 作为基础，确保测试运行前用户已登录

@pytest.fixture(scope="function")
async def online_consultation_page(page: Page, base_url: str):
    """Online consultation page object (未自动登录，仅用于测试登录前的状态)"""
    from pages.online_consultation_page import OnlineConsultationPage
    return OnlineConsultationPage(page, base_url)


@pytest.fixture(scope="function")
async def authenticated_page(page: Page, base_url: str):
    """
    通用的已认证页面 fixture - 适用于所有需要登录的测试

    自动登录并返回已认证的 page 对象
    如果存在保存的登录状态则使用，否则执行登录并保存状态

    This fixture ensures:
    1. User is logged in
    2. Page is on the home page (#/home)
    3. Doctor is selected

    Returns:
        Page: 已登录的 Playwright Page 对象
    """
    # Get test credentials
    username = os.getenv("GST_USERNAME", "17671792742")
    password = os.getenv("GST_PASSWORD", "123456")
    doctor_name = os.getenv("GST_DOCTOR_NAME", "罗慧")

    # Storage state file path
    storage_state_file = project_root / "tests" / "storage_state.json"

    # Navigate to home page
    await page.goto(f"{base_url}#/home")

    # 等待页面加载
    await page.wait_for_timeout(2000)

    # 检查是否需要登录（如果不在登录页面，说明已使用保存的状态登录）
    if "#/login" in page.url:
        test_logger.info("No saved login state found, performing login...")
        # 需要登录
        try:
            # 等待登录表单出现
            await page.wait_for_selector("input[placeholder*='手机号']", timeout=10000)
            test_logger.info("Login page loaded, filling credentials...")

            # 填写手机号和验证码
            await page.fill("input[placeholder*='手机号']", username)
            await page.fill("input[placeholder*='验证码']", password)
            test_logger.info(f"Credentials filled: {username}")

            # 直接点击登录按钮（不点击"获取验证码"）
            await page.click("button:has-text('登录')")
            test_logger.info("Login button clicked")

            # 等待登录响应和页面跳转 - 增加等待时间
            await page.wait_for_timeout(5000)

            # 登录后选择医生
            test_logger.info("Waiting for doctor selection dialog...")

            # 先等待医生对话框出现（最多等待10秒）
            try:
                # 等待对话框出现
                await page.wait_for_selector("dialog, .dialog, [role='dialog']", timeout=10000)
                test_logger.info("Doctor selection dialog appeared")
            except:
                test_logger.warning("No doctor selection dialog found after 10 seconds")

            # 等待2秒让对话框完全加载
            await page.wait_for_timeout(2000)

            # 检查是否有对话框或单选按钮
            dialog_found = False
            dialogs = page.locator("dialog, .dialog, [role='dialog']")
            dialog_count = await dialogs.count()
            radios = page.locator("input[type='radio'], [role='radio']")
            radio_count = await radios.count()

            test_logger.info(f"Dialog count: {dialog_count}, Radio count: {radio_count}")

            if dialog_count > 0 or radio_count > 0:
                dialog_found = True
                test_logger.info("Doctor selection UI found, proceeding with selection")

            if dialog_found:
                # 选择医生
                doctor_radio = page.locator(f"radio:has-text('{doctor_name}')")
                if await doctor_radio.count() > 0:
                    await doctor_radio.first.click()
                    test_logger.info(f"Selected doctor: {doctor_name}")
                else:
                    await radios.first.click()
                    test_logger.info("Selected first available doctor")

                # 等待500ms确保选择生效
                await page.wait_for_timeout(500)

                # 点击确认切换按钮
                await page.click("button:has-text('确认'), button:has-text('确认切换')")
                test_logger.info("Confirmed doctor selection")

                # 等待页面跳转
                await page.wait_for_timeout(3000)
            else:
                # 没有找到医生对话框，检查URL
                current_url = page.url
                test_logger.info(f"No doctor dialog found. Current URL: {current_url}")

                # 如果还在登录页面，说明登录失败
                if "#/login" in current_url:
                    raise Exception("Login failed - still on login page and no doctor dialog found")

            # 保存登录状态到文件
            test_logger.info("Saving login state to file...")
            await page.context.storage_state(path=str(storage_state_file))
            test_logger.info(f"Login state saved to: {storage_state_file}")

        except Exception as e:
            test_logger.error(f"Login failed: {e}")
            raise
    else:
        test_logger.info("Using saved login state - already authenticated")

    # 验证已在在线问诊页面
    current_url = page.url
    if "#/login" in current_url:
        raise Exception(f"Login verification failed - still on login page: {current_url}")

    test_logger.info(f"GST authenticated: {username} as doctor {doctor_name}")
    test_logger.info(f"Successfully entered home page: {current_url}")

    return page


@pytest.fixture(scope="function")
async def dashboard_page(authenticated_page: Page, base_url: str):
    """Dashboard page object with authenticated state"""
    from pages.dashboard_page import DashboardPage
    return DashboardPage(authenticated_page, base_url)


@pytest.fixture(scope="function")
async def user_management_page(authenticated_page: Page, base_url: str):
    """User management page object with authenticated state"""
    from pages.user_management_page import UserManagementPage
    return UserManagementPage(authenticated_page, base_url)


@pytest.fixture(scope="function")
async def login_page(page: Page, base_url: str):
    """Login page object - for testing login functionality (no auto-login)"""
    from pages.login_page import LoginPage
    return LoginPage(page, base_url)


@pytest.fixture(scope="function")
async def gst_online_consultation_page(page: Page, base_url: str):
    """
    Authenticated online consultation page object for GST platform

    Auto-login and return authenticated page object
    Uses saved login state if available, otherwise performs login and saves state

    This fixture ensures:
    1. User is logged in
    2. Page is on the online consultation page (#/home)
    3. Doctor is selected
    """
    from pages.online_consultation_page import OnlineConsultationPage

    # Get test credentials
    username = os.getenv("GST_USERNAME", "17671792742")
    password = os.getenv("GST_PASSWORD", "123456")
    doctor_name = os.getenv("GST_DOCTOR_NAME", "罗慧")

    # Storage state file path
    storage_state_file = project_root / "tests" / "storage_state.json"

    # Create page object
    online_page = OnlineConsultationPage(page, base_url)

    # Navigate to home page
    await online_page.goto_online_consultation()

    # 等待页面加载
    await page.wait_for_timeout(2000)

    # 检查是否需要登录（如果不在登录页面，说明已使用保存的状态登录）
    if "#/login" in page.url:
        test_logger.info("No saved login state found, performing login...")
        # 需要登录
        try:
            # 等待登录表单出现
            await page.wait_for_selector("input[placeholder*='手机号']", timeout=10000)
            test_logger.info("Login page loaded, filling credentials...")

            # 填写手机号和验证码
            await page.fill("input[placeholder*='手机号']", username)
            await page.fill("input[placeholder*='验证码']", password)
            test_logger.info(f"Credentials filled: {username}")

            # 直接点击登录按钮（不点击"获取验证码"）
            await page.click("button:has-text('登录')")
            test_logger.info("Login button clicked")

            # 等待登录响应和页面跳转 - 增加等待时间
            await page.wait_for_timeout(5000)

            # 登录后选择医生
            test_logger.info("Waiting for doctor selection dialog...")

            # 先等待医生对话框出现（最多等待10秒）
            try:
                # 等待对话框出现
                await page.wait_for_selector("dialog, .dialog, [role='dialog']", timeout=10000)
                test_logger.info("Doctor selection dialog appeared")
            except:
                test_logger.warning("No doctor selection dialog found after 10 seconds")

            # 等待2秒让对话框完全加载
            await page.wait_for_timeout(2000)

            # 检查是否有对话框或单选按钮
            dialog_found = False
            dialogs = page.locator("dialog, .dialog, [role='dialog']")
            dialog_count = await dialogs.count()
            radios = page.locator("input[type='radio'], [role='radio']")
            radio_count = await radios.count()

            test_logger.info(f"Dialog count: {dialog_count}, Radio count: {radio_count}")

            if dialog_count > 0 or radio_count > 0:
                dialog_found = True
                test_logger.info("Doctor selection UI found, proceeding with selection")

            if dialog_found:
                # 选择医生
                doctor_radio = page.locator(f"radio:has-text('{doctor_name}')")
                if await doctor_radio.count() > 0:
                    await doctor_radio.first.click()
                    test_logger.info(f"Selected doctor: {doctor_name}")
                else:
                    await radios.first.click()
                    test_logger.info("Selected first available doctor")

                # 等待500ms确保选择生效
                await page.wait_for_timeout(500)

                # 点击确认切换按钮
                await page.click("button:has-text('确认'), button:has-text('确认切换')")
                test_logger.info("Confirmed doctor selection")

                # 等待页面跳转
                await page.wait_for_timeout(3000)
            else:
                # 没有找到医生对话框，检查URL
                current_url = page.url
                test_logger.info(f"No doctor dialog found. Current URL: {current_url}")

                # 如果还在登录页面，说明登录失败
                if "#/login" in current_url:
                    raise Exception("Login failed - still on login page and no doctor dialog found")

            # 保存登录状态到文件
            test_logger.info("Saving login state to file...")
            await page.context.storage_state(path=str(storage_state_file))
            test_logger.info(f"Login state saved to: {storage_state_file}")

        except Exception as e:
            test_logger.error(f"Login failed: {e}")
            raise
    else:
        test_logger.info("Using saved login state - already authenticated")

    # 验证已在在线问诊页面
    current_url = page.url
    if "#/login" in current_url:
        raise Exception(f"Login verification failed - still on login page: {current_url}")

    test_logger.info(f"GST authenticated: {username} as doctor {doctor_name}")
    test_logger.info(f"Successfully entered online consultation page: {current_url}")

    return online_page


# ==================== Pytest Hooks ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Test report hook - screenshot on failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = None
        if "page" in item.fixturenames:
            page = item.funcargs.get("page")

        if report.failed and page is not None:
            try:
                test_name = item.nodeid.replace("::", "_").replace("/", "_")
                screenshot_path = f"reports/screenshots/failure_{test_name}.png"

                # Ensure directory exists
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

                # Sync screenshot using asyncio.run
                try:
                    asyncio.run(page.screenshot(path=screenshot_path))
                except RuntimeError:
                    # Event loop is running, use sync_screenshot if available
                    pass

                # Attach to Allure report if file exists
                if os.path.exists(screenshot_path):
                    allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                test_logger.warning(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """Pytest configure hook - register custom markers"""
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "api: API测试")
    config.addinivalue_line("markers", "ui: UI测试")
    config.addinivalue_line("markers", "page: 页面标记")
    config.addinivalue_line("markers", "P0: P0级别测试-核心流程")
    config.addinivalue_line("markers", "P1: P1级别测试-重要功能")
    config.addinivalue_line("markers", "P2: P2级别测试-边缘场景")


def pytest_collection_modifyitems(config, items):
    """Modify collected test items - add default markers"""
    for item in items:
        if not any(item.get_closest_marker(name) for name in ["smoke", "regression", "api", "ui"]):
            item.add_marker(pytest.mark.regression)
