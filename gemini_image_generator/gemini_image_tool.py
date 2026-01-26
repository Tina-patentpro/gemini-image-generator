"""Gemini图像生成工具节点

这是Dify工作流的核心工具类，整合了API客户端、模板管理和参数验证。
"""
import os
from typing import Dict, Any, Optional
from .api_client import OpenRouterAPIClient
from .templates import get_template_manager
from .utils import (
    get_api_key,
    validate_size,
    validate_num_images,
    validate_mode,
    format_error
)


class GeminiImageGenerator:
    """Gemini图像生成工具类

    提供文生图、图生图、专利附图和产品原型图生成功能。
    """

    def __init__(self):
        """初始化工具实例"""
        self.api_key = self._load_api_key()
        self.api_client = None
        self.template_manager = get_template_manager()

        # 如果有API密钥，创建API客户端
        if self.api_key:
            self.api_client = OpenRouterAPIClient(
                api_key=self.api_key,
                api_base="https://openrouter.ai/api/v1",
                timeout=30,
                max_retries=3
            )

    def _load_api_key(self) -> Optional[str]:
        """从环境变量加载API密钥

        Returns:
            API密钥字符串，如果未配置返回None
        """
        return get_api_key()

    def _validate_parameters(self, params: Dict[str, Any]) -> bool:
        """验证输入参数

        Args:
            params: 参数字典

        Returns:
            验证是否通过
        """
        # 验证mode
        mode = params.get("mode")
        if not mode or not validate_mode(mode):
            return False

        # 验证prompt
        prompt = params.get("prompt")
        if not prompt or not isinstance(prompt, str):
            return False

        # 验证size（必须显式提供）
        if "size" not in params:
            return False
        size = params["size"]
        if not validate_size(size):
            return False

        # 验证num_images（必须显式提供）
        if "num_images" not in params:
            return False
        num_images = params["num_images"]
        if not validate_num_images(num_images):
            return False

        # 图生图模式需要reference_image_url
        if mode == "image_to_image":
            reference_image_url = params.get("reference_image_url")
            if not reference_image_url:
                return False

        return True

    def _apply_template_if_needed(
        self,
        mode: str,
        prompt: str,
        params: Dict[str, Any]
    ) -> str:
        """根据模式应用模板

        Args:
            mode: 工作模式
            prompt: 原始提示词
            params: 参数字典

        Returns:
            应用模板后的提示词
        """
        # 专利附图模式
        if mode == "patent_drawing":
            template_id = params.get("template_id", "explosion")
            template = self.template_manager.get_patent_template(template_id)
            if template:
                return self.template_manager.apply_template(template, prompt)

        # 产品原型图模式
        elif mode == "product_prototype":
            template_id = params.get("template_id", "concept")
            template = self.template_manager.get_product_template(template_id)
            if template:
                return self.template_manager.apply_template(template, prompt)

        # 其他模式不应用模板
        return prompt

    def _format_result(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """格式化API响应为Dify兼容格式

        Args:
            api_response: API响应

        Returns:
            Dify格式结果
        """
        if not api_response.get("success"):
            # API调用失败
            return {
                "success": False,
                "error": api_response.get("error", "未知错误")
            }

        # API调用成功
        images = api_response.get("images", [])

        # 格式化图像列表
        formatted_images = []
        for img_url in images:
            formatted_images.append({
                "url": img_url
            })

        return {
            "success": True,
            "images": formatted_images,
            "count": len(formatted_images)
        }

    def invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """工具调用入口点（Dify工作流调用）

        Args:
            params: 参数字典，包含：
                - mode: 工作模式（text_to_image/image_to_image/patent_drawing/product_prototype）
                - prompt: 提示词
                - size: 图像尺寸（默认1024x1024）
                - num_images: 生成数量（默认1）
                - reference_image_url: 参考图像URL（图生图模式需要）
                - template_id: 模板ID（专利/产品模式需要）

        Returns:
            结果字典，包含：
                - success: 是否成功
                - images: 图像列表（成功时）
                - count: 图像数量（成功时）
                - error: 错误信息（失败时）
        """
        # 检查API密钥
        if not self.api_key or not self.api_client:
            return {
                "success": False,
                "error": format_error(
                    "auth_error",
                    "API密钥未配置，请设置OPENROUTER_API_KEY环境变量",
                    retry_possible=False
                )
            }

        # 验证参数
        if not self._validate_parameters(params):
            return {
                "success": False,
                "error": format_error(
                    "validation_error",
                    "参数验证失败，请检查输入参数",
                    retry_possible=False
                )
            }

        # 提取参数
        mode = params["mode"]
        prompt = params["prompt"]
        size = params.get("size", "1024x1024")
        num_images = params.get("num_images", 1)
        reference_image_url = params.get("reference_image_url")

        # 应用模板（如果需要）
        enhanced_prompt = self._apply_template_if_needed(mode, prompt, params)

        # 映射模式到API调用参数
        api_mode = "text_to_image" if mode in ["text_to_image", "patent_drawing", "product_prototype"] else "image_to_image"

        # 调用API生成图像
        try:
            api_response = self.api_client.generate_image(
                prompt=enhanced_prompt,
                size=size,
                mode=api_mode,
                input_image_url=reference_image_url,
                num_images=num_images
            )

            # 格式化并返回结果
            return self._format_result(api_response)

        except Exception as e:
            # 异常处理
            return {
                "success": False,
                "error": format_error(
                    "unknown_error",
                    f"图像生成失败: {str(e)}",
                    retry_possible=True
                )
            }
