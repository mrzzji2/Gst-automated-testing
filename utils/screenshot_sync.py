"""
Screenshot Utilities - Synchronous Version
失败自动截图和视频录制 - 同步版本
"""
from pathlib import Path
from typing import Optional
from datetime import datetime
from playwright.sync_api import Page
from loguru import logger


class ScreenshotUtils:
    """截图工具类 - 同步版本"""

    def __init__(self, screenshot_dir: str = "reports/screenshots"):
        """
        初始化截图工具

        Args:
            screenshot_dir: 截图保存目录
        """
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def capture_screenshot(
        self,
        page: Page,
        filename: Optional[str] = None,
        full_page: bool = True
    ) -> str:
        """
        截取页面截图

        Args:
            page: Playwright Page 对象
            filename: 截图文件名（可选）
            full_page: 是否截取整个页面

        Returns:
            截图文件路径
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"screenshot_{timestamp}.png"

            filepath = self.screenshot_dir / filename

            page.screenshot(
                path=str(filepath),
                full_page=full_page
            )

            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return ""

    def capture_element_screenshot(
        self,
        page: Page,
        selector: str,
        filename: Optional[str] = None
    ) -> str:
        """
        截取指定元素截图

        Args:
            page: Playwright Page 对象
            selector: 元素选择器
            filename: 截图文件名（可选）

        Returns:
            截图文件路径
        """
        try:
            element = page.query_selector(selector)
            if element is None:
                logger.warning(f"Element not found: {selector}")
                return ""

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"element_{timestamp}.png"

            filepath = self.screenshot_dir / filename

            element.screenshot(path=str(filepath))

            logger.info(f"Element screenshot saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {e}")
            return ""

    def capture_on_failure(
        self,
        page: Page,
        test_name: str,
        error_message: Optional[str] = None
    ) -> str:
        """
        测试失败时自动截图

        Args:
            page: Playwright Page 对象
            test_name: 测试名称
            error_message: 错误信息（可选）

        Returns:
            截图文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = test_name.replace("/", "_").replace("\\", "_")[:50]
        filename = f"failure_{safe_test_name}_{timestamp}.png"

        filepath = self.capture_screenshot(page, filename)

        # 记录错误信息
        if error_message:
            logger.error(f"Test failed: {test_name} - {error_message}")

        return filepath


class VideoRecorder:
    """视频录制工具类"""

    def __init__(self, video_dir: str = "reports/videos"):
        """
        初始化视频录制工具

        Args:
            video_dir: 视频保存目录
        """
        self.video_dir = Path(video_dir)
        self.video_dir.mkdir(parents=True, exist_ok=True)

    def get_video_path(self, test_name: str) -> str:
        """
        获取视频保存路径

        Args:
            test_name: 测试名称

        Returns:
            视频文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = test_name.replace("/", "_").replace("\\", "_")[:50]
        filename = f"{safe_test_name}_{timestamp}.webm"
        return str(self.video_dir / filename)


# 全局实例
screenshot_utils = ScreenshotUtils()
video_recorder = VideoRecorder()

__all__ = ["ScreenshotUtils", "VideoRecorder", "screenshot_utils", "video_recorder"]