#!/bin/bash
# Setup Script for Jenkins
# 环境准备脚本

set -e  # 遇到错误立即退出

echo "========================================="
echo "  Environment Setup Script"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Python 版本
check_python() {
    print_info "Checking Python version..."

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_info "Python found: $PYTHON_VERSION"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        print_info "Python found: $PYTHON_VERSION"
    else
        print_error "Python is not installed!"
        exit 1
    fi

    # 检查 Python 版本是否 >= 3.8
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python version must be >= 3.8, found: $PYTHON_VERSION"
        exit 1
    fi
}

# 创建虚拟环境
create_venv() {
    print_info "Creating virtual environment..."

    if [ -d "venv" ]; then
        print_warn "Virtual environment already exists, skipping..."
    else
        python3 -m venv venv || python -m venv venv
        print_info "Virtual environment created"
    fi
}

# 安装依赖
install_dependencies() {
    print_info "Installing Python dependencies..."

    # 激活虚拟环境
    source venv/bin/activate

    # 升级 pip
    pip install --upgrade pip setuptools wheel

    # 安装项目依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        print_warn "requirements.txt not found, skipping..."
    fi

    # 安装开发依赖
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
    else
        print_warn "requirements-dev.txt not found, skipping..."
    fi

    print_info "Dependencies installed"
}

# 安装 Playwright 浏览器
install_browsers() {
    print_info "Installing Playwright browsers..."

    # 激活虚拟环境
    source venv/bin/activate

    # 安装所有浏览器
    playwright install --with-deps chromium

    # 可选：安装其他浏览器
    # playwright install --with-deps firefox
    # playwright install --with-deps webkit

    print_info "Playwright browsers installed"
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

    print_info "Directories created"
}

# 创建 .env 文件
create_env_file() {
    print_info "Creating .env file..."

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_info ".env file created from .env.example"
            print_warn "Please update .env with your actual values"
        else
            print_warn ".env.example not found, creating basic .env file..."
            cat > .env << EOF
# Environment Variables
APP_ENV=test
APP_BASE_URL=https://test.example.com
BROWSER_HEADLESS=true
EOF
        fi
    else
        print_warn ".env file already exists, skipping..."
    fi
}

# 验证安装
verify_installation() {
    print_info "Verifying installation..."

    # 激活虚拟环境
    source venv/bin/activate

    # 检查 pytest
    if command -v pytest &> /dev/null; then
        PYTEST_VERSION=$(pytest --version)
        print_info "pytest installed: $PYTEST_VERSION"
    else
        print_error "pytest not found!"
        exit 1
    fi

    # 检查 Playwright
    python -c "import playwright; print(f'Playwright version: {playwright.__version__}')" || {
        print_error "Playwright not found!"
        exit 1
    }

    print_info "Installation verified successfully"
}

# 主函数
main() {
    echo ""
    print_info "Starting environment setup..."
    echo ""

    check_python
    create_venv
    install_dependencies
    install_browsers
    create_directories
    create_env_file
    verify_installation

    echo ""
    print_info "========================================="
    print_info "  Setup completed successfully!"
    print_info "========================================="
    echo ""
    print_info "To activate the virtual environment, run:"
    print_info "  source venv/bin/activate"
    echo ""
    print_info "To run tests, use:"
    print_info "  pytest tests/"
    echo ""
}

# 执行主函数
main
