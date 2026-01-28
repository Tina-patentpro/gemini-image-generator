"""Gemini图像生成工具节点包装器

这个文件将实际的工具实现从provider/目录导入到tools/目录，
符合Dify官方插件标准结构。
"""
import sys
from pathlib import Path

# 添加 provider 目录到 Python 路径
provider_dir = Path(__file__).parent.parent / "provider"
sys.path.insert(0, str(provider_dir))

from gemini_image_tool import GeminiImageGenerator

__all__ = ["GeminiImageGenerator"]
