"""Gemini图像生成插件 Provider

提供凭证验证功能。
"""
import httpx
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GeminiImageProvider(ToolProvider):
    """Gemini图像生成插件 Provider

    负责验证 OpenRouter API 密钥的有效性。
    """

    def _validate_credentials(self, credentials: dict) -> None:
        """验证 API 凭证

        通过调用 OpenRouter API 的模型列表端点来验证 API 密钥是否有效。

        Args:
            credentials: 凭证字典，包含 openrouter_api_key

        Raises:
            ToolProviderCredentialValidationError: 凭证验证失败时抛出
        """
        # 获取 API 密钥
        api_key = credentials.get("openrouter_api_key")

        # 检查密钥是否存在
        if not api_key:
            raise ToolProviderCredentialValidationError("OpenRouter API Key is required")

        # 验证密钥格式
        if not api_key.startswith("sk-or-"):
            raise ToolProviderCredentialValidationError(
                "Invalid OpenRouter API Key format. "
                "API Key should start with 'sk-or-'"
            )

        # 调用 API 验证密钥
        try:
            response = httpx.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/YOUR_USERNAME/gemini-image-generator",
                    "X-Title": "Gemini Image Generator"
                },
                timeout=10
            )

            # 检查响应状态
            if response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Invalid OpenRouter API Key. Please check your API key."
                )
            elif response.status_code == 429:
                raise ToolProviderCredentialValidationError(
                    "API rate limit exceeded. Please check your OpenRouter account."
                )
            elif response.status_code >= 400:
                raise ToolProviderCredentialValidationError(
                    f"API validation failed with status {response.status_code}: {response.text}"
                )

            # 验证成功
            response.raise_for_status()

        except httpx.TimeoutException:
            raise ToolProviderCredentialValidationError(
                "API validation timeout. Please check your network connection."
            )
        except httpx.HTTPStatusError as e:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate API key: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestException as e:
            raise ToolProviderCredentialValidationError(
                f"Network error during validation: {str(e)}"
            )
