"""工具函数"""
import os
from typing import Optional


def get_api_key() -> Optional[str]:
    """从环境变量获取API密钥"""
    return os.getenv("OPENROUTER_API_KEY")


def validate_size(size: str) -> bool:
    """验证图像尺寸是否有效"""
    from .config import SUPPORTED_SIZES
    return size in SUPPORTED_SIZES


def validate_num_images(num: int) -> bool:
    """验证生成数量是否有效"""
    return 1 <= num <= 4


def validate_mode(mode: str) -> bool:
    """验证工作模式是否有效"""
    from .config import MODES
    return mode in MODES


def format_error(error_type: str, message: str, retry_possible: bool = False) -> dict:
    """格式化错误响应"""
    return {
        "type": error_type,
        "message": message,
        "retry_possible": retry_possible
    }
