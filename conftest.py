"""
GST Online Consultation Testing - Simplified Configuration
结合 gst 项目业务特色 + automation 项目简洁架构
"""
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

import pytest
import allure
from dotenv import load_dotenv

from utils.config_loader import load_config
from utils.wecom_notify import send_wecom_notification

# 全局配置
config = None

# 加载环境变量和配置
load_dotenv()

# 报告相关全局变量
_TEST_RESULTS = []

# 存储状态文件路径
_STORAGE_STATE = None


# ---------------------------------------------------------------------------
# 启动时清理旧报告和截图
# ---------------------------------------------------------------------------
def _cleanup_old_files():
    """清理3天前的旧文件"""
    global config
    if config is None:
        config = load_config()
    
    cutoff = datetime.now() - timedelta(days=config.get('cleanup', {}).get('days', 3))
    
    # 清理HTML报告
    html_dir = Path(config['reports']['html_dir'])
    if html_dir.exists():
        for f in html_dir.iterdir():
            if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                f.unlink()
    
    # 清理Allure结果
    allure_dir = Path(config['reports']['allure_dir'])
    if allure_dir.exists():
        for f in allure_dir.iterdir():
            if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                f.unlink()
    
    # 清理截图
    screenshots_dir = Path(config['reports']['screenshots_dir'])
    if screenshots_dir.exists():
        for date_dir in screenshots_dir.iterdir():
            if date_dir.is_dir():
                try:
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    if dir_date.date() < cutoff.date():
                        shutil.rmtree(date_dir)
                except ValueError:
                    # 目录名不是日期格式，跳过
                    pass


# ---------------------------------------------------------------------------
# 测试数据 fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_user():
    """测试用户数据 - 保持向后兼容"""
    return {
        "username": os.getenv("GST_USERNAME", "17671792742"),
        "password": os.getenv("GST_PASSWORD", "123456")
    }

@pytest.fixture(scope="session")
def test_admin():
    """测试管理员数据"""
    return {
        "username": os.getenv("GST_ADMIN_USERNAME", "admin"),
        "password": os.getenv("GST_ADMIN_PASSWORD", "admin123")
    }


# ---------------------------------------------------------------------------
# 浏览器和页面 fixtures (同步版本)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser_type():
    """启动 Playwright - 同步版本"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="function")
def browser(browser_type):
    """启动浏览器 - 同步版本"""
    global config
    if config is None:
        config = load_config()
    
    browser = browser_type.chromium.launch(
        headless=config['headless'],
        channel="chrome",
        args=["--start-maximized"]
    )
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    """创建浏览器上下文 - 同步版本"""
    global config, _STORAGE_STATE
    if config is None:
        config = load_config()
    if _STORAGE_STATE is None:
        _STORAGE_STATE = config['reports']['auth_state']
    
    # 确保目录存在
    Path(_STORAGE_STATE).parent.mkdir(parents=True, exist_ok=True)
    
    # 如果存在保存的登录状态，直接使用
    if Path(_STORAGE_STATE).exists():
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            ignore_https_errors=True,
            accept_downloads=True,
            storage_state=_STORAGE_STATE
        )
    else:
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            ignore_https_errors=True,
            accept_downloads=True
        )
    
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """创建页面 - 同步版本"""
    global config
    if config is None:
        config = load_config()
    
    page = context.new_page()
    page.set_default_timeout(config['timeout']['default'])
    page.set_default_navigation_timeout(config['timeout']['navigation'])
    yield page
    page.close()

@pytest.fixture(scope="session")
def base_url():
    """获取基础URL - 优先使用配置文件，环境变量作为备用"""
    global config
    if config is None:
        config = load_config()
    # 优先使用配置文件中的 base_url
    base_url_from_config = config.get('base_url')
    print(f"DEBUG: base_url_from_config = {base_url_from_config}")
    if base_url_from_config:
        return base_url_from_config
    # 备用：从环境变量获取
    env_base_url = os.getenv("GST_BASE_URL", "https://doc-online-test.gstyun.cn/webClinic")
    print(f"DEBUG: env_base_url = {env_base_url}")
    return env_base_url


# ---------------------------------------------------------------------------
# GST 特色页面对象 fixtures (同步版本)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def gst_online_consultation_page(page, base_url):
    """
    GST在线问诊页面对象 - 保留原有业务逻辑（同步版本）
    """
    global config, _STORAGE_STATE
    if config is None:
        config = load_config()
    if _STORAGE_STATE is None:
        _STORAGE_STATE = config['reports']['auth_state']
    
    from pages.online_consultation_page_sync import OnlineConsultationPage
    
    # 获取测试账号
    username = os.getenv("GST_USERNAME", "17671792742")
    password = os.getenv("GST_PASSWORD", "123456")
    doctor_name = os.getenv("GST_DOCTOR_NAME", "罗慧")
    print(f"DEBUG: GST_USERNAME={username}, GST_PASSWORD={password}")
    
    # 创建页面对象
    online_page = OnlineConsultationPage(page, base_url)
    
    # 导航到主页
    online_page.goto_online_consultation()
    page.wait_for_timeout(2000)
    
    # 检查是否需要登录 - 调试URL
    print(f"DEBUG: Current page URL = {page.url}")
    if "#/login" in page.url:
        try:
            # 执行登录
            page.fill(config['selectors']['username'], username)
            page.fill(config['selectors']['password'], password)
            page.click(config['selectors']['login_btn'])
            page.wait_for_timeout(3000)
            
            # 选择医生
            try:
                page.wait_for_timeout(2000)
                radios = page.locator(config['selectors']['doctor_radio'])
                if radios.count() > 0:
                    radios.first.click()
                
                page.click(config['selectors']['confirm_btn'])
                page.wait_for_timeout(2000)
            except Exception as e:
                pass  # 可能不需要选择医生
            
            # 确保目录存在
            Path(_STORAGE_STATE).parent.mkdir(parents=True, exist_ok=True)
            # 保存登录状态
            page.context.storage_state(path=_STORAGE_STATE)
            
        except Exception as e:
            raise Exception(f"登录失败: {e}")
    
    return online_page


# ---------------------------------------------------------------------------
# 截图目录管理
# ---------------------------------------------------------------------------
def _ensure_screenshot_directory():
    """确保截图目录按日期分类"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        screenshot_dir = Path("screenshots") / today
        screenshot_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"\n[WARNING] 截图目录创建失败: {e}")


