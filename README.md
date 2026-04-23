# GST在线问诊自动化测试框架

基于 **Python + Playwright + pytest** 的 Web 自动化测试框架，专为固生堂在线问诊系统设计，支持 Page Object Model (POM)、数据驱动测试、MCP AI集成、企业微信通知等功能。

## ✨ 特性

- 🎭 **Playwright** - 现代化的浏览器自动化工具
- 📄 **POM 模式** - Page Object Model 设计模式，易于维护
- 🧪 **Pytest** - 强大的测试框架，支持丰富的断言和插件
- 🤖 **MCP AI集成** - 支持AI辅助测试生成和智能元素定位
- 💬 **企业微信通知** - 测试结果自动推送企业微信群
- 📊 **多种报告** - HTML、Allure 报告（可选）
- 🔀 **并行执行** - 支持 pytest-xdist 并行运行测试（可选）
- 🎬 **视频录制** - 失败时自动录制视频（可选）
- 📸 **自动截图** - 失败时自动截图，按日期分类存储
- 🔁 **数据驱动** - 支持 JSON、CSV 数据源
- 🌍 **多环境** - 支持开发、测试、生产环境切换

## 📁 项目结构

```
d:/work/gst/
├── testcases/                  # 测试用例目录
│   ├── ui/                    # UI测试用例
│   └── api/                   # API测试用例（预留）
├── pages/                      # Page Object Model (POM)
│   ├── base_page.py           # 基础页面类
│   ├── login_page.py          # 登录页面对象
│   ├── online_consultation_page.py  # 在线问诊页面对象
│   └── user_management_page.py      # 用户管理页面对象
├── utils/                      # 工具类
│   ├── config_loader.py       # 配置读取工具
│   ├── html_report.py         # HTML报告生成（预留）
│   └── wecom_notify.py        # 企业微信通知
├── config/                     # 配置文件
│   └── config.yaml            # 主配置文件
├── reports/                    # 测试报告
│   ├── html/                  # HTML报告（预留）
│   └── allure/                # Allure报告（预留）
├── screenshots/                # 失败截图（按日期分类）
│   └── 2026-04-23/            # 日期目录示例
├── requirements.txt            # Python依赖
├── .env                       # 环境变量
└── conftest.py                # Pytest核心配置
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
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
playwright install --with-deps chromium
```

4. 配置环境变量
```bash
# 编辑 .env 文件，填写实际配置
GST_USERNAME=17671792742
GST_PASSWORD=123456
GST_DOCTOR_NAME=罗慧
WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
WECHAT_NOTIFICATIONS=true
```

### 运行测试

```bash
# 运行所有测试
pytest testcases/

# 运行冒烟测试
pytest testcases/ -m smoke

# 运行特定文件
pytest testcases/ui/test_online_consultation.py

# 运行特定标记
pytest testcases/ -m "P0"  # 核心流程
pytest testcases/ -m "P1"  # 重要功能  
pytest testcases/ -m "P2"  # 边缘场景
```

## 🏷️ 测试标记规范

### 优先级标记
- `@pytest.mark.P0` - 核心业务流程，必须通过
- `@pytest.mark.P1` - 重要功能，回归测试必跑
- `@pytest.mark.P2` - 边缘场景，完整回归时跑

### 测试类型标记  
- `@pytest.mark.smoke` - 冒烟测试（快速验证核心功能）
- `@pytest.mark.regression` - 回归测试（完整功能验证）

### 使用示例
```python
@allure.feature("在线问诊")
@pytest.mark.page("在线问诊")
class TestOnlineConsultation:

    @pytest.mark.P0
    @pytest.mark.smoke
    async def test_verify_page_elements(self, gst_online_consultation_page):
        """验证页面元素"""
        pass

    @pytest.mark.P1  
    @pytest.mark.regression
    async def test_search_patient_by_name(self, gst_online_consultation_page):
        """患者搜索功能"""
        pass
```

## 📝 用例编写规范

### 1. 文件命名
- **UI测试**: `testcases/ui/test_<功能模块>.py`
- **API测试**: `testcases/api/test_<功能模块>.py`

### 2. 类和方法结构
```python
@allure.feature("功能模块名称")
@pytest.mark.page("页面名称")
class Test功能模块名:

    @pytest.mark.P0/P1/P2
    @pytest.mark.smoke/regression  
    @allure.title("具体测试场景描述")
    async def test_具体功能(self, 页面对象fixture):
        """
        测试用例描述
        
        步骤：
        1. 前置条件
        2. 执行操作  
        3. 验证结果
        
        预期结果：
        - 具体预期行为
        """
        # 测试代码
```

### 3. Fixture使用
- **GST特有页面**: `gst_online_consultation_page` (自动登录+医生选择)
- **通用页面**: `login_page`, `dashboard_page` 等
- **测试数据**: `test_user` (向后兼容)

### 4. 断言规范
- 使用明确的断言信息
- 验证业务逻辑而非仅UI元素
- 包含失败时的详细错误信息

## 🔧 配置说明

### config/config.yaml
```yaml
base_url: "https://doc-online-test.gstyun.cn/webClinic/index.html"
headless: false
timeout:
  default: 30000
  navigation: 30000
reports:
  html_dir: "reports/html"
  allure_dir: "reports/allure" 
  screenshots_dir: "screenshots"
  auth_state: "reports/.auth/state.json"
cleanup:
  days: 3  # 自动清理3天前的旧文件
```

### .env 环境变量
```bash
# GST账号配置
GST_USERNAME=手机号
GST_PASSWORD=验证码/密码  
GST_DOCTOR_NAME=医生姓名

# 企业微信通知
WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
WECHAT_NOTIFICATIONS=true/false  # 开关控制

# 浏览器配置
HEADLESS=false
```

## 📈 报告查看

### 控制台报告
测试完成后自动显示统计信息：
```
[REPORT] 测试结果统计:
总计: 24 | 通过: 22 | 失败: 2 | 跳过: 0
```

### 企业微信通知
启用后自动推送测试结果到企业微信群。

### HTML/Allure报告（预留）
未来版本将支持完整的可视化报告。

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
- [MCP Protocol](https://github.com/modelcontextprotocol)