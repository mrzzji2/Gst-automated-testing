import os
import base64
import webbrowser
from datetime import datetime
from pathlib import Path

def generate_html_report(test_results, screenshots):
    """生成自包含HTML报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("reports/html")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"{timestamp}.html"
    
    # 统计信息
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    skipped = sum(1 for r in test_results if r['status'] == 'skipped')
    
    # 生成HTML内容
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GST自动化测试报告 - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .stats {{ display: flex; gap: 20px; }}
        .stat {{ text-align: center; padding: 10px; border-radius: 5px; }}
        .total {{ background: #e3f2fd; }}
        .passed {{ background: #e8f5e8; }}
        .failed {{ background: #ffebee; }}
        .skipped {{ background: #fff3e0; }}
        .test-case {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .test-case.passed {{ border-left-color: #4caf50; }}
        .test-case.failed {{ border-left-color: #f44336; }}
        .test-case.skipped {{ border-left-color: #ff9800; }}
        .screenshot {{ max-width: 100%; cursor: pointer; margin: 10px 0; }}
        .screenshot.hidden {{ display: none; }}
        .error {{ color: #f44336; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <h1>GST自动化测试报告</h1>
    <div class="summary">
        <h2>执行摘要</h2>
        <div class="stats">
            <div class="stat total">总计<br><strong>{total}</strong></div>
            <div class="stat passed">通过<br><strong>{passed}</strong></div>
            <div class="stat failed">失败<br><strong>{failed}</strong></div>
            <div class="stat skipped">跳过<br><strong>{skipped}</strong></div>
        </div>
    </div>
"""
    
    # 添加测试用例详情
    for result in test_results:
        status_class = result['status']
        error_info = f"<div class='error'>{result.get('error', '')}</div>" if result['status'] == 'failed' else ""
        
        # 处理截图
        screenshot_html = ""
        if result['status'] == 'failed' and result.get('screenshot'):
            screenshot_path = result['screenshot']
            if os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                screenshot_html = f"""
                <img src="data:image/png;base64,{img_data}" class="screenshot" onclick="this.classList.toggle('hidden')" title="点击隐藏/显示截图">
                """
        
        html_content += f"""
    <div class="test-case {status_class}">
        <strong>{result['name']}</strong> - {result['status'].upper()}
        {error_info}
        {screenshot_html}
    </div>
"""
    
    html_content += """
    <script>
        // 自动滚动到第一个失败用例
        document.addEventListener('DOMContentLoaded', function() {
            const firstFailed = document.querySelector('.test-case.failed');
            if (firstFailed) {
                firstFailed.scrollIntoView({behavior: 'smooth'});
            }
        });
    </script>
</body>
</html>
"""
    
    # 写入文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return str(report_file)

def open_report_in_browser(report_path):
    """在浏览器中打开报告"""
    try:
        webbrowser.open(f"file://{os.path.abspath(report_path)}")
    except Exception as e:
        print(f"无法打开浏览器: {e}")