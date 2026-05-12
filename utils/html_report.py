import os
import json
import base64
import webbrowser
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def format_timestamp(ts: str) -> str:
    """将 20260509_152042 格式化为 2026-05-09 15:20"""
    return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}"


def scan_historical_reports(report_dir: Path) -> list:
    """扫描历史报告，返回按时间倒序排列的报告列表"""
    json_reports = {}
    for f in report_dir.glob("*.json"):
        try:
            with open(f, encoding='utf-8') as fh:
                stats = json.load(fh)
            json_reports[stats["timestamp"]] = stats
        except:
            continue

    for f in report_dir.glob("*.html"):
        if f.name == "index.html":
            continue
        ts = f.stem
        if ts not in json_reports:
            json_reports[ts] = {"timestamp": ts, "no_stats": True}

    reports = []
    for ts, stats in sorted(json_reports.items(), reverse=True):
        html_path = f"{ts}.html"
        if (report_dir / html_path).exists():
            reports.append({**stats, "html_path": html_path})
    return reports


def generate_html_report(test_results, screenshots, report_title=""):
    """生成自包含HTML报告 - 支持中文名、执行时间、按优先级分组"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("reports/html")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"{timestamp}.html"

    # 组装标题
    if report_title:
        full_title = f"{report_title} 测试报告"
    else:
        full_title = "GST 自动化测试报告"

    # 扫描历史报告
    all_reports = scan_historical_reports(report_dir)
    # 按日期分组（排除当前报告）
    from collections import defaultdict
    date_groups = defaultdict(list)
    for r in all_reports:
        if r["timestamp"] == timestamp:
            continue
        date_key = r["timestamp"][:8]  # YYYYMMDD
        date_groups[date_key].append(r)
    history_count = sum(len(v) for v in date_groups.values())

    # 构建时间线风格 HTML
    timeline_groups = []
    group_idx = 0
    for date_key in sorted(date_groups.keys(), reverse=True):
        date_str = f"{date_key[:4]}-{date_key[4:6]}-{date_key[6:8]}"
        reports_in_day = date_groups[date_key]
        day_passed = sum(1 for r in reports_in_day if not r.get("no_stats") and r.get("failed", 0) == 0)
        day_total = sum(1 for r in reports_in_day if not r.get("no_stats"))

        items = []
        for r in reports_in_day:
            ts = r["timestamp"]
            time_str = ts[9:11] + ":" + ts[11:13]
            title = r.get("title", "")
            # 状态圆点
            if r.get("no_stats"):
                dot = "⚪"
                summary = "详情未知"
            elif r["failed"] > 0:
                dot = "🔴"
                summary = f"❌ {r['passed']}/{r['total']} 通过, {r['failed']} 失败"
            elif r["skipped"] > 0:
                dot = "🟡"
                summary = f"🟡 {r['passed']}/{r['total']} 通过, {r['skipped']} 跳过"
            else:
                dot = "🟢"
                summary = f"✅ {r['passed']}/{r['total']} 通过"

            items.append(f"""
            <a href="{r['html_path']}" class="tl-item">
                <span class="tl-dot">{dot}</span>
                <span class="tl-line"></span>
                <span class="tl-time">{time_str}</span>
                <span class="tl-body">
                    <span class="tl-title">{title}</span>
                    <span class="tl-summary">{summary}</span>
                </span>
                <span class="tl-link">查看</span>
            </a>""")

        items_html = "".join(items)
        collapsed = "collapsed"
        timeline_groups.append(f"""
        <div class="tl-group {collapsed}">
            <div class="tl-date-header" onclick="toggleDateGroup(this)">
                <span class="tl-date-label">📅 {date_str}</span>
                <span class="tl-date-count">({len(reports_in_day)} 份)</span>
                <span class="tl-date-arrow">▼</span>
            </div>
            <div class="tl-items">{items_html}</div>
        </div>""")
        group_idx += 1

    history_html = "".join(timeline_groups) if timeline_groups else "<div class='history-empty'>暂无历史报告</div>"

    # 统计信息
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    skipped = sum(1 for r in test_results if r['status'] == 'skipped')

    # 按优先级分组
    p0_tests = [r for r in test_results if r.get('priority') == 'P0']
    p1_tests = [r for r in test_results if r.get('priority') == 'P1']
    p2_tests = [r for r in test_results if r.get('priority') == 'P2']

    # 计算总执行时间
    total_duration = sum(r.get('duration', 0) for r in test_results)

    # 生成通过率显示
    if failed > 0:
        if skipped > 0:
            rate_display = f'📈 通过率: <strong>{passed/total*100:.1f}%</strong> ({failed}/{total} 失败，{skipped}/{total} 跳过)'
        else:
            rate_display = f'📈 通过率: <strong>{passed/total*100:.1f}%</strong> ({failed}/{total} 失败)'
    elif skipped > 0:
        rate_display = f'📈 通过率: <strong>{passed/total*100:.1f}%</strong> ({skipped}/{total} 跳过)'
    else:
        rate_display = f'✅ 通过率: <strong>{passed/total*100:.1f}%</strong>'

    def format_duration(seconds):
        """格式化执行时间"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        else:
            mins = int(seconds // 60)
            secs = seconds % 60
            return f"{mins}m {secs:.1f}s"

    def generate_test_cases(tests, group_name):
        """生成测试用例HTML"""
        if not tests:
            return ""

        group_passed = sum(1 for t in tests if t['status'] == 'passed')
        group_failed = sum(1 for t in tests if t['status'] == 'failed')
        group_skipped = sum(1 for t in tests if t['status'] == 'skipped')

        html = f"""
    <div class="priority-group">
        <div class="priority-header" onclick="toggleGroup('{group_name}')">
            <h3>{group_name} <span class="count">({len(tests)})</span></h3>
            <div class="group-stats">
                <span class="passed-count">✅ {group_passed}</span>
                <span class="failed-count">❌ {group_failed}</span>
                <span class="skipped-count">⏭️ {group_skipped}</span>
            </div>
        </div>
        <div class="priority-content" id="{group_name}-content">
"""

        for result in tests:
            status_class = result['status']
            detail_info = ""
            if result['status'] == 'failed' and result.get('error'):
                detail_info = f"<div class='error'>{result.get('error', '')}</div>"
            elif result['status'] == 'skipped' and result.get('error'):
                detail_info = f"<div class='skip-reason'>⏭️ {result['error']}</div>"

            # 处理截图
            screenshot_html = ""
            if result['status'] == 'failed' and result.get('screenshot'):
                screenshot_path = result['screenshot']
                if os.path.exists(screenshot_path):
                    with open(screenshot_path, "rb") as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                    screenshot_html = f"""
                    <details class="screenshot-details">
                        <summary>📸 查看失败截图</summary>
                        <img src="data:image/png;base64,{img_data}" class="screenshot" alt="失败截图">
                    </details>
                    """

            duration_str = format_duration(result.get('duration', 0))

            # 额外信息（如果有）
            extra_info_html = ""
            if result.get('extra_info'):
                extra_info_html = f'<div class="test-extra-info">📊 {result["extra_info"]}</div>'

            html += f"""
            <div class="test-case {status_class}" data-priority="{result.get('priority', 'P2')}">
                <div class="test-header">
                    <span class="test-title">{result['title']}</span>
                    <span class="test-meta">
                        <span class="priority-badge">{result.get('priority', 'P2')}</span>
                        <span class="duration">⏱️ {duration_str}</span>
                    </span>
                </div>
                <div class="test-name">{result['name']}</div>
                <div class="test-status {status_class}">{status_class.upper()}</div>
                {extra_info_html}
                {detail_info}
                {screenshot_html}
            </div>
"""

        html += """
        </div>
    </div>
"""
        return html

    # 生成HTML内容
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GST自动化测试报告 - {timestamp}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            color: #333;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; margin-bottom: 20px; font-size: 28px; }}
        h2 {{ color: #34495e; font-size: 18px; margin-bottom: 10px; }}
        h3 {{ margin: 0; }}

        /* 摘要区域 */
        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .summary h2 {{ color: white; }}
        .stats {{ display: flex; gap: 15px; flex-wrap: wrap; }}
        .stat {{
            flex: 1;
            min-width: 120px;
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }}
        .stat strong {{ font-size: 32px; display: block; }}
        .total {{ background: rgba(255,255,255,0.3); }}
        .passed {{ background: rgba(76, 175, 80, 0.3); }}
        .failed {{ background: rgba(244, 67, 54, 0.3); }}
        .skipped {{ background: rgba(255, 152, 0, 0.3); }}

        /* 执行时间 */
        .execution-time {{
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .execution-time span {{ font-size: 16px; color: #555; }}

        /* 优先级分组 */
        .priority-group {{
            background: white;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .priority-header {{
            padding: 18px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }}
        .priority-header:hover {{ background: #f8f9fa; }}
        .priority-header h3 {{ font-size: 18px; }}
        .count {{ font-size: 14px; opacity: 0.7; margin-left: 8px; }}
        .group-stats {{ display: flex; gap: 15px; font-size: 14px; }}
        .group-stats span {{ display: flex; align-items: center; gap: 4px; }}
        .priority-content {{ padding: 0 20px 20px; }}
        .priority-content.collapsed {{ display: none; }}

        /* P0/P1/P2 颜色 */
        .priority-header[data-priority="P0"] {{ border-left: 4px solid #f44336; background: #ffebee; }}
        .priority-header[data-priority="P1"] {{ border-left: 4px solid #ff9800; background: #fff3e0; }}
        .priority-header[data-priority="P2"] {{ border-left: 4px solid #2196f3; background: #e3f2fd; }}

        /* 测试用例 */
        .test-case {{
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ccc;
            background: #fafafa;
            transition: all 0.2s;
        }}
        .test-case:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .test-case.passed {{ border-left-color: #4caf50; background: #f1f8f4; }}
        .test-case.failed {{ border-left-color: #f44336; background: #ffebee; }}
        .test-case.skipped {{ border-left-color: #ff9800; background: #fff8f0; }}

        .test-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
        .test-title {{ font-weight: 600; font-size: 16px; color: #2c3e50; }}
        .test-meta {{ display: flex; gap: 10px; align-items: center; }}

        .priority-badge {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        .priority-badge[data-priority="P0"] {{ background: #f44336; color: white; }}
        .priority-badge[data-priority="P1"] {{ background: #ff9800; color: white; }}
        .priority-badge[data-priority="P2"] {{ background: #2196f3; color: white; }}

        .duration {{ font-size: 13px; color: #666; }}
        .test-name {{ font-size: 12px; color: #888; margin-bottom: 5px; font-family: monospace; }}
        .test-status {{ font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }}
        .test-status.passed {{ color: #4caf50; }}
        .test-status.failed {{ color: #f44336; }}
        .test-status.skipped {{ color: #ff9800; }}

        /* 额外信息 */
        .test-extra-info {{
            font-size: 13px;
            color: #1976d2;
            background: #e3f2fd;
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 8px;
            border-left: 3px solid #1976d2;
        }}

        /* 错误信息 */
        .error {{
            color: #d32f2f;
            background: #ffebee;
            padding: 12px;
            border-radius: 6px;
            font-size: 13px;
            white-space: pre-wrap;
            word-break: break-word;
            margin-top: 10px;
            border-left: 3px solid #f44336;
        }}
        .skip-reason {{
            color: #e67e22;
            background: #fff8e1;
            padding: 10px 12px;
            border-radius: 6px;
            font-size: 13px;
            margin-top: 8px;
            border-left: 3px solid #f39c12;
        }}

        /* 截图 */
        .screenshot-details {{ margin-top: 10px; }}
        .screenshot-details summary {{
            cursor: pointer;
            color: #1976d2;
            padding: 8px;
            background: #e3f2fd;
            border-radius: 6px;
            font-size: 13px;
        }}
        .screenshot-details summary:hover {{ background: #bbdefb; }}
        .screenshot {{
            max-width: 100%;
            max-height: 400px;
            margin-top: 10px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }}

        /* 历史报告 — 时间线风格 */
        .history-box {{
            background: white; border-radius: 12px; margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden;
        }}
        .history-header {{
            padding: 16px 20px; cursor: pointer; display: flex;
            justify-content: space-between; align-items: center;
            background: #f8f9fa; font-size: 15px; font-weight: 600; color: #555;
            user-select: none;
        }}
        .history-header:hover {{ background: #f0f1f3; }}
        .history-header .count {{ color: #999; font-weight: normal; font-size: 13px; }}
        .history-body {{ padding: 4px 4px 8px; }}
        .history-body.collapsed {{ display: none; }}
        .history-empty {{ padding: 30px; text-align: center; color: #ccc; font-size: 14px; }}

        /* 日期分组 */
        .tl-group {{
            margin: 4px 10px; border-radius: 10px; overflow: hidden;
            border: 1px solid #f0f0f0;
        }}
        .tl-group.collapsed .tl-items {{ display: none; }}
        .tl-date-header {{
            padding: 10px 14px; cursor: pointer; display: flex;
            align-items: center; gap: 8px; font-size: 14px; font-weight: 600;
            color: #444; background: #fafbfc; user-select: none;
        }}
        .tl-date-header:hover {{ background: #f0f4ff; }}
        .tl-date-count {{ font-weight: normal; color: #999; font-size: 13px; }}
        .tl-date-arrow {{ margin-left: auto; font-size: 12px; color: #999; transition: transform 0.2s; }}
        .tl-group.collapsed .tl-date-arrow {{ transform: rotate(-90deg); }}

        /* 时间线条目 */
        .tl-items {{ position: relative; padding: 0 0 6px; }}
        .tl-item {{
            display: flex; align-items: flex-start; padding: 8px 14px 8px 0;
            text-decoration: none; color: #333; position: relative;
            margin-left: 32px; transition: background 0.15s; border-radius: 8px;
        }}
        .tl-item:hover {{ background: #f5f7ff; }}
        .tl-dot {{ position: absolute; left: -26px; top: 10px; font-size: 14px; z-index: 1; }}
        .tl-line {{
            position: absolute; left: -19px; top: 24px; bottom: -8px;
            width: 2px; background: #e8ecf0;
        }}
        .tl-item:last-child .tl-line {{ display: none; }}
        .tl-time {{ font-size: 12px; color: #888; width: 40px; flex-shrink: 0; padding-top: 2px; }}
        .tl-body {{ flex: 1; min-width: 0; }}
        .tl-title {{ display: inline; font-size: 13px; font-weight: 500; color: #333; }}
        .tl-summary {{ display: inline; font-size: 12px; color: #666; margin-left: 8px; }}
        .tl-link {{
            font-size: 12px; color: #667eea; flex-shrink: 0;
            padding: 2px 10px; border-radius: 4px; margin-left: 8px;
        }}
        .tl-item:hover .tl-link {{ background: #eef1ff; }}

        /* 响应式 */
        @media (max-width: 768px) {{
            .stats {{ flex-direction: column; }}
            .test-header {{ flex-direction: column; }}
            .test-meta {{ margin-top: 8px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="history-box">
            <div class="history-header" onclick="toggleHistory()">
                <span>📊 历史报告 <span class="count">({history_count} 份)</span></span>
                <span id="history-arrow">▼</span>
            </div>
            <div class="history-body" id="history-body">
                {history_html}
            </div>
        </div>
        <h1>🤖 {full_title}</h1>
        <p style="color: #666; margin-bottom: 20px;">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="summary">
            <h2>📊 执行摘要</h2>
            <div class="stats">
                <div class="stat total">总计<br><strong>{total}</strong></div>
                <div class="stat passed">通过<br><strong>{passed}</strong></div>
                <div class="stat failed">失败<br><strong>{failed}</strong></div>
                <div class="stat skipped">跳过<br><strong>{skipped}</strong></div>
            </div>
        </div>

        <div class="execution-time">
            <span>⏱️ 总执行时间: <strong>{format_duration(total_duration)}</strong></span>
            <span>{rate_display}</span>
        </div>

        <!-- P0 核心流程 -->
        {generate_test_cases(p0_tests, 'P0')}

        <!-- P1 重要功能 -->
        {generate_test_cases(p1_tests, 'P1')}

        <!-- P2 边缘场景 -->
        {generate_test_cases(p2_tests, 'P2')}
    </div>

    <script>
        // 切换分组展开/收起
        function toggleGroup(groupId) {{
            const content = document.getElementById(groupId + '-content');
            content.classList.toggle('collapsed');
        }}

        // 切换历史报告列表展开/收起
        function toggleHistory() {{
            const body = document.getElementById('history-body');
            const arrow = document.getElementById('history-arrow');
            body.classList.toggle('collapsed');
            arrow.textContent = body.classList.contains('collapsed') ? '▶' : '▼';
        }}

        // 按日期分组展开/收起
        function toggleDateGroup(header) {{
            const group = header.closest('.tl-group');
            group.classList.toggle('collapsed');
        }}

        // 自动滚动到第一个失败用例
        document.addEventListener('DOMContentLoaded', function() {{
            const firstFailed = document.querySelector('.test-case.failed');
            if (firstFailed) {{
                firstFailed.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                firstFailed.style.animation = 'highlight 2s ease';
            }}
        }});

        // 高亮动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes highlight {{
                0%, 100% {{ box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3); }}
                50% {{ box-shadow: 0 4px 20px rgba(244, 67, 54, 0.6); }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""

    # 写入 HTML 文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 保存统计信息到侧边 JSON，供索引页读取
    stats = {
        "timestamp": timestamp,
        "title": full_title,
        "total": total, "passed": passed,
        "failed": failed, "skipped": skipped,
        "total_duration": total_duration
    }
    stats_file = report_dir / f"{timestamp}.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False)

    return str(report_file)


def generate_report_index():
    """生成历史报告索引页 - 列出所有历史测试报告"""
    report_dir = Path("reports/html")
    if not report_dir.exists():
        return

    reports = scan_historical_reports(report_dir)

    if not reports:
        reports_html = '<div style="text-align:center;padding:60px;color:#999;"><p>暂无测试报告</p></div>'
    else:
        rows = []
        for r in reports:
            ts = r["timestamp"]
            dt = format_timestamp(ts)
            if r.get("no_stats"):
                summary = r.get("title", "📄 历史报告（详情未知）")
            else:
                status_icon = "✅" if r["failed"] == 0 else "❌"
                summary = r.get("title", "") + " " if r.get("title") else ""
                summary += f"{status_icon} {r['passed']}/{r['total']} 通过"
                if r["failed"] > 0:
                    summary += f", {r['failed']} 失败"
                if r["skipped"] > 0:
                    summary += f", {r['skipped']} 跳过"
            link = f'<a href="{r["html_path"]}" class="report-link" target="_blank">查看</a>'
            rows.append(f"""
            <div class="report-row">
                <span class="report-time">{dt}</span>
                <span class="report-summary">{summary}</span>
                <span class="report-link-wrap">{link}</span>
            </div>""")
        reports_html = "".join(rows)

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{reports[0].get('title', '测试报告')} - 历史</title>
<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f5f7fa; padding: 40px 20px; color: #333;
    }}
    .container {{ max-width: 800px; margin:0 auto; }}
    h1 {{ color:#2c3e50; font-size: 26px; margin-bottom:8px; }}
    .subtitle {{ color:#888; font-size:14px; margin-bottom:30px; }}
    .report-row {{
        display: flex; align-items: center; padding: 16px 20px;
        background: white; border-radius: 10px; margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }}
    .report-row:hover {{ box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
    .report-time {{ width:160px; color:#555; font-size:14px; flex-shrink:0; }}
    .report-summary {{ flex:1; font-size:15px; }}
    .report-link-wrap {{ width:60px; text-align:right; }}
    .report-link {{
        display:inline-block; padding:6px 16px; background:#667eea;
        color:white; border-radius:6px; text-decoration:none; font-size:13px;
    }}
    .report-link:hover {{ background:#5a6fd6; }}
    .empty {{ text-align:center; padding:60px; color:#999; }}
    @media (max-width:640px) {{
        .report-row {{ flex-wrap:wrap; }}
        .report-time {{ width:100%; margin-bottom:6px; }}
    }}
</style>
</head>
<body>
<div class="container">
    <h1>📊 {reports[0].get('title', 'GST 自动化测试报告')}</h1>
    <p class="subtitle">共 {len(reports)} 份报告 | 最新: {reports[0]['timestamp'][:4]}-{reports[0]['timestamp'][4:6]}-{reports[0]['timestamp'][6:8]} {reports[0]['timestamp'][9:11]}:{reports[0]['timestamp'][11:13]}</p>
    <div class="report-list">{reports_html}</div>
</div>
</body>
</html>"""

    index_file = report_dir / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)


def open_report_in_browser(report_path):
    """在浏览器中打开报告"""
    try:
        webbrowser.open(f"file://{os.path.abspath(report_path)}")
    except Exception as e:
        print(f"无法打开浏览器: {e}")