# ---------------------------------------------------------------------------
# 测试结果收集
# ---------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """收集测试结果"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # 记录测试结果
        test_result = {
            'name': item.nodeid,
            'status': report.outcome,
            'error': str(call.excinfo.value) if call.excinfo else ''
        }
        
        _TEST_RESULTS.append(test_result)


# ---------------------------------------------------------------------------
# 测试会话结束处理
# ---------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时生成简单报告并处理截图"""
    try:
        if _TEST_RESULTS:
            # 只生成最简单的统计信息
            total = len(_TEST_RESULTS)
            passed = sum(1 for r in _TEST_RESULTS if r['status'] == 'passed')
            failed = sum(1 for r in _TEST_RESULTS if r['status'] == 'failed')
            skipped = sum(1 for r in _TEST_RESULTS if r['status'] == 'skipped')
            
            print(f"\n[REPORT] 测试结果统计:")
            print(f"总计: {total} | 通过: {passed} | 失败: {failed} | 跳过: {skipped}")
            
            # 确保截图目录按日期分类
            if failed > 0:
                _ensure_screenshot_directory()
            
            # 发送企业微信通知
            send_wecom_notification(_TEST_RESULTS)
            
    except Exception as e:
        print(f"\n[WARNING] 统计生成失败: {e}")


# ---------------------------------------------------------------------------
# 标记注册
# ---------------------------------------------------------------------------
def pytest_configure(config):
    # 注册自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "ui: UI测试")
    config.addinivalue_line("markers", "P0: P0级别测试-核心流程")
    config.addinivalue_line("markers", "P1: P1级别测试-重要功能")
    config.addinivalue_line("markers", "P2: P2级别测试-边缘场景")
    config.addinivalue_line("markers", "page: 页面标记")
    config.addinivalue_line("markers", "critical: 关键业务流程")
    
    # 启动时清理3天前的旧文件
    _cleanup_old_files()


# ---------------------------------------------------------------------------
# 默认标记设置
# ---------------------------------------------------------------------------
def pytest_collection_modifyitems(config, items):
    """为所有测试添加默认标记"""
    for item in items:
        if not any(item.get_closest_marker(name) for name in ["smoke", "regression", "ui"]):
            item.add_marker(pytest.mark.regression)