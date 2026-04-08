"""
Jenkins Utilities
Jenkins集成工具（可选）
"""
import os
import json
import requests
from typing import Optional, Dict, Any
from pathlib import Path
from loguru import logger


class JenkinsUtils:
    """
    Jenkins工具类
    用于与Jenkins交互，获取构建信息、发送通知等
    """

    def __init__(
        self,
        jenkins_url: str = "",
        username: str = "",
        api_token: str = ""
    ):
        """
        初始化Jenkins工具

        Args:
            jenkins_url: Jenkins URL
            username: 用户名
            api_token: API Token
        """
        self.jenkins_url = jenkins_url.rstrip("/")
        self.username = username
        self.api_token = api_token
        self.auth = (username, api_token) if username and api_token else None

    def get_build_info(self, job_name: str, build_number: int) -> Dict[str, Any]:
        """
        获取构建信息

        Args:
            job_name: 任务名称
            build_number: 构建编号

        Returns:
            构建信息字典
        """
        try:
            url = f"{self.jenkins_url}/job/{job_name}/{build_number}/api/json"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get build info: {e}")
            return {}

    def get_test_results(self, job_name: str, build_number: int) -> Dict[str, Any]:
        """
        获取测试结果

        Args:
            job_name: 任务名称
            build_number: 构建编号

        Returns:
            测试结果字典
        """
        try:
            url = f"{self.jenkins_url}/job/{job_name}/{build_number}/testReport/api/json"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get test results: {e}")
            return {}

    def set_build_description(self, job_name: str, build_number: int, description: str):
        """
        设置构建描述

        Args:
            job_name: 任务名称
            build_number: 构建编号
            description: 描述内容
        """
        try:
            url = f"{self.jenkins_url}/job/{job_name}/{build_number}/submitDescription"
            data = {"description": description}
            response = requests.post(url, data=data, auth=self.auth)
            response.raise_for_status()
            logger.info(f"Build description updated: {description}")
        except Exception as e:
            logger.error(f"Failed to set build description: {e}")

    def add_build_badge(self, job_name: str, build_number: int, badge_text: str, badge_color: str = "blue"):
        """
        添加构建徽章（需要插件支持）

        Args:
            job_name: 任务名称
            build_number: 构建编号
            badge_text: 徽章文本
            badge_color: 徽章颜色
        """
        # 这需要Jenkins插件支持，如 "Badge Plugin"
        logger.info(f"Build badge would be added: {badge_text} ({badge_color})")

    def archive_artifacts(self, source_dir: str, job_name: str, build_number: int):
        """
        归档构建产物

        Args:
            source_dir: 源目录
            job_name: 任务名称
            build_number: 构建编号
        """
        logger.info(f"Archiving artifacts from {source_dir}")
        # 通常通过Jenkinsfile中的post步骤完成


class NotificationUtils:
    """
    通知工具类
    支持钉钉、企业微信、邮件等通知方式
    """

    @staticmethod
    def send_dingtalk(webhook: str, secret: str, content: str, at_mobiles: Optional[list] = None):
        """
        发送钉钉通知

        Args:
            webhook: 钉钉机器人Webhook
            secret: 钉钉机器人密钥
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
                "msgtype": "text",
                "text": {
                    "content": content
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
            logger.info("DingTalk notification sent successfully")

        except Exception as e:
            logger.error(f"Failed to send DingTalk notification: {e}")

    @staticmethod
    def send_email(
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        to_addrs: list,
        subject: str,
        content: str,
        content_type: str = "plain"
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
            content_type: 内容类型 (plain, html)
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
            mime_type = f"text/{content_type}"
            msg.attach(MIMEText(content, mime_type, 'utf-8'))

            # 发送邮件
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_addrs}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    @staticmethod
    def format_test_summary(test_results: Dict[str, Any]) -> str:
        """
        格式化测试结果摘要

        Args:
            test_results: 测试结果字典

        Returns:
            格式化的摘要文本
        """
        total = test_results.get("total", 0)
        passed = test_results.get("passed", 0)
        failed = test_results.get("failed", 0)
        skipped = test_results.get("skipped", 0)
        duration = test_results.get("duration", 0)

        summary = f"""
测试报告摘要
================
总计: {total} 个用例
通过: {passed} 个
失败: {failed} 个
跳过: {skipped} 个
耗时: {duration:.2f} 秒
通过率: {(passed/total*100):.1f}%
================
        """
        return summary.strip()


def get_jenkins_utils() -> Optional[JenkinsUtils]:
    """
    获取Jenkins工具实例

    Returns:
        JenkinsUtils 实例或None
    """
    jenkins_enabled = os.getenv("JENKINS_ENABLED", "false").lower() == "true"
    if not jenkins_enabled:
        return None

    return JenkinsUtils(
        jenkins_url=os.getenv("JENKINS_URL", ""),
        username=os.getenv("JENKINS_USER", ""),
        api_token=os.getenv("JENKINS_API_TOKEN", "")
    )


__all__ = ["JenkinsUtils", "NotificationUtils", "get_jenkins_utils"]
