"""
Jenkins Notification Script
Jenkins 通知脚本（钉钉/企业微信/邮件）
"""
import os
import sys
import argparse
import requests
from typing import Optional


def send_dingtalk_notification(
    webhook: str,
    secret: str,
    title: str,
    content: str,
    at_mobiles: Optional[list] = None
):
    """
    发送钉钉通知

    Args:
        webhook: 钉钉机器人Webhook
        secret: 钉钉机器人密钥
        title: 消息标题
        content: 消息内容
        at_mobiles: @的手机号列表
    """
    import time
    import hmac
    import hashlib
    import base64
    import urllib.parse

    try:
        # 生成签名
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        # 构建消息
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"## {title}\n\n{content}"
            }
        }

        if at_mobiles:
            data["at"] = {
                "atMobiles": at_mobiles,
                "isAtAll": False
            }

        # 发送请求
        url = f"{webhook}&timestamp={timestamp}&sign={sign}"
        response = requests.post(url, json=data)
        response.raise_for_status()

        print(f"DingTalk notification sent: {title}")

    except Exception as e:
        print(f"Failed to send DingTalk notification: {e}")


def send_wechat_notification(
    webhook: str,
    title: str,
    content: str
):
    """
    发送企业微信通知

    Args:
        webhook: 企业微信机器人Webhook
        title: 消息标题
        content: 消息内容
    """
    try:
        # 构建消息
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"## {title}\n\n{content}"
            }
        }

        # 发送请求
        response = requests.post(webhook, json=data)
        response.raise_for_status()

        print(f"WeChat notification sent: {title}")

    except Exception as e:
        print(f"Failed to send WeChat notification: {e}")


def send_email_notification(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    to_addrs: list,
    subject: str,
    content: str
):
    """
    发送邮件通知

    Args:
        smtp_host: SMTP服务器
        smtp_port: SMTP端口
        smtp_user: SMTP用户名
        smtp_password: SMTP密码
        to_addrs: 收件人列表
        subject: 邮件主题
        content: 邮件内容
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = ', '.join(to_addrs)
        msg['Subject'] = subject

        # 添加内容
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        # 发送邮件
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print(f"Email sent: {subject}")

    except Exception as e:
        print(f"Failed to send email: {e}")


def format_test_report(
    build_number: str,
    build_url: str,
    status: str,
    duration: str,
    passed: int = 0,
    failed: int = 0,
    skipped: int = 0
) -> str:
    """
    格式化测试报告

    Args:
        build_number: 构建编号
        build_url: 构建URL
        status: 构建状态
        duration: 持续时间
        passed: 通过数量
        failed: 失败数量
        skipped: 跳过数量

    Returns:
        格式化的报告文本
    """
    total = passed + failed + skipped

    # 状态图标
    if status == "success":
        icon = "✅"
        color = "green"
    elif status == "failed":
        icon = "❌"
        color = "red"
    else:
        icon = "⚠️"
        color = "orange"

    # 构建报告
    report = f"""
{icon} **自动化测试报告**

---

### 构建信息
| 项目 | 内容 |
|------|------|
| 构建编号 | [{build_number}]({build_url}) |
| 构建状态 | <font color='{color}'>{status.upper()}</font> |
| 持续时间 | {duration} |

### 测试结果
| 结果 | 数量 |
|------|------|
| 总计 | {total} |
| 通过 | ✅ {passed} |
| 失败 | ❌ {failed} |
| 跳过 | ⏭️ {skipped} |

---

[查看详细报告]({build_url})
"""

    return report.strip()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Jenkins Notification Script")
    parser.add_argument("--status", required=True, choices=["success", "failed", "unstable"],
                       help="构建状态")
    parser.add_argument("--build-number", default=os.getenv("BUILD_NUMBER", ""),
                       help="构建编号")
    parser.add_argument("--build-url", default=os.getenv("BUILD_URL", ""),
                       help="构建URL")
    parser.add_argument("--duration", default="",
                       help="构建持续时间")
    parser.add_argument("--passed", type=int, default=0,
                       help="通过的测试数量")
    parser.add_argument("--failed", type=int, default=0,
                       help="失败的测试数量")
    parser.add_argument("--skipped", type=int, default=0,
                       help="跳过的测试数量")

    args = parser.parse_args()

    # 格式化报告
    report = format_test_report(
        build_number=args.build_number,
        build_url=args.build_url,
        status=args.status,
        duration=args.duration,
        passed=args.passed,
        failed=args.failed,
        skipped=args.skipped
    )

    # 发送钉钉通知
    dingtalk_webhook = os.getenv("DINGTALK_WEBHOOK")
    dingtalk_secret = os.getenv("DINGTALK_SECRET")

    if dingtalk_webhook and dingtalk_secret:
        title = f"测试报告 - {'成功' if args.status == 'success' else '失败'}"
        send_dingtalk_notification(dingtalk_webhook, dingtalk_secret, title, report)

    # 发送企业微信通知
    wechat_webhook = os.getenv("WECHAT_WEBHOOK")

    if wechat_webhook:
        title = f"测试报告 - {'成功' if args.status == 'success' else '失败'}"
        send_wechat_notification(wechat_webhook, title, report)

    # 发送邮件通知
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_recipients = os.getenv("EMAIL_RECIPIENTS", "").split(",")

    if smtp_host and smtp_user and email_recipients:
        subject = f"测试报告 - Build #{args.build_number} - {args.status.upper()}"
        send_email_notification(
            smtp_host, smtp_port, smtp_user, smtp_password,
            email_recipients, subject, report
        )


if __name__ == "__main__":
    main()
