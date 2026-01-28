"""Gemini图像生成工具节点

这是Dify工作流的核心工具类，整合了API客户端、模板管理和参数验证。
"""
from typing import Generator, Any
from dify_plugin import Tool
from dify_plugin.interfaces.tool import ToolInvokeMessage

from .api_client import OpenRouterAPIClient
from .templates import get_template_manager
from .utils import validate_size, validate_num_images, validate_mode


class GeminiImageGenerator(Tool):
    """Gemini图像生成工具类

    提供文生图、图生图、专利附图和产品原型图生成功能。
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """工具调用入口点（Dify工作流调用）

        Args:
            tool_parameters: 参数字典，包含：
                - mode: 工作模式（text_to_image/image_to_image/patent_drawing/product_prototype）
                - prompt: 提示词
                - size: 图像尺寸（默认1024x1024）
                - num_images: 生成数量（默认1）
                - reference_image_url: 参考图像URL（图生图模式需要）
                - preset_template: 预设模板ID（专利/产品模式）

        Yields:
            ToolInvokeMessage: 执行结果消息

        Raises:
            ValueError: 参数验证失败
            Exception: API 调用失败
        """
        # 1. 获取并验证凭证
        credentials = self.runtime.credentials
        api_key = credentials.get("openrouter_api_key")
        if not api_key:
            raise ValueError("OpenRouter API Key is required. Please configure it in the plugin settings.")

        # 2. 验证基本参数
        mode = tool_parameters.get("mode")
        if not mode or not validate_mode(mode):
            raise ValueError(f"Invalid mode: {mode}. Must be one of: text_to_image, image_to_image, patent_drawing, product_prototype")

        prompt = tool_parameters.get("prompt")
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt is required and must be a string")

        size = tool_parameters.get("size", "1024x1024")
        if not validate_size(size):
            raise ValueError(f"Invalid size: {size}. Supported sizes: 1024x1024, 1024x768, 768x1024, 832x1216, 1216x832")

        num_images = tool_parameters.get("num_images", 1)
        if not validate_num_images(num_images):
            raise ValueError(f"Invalid num_images: {num_images}. Must be between 1 and 4")

        # 3. 图生图模式需要参考图像
        reference_image_url = tool_parameters.get("reference_image_url")
        if mode == "image_to_image" and not reference_image_url:
            raise ValueError("reference_image_url is required for image_to_image mode")

        # 4. 应用模板（如果需要）
        template_id = tool_parameters.get("preset_template")
        enhanced_prompt = prompt

        if template_id:
            template_manager = get_template_manager()

            if mode == "patent_drawing":
                template = template_manager.get_patent_template(template_id)
                if template:
                    enhanced_prompt = template_manager.apply_template(template, prompt)
                else:
                    import warnings
                    warnings.warn(f"Template '{template_id}' not found for patent_drawing mode, using original prompt")

            elif mode == "product_prototype":
                template = template_manager.get_product_template(template_id)
                if template:
                    enhanced_prompt = template_manager.apply_template(template, prompt)
                else:
                    import warnings
                    warnings.warn(f"Template '{template_id}' not found for product_prototype mode, using original prompt")

        # 5. 创建 API 客户端
        api_client = OpenRouterAPIClient(
            api_key=api_key,
            api_base="https://openrouter.ai/api/v1",
            timeout=30,
            max_retries=3
        )

        # 6. 映射模式到API调用参数
        api_mode = "text_to_image" if mode in ["text_to_image", "patent_drawing", "product_prototype"] else "image_to_image"

        # 7. 调用 API 生成图像
        try:
            api_response = api_client.generate_image(
                prompt=enhanced_prompt,
                size=size,
                mode=api_mode,
                input_image_url=reference_image_url,
                num_images=num_images
            )

            # 8. 检查 API 响应
            if not api_response["success"]:
                error_msg = api_response.get("error", {})
                if isinstance(error_msg, dict):
                    error_message = error_msg.get("message", "Unknown API error")
                else:
                    error_message = str(error_msg)

                raise Exception(f"Image generation failed: {error_message}")

            # 9. 成功 - 返回结果
            images = api_response.get("images", [])
            formatted_images = [{"url": url} for url in images]

            yield self.create_json_message({
                "success": True,
                "images": formatted_images,
                "count": len(formatted_images)
            })

        except Exception as e:
            # 重新抛出已知的异常
            if "timeout" in str(e).lower():
                raise Exception("API request timeout. Please try again.")
            elif "network" in str(e).lower() or "connection" in str(e).lower():
                raise Exception(f"Network error: {str(e)}")
            else:
                raise
