"""OpenRouter API客户端测试"""
import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from gemini_image_generator.api_client import OpenRouterAPIClient


class TestOpenRouterAPIClient:
    """测试OpenRouterAPIClient类"""

    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = OpenRouterAPIClient(api_key="test-key")

    def test_init_default_params(self):
        """测试客户端初始化默认参数"""
        assert self.client.api_key == "test-key"
        assert self.client.api_base == "https://openrouter.ai/api/v1"
        assert self.client.timeout == 30
        assert self.client.max_retries == 3

    def test_init_custom_params(self):
        """测试客户端初始化自定义参数"""
        client = OpenRouterAPIClient(
            api_key="custom-key",
            api_base="https://custom.api.com",
            timeout=60,
            max_retries=5
        )
        assert client.api_key == "custom-key"
        assert client.api_base == "https://custom.api.com"
        assert client.timeout == 60
        assert client.max_retries == 5

    def test_build_headers(self):
        """测试请求头构建"""
        headers = self.client._build_headers()
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"
        assert "HTTP-Referer" in headers
        assert "X-Title" in headers

    @patch("requests.post")
    def test_generate_image_text_to_image_success(self, mock_post):
        """测试文生图成功"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "![image](https://example.com/image1.png)"
                }
            }]
        }
        mock_post.return_value = mock_response

        result = self.client.generate_image(
            prompt="A beautiful sunset",
            size="1024x1024",
            mode="text_to_image"
        )

        assert result["success"] is True
        assert len(result["images"]) == 1
        assert result["images"][0] == "https://example.com/image1.png"
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_generate_image_image_to_image_success(self, mock_post):
        """测试图生图成功"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "![image](https://example.com/image1.png)"
                }
            }]
        }
        mock_post.return_value = mock_response

        result = self.client.generate_image(
            prompt="Make it brighter",
            size="1024x1024",
            mode="image_to_image",
            input_image_url="https://example.com/input.png"
        )

        assert result["success"] is True
        assert len(result["images"]) == 1
        assert result["images"][0] == "https://example.com/image1.png"

    @patch("requests.post")
    def test_generate_image_network_error(self, mock_post):
        """测试网络错误"""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        result = self.client.generate_image(
            prompt="A beautiful sunset",
            size="1024x1024",
            mode="text_to_image"
        )

        assert result["success"] is False
        assert result["error"]["type"] == "network_error"
        assert "retry_possible" in result["error"]

    @patch("requests.post")
    def test_generate_image_api_error(self, mock_post):
        """测试API错误"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": {
                "message": "Invalid request"
            }
        }
        mock_post.return_value = mock_response

        result = self.client.generate_image(
            prompt="A beautiful sunset",
            size="1024x1024",
            mode="text_to_image"
        )

        assert result["success"] is False
        assert result["error"]["type"] == "api_error"

    @patch("requests.post")
    def test_generate_image_timeout(self, mock_post):
        """测试超时"""
        mock_post.side_effect = requests.exceptions.Timeout("Request timeout")

        result = self.client.generate_image(
            prompt="A beautiful sunset",
            size="1024x1024",
            mode="text_to_image"
        )

        assert result["success"] is False
        assert result["error"]["type"] == "timeout_error"

    def test_parse_image_response_single(self):
        """测试解析单个图片响应"""
        response = {
            "choices": [{
                "message": {
                    "content": "![image](https://example.com/image.png)"
                }
            }]
        }

        images = self.client._parse_image_response(response)
        assert len(images) == 1
        assert images[0] == "https://example.com/image.png"

    def test_parse_image_response_multiple(self):
        """测试解析多个图片响应"""
        response = {
            "choices": [{
                "message": {
                    "content": """![image](https://example.com/image1.png)
![image](https://example.com/image2.png)
![image](https://example.com/image3.png)
![image](https://example.com/image4.png)"""
                }
            }]
        }

        images = self.client._parse_image_response(response)
        assert len(images) == 4
        assert images[0] == "https://example.com/image1.png"
        assert images[3] == "https://example.com/image4.png"
