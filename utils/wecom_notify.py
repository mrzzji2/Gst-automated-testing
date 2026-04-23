import os
import requests
import json
from datetime import datetime

def send_wecom_notification(test_results):
    """
    发送企业微信通知
    
    Args:
        test_results: 测试结果列表
    """
    # 检查是否启用通知
    if os.getenv('WECHAT_NOTIFICATIONS', 'false').lower() != 'true':
        print("[INFO] 企业微信通知已禁用")
        return
    
    webhook_url = os.getenv('WECHAT_WEBHOOK')
    if not webhook_url:
        print("[WARNING] 未配置企业微信 webhook URL")
        return
    
    # 统计测试结果
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    skipped = sum(1 for r in test_results if r['status'] == 'skipped')
    
    # 构建消息内容
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_emoji = "✅" if failed == 0 else "❌"
    
    message = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""# 🤖 GST自动化测试报告 {status_emoji}
**执行时间**: {timestamp}

**执行结果**: {'✅ 全部通过' if failed == 0 else '❌ 有失败用例'}

**统计信息**:
- 总计: {total}
- 通过: {passed}  
- 失败: {failed}
- 跳过: {skipped}

> 💡 查看详细报告"""
        }
    }
    
    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        if response.status_code == 200:
            print("[SUCCESS] 企业微信通知发送成功")
        else:
            print(f"[ERROR] 企业微信通知发送失败: {response.text}")
    except Exception as e:
        print(f"[ERROR] 企业微信通知异常: {e}")

def toggle_wecom_notifications(enable=True):
    """
    切换企业微信通知开关
    
    Args:
        enable: True 启用, False 禁用
    """
    env_file = ".env"
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if enable:
        new_content = content.replace("WECHAT_NOTIFICATIONS=false", "WECHAT_NOTIFICATIONS=true")
        if "WECHAT_NOTIFICATIONS=" not in new_content:
            new_content += "\nWECHAT_NOTIFICATIONS=true"
    else:
        new_content = content.replace("WECHAT_NOTIFICATIONS=true", "WECHAT_NOTIFICATIONS=false")
        if "WECHAT_NOTIFICATIONS=" not in new_content:
            new_content += "\nWECHAT_NOTIFICATIONS=false"
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    status = "启用" if enable else "禁用"
    print(f"[INFO] 企业微信通知已{status}")