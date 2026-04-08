#!/bin/bash
# Docker Entrypoint Script
# 容器启动脚本

set -e

echo "========================================="
echo "  Web Automation Test Container"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 显示环境信息
show_env_info() {
    print_info "Environment Information:"
    echo "  APP_ENV:        ${APP_ENV:-test}"
    echo "  APP_BASE_URL:   ${APP_BASE_URL:-not set}"
    echo "  BROWSER_TYPE:   ${BROWSER_TYPE:-chromium}"
    echo "  BROWSER_HEADLESS: ${BROWSER_HEADLESS:-true}"
    echo "  LOG_LEVEL:      ${LOG_LEVEL:-INFO}"
    echo ""
}

# 创建必要的目录
create_directories() {
    print_info "Creating necessary directories..."

    mkdir -p reports/html
    mkdir -p reports/allure
    mkdir -p reports/junit
    mkdir -p reports/screenshots
    mkdir -p reports/videos
    mkdir -p logs/auto
}

# 验证 Playwright 安装
verify_playwright() {
    print_info "Verifying Playwright installation..."

    python -c "import playwright; print(f'Playwright version: {playwright.__version__}')" || {
        print_warn "Playwright not found, installing..."
        playwright install --with-deps chromium
    }
}

# 执行传入的命令
execute_command() {
    print_info "Executing command..."

    # 如果没有提供命令，运行默认测试
    if [ -z "$1" ]; then
        print_info "No command provided, running default tests..."
        exec pytest tests/ -v --browser=chromium --headless=true
    else
        # 执行提供的命令
        exec "$@"
    fi
}

# 主函数
main() {
    echo ""

    show_env_info
    create_directories
    verify_playwright

    print_info "Container ready!"
    echo ""

    # 执行命令
    execute_command "$@"
}

# 执行主函数
main "$@"
