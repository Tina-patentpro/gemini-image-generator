"""OpenRouter API客户端"""
import time
import re
import requests
from typing import Optional, Dict, Any, List
from .utils import format_error


class OpenRouterAPIClient:
    """OpenRouter API客户端类"""

    def __init__(
        self,
        api_key: str,
        api_base: str = "https://openrouter.ai/api/v1",
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        初始化API客户端

        Args:
            api_key: OpenRouter API密钥
            api_base: API基础URL
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.api_key = api_key
        self.api_base = api_base
        self.timeout = timeout
        self.max_retries = max_retries

    def _build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dify-plugin",
            "X-Title": "Dify Gemini Image Plugin"
        }

    def _build_payload(
        self,
        prompt: str,
        size: str,
        mode: str,
        input_image_url: Optional[str] = None,
        num_images: int = 1
    ) -> Dict[str, Any]:
        """
        构建API请求负载

        Args:
            prompt: 提示词
            size: 图像尺寸
            mode: 工作模式
            input_image_url: 输入图像URL（图生图模式）
            num_images: 生成图像数量

        Returns:
            请求负载字典
        """
        from .config import (
            MODEL_ID,
            DEFAULT_SIZE,
            DEFAULT_EDIT,
            EDIT_TYPES
        )

        messages = []

        if mode == "text_to_image":
            # 文生图模式
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate an image: {prompt}\n\nSize: {size or DEFAULT_SIZE}"
                    }
                ]
            })
        elif mode == "image_to_image":
            # 图生图模式
            edit_type = self._get_edit_type_desc(prompt)
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{edit_type}\n\nSize: {size or DEFAULT_SIZE}\n\nInstruction: {prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": input_image_url
                        }
                    }
                ]
            })

        return {
            "model": MODEL_ID,
            "messages": messages,
            "max_tokens": 1000
        }

    def _get_edit_type_desc(self, prompt: str) -> str:
        """
        根据提示词获取编辑类型描述

        Args:
            prompt: 用户提示词

        Returns:
            编辑类型描述
        """
        from .config import EDIT_TYPES

        prompt_lower = prompt.lower()

        # 检查是否包含特定编辑类型关键词
        for edit_type, keywords in EDIT_TYPES.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return f"Edit type: {edit_type}"

        return "Edit type: general"

    def _parse_image_response(self, response: Dict[str, Any]) -> List[str]:
        """
        解析API响应中的图像URL

        Args:
            response: API响应

        Returns:
            图像URL列表
        """
        try:
            content = response["choices"][0]["message"]["content"]

            # 使用正则表达式提取所有图像URL
            # 格式: ![image](url) 或
            pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
            matches = re.findall(pattern, content)

            return matches
        except (KeyError, IndexError, AttributeError) as e:
            return []

    def generate_image(
        self,
        prompt: str,
        size: str,
        mode: str,
        input_image_url: Optional[str] = None,
        num_images: int = 1
    ) -> Dict[str, Any]:
        """
        生成图像

        Args:
            prompt: 提示词
            size: 图像尺寸
            mode: 工作模式（text_to_image/image_to_image）
            input_image_url: 输入图像URL（图生图模式需要）
            num_images: 生成图像数量

        Returns:
            包含生成结果或错误信息的字典
        """
        url = f"{self.api_base}/chat/completions"
        headers = self._build_headers()
        payload = self._build_payload(
            prompt=prompt,
            size=size,
            mode=mode,
            input_image_url=input_image_url,
            num_images=num_images
        )

        # 重试逻辑
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )

                # 检查HTTP状态码
                response.raise_for_status()

                # 解析响应
                response_data = response.json()
                images = self._parse_image_response(response_data)

                if not images:
                    return {
                        "success": False,
                        "error": format_error(
                            "api_error",
                            "未能从API响应中提取图像URL",
                            retry_possible=True
                        )
                    }

                return {
                    "success": True,
                    "images": images[:num_images],  # 限制返回数量
                    "count": len(images[:num_images])
                }

            except requests.exceptions.Timeout as e:
                last_error = e
                # 超时重试
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                else:
                    return {
                        "success": False,
                        "error": format_error(
                            "timeout_error",
                            f"请求超时: {str(e)}",
                            retry_possible=True
                        )
                    }

            except requests.exceptions.HTTPError as e:
                # HTTP错误不重试
                error_msg = str(e)
                try:
                    error_detail = response.json()
                    if "error" in error_detail:
                        error_msg = error_detail["error"].get("message", error_msg)
                except:
                    pass

                return {
                    "success": False,
                    "error": format_error(
                        "api_error",
                        f"API错误: {error_msg}",
                        retry_possible=False
                    )
                }

            except requests.exceptions.RequestException as e:
                last_error = e
                # 网络错误重试
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                else:
                    return {
                        "success": False,
                        "error": format_error(
                            "network_error",
                            f"网络错误: {str(e)}",
                            retry_possible=True
                        )
                    }

            except Exception as e:
                # 其他错误不重试
                return {
                    "success": False,
                    "error": format_error(
                        "unknown_error",
                        f"未知错误: {str(e)}",
                        retry_possible=False
                    )
                }

        # 所有重试都失败
        return {
            "success": False,
            "error": format_error(
                "network_error",
                f"达到最大重试次数 ({self.max_retries})",
                retry_possible=False
            )
        }
