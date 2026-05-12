"""
GST Online Consultation Testing - Simplified Configuration
结合 gst 项目业务特色 + automation 项目简洁架构
"""
import os
import shutil
import inspect
from pathlib import Path
from datetime import datetime, timedelta

import pytest
import allure
from dotenv import load_dotenv
from loguru import logger

from utils.config_loader import load_config
from utils.wecom_notify import send_wecom_notification

# 全局配置
config = None

# 加载环境变量和配置
load_dotenv()

# 报告相关全局变量
_TEST_RESULTS = []
_SCREENSHOTS = []

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
    """获取基础URL"""
    global config
    if config is None:
        config = load_config()
    return config['base_url']


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
    
    from pages.online_consultation_page import OnlineConsultationPage
    
    # 获取测试账号
    username = os.getenv("GST_USERNAME", "18500629847")
    password = os.getenv("GST_PASSWORD", "123456")
    
    # 创建页面对象
    online_page = OnlineConsultationPage(page, base_url)

    # 导航到主页
    online_page.goto_online_consultation()
    logger.info("Navigation completed")

    # 会话有效性检查：检查患者列表是否为空
    patient_count = online_page.get_patient_list_count()
    logger.info(f"Patient count after navigation: {patient_count}")

    # 如果患者列表为空，需要执行登录流程
    if patient_count == 0:
        logger.info("Patient list is empty, proceeding with login")
    else:
        logger.info(f"Session valid, found {patient_count} patients")
        # 已登录，直接返回
        return online_page

    # 检查是否需要登录
    if "#/login" in page.url:
        logger.info("Login page detected, proceeding with login")
        try:
            # 智能等待：等待登录表单出现
            page.wait_for_selector(config['selectors']['username'], timeout=10000)

            # 调试：检查当前页面状态
            logger.info(f"Current URL before login: {page.url}")

            # 调试：检查登录表单是否存在
            username_field = page.locator(config['selectors']['username']).first
            password_field = page.locator(config['selectors']['password']).first
            login_button = page.locator(config['selectors']['login_btn']).first

            logger.info(f"Username field count: {username_field.count()}")
            logger.info(f"Password field count: {password_field.count()}")
            logger.info(f"Login button count: {login_button.count()}")

            # 执行登录
            username_field.fill(username)
            logger.info(f"Filled username: {username}")

            password_field.fill(password)
            logger.info(f"Filled password: ***")

            login_button.click()
            logger.info("Clicked login button")

            # 智能等待：等待登录后URL变化或医生选择对话框出现
            login_success = False
            try:
                page.wait_for_selector('[role="dialog"]', timeout=8000)
                logger.info("Doctor selection dialog appeared")

                # 选择医生
                try:
                    # 智能等待：等待单选按钮出现
                    first_doctor = page.get_by_role("radio").first
                    first_doctor.wait_for(state="visible", timeout=3000)
                    if first_doctor.count() > 0:
                        first_doctor.click()
                        logger.info("Selected first doctor from the list")

                    page.click(config['selectors']['confirm_btn'])
                    # 智能等待：等待跳转到主页（可能是 home 或 aiHome）
                    page.wait_for_url("**/aiHome", timeout=10000)
                    logger.info("Navigated to AI home page")
                    # 导航到在线问诊页面
                    online_page.goto_online_consultation()
                    login_success = True
                except Exception as e:
                    logger.warning(f"Doctor selection warning: {e}")
                    # 即使医生选择失败，也尝试保存状态
                    login_success = True
            except:
                # 没有医生选择对话框，可能已经登录了
                try:
                    page.wait_for_url("**/home", timeout=5000)
                    login_success = True
                except:
                    pass

            # 登录成功后保存状态
            if login_success:
                # 确保目录存在
                Path(_STORAGE_STATE).parent.mkdir(parents=True, exist_ok=True)
                # 保存登录状态
                page.context.storage_state(path=_STORAGE_STATE)
                logger.info(f"Login state saved to: {_STORAGE_STATE}")
            
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
# 错误信息翻译（将 Playwright 英文错误转中文）
# ---------------------------------------------------------------------------
_ERROR_TRANSLATIONS = [
    ("Timeout", "操作超时，页面响应过慢或元素未出现"),
    ("strict mode violation", "选择器匹配到多个元素，请使用精确选择器"),
    ("wait_for_selector", "等待指定元素超时，目标元素未在预期时间内出现"),
    ("wait_for_timeout", "等待超时，页面加载或响应过慢"),
    ("page.goto", "页面导航失败，目标网址无法访问"),
    ("Target closed", "页面、浏览器上下文或浏览器已被关闭"),
    ("connection refused", "网络连接被拒绝，目标服务可能未启动"),
    ("No element found", "找不到指定元素，页面结构可能已变化"),
    ("is not visible", "元素不可见，无法进行操作"),
    ("is not enabled", "元素未启用，无法进行操作"),
    ("404", "请求的资源不存在（404）"),
    ("500", "服务器内部错误（500）"),
    ("assert", "断言失败，实际结果与预期不符"),
]


def translate_error(msg: str) -> str:
    """将常见的自动化测试错误信息翻译为中文"""
    if not msg:
        return msg
    for eng, chn in _ERROR_TRANSLATIONS:
        if eng in msg:
            return f"【{chn}】\n{msg}"
    return msg


