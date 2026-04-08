"""
Run Tests Script
测试入口脚本
"""
import sys
import subprocess
import argparse
from pathlib import Path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Web Automation Test Framework - 测试入口"
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="浏览器类型"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="有头模式"
    )
    parser.add_argument(
        "--base-url",
        default="",
        help="基础URL"
    )
    parser.add_argument(
        "--marker",
        default="",
        help="测试标记 (smoke, regression, etc.)"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="并行执行"
    )
    parser.add_argument(
        "--workers",
        default="auto",
        help="并行工作进程数"
    )
    parser.add_argument(
        "--slow",
        action="store_true",
        help="包含慢速测试"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="生成报告"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="详细输出"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="tests/",
        help="测试路径"
    )

    args = parser.parse_args()

    # 构建 pytest 命令
    pytest_cmd = ["pytest"]

    # 添加测试路径
    pytest_cmd.append(args.path)

    # 添加浏览器选项
    pytest_cmd.extend(["--browser", args.browser])

    # 添加有头模式
    if args.headed:
        pytest_cmd.append("--headed")

    # 添加基础URL
    if args.base_url:
        pytest_cmd.extend(["--base-url", args.base_url])

    # 添加测试标记
    if args.marker:
        pytest_cmd.extend(["-m", args.marker])

    # 添加并行执行
    if args.parallel:
        pytest_cmd.extend(["-n", args.workers])

    # 添加慢速测试
    if args.slow:
        pytest_cmd.append("--slow")

    # 添加报告
    if args.report:
        pytest_cmd.extend([
            "--html=reports/html/report.html",
            "--self-contained-html",
            "--alluredir=reports/allure",
            "--junitxml=reports/junit/results.xml"
        ])

    # 添加详细输出
    if args.verbose:
        pytest_cmd.append("-vv")
    else:
        pytest_cmd.append("-v")

    # 打印命令
    print(f"Running: {' '.join(pytest_cmd)}")
    print()

    # 执行测试
    result = subprocess.run(pytest_cmd)

    # 返回退出码
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
