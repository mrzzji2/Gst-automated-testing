# Makefile
# 常用命令快捷方式

.PHONY: help install test clean lint format docker-build docker-run

# 默认目标
.DEFAULT_GOAL := help

# 项目配置
PROJECT_NAME := web-automation
PYTHON := python3
VENV := venv
ACTIVATE := $(VENV)/bin/activate

# 颜色定义
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

## help: 显示帮助信息
help:
	@echo "$(GREEN)Web Automation Test Framework - 常用命令$(NC)"
	@echo ""
	@echo "$(YELLOW)安装和设置$(NC)"
	@echo "  make install        - 安装依赖"
	@echo "  make setup          - 初始化项目"
	@echo "  make install-browsers - 安装浏览器"
	@echo ""
	@echo "$(YELLOW)测试命令$(NC)"
	@echo "  make test           - 运行所有测试"
	@echo "  make test-smoke     - 运行冒烟测试"
	@echo "  make test-regression - 运行回归测试"
	@echo "  make test-parallel  - 并行运行测试"
	@echo "  make test-report    - 运行测试并生成报告"
	@echo ""
	@echo "$(YELLOW)代码质量$(NC)"
	@echo "  make lint           - 代码检查"
	@echo "  make format         - 代码格式化"
	@echo ""
	@echo "$(YELLOW)Docker 命令$(NC)"
	@echo "  make docker-build   - 构建 Docker 镜像"
	@echo "  make docker-run     - 运行 Docker 容器"
	@echo "  make docker-compose - 使用 Docker Compose"
	@echo ""
	@echo "$(YELLOW)其他命令$(NC)"
	@echo "  make clean          - 清理临时文件"
	@echo "  make show-report    - 显示测试报告"
	@echo "  make allure-serve   - 启动 Allure 服务"

## install: 安装 Python 依赖
install:
	@echo "$(GREEN)安装依赖...$(NC)"
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@. $(ACTIVATE) && pip install --upgrade pip
	@. $(ACTIVATE) && pip install -r requirements.txt
	@. $(ACTIVATE) && pip install -r requirements-dev.txt
	@echo "$(GREEN)依赖安装完成$(NC)"

## setup: 初始化项目
setup: install install-browsers create-dirs
	@echo "$(GREEN)项目初始化完成$(NC)"

## install-browsers: 安装 Playwright 浏览器
install-browsers:
	@echo "$(GREEN)安装浏览器...$(NC)"
	@. $(ACTIVATE) && playwright install --with-deps chromium
	@echo "$(GREEN)浏览器安装完成$(NC)"

## create-dirs: 创建必要的目录
create-dirs:
	@mkdir -p reports/html reports/allure reports/junit reports/screenshots reports/videos logs/auto

## test: 运行所有测试
test:
	@echo "$(GREEN)运行测试...$(NC)"
	@. $(ACTIVATE) && pytest tests/ -v

## test-smoke: 运行冒烟测试
test-smoke:
	@echo "$(GREEN)运行冒烟测试...$(NC)"
	@. $(ACTIVATE) && pytest tests/ -m smoke -v

## test-regression: 运行回归测试
test-regression:
	@echo "$(GREEN)运行回归测试...$(NC)"
	@. $(ACTIVATE) && pytest tests/ -m regression -v

## test-parallel: 并行运行测试
test-parallel:
	@echo "$(GREEN)并行运行测试...$(NC)"
	@. $(ACTIVATE) && pytest tests/ -n auto -v

## test-report: 运行测试并生成报告
test-report:
	@echo "$(GREEN)运行测试并生成报告...$(NC)"
	@. $(ACTIVATE) && pytest tests/ -v \
		--html=reports/html/report.html \
		--self-contained-html \
		--alluredir=reports/allure \
		--junitxml=reports/junit/results.xml
	@echo "$(GREEN)报告已生成$(NC)"

## lint: 代码检查
lint:
	@echo "$(GREEN)代码检查...$(NC)"
	@. $(ACTIVATE) && flake8 tests/ pages/ utils/ elements/

## format: 代码格式化
format:
	@echo "$(GREEN)代码格式化...$(NC)"
	@. $(ACTIVATE) && black tests/ pages/ utils/ elements/

## clean: 清理临时文件
clean:
	@echo "$(GREEN)清理临时文件...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf reports/html/* reports/allure/* reports/junit/*
	@echo "$(GREEN)清理完成$(NC)"

## docker-build: 构建 Docker 镜像
docker-build:
	@echo "$(GREEN)构建 Docker 镜像...$(NC)"
	@docker build -f docker/Dockerfile -t $(PROJECT_NAME):test .

## docker-run: 运行 Docker 容器
docker-run: docker-build
	@echo "$(GREEN)运行 Docker 容器...$(NC)"
	@docker run --rm \
		-v $(PWD)/reports:/app/reports \
		-e APP_BASE_URL=$(APP_BASE_URL) \
		$(PROJECT_NAME):test

## docker-compose: 使用 Docker Compose
docker-compose:
	@echo "$(GREEN)使用 Docker Compose...$(NC)"
	@docker-compose -f docker/docker-compose.yml up --build

## show-report: 显示测试报告
show-report:
	@echo "$(GREEN)打开测试报告...$(NC)"
	@python -m webbrowser reports/html/report.html || true

## allure-serve: 启动 Allure 服务
allure-serve:
	@echo "$(GREEN)启动 Allure 服务...$(NC)"
	@allure serve reports/allure

## allure-generate: 生成 Allure 报告
allure-generate:
	@echo "$(GREEN)生成 Allure 报告...$(NC)"
	@allure generate reports/allure -o reports/allure-report --clean

## update-dependencies: 更新依赖
update-dependencies:
	@echo "$(GREEN)更新依赖...$(NC)"
	@. $(ACTIVATE) && pip install --upgrade -r requirements.txt
	@. $(ACTIVATE) && pip install --upgrade -r requirements-dev.txt

## freeze: 导出依赖版本
freeze:
	@. $(ACTIVATE) && pip freeze > requirements-freeze.txt
	@echo "$(GREEN)依赖版本已导出到 requirements-freeze.txt$(NC)"
