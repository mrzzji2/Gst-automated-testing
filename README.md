# Web Automation Test Framework

基于 Python + Playwright 的 Web 自动化测试框架，支持 Page Object Model (POM)、数据驱动测试、并行执行、Jenkins 集成等功能。

## ✨ 特性

- 🎭 **Playwright** - 现代化的浏览器自动化工具
- 📄 **POM 模式** - Page Object Model 设计模式，易于维护
- 🧪 **Pytest** - 强大的测试框架，支持丰富的断言和插件
- 📊 **多种报告** - HTML、Allure、JUnit XML 报告
- 🔀 **并行执行** - 支持 pytest-xdist 并行运行测试
- 🎬 **视频录制** - 失败时自动录制视频
- 📸 **自动截图** - 失败时自动截图
- 🔁 **数据驱动** - 支持 JSON、CSV、Excel 数据源
- 🌍 **多环境** - 支持开发、测试、生产环境切换
- 🐳 **Docker 支持** - 容器化测试环境
- 🔄 **Jenkins 集成** - 开箱即用的 Jenkinsfile

## 📁 项目结构

```
d:/work/gst/
├── tests/                      # 测试用例目录
│   ├── conftest.py            # pytest核心配置
│   └── test_cases/            # 具体测试用例
├── pages/                      # Page Object Model (POM)
│   ├── base_page.py           # 基础页面类
│   ├── login_page.py          # 登录页面对象
│   └── dashboard_page.py      # 仪表盘页面对象
├── elements/                   # 页面元素定位器
│   ├── base_locators.py       # 通用定位器
│   ├── login_locators.py      # 登录页定位器
│   └── dashboard_locators.py  # 仪表盘页定位器
├── utils/                      # 工具类
│   ├── webdriver.py           # Playwright浏览器管理
│   ├── config.py              # 配置读取工具
│   ├── logger.py              # 日志封装
│   ├── screenshot.py          # 截图工具
│   └── wait_utils.py          # 等待策略封装
├── data/                       # 测试数据
│   └── fixtures/              # 数据文件
├── config/                     # 配置文件
│   ├── config.yaml            # 主配置
│   ├── environments/          # 环境配置
│   └── pytest.ini             # pytest配置
├── reports/                    # 测试报告
├── jenkins/                    # Jenkins集成
│   ├── Jenkinsfile            # Pipeline定义
│   └── scripts/               # 辅助脚本
├── docker/                     # Docker支持
│   ├── Dockerfile             # 测试环境镜像
│   └── docker-compose.yml     # 本地开发环境
├── requirements.txt            # Python依赖
├── .env                        # 环境变量
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip
- 浏览器（Chromium/Firefox/WebKit）

### 安装

1. 克隆项目
```bash
git clone <repository-url>
cd d:/work/gst
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. 安装 Playwright 浏览器
```bash
playwright install --with-deps chromium
```

5. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填写实际配置
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定标记的测试
pytest tests/ -m smoke

# 运行特定文件
pytest tests/test_cases/test_login.py

# 并行执行
pytest tests/ -n auto

# 生成报告
pytest tests/ --html=reports/html/report.html --self-contained-html
```

## 📋 命令行选项

```bash
pytest tests/ \
  --browser=chromium \          # 浏览器类型
  --headed \                    # 有头模式
  --base-url=https://test.com \ # 基础URL
  -v \                          # 详细输出
  --tb=short \                  # 回溯信息
  -m "smoke" \                  # 测试标记
  --slow \                      # 包含慢速测试
  --alluredir=reports/allure    # Allure报告目录
```

## 🐳 Docker 使用

### 构建镜像

```bash
docker build -f docker/Dockerfile -t web-automation:test .
```

### 运行测试

```bash
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  -e APP_BASE_URL=https://test.example.com \
  web-automation:test
```

### 使用 Docker Compose

```bash
# 运行测试
docker-compose -f docker/docker-compose.yml up

# 启动 Allure 报告服务
docker-compose -f docker/docker-compose.yml --profile report up

# 启动 Jenkins Agent
docker-compose -f docker/docker-compose.yml --profile jenkins up
```

## 📊 Jenkins 集成

1. 创建新的 Pipeline 任务
2. 配置 SCM 指向项目仓库
3. Pipeline 脚本路径填写：`jenkins/Jenkinsfile`
4. 构建参数：
   - `BROWSER`: 浏览器类型
   - `ENVIRONMENT`: 测试环境
   - `RUN_SLOW_TESTS`: 是否运行慢速测试
   - `HEADED_MODE`: 是否使用有头模式
   - `PYTEST_ARGS`: 额外的 pytest 参数

## 🔧 配置说明

### config/config.yaml

主配置文件，包含应用、URL、浏览器、测试、日志等配置。

### config/environments/

环境特定配置：
- `dev.yaml` - 开发环境
- `test.yaml` - 测试环境
- `prod.yaml` - 生产环境

### .env

环境变量配置（敏感信息）：
```bash
APP_ENV=test
APP_BASE_URL=https://test.example.com
TEST_USER_USERNAME=test@example.com
TEST_USER_PASSWORD=password123
```

## 📝 编写测试

### 基础测试示例

```python
import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
async def test_login(page, base_url, login_page):
    """测试登录功能"""
    await login_page.goto_login()
    await login_page.login("test@example.com", "password123")

    await login_page.wait_for_url("**/dashboard")
    assert "dashboard" in login_page.get_current_url()
```

### 使用 Page Object

```python
from pages.dashboard_page import DashboardPage

async def test_dashboard(dashboard_page):
    """测试仪表盘"""
    await dashboard_page.goto_dashboard()
    await dashboard_page.assert_on_dashboard()

    stats = await dashboard_page.get_all_stats()
    assert stats["users"] > 0
```

### 数据驱动测试

```python
@pytest.mark.parametrize("username,password,expected", [
    ("user1@example.com", "pass123", "success"),
    ("user2@example.com", "pass123", "success"),
    ("invalid@example.com", "wrong", "error"),
])
async def test_login_scenarios(login_page, username, password, expected):
    """参数化登录测试"""
    await login_page.goto_login()
    await login_page.login(username, password)

    if expected == "success":
        await login_page.wait_for_url("**/dashboard")
    else:
        await login_page.assert_on_login_page()
```

## 🏷️ 测试标记

```python
@pytest.mark.smoke         # 冒烟测试
@pytest.mark.regression    # 回归测试
@pytest.mark.sanity        # 精简测试
@pytest.mark.api           # API测试
@pytest.mark.ui            # UI测试
@pytest.mark.slow          # 慢速测试
@pytest.mark.critical      # 关键业务流程
```

## 📈 报告查看

### HTML 报告

```bash
pytest tests/ --html=reports/html/report.html --self-contained-html
# 在浏览器中打开 reports/html/report.html
```

### Allure 报告

```bash
# 安装 Allure 命令行工具
# macOS: brew install allure
# Linux: sudo apt-get install allure
# Windows: scoop install allure

# 生成报告
allure generate reports/allure -o reports/allure-report --clean

# 打开报告
allure open reports/allure-report
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 👥 作者

- Your Name - 初始工作

## 🙏 致谢

- [Playwright Python](https://playwright.dev/python/)
- [Pytest](https://docs.pytest.org/)
- [Allure Report](https://allurereport.org/)
