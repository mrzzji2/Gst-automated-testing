import os
import yaml
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 环境变量覆盖
    if 'GST_BASE_URL' in os.environ:
        config['base_url'] = os.environ['GST_BASE_URL']
    if 'HEADLESS' in os.environ:
        config['headless'] = os.environ['HEADLESS'].lower() == 'true'
    
    return config