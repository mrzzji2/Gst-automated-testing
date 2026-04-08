#!/bin/bash
# Test Execution Script for Jenkins
# 测试执行脚本

set -e  # 遇到错误立即退出

echo "========================================="
echo "  Test Execution Script"
echo "========================================="

# 默认参数
BROWSER="${BROWSER:-chromium}"
ENVIRONMENT="${ENVIRONMENT:-test}"
BASE_URL="${BASE_URL:-https://test.example.com}"
HEADLESS="${HEADLESS:-true}"
PYTEST_ARGS="${PYTEST_ARGS:-}"
PYTEST_MARKERS="${PYTEST_MARKERS:-smoke or regression}"

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

# 激活虚拟环境
activate_venv() {
    print_info "Activating virtual environment..."

    if [ -d "venv" ]; then
        source venv/bin/activate
        print_info "Virtual environment activated"
    else
        print_warn "Virtual environment not found, creating..."
        bash jenkins/scripts/setup.sh
        source venv/bin/activate
    fi
}

# 创建报告目录
create_report_dirs() {
    print_info "Creating report directories..."

    mkdir -p reports/html
    mkdir -p reports/allure
    mkdir -p reports/junit
    mkdir -p reports/screenshots
    mkdir -p reports/videos
    mkdir -p logs/auto
}

# 显示配置信息
show_config() {
    print_info "========================================="
    print_info "  Test Configuration"
    print_info "========================================="
    print_info "Browser:       $BROWSER"
    print_info "Environment:   $ENVIRONMENT"
    print_info "Base URL:      $BASE_URL"
    print_info "Headless:      $HEADLESS"
    print_info "Markers:       $PYTEST_MARKERS"
    print_info "Pytest Args:   $PYTEST_ARGS"
    print_info "========================================="
}

# 运行测试
run_tests() {
    print_info "Starting test execution..."

    # 构建 pytest 命令
    PYTEST_CMD="pytest tests/ \
        --browser=$BROWSER \
        --base-url=$BASE_URL \
        --headed=$HEADLESS \
        -v \
        --tb=short \
        --html=reports/html/report.html \
        --self-contained-html \
        --alluredir=reports/allure \
        --junitxml=reports/junit/results.xml \
        -m \"$PYTEST_MARKERS\" \
        $PYTEST_ARGS"

    print_info "Running: $PYTEST_CMD"
    echo ""

    # 执行测试
    eval $PYTEST_CMD
    TEST_EXIT_CODE=$?

    echo ""

    # 返回测试退出码
    return $TEST_EXIT_CODE
}

# 生成摘要报告
generate_summary() {
    print_info "Generating test summary..."

    # 解析 JUnit XML（如果存在）
    if [ -f "reports/junit/results.xml" ]; then
        # 使用 Python 解析 JUnit XML
        python << EOF
import xml.etree.ElementTree as ET
import sys

try:
    tree = ET.parse('reports/junit/results.xml')
    root = tree.getroot()

    tests = root.get('tests', '0')
    failures = root.get('failures', '0')
    errors = root.get('errors', '0')
    skipped = root.get('skipped', '0')

    passed = int(tests) - int(failures) - int(errors) - int(skipped)

    print(f"\n{'='*40}")
    print(f"  Test Summary")
    print(f"{'='*40}")
    print(f"Total:     {tests}")
    print(f"Passed:    {passed}")
    print(f"Failed:    {failures}")
    print(f"Errors:    {errors}")
    print(f"Skipped:   {skipped}")
    print(f"{'='*40}\n")

    # 设置退出码
    if int(failures) > 0 or int(errors) > 0:
        sys.exit(1)
    else:
        sys.exit(0)

except Exception as e:
    print(f"Error parsing test results: {e}")
    sys.exit(1)
EOF
    else
        print_warn "JUnit XML not found, skipping summary"
    fi
}

# 主函数
main() {
    echo ""

    activate_venv
    create_report_dirs
    show_config

    run_tests
    TEST_EXIT_CODE=$?

    generate_summary || true

    echo ""

    if [ $TEST_EXIT_CODE -eq 0 ]; then
        print_info "========================================="
        print_info "  Tests PASSED!"
        print_info "========================================="
    else
        print_warn "========================================="
        print_warn "  Tests FAILED!"
        print_warn "========================================="
    fi

    echo ""
    print_info "Report locations:"
    print_info "  HTML Report:  reports/html/report.html"
    print_info "  Allure Report: reports/allure"
    print_info "  JUnit XML:    reports/junit/results.xml"
    echo ""

    exit $TEST_EXIT_CODE
}

# 执行主函数
main
