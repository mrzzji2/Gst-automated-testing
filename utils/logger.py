"""
Logger Configuration
使用 loguru 进行日志管理
"""
import sys
from pathlib import Path
from loguru import logger
from typing import Optional


class Logger:
    """
    日志管理器
    支持控制台和文件输出，按日期分割
    """

    def __init__(
        self,
        log_level: str = "INFO",
        log_path: Optional[str] = None,
        console_output: bool = True,
        file_output: bool = True
    ):
        """
        初始化日志

        Args:
            log_level: 日志级别
            log_path: 日志文件路径
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
        """
        self.log_level = log_level
        self.log_path = log_path or "logs/auto"
        self.console_output = console_output
        self.file_output = file_output

        # 项目根目录
        self.root_dir = Path(__file__).parent.parent

        # 配置日志
        self._configure_logger()

    def _configure_logger(self):
        """配置 loguru 日志"""

        # 移除默认处理器
        logger.remove()

        # 日志格式
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        # 控制台输出
        if self.console_output:
            logger.add(
                sys.stderr,
                format=log_format,
                level=self.log_level,
                colorize=True,
                backtrace=True,
                diagnose=True
            )

        # 文件输出
        if self.file_output:
            log_dir = self.root_dir / self.log_path
            log_dir.mkdir(parents=True, exist_ok=True)

            # 普通日志文件（按日期分割）
            logger.add(
                log_dir / "app_{time:YYYY-MM-DD}.log",
                format=log_format,
                level=self.log_level,
                rotation="100 MB",
                retention="7 days",
                compression="zip",
                encoding="utf-8",
                backtrace=True,
                diagnose=True
            )

            # 错误日志文件（单独记录）
            logger.add(
                log_dir / "error_{time:YYYY-MM-DD}.log",
                format=log_format,
                level="ERROR",
                rotation="100 MB",
                retention="30 days",
                compression="zip",
                encoding="utf-8",
                backtrace=True,
                diagnose=True
            )

    @staticmethod
    def get_logger(name: Optional[str] = None):
        """
        获取 logger 实例

        Args:
            name: logger 名称

        Returns:
            logger 实例
        """
        if name:
            return logger.bind(name=name)
        return logger


# 预定义的 logger 实例
def setup_logger(
    log_level: str = "INFO",
    log_path: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True
) -> None:
    """
    设置全局日志

    Args:
        log_level: 日志级别
        log_path: 日志文件路径
        console_output: 是否输出到控制台
        file_output: 是否输出到文件
    """
    Logger(log_level, log_path, console_output, file_output)


# 导出 logger
__all__ = ["logger", "setup_logger", "Logger"]
