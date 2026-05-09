#!/usr/bin/env python3
"""运行测试并打开 Allure 报告"""
import sys, os, subprocess, argparse, webbrowser
from pathlib import Path

def run_pytest(args, test_file="testcases/ui/"):
    cmd = ["pytest", test_file] + args
    print(f"\n{'='*50}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*50}\n")
    return subprocess.run(cmd).returncode

def main():
    parser = argparse.ArgumentParser(description="运行测试并打开 Allure 报告")
    parser.add_argument("--p0", action="store_true", help="运行 P0 冒烟测试")
    parser.add_argument("--p1", action="store_true", help="运行 P1 回归测试")
    parser.add_argument("--p2", action="store_true", help="运行 P2 边缘场景测试")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--regression", action="store_true")
    parser.add_argument("--file", type=str, help="运行指定的测试文件")
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    pytest_args = ["-v", "--tb=short"]
    if args.p0: pytest_args.extend(["-m", "P0"])
    elif args.p1: pytest_args.extend(["-m", "P1"])
    elif args.p2: pytest_args.extend(["-m", "P2"])
    elif args.smoke: pytest_args.extend(["-m", "smoke"])
    elif args.regression: pytest_args.extend(["-m", "regression"])
    if args.verbose: pytest_args.remove("--tb=short"); pytest_args.append("-vv")

    test_file = args.file or "testcases/ui/"
    run_pytest(pytest_args, test_file)

    if not args.no_report:
        print("\n测试完成！运行以下命令查看报告:")
        print("  allure serve reports/allure")

if __name__ == "__main__":
    main()
