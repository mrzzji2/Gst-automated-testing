# Allure 报告工具配置

本项目已集成 Allure 测试报告工具，支持生成美观、详细的测试报告。

## 快速开始

### 1. 安装 Allure

运行项目根目录下的安装脚本：

```bash
install_allure.bat
```

该脚本会自动：
- 下载 Allure 最新版本
- 解压到用户目录
- 配置环境变量

**手动安装：**

1. 下载 Allure: https://github.com/allure-framework/allure2/releases
2. 解压到本地目录，例如 `C:\allure-2.29.0`
3. 将 `C:\allure-2.29.0\bin` 添加到系统 PATH 环境变量
4. 验证安装：`allure --version`

### 2. 运行测试

安装 Allure 后，所有运行脚本会自动使用 Allure 生成报告：

```bash
# 方式 1: 使用批处理文件
run_tests.bat

# 方式 2: 使用 Python 脚本
python run_tests.py --p0

# 方式 3: 使用简单批处理
run_with_report --p0
```

### 3. 查看报告

**动态报告（推荐）：**
```bash
allure serve reports/allure
```
会自动在浏览器打开报告，支持实时更新。

**静态报告：**
```bash
allure generate reports/allure --clean -o reports/allure-html
```
生成静态 HTML 文件，可部署到服务器。

## Allure vs pytest-html

| 特性 | Allure | pytest-html |
|------|--------|-------------|
| **历史记录** | ✅ 累积所有测试数据 | ❌ 每次覆盖 |
| **图表统计** | ✅ 丰富的图表和趋势 | ✅ 基础图表 |
| **截图/附件** | ✅ 自动附加 | ✅ 支持 |
| **插件扩展** | ✅ 支持自定义插件 | ❌ 有限 |
| **安装复杂度** | ⚠️ 需要单独安装 | ✅ pip install |
| **报告格式** | 需要服务或生成静态 | 静态 HTML |

## 使用建议

- **开发/调试**：使用 pytest-html（快速、简单）
- **CI/CD**：使用 Allure（历史追踪、趋势分析）
- **团队协作**：使用 Allure（更好的报告展示）

## 自动切换机制

项目中的所有运行脚本都支持自动检测：

1. **如果 Allure 可用**：使用 Allure 生成报告
2. **如果 Allure 不可用**：自动降级使用 pytest-html

无需修改代码，安装 Allure 后即自动生效。

## 常见问题

### Q: 安装后仍提示找不到 Allure 命令？

A: 重启终端或运行以下命令：
```bash
set PATH=%USERPROFILE%\allure\allure-2.29.0\bin;%PATH%
```

### Q: 如何更新 Allure 版本？

A: 重新运行 `install_allure.bat`，会自动更新到最新版本。

### Q: Allure 报告数据保存在哪里？

A: `reports/allure/` 目录，每次运行测试会累积数据。

### Q: 如何清除 Allure 历史数据？

A: 删除 `reports/allure/` 目录：
```bash
rmdir /s /q reports\allure
mkdir reports\allure
```

## 相关文件

- `install_allure.bat` - Allure 安装脚本
- `allure_env.bat` - Allure 环境变量配置
- `run_tests.bat` - 交互式测试运行（自动检测 Allure）
- `run_tests.py` - Python 测试运行（自动检测 Allure）
- `run_with_report.bat` - 快速测试运行（自动检测 Allure）