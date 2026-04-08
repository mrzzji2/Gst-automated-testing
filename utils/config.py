"""
Configuration Reader
支持 YAML 配置文件和环境变量
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from loguru import logger


class Config:
    """
    配置读取器
    支持多环境配置和环境变量覆盖
    """

    def __init__(self, config_path: Optional[str] = None, env: Optional[str] = None):
        """
        初始化配置

        Args:
            config_path: 配置文件路径
            env: 环境 (dev, test, prod)
        """
        # 加载环境变量
        load_dotenv()

        # 项目根目录
        self.root_dir = Path(__file__).parent.parent

        # 配置文件路径
        if config_path is None:
            config_path = self.root_dir / "config" / "config.yaml"

        self.config_path = Path(config_path)

        # 当前环境
        self.env = env or os.getenv("APP_ENV", "test")

        # 加载配置
        self._config: Dict[str, Any] = {}
        self._load_config()

        logger.info(f"Config loaded: {self.config_path} (env={self.env})")

    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}

            # 加载环境特定配置
            env_config_path = self.root_dir / "config" / "environments" / f"{self.env}.yaml"
            if env_config_path.exists():
                with open(env_config_path, 'r', encoding='utf-8') as f:
                    env_config = yaml.safe_load(f) or {}
                    self._merge_config(self._config, env_config)

            # 替换环境变量占位符
            self._replace_env_variables(self._config)

        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}")
            self._config = {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            self._config = {}

    def _merge_config(self, base: Dict, override: Dict):
        """递归合并配置"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _replace_env_variables(self, config: Any):
        """替换配置中的环境变量占位符"""
        if isinstance(config, dict):
            for key, value in config.items():
                config[key] = self._replace_env_variables(value)
        elif isinstance(config, list):
            config = [self._replace_env_variables(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            # ${VAR:default} 格式
            var_spec = config[2:-1]
            if ":" in var_spec:
                var_name, default_value = var_spec.split(":", 1)
                config = os.getenv(var_name, default_value)
            else:
                config = os.getenv(var_spec, "")

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号分隔的路径）

        Args:
            key: 配置键 (app.name, urls.base, etc.)
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_int(self, key: str, default: int = 0) -> int:
        """获取整数配置"""
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔配置"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return bool(value)

    def get_list(self, key: str, default: Optional[list] = None) -> list:
        """获取列表配置"""
        value = self.get(key, default)
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return [value]

    def get_dict(self, key: str, default: Optional[dict] = None) -> dict:
        """获取字典配置"""
        value = self.get(key, default)
        if isinstance(value, dict):
            return value
        return {}

    @property
    def app_name(self) -> str:
        """应用名称"""
        return self.get("app.name", "Web Automation Framework")

    @property
    def app_version(self) -> str:
        """应用版本"""
        return self.get("app.version", "1.0.0")

    @property
    def environment(self) -> str:
        """当前环境"""
        return self.env

    @property
    def base_url(self) -> str:
        """基础URL"""
        return self.get("urls.base", "https://example.com")

    @property
    def browser_type(self) -> str:
        """浏览器类型"""
        return self.get("browser.type", "chromium")

    @property
    def browser_headless(self) -> bool:
        """是否无头模式"""
        return self.get_bool("browser.headless", True)

    @property
    def browser_channel(self) -> str:
        """浏览器通道"""
        return self.get("browser.channel", "chrome")

    @property
    def timeout_default(self) -> int:
        """默认超时时间(ms)"""
        return self.get_int("browser.timeout.default", 30000)

    @property
    def timeout_navigation(self) -> int:
        """导航超时时间(ms)"""
        return self.get_int("browser.timeout.navigation", 60000)

    @property
    def parallel_enabled(self) -> bool:
        """是否启用并行执行"""
        return self.get_bool("test.parallel.enabled", True)

    @property
    def parallel_workers(self) -> str:
        """并行工作进程数"""
        return self.get("test.parallel.workers", "auto")

    @property
    def screenshot_on_failure(self) -> bool:
        """失败时是否截图"""
        return self.get_bool("screenshot.on_failure", True)

    @property
    def video_enabled(self) -> bool:
        """是否启用视频录制"""
        return self.get_bool("video.enabled", True)

    @property
    def log_level(self) -> str:
        """日志级别"""
        return self.get("logging.level", "INFO")

    def __repr__(self) -> str:
        return f"Config(env={self.env}, base_url={self.base_url})"


# 全局配置实例
config = Config()
