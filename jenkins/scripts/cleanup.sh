#!/bin/bash
# Cleanup Script for Jenkins
# 清理脚本

set -e

echo "========================================="
echo "  Cleanup Script"
echo "========================================="

GREEN='\033[0;32m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# 清理旧的报告
cleanup_old_reports() {
    print_info "Cleaning up old reports (older than 7 days)..."

    find reports/ -type f -mtime +7 -delete 2>/dev/null || true
    find logs/ -type f -mtime +7 -delete 2>/dev/null || true

    print_info "Old reports cleaned"
}

# 清理临时文件
cleanup_temp_files() {
    print_info "Cleaning up temporary files..."

    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true

    print_info "Temporary files cleaned"
}

# 清理空目录
cleanup_empty_dirs() {
    print_info "Cleaning up empty directories..."

    find reports/ -type d -empty -delete 2>/dev/null || true
    find logs/ -type d -empty -delete 2>/dev/null || true

    print_info "Empty directories cleaned"
}

# 主函数
main() {
    cleanup_old_reports
    cleanup_temp_files
    cleanup_empty_dirs

    print_info "Cleanup completed"
}

# 执行主函数
main
