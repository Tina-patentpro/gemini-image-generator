"""主工具节点测试"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from gemini_image_generator.gemini_image_tool import GeminiImageGenerator


class TestGeminiImageGenerator:
    """GeminiImageGenerator工具类测试"""

    def test_tool_initialization(self):
        """测试工具初始化"""
        # 设置环境变量
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"

        # 创建工具实例
        tool = GeminiImageGenerator()

        # 验证初始化
        assert tool.api_key == "test-api-key"
        assert tool.api_client is not None
        assert tool.template_manager is not None

    def test_validate_parameters_success(self):
        """测试参数验证成功"""
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"
        tool = GeminiImageGenerator()

        # 有效参数
        params = {
            "mode": "text_to_image",
            "prompt": "A beautiful sunset",
            "size": "1024x1024",
            "num_images": 1
        }

        # 验证应该成功
        assert tool._validate_parameters(params) is True

    def test_validate_parameters_failure(self):
        """测试参数验证失败"""
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"
        tool = GeminiImageGenerator()

        # 缺少必需参数
        params = {
            "mode": "text_to_image",
            "prompt": "A beautiful sunset"
            # 缺少size和num_images
        }

        # 验证应该失败
        assert tool._validate_parameters(params) is False

    @patch('gemini_image_generator.gemini_image_tool.OpenRouterAPIClient')
    def test_invoke_text_to_image(self, mock_api_client):
        """测试文生图功能"""
        # Mock API响应
        mock_client_instance = Mock()
        mock_client_instance.generate_image.return_value = {
            "success": True,
            "images": ["https://example.com/image1.png"],
            "count": 1
        }
        mock_api_client.return_value = mock_client_instance

        # 创建工具实例
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"
        tool = GeminiImageGenerator()

        # 调用工具
        params = {
            "mode": "text_to_image",
            "prompt": "A beautiful sunset",
            "size": "1024x1024",
            "num_images": 1
        }

        result = tool.invoke(params)

        # 验证结果
        assert result["success"] is True
        assert len(result["images"]) == 1
        assert result["images"][0]["url"] == "https://example.com/image1.png"

    @patch('gemini_image_generator.gemini_image_tool.OpenRouterAPIClient')
    def test_invoke_with_patent_template(self, mock_api_client):
        """测试使用专利模板"""
        # Mock API响应
        mock_client_instance = Mock()
        mock_client_instance.generate_image.return_value = {
            "success": True,
            "images": ["https://example.com/patent_image.png"],
            "count": 1
        }
        mock_api_client.return_value = mock_client_instance

        # 创建工具实例
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"
        tool = GeminiImageGenerator()

        # 使用专利模板
        params = {
            "mode": "patent_drawing",
            "prompt": "智能手表",  # 简短提示词，会被模板增强
            "size": "1024x1024",
            "num_images": 1
        }

        result = tool.invoke(params)

        # 验证结果
        assert result["success"] is True
        # 验证提示词被模板增强（包含更详细的描述）
        mock_client_instance.generate_image.assert_called_once()
        call_args = mock_client_instance.generate_image.call_args
        enhanced_prompt = call_args[1]["prompt"]
        assert len(enhanced_prompt) > len(params["prompt"])

    @patch('gemini_image_generator.gemini_image_tool.OpenRouterAPIClient')
    def test_invoke_with_api_error(self, mock_api_client):
        """测试API错误处理"""
        # Mock API错误
        mock_client_instance = Mock()
        mock_client_instance.generate_image.side_effect = Exception("API Error: Rate limit exceeded")
        mock_api_client.return_value = mock_client_instance

        # 创建工具实例
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"
        tool = GeminiImageGenerator()

        # 调用工具
        params = {
            "mode": "text_to_image",
            "prompt": "A beautiful sunset",
            "size": "1024x1024",
            "num_images": 1
        }

        result = tool.invoke(params)

        # 验证错误处理
        assert result["success"] is False
        assert "error" in result
        # error是一个字典
        assert "Rate limit exceeded" in result["error"]["message"]

    def test_invoke_without_api_key(self):
        """测试没有API密钥的情况"""
        # 移除API密钥
        if "OPENROUTER_API_KEY" in os.environ:
            del os.environ["OPENROUTER_API_KEY"]

        # 创建工具实例
        tool = GeminiImageGenerator()

        # 调用工具应该返回错误
        params = {
            "mode": "text_to_image",
            "prompt": "A beautiful sunset",
            "size": "1024x1024",
            "num_images": 1
        }

        result = tool.invoke(params)

        # 验证错误
        assert result["success"] is False
        # error是一个字典
        assert "API密钥未配置" in result["error"]["message"]

        # 恢复环境变量
        os.environ["OPENROUTER_API_KEY"] = "test-api-key"