# ---------------------------------------------------------------------------
# 测试结果收集
# ---------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """收集测试结果"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # 获取 Allure title（中文名）
        title = None

        # 方法1：从函数的 allure.title 装饰器获取
        if hasattr(item, 'obj') and item.obj:
            try:
                # 获取源代码行
                source = inspect.getsource(item.obj)

                # 查找 @allure.title("xxx") 或 @allure.title('xxx')
                import re
                title_match = re.search(r'@allure\.title\([\'"]([^\'"]+)[\'"]\)', source)
                if title_match:
                    title = title_match.group(1)
                else:
                    # 尝试获取整个文件的源代码
                    file_path = str(item.fspath)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_source = f.read()
                    # 使用函数名定位
                    func_name = item.name
                    # 在函数定义前查找 allure.title
                    pattern = rf'@allure\.title\([\'"]([^\'"]+)[\'"]\)[^@]*def {func_name}'
                    title_match = re.search(pattern, file_source, re.DOTALL)
                    if title_match:
                        title = title_match.group(1)
            except Exception as e:
                logger.debug(f"Failed to get allure title: {e}")

        # 方法2：从函数的 docstring 获取（如果没有找到 title）
        if not title and hasattr(item, 'obj') and item.obj:
            doc = item.obj.__doc__
            if doc:
                title = doc.strip().split('\n')[0].strip()

        # 方法3：使用函数名作为后备
        if not title:
            title = item.nodeid.split('::')[-1]

        # 获取优先级
        priority = None
        for p in ["P0", "P1", "P2"]:
            if item.get_closest_marker(p):
                priority = p
                break

        # 获取额外信息（如看诊数量等）
        extra_info = ""
        for key, value in item.user_properties:
            if key == 'extra_info':
                extra_info = value
                break

        # 记录测试结果
        test_result = {
            'name': item.nodeid,
            'title': title,
            'status': report.outcome,
            'error': translate_error(str(call.excinfo.value)) if call.excinfo else '',
            'duration': report.duration if hasattr(report, 'duration') else 0,
            'priority': priority or 'P2',
            'extra_info': extra_info
        }

        _TEST_RESULTS.append(test_result)


# ---------------------------------------------------------------------------
# 测试会话结束处理
# ---------------------------------------------------------------------------
def _get_report_title(test_results: list) -> str:
    """从测试结果中提取项目名称，组装报告标题"""
    import re
    # 提取所有涉及的测试文件路径（去重）
    file_paths = set()
    for r in test_results:
        nodeid = r.get("name", "")
        parts = nodeid.split("::")
        if parts:
            file_paths.add(parts[0])

    # 从每个文件的 docstring 提取项目名
    project_names = []
    for fp in sorted(file_paths):
        try:
            with open(fp, encoding="utf-8") as fh:
                content = fh.read()
            # 找文档注释
            m = re.search(r'"""(.+?)"""', content, re.DOTALL)
            if m:
                doc = m.group(1)
                # 在文档注释中查找包含"测试用例"的行，提取前面的文字
                for line in doc.split("\n"):
                    line = line.strip()
                    if "测试用例" in line:
                        name_m = re.match(r"^(.*?)测试用例", line)
                        if name_m:
                            name = name_m.group(1).strip().rstrip(" -—（(")
                            if name and name not in project_names:
                                project_names.append(name)
                                break
        except:
            continue

    if not project_names:
        return ""
    elif len(project_names) == 1:
        return project_names[0]
    else:
        return " + ".join(project_names)


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时生成自动化报告样式并发送企业微信通知"""
    try:
        from _pytest.terminal import TerminalReporter
        reporter = session.config.pluginmanager.get_plugin('terminalreporter')
        if reporter:
            stats = reporter.stats

            # 收集本次所有报告的 page_name 标记，用于组装企业微信标题
            all_reports = []
            for key in ("passed", "failed", "error", "skipped"):
                all_reports.extend(stats.get(key, []))

            # 计算统计信息
            total = len(all_reports)
            passed = len(stats.get("passed", []))
            failed = len(stats.get("failed", [])) + len(stats.get("error", []))
            skipped = len(stats.get("skipped", []))

            # 从测试文件 docstring 提取项目名
            project_title = _get_report_title(_TEST_RESULTS)
            if project_title:
                title = f"[GST] {project_title} 测试报告"
            else:
                title = "[GST] 自动化测试报告"

            # 打印报告统计
            print(f"\n{title}")
            print(f"[PASS] 通过: {passed}/{total}")
            print(f"[FAIL] 失败: {failed}/{total}")
            print(f"[SKIP] 跳过: {skipped}/{total}")

            # 确保截图目录按日期分类
            if failed > 0:
                _ensure_screenshot_directory()

            # 生成并打开 HTML 报告
            try:
                from utils.html_report import generate_html_report, generate_report_index, open_report_in_browser
                html_report_path = generate_html_report(_TEST_RESULTS, _SCREENSHOTS, report_title=project_title)
                if html_report_path:
                    open_report_in_browser(html_report_path)
                # 更新历史报告索引
                generate_report_index()
            except Exception as e:
                print(f"\n[WARNING] HTML报告生成失败: {e}")
            
            # 发送企业微信通知（保留 gst 特色）
            send_wecom_notification(_TEST_RESULTS)
            
    except Exception as e:
        print(f"\n[WARNING] 报告生成失败: {e}")


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