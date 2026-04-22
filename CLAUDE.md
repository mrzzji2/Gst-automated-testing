# 项目 AI 上下文

## 项目简介

这是一个基于 **Playwright + pytest + Allure** 的 Web UI 自动化回归测试框架，被测平台为 `https://doc-online-test.gstyun.cn/webClinic/index.html#/`。

## 核心约定

### 用例放在哪里
- UI 测试用例放在 `testcases/ui/` 目录下，命名规则：`test_<模块名>.py`
- API 测试用例放在 `testcases/api/` 目录下，命名规则：`test_<模块名>_api.py`
- 一个业务模块一个文件

### 页面对象放在哪里
- 所有页面对象放在 `pages/` 目录下，命名规则：`<模块名>_page.py`
- 必须继承 `pages/base_page.py` 中的 `BasePage`

### 不需要动的文件
- `conftest.py`：登录 fixture、失败截图、飞书通知，已配置好，不需要修改
- `utils/`：工具函数，不需要修改
- `config/config.yaml`：平台配置，不需要修改

## 用例编写规范

```python
import pytest
import allure
from pages.xxx_page import XxxPage
from utils.config_loader import load_config

config = load_config()


@allure.feature("模块名")          # 对应 Allure 报告中的一级分类
@pytest.mark.page("页面中文名")    # 通知展示用，填页面的中文名称，如"医生工作台"
class TestXxx:

    @allure.story("子功能名")       # 对应 Allure 报告中的二级分类
    @allure.title("具体场景描述")
    @pytest.mark.P0               # 优先级：P0 / P1 / P2
    @pytest.mark.smoke            # 标签：smoke / regression（可叠加）
    def test_xxx(self, page):
        """用一句话描述这个用例在验证什么"""
        xxx_page = XxxPage(page)
        # ...
```

### 优先级说明
- `P0 + smoke`：核心流程，每次部署必跑
- `P1 + regression`：重要功能，回归时必跑
- `P2`：边缘场景，完整回归时跑

## Page Object 编写规范

```python
import allure
from pages.base_page import BasePage
from utils.config_loader import load_config

config = load_config()


class XxxPage(BasePage):

    # 把选择器定义为类属性，方便维护
    BTN_SUBMIT = "button:has-text('提交')"
    INPUT_NAME  = "input[placeholder='请输入名称']"

    @allure.step("执行某个操作")
    def do_something(self, value: str) -> None:
        self.fill(self.INPUT_NAME, value, "名称输入框")
        self.click(self.BTN_SUBMIT, "提交按钮")
```

## BasePage 提供的方法

| 方法 | 说明 |
|------|------|
| `navigate(path)` | 跳转到指定路径 |
| `click(selector, description)` | 点击元素 |
| `fill(selector, text, description)` | 填写输入框 |
| `get_text(selector)` | 获取元素文本 |
| `is_visible(selector)` | 判断元素是否可见 |
| `wait_for_element(selector)` | 等待元素出现 |
| `expect_url(pattern)` | 断言 URL 匹配 |
| `expect_text(selector, text)` | 断言元素文本 |
| `expect_visible(selector)` | 断言元素可见 |
| `take_screenshot(name)` | 手动截图并附加到 Allure |

## Fixture 说明

- `page`：已注入登录态，直接使用，无需手动登录
- `browser`：需要无登录态时使用（如测试登录失败场景）
- `api_session`：用于接口测试或需要与接口数据比对的 UI 测试，返回 dict，包含：
  - `request`：Playwright `APIRequestContext`，自动携带登录 session 和鉴权 headers
  - `url`：optionTable 接口完整 URL
  - `method`：请求方法（通常为 POST）
  - `headers`：含 `authorization`、`indentifyid` 的请求头
  - `body`：选完用户组后的实际请求体（含正确 groupId）；未捕获时为 `None`，需在用例中 `pytest.skip`
  - UI 测试需要接口原始数据时可直接在方法签名加 `api_session` 参数，例如 `def test_xxx(self, page, api_session)`

## 运行命令

```bash
pytest -m smoke        # 冒烟测试
pytest -m regression   # 回归测试
pytest                 # 全量
```
