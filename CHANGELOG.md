# Change Log

## [Unreleased]

### Added
- 初始化项目结构
- 实现基础页面类 (BasePage)
- 实现登录页面对象 (LoginPage)
- 实现仪表盘页面对象 (DashboardPage)
- 实现用户管理页面对象 (UserManagementPage)
- 实现 pytest 配置和 fixtures
- 实现工具类 (webdriver, config, logger, screenshot, wait_utils)
- 实现 Jenkins 集成 (Jenkinsfile, 脚本)
- 实现 Docker 支持 (Dockerfile, docker-compose)
- 实现测试用例示例 (login, dashboard, user_management)
- 实现元素定位器 (base, login, dashboard, user_management)

### Features
- Page Object Model (POM) 设计模式
- 多环境配置支持 (dev, test, prod)
- 失败自动截图和视频录制
- 并行测试执行支持
- 多种报告格式 (HTML, Allure, JUnit XML)
- 数据驱动测试支持
- Jenkins CI/CD 集成
- Docker 容器化测试环境
- 智能等待策略
- 日志记录系统

### Configuration
- 支持通过 config.yaml 配置
- 支持通过 .env 文件配置环境变量
- 支持命令行参数覆盖

### Testing
- 冒烟测试标记
- 回归测试标记
- API 测试标记
- UI 测试标记
- 慢速测试标记
- 关键业务流程标记

---

## [1.0.0] - 2025-01-08

### Added
- 项目初始版本
- 完整的测试框架实现
- 文档和示例
