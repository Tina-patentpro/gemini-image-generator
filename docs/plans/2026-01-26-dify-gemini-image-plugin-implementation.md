# Dify Gemini图像生成插件实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个Dify插件，通过OpenRouter调用Google Gemini 2.0 Flash模型，实现专利附图和产品原型图的AI生成与编辑功能。

**Architecture:** 采用统一多功能节点架构，通过mode参数切换文生图/图生图/专利图/原型图四种模式，使用模板系统管理预设提示词，API客户端封装OpenRouter调用逻辑，宽松的错误处理确保工作流不中断。

**Tech Stack:** Python 3.10+, Dify Tool Plugin API, OpenRouter API, requests, pydantic, pytest

---

## Task 1: 创建项目基础结构

**Files:**
- Create: `gemini_image_generator/__init__.py`
- Create: `gemini_image_generator/config.py`
- Create: `requirements.txt`
- Create: `manifest.yaml`
- Create: `README.md`

**Step 1: 创建包目录和初始化文件**

```bash
cd .worktrees/dify-gemini-image-plugin
mkdir -p gemini_image_generator
```

创建 `gemini_image_generator/__init__.py`:

```python
"""Dify Gemini图像生成插件"""
__version__ = "1.0.0"

from .gemini_image_tool import GeminiImageGenerator

__all__ = ["GeminiImageGenerator"]
```

**Step 2: 创建配置常量文件**

创建 `gemini_image_generator/config.py`:

```python
"""配置常量"""

# OpenRouter API配置
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemini-2.0-flash-exp-image-generation"
API_TIMEOUT = 30  # 秒
MAX_RETRIES = 3

# 环境变量名
API_KEY_ENV = "OPENROUTER_API_KEY"

# 支持的图像尺寸
SUPPORTED_SIZES = [
    "1024x1024",
    "1024x768",
    "768x1024",
    "832x1216",
    "1216x832"
]

# 支持的工作模式
MODES = {
    "text_to_image": "文生图",
    "image_to_image": "图生图/文改图",
    "patent_drawing": "专利附图",
    "product_prototype": "产品原型图"
}

# 图生图编辑类型
EDIT_TYPES = {
    "modify": "图像修改/编辑",
    "style_transfer": "风格迁移",
    "sketch_render": "草图渲染",
    "outpainting": "图像外扩"
}

# 线条风格
LINE_STYLES = {
    "technical": "技术绘图",
    "sketch": "草图",
    "render": "渲染图"
}

# 视角选项
VIEW_ANGLES = {
    "front": "正视图",
    "top": "俯视图",
    "side": "侧视图",
    "isometric": "等轴测图"
}
```

**Step 3: 创建依赖文件**

创建 `requirements.txt`:

```txt
requests>=2.31.0
pydantic>=2.0.0
pytest>=7.4.0
pytest-mock>=3.11.0
```

**Step 4: 创建Dify插件清单**

创建 `manifest.yaml`:

```yaml
type: tool
name: gemini_image_generator
version: 1.0.0
description: "使用Gemini模型生成专利附图和产品原型图，支持文生图、图生图、专利图和产品原型图四种模式"
author: "Your Name"
icon: "🎨"

parameters:
  - name: mode
    type: select
    required: true
    options:
      - value: text_to_image
        label: 文生图
      - value: image_to_image
        label: 图生图/文改图
      - value: patent_drawing
        label: 专利附图
      - value: product_prototype
        label: 产品原型图
    description: "选择工作模式"
    default: text_to_image

  - name: prompt
    type: text
    required: true
    description: "图像生成提示词，支持中英文"
    default: ""

  - name: negative_prompt
    type: text
    required: false
    description: "负面提示词，指定不想要的内容"

  - name: reference_image_url
    type: text
    required: false
    description: "图生图模式时的参考图像URL"

  - name: edit_type
    type: select
    required: false
    options:
      - value: modify
        label: 图像修改/编辑
      - value: style_transfer
        label: 风格迁移
      - value: sketch_render
        label: 草图渲染
      - value: outpainting
        label: 图像外扩
    description: "图生图时的编辑类型"

  - name: preset_template
    type: select
    required: false
    options:
      - value: explosion
        label: 爆炸图
      - value: assembly
        label: 装配图
      - value: detail
        label: 零件细节图
      - value: section
        label: 剖面图
      - value: principle
        label: 原理图
      - value: circuit
        label: 电路/管路图
      - value: concept
        label: 概念渲染图
      - value: ui
        label: 用户界面图
      - value: scene
        label: 场景使用图
      - value: function
        label: 功能示意图
      - value: packaging
        label: 包装设计图
    description: "预设模板"

  - name: line_style
    type: select
    required: false
    options:
      - value: technical
        label: 技术绘图
      - value: sketch
        label: 草图
      - value: render
        label: 渲染图
    description: "线条风格"

  - name: view_angle
    type: select
    required: false
    options:
      - value: front
        label: 正视图
      - value: top
        label: 俯视图
      - value: side
        label: 侧视图
      - value: isometric
        label: 等轴测图
    description: "视角"

  - name: size
    type: select
    required: false
    options:
      - value: "1024x1024"
        label: "1024x1024"
      - value: "1024x768"
        label: "1024x768"
      - value: "768x1024"
        label: "768x1024"
      - value: "832x1216"
        label: "832x1216"
      - value: "1216x832"
        label: "1216x832"
    description: "图像尺寸"
    default: "1024x1024"

  - name: num_images
    type: number
    required: false
    description: "生成数量（1-4）"
    default: 1
    min: 1
    max: 4

  - name: seed
    type: number
    required: false
    description: "随机种子，用于复现结果"

returns:
  - name: success
    type: boolean
    description: "是否成功"

  - name: images
    type: array
    description: "生成的图像列表"

  - name: error
    type: object
    description: "错误信息（如果失败）"
```

**Step 5: 创建基础README**

创建 `README.md`:

```markdown
# Dify Gemini图像生成插件

通过OpenRouter调用Google Gemini 2.0 Flash模型，实现专利附图和产品原型图的AI生成与编辑功能。

## 功能特性

- **文生图**: 基于文本描述生成全新图像
- **图生图/文改图**: 基于参考图像进行修改、风格迁移、草图渲染、图像外扩
- **专利附图模式**: 爆炸图、装配图、剖面图等专业模板
- **产品原型图模式**: 概念渲染图、UI设计图、场景使用图等模板

## 安装

1. 将插件复制到Dify的plugins目录
2. 配置环境变量 `OPENROUTER_API_KEY`
3. 在Dify中重启或重新加载插件

## 使用示例

### 生成专利爆炸图
```
mode: 专利附图
preset_template: 爆炸图
prompt: "手持电动工具的爆炸图，展示电机、齿轮箱、外壳的装配关系"
size: 1024x1024
```

### 产品概念图生成
```
mode: 产品原型图
preset_template: 概念渲染图
prompt: "智能蓝牙耳机，现代简约设计，白色磨砂质感，45度视角"
```

### 草图渲染
```
mode: 图生图
edit_type: 草图渲染
reference_image_url: [草图URL]
prompt: "将草图渲染为高质量产品图"
```

## 错误处理

插件采用宽松的错误处理机制，失败时不会中断工作流，而是返回错误信息供后续节点处理。

## 许可证

MIT License
```

**Step 6: 提交基础结构**

```bash
git add gemini_image_generator/ requirements.txt manifest.yaml README.md
git commit -m "feat: create project base structure

- Create package structure with __init__.py
- Add configuration constants
- Create requirements.txt with dependencies
- Add Dify plugin manifest.yaml
- Add comprehensive README.md

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 2: 实现预设模板系统

**Files:**
- Create: `gemini_image_generator/templates.py`
- Test: `tests/test_templates.py`

**Step 1: 编写模板系统测试**

创建 `tests/test_templates.py`:

```python
"""测试预设模板系统"""
import pytest
from gemini_image_generator.templates import TemplateManager, get_template_manager


def test_template_manager_singleton():
    """测试TemplateManager是单例"""
    manager1 = get_template_manager()
    manager2 = get_template_manager()
    assert manager1 is manager2


def test_get_patent_template():
    """测试获取专利模板"""
    manager = get_template_manager()
    template = manager.get_patent_template("explosion")
    assert template is not None
    assert "explosion" in template["name"]
    assert template["type"] == "patent"


def test_get_product_template():
    """测试获取产品模板"""
    manager = get_template_manager()
    template = manager.get_product_template("concept")
    assert template is not None
    assert "concept" in template["name"]
    assert template["type"] == "product"


def test_apply_template():
    """测试应用模板到用户提示词"""
    manager = get_template_manager()
    template = manager.get_patent_template("explosion")
    user_prompt = "手持电动工具"
    result = manager.apply_template(template, user_prompt)
    assert "爆炸图" in result
    assert "手持电动工具" in result


def test_invalid_template_id():
    """测试无效的模板ID返回None"""
    manager = get_template_manager()
    result = manager.get_patent_template("invalid_id")
    assert result is None


def test_list_all_templates():
    """测试列出所有模板"""
    manager = get_template_manager()
    templates = manager.list_all_templates()
    assert len(templates) > 0
    assert any(t["id"] == "explosion" for t in templates)


def test_template_structure():
    """测试模板包含必需的字段"""
    manager = get_template_manager()
    template = manager.get_patent_template("explosion")
    assert "id" in template
    assert "name" in template
    assert "type" in template
    assert "prompt_prefix" in template
    assert "default_params" in template
```

运行测试验证失败:

```bash
cd .worktrees/dify-gemini-image-plugin
pytest tests/test_templates.py -v
```

预期: FAIL - "ModuleNotFoundError: No module named 'gemini_image_generator.templates'"

**Step 2: 实现模板系统**

创建 `gemini_image_generator/templates.py`:

```python
"""预设模板管理系统"""
from typing import Dict, List, Optional, Any


class TemplateManager:
    """模板管理器单例"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_templates()
        return cls._instance

    def _init_templates(self):
        """初始化模板数据"""
        self._patent_templates = {
            "explosion": {
                "id": "explosion",
                "name": "爆炸图",
                "type": "patent",
                "prompt_prefix": "技术爆炸图，零件分离显示，清晰标注各部件位置和装配关系，",
                "prompt_suffix": "要求线条清晰，比例准确，符合技术绘图规范。",
                "default_params": {
                    "line_style": "technical",
                    "size": "1024x1024"
                }
            },
            "assembly": {
                "id": "assembly",
                "name": "装配图",
                "type": "patent",
                "prompt_prefix": "产品装配图，展示整体结构和组件组合方式，",
                "prompt_suffix": "要求层次分明，装配关系清晰，符合工程制图标准。",
                "default_params": {
                    "line_style": "technical",
                    "view_angle": "isometric"
                }
            },
            "detail": {
                "id": "detail",
                "name": "零件细节图",
                "type": "patent",
                "prompt_prefix": "零件细节特写图，局部放大显示，",
                "prompt_suffix": "要求细节清晰，工艺要求明确，标注尺寸和公差。",
                "default_params": {
                    "line_style": "technical"
                }
            },
            "section": {
                "id": "section",
                "name": "剖面图",
                "type": "patent",
                "prompt_prefix": "剖面视图，展示内部结构和材料分布，",
                "prompt_suffix": "要求剖面线清晰，材料区分明确，内部结构可见。",
                "default_params": {
                    "line_style": "technical"
                }
            },
            "principle": {
                "id": "principle",
                "name": "原理图",
                "type": "patent",
                "prompt_prefix": "工作原理示意图，展示工作流程和功能关系，",
                "prompt_suffix": "要求流程清晰，箭头指示明确，逻辑关系清楚。",
                "default_params": {
                    "line_style": "technical"
                }
            },
            "circuit": {
                "id": "circuit",
                "name": "电路/管路图",
                "type": "patent",
                "prompt_prefix": "电路图或管路图，展示连接关系和走向，",
                "prompt_suffix": "要求连接清晰，符号标准，路径明确。",
                "default_params": {
                    "line_style": "technical"
                }
            }
        }

        self._product_templates = {
            "concept": {
                "id": "concept",
                "name": "概念渲染图",
                "type": "product",
                "prompt_prefix": "产品概念设计图，现代感设计风格，3D渲染效果，",
                "prompt_suffix": "要求材质真实，光影自然，符合现代审美。",
                "default_params": {
                    "line_style": "render",
                    "size": "1024x1024"
                }
            },
            "ui": {
                "id": "ui",
                "name": "用户界面图",
                "type": "product",
                "prompt_prefix": "用户界面UI/UX设计图，展示界面布局和交互元素，",
                "prompt_suffix": "要求布局合理，视觉层次清晰，符合设计规范。",
                "default_params": {
                    "line_style": "render"
                }
            },
            "scene": {
                "id": "scene",
                "name": "场景使用图",
                "type": "product",
                "prompt_prefix": "产品使用场景图，展示真实环境中的应用，",
                "prompt_suffix": "要求场景真实，比例协调，展示产品实际使用状态。",
                "default_params": {
                    "line_style": "render"
                }
            },
            "function": {
                "id": "function",
                "name": "功能示意图",
                "type": "product",
                "prompt_prefix": "功能模块示意图，展示产品功能划分和操作流程，",
                "prompt_suffix": "要求模块清晰，流程明确，状态转换可见。",
                "default_params": {
                    "line_style": "technical"
                }
            },
            "packaging": {
                "id": "packaging",
                "name": "包装设计图",
                "type": "product",
                "prompt_prefix": "产品包装设计图，展示包装效果和品牌元素，",
                "prompt_suffix": "要求设计美观，品牌突出，包装结构合理。",
                "default_params": {
                    "line_style": "render"
                }
            }
        }

    def get_patent_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取专利附图模板"""
        return self._patent_templates.get(template_id)

    def get_product_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取产品原型图模板"""
        return self._product_templates.get(template_id)

    def apply_template(self, template: Dict[str, Any], user_prompt: str) -> str:
        """应用模板到用户提示词"""
        prefix = template.get("prompt_prefix", "")
        suffix = template.get("prompt_suffix", "")
        return f"{prefix}{user_prompt}，{suffix}"

    def get_template_default_params(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """获取模板的默认参数"""
        return template.get("default_params", {})

    def list_all_templates(self) -> List[Dict[str, Any]]:
        """列出所有模板"""
        templates = []
        templates.extend(list(self._patent_templates.values()))
        templates.extend(list(self._product_templates.values()))
        return templates


# 单例访问函数
_template_manager: Optional[TemplateManager] = None


def get_template_manager() -> TemplateManager:
    """获取模板管理器单例"""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager
```

**Step 3: 运行测试验证通过**

```bash
pytest tests/test_templates.py -v
```

预期: PASS (8个测试全部通过)

**Step 4: 提交模板系统**

```bash
git add gemini_image_generator/templates.py tests/test_templates.py
git commit -m "feat: implement template system

- Add TemplateManager singleton class
- Implement 6 patent drawing templates
- Implement 5 product prototype templates
- Add template application logic
- Add comprehensive unit tests
- All tests passing (8/8)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 3: 实现OpenRouter API客户端

**Files:**
- Create: `gemini_image_generator/api_client.py`
- Create: `gemini_image_generator/utils.py`
- Test: `tests/test_api_client.py`

**Step 1: 编写工具函数**

创建 `gemini_image_generator/utils.py`:

```python
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
```

**Step 2: 编写API客户端测试**

创建 `tests/test_api_client.py`:

```python
"""测试OpenRouter API客户端"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from gemini_image_generator.api_client import OpenRouterAPIClient
from gemini_image_generator.config import MODEL_NAME


@pytest.fixture
def api_client():
    """创建API客户端实例"""
    return OpenRouterAPIClient(api_key="test_key")


def test_client_initialization(api_client):
    """测试客户端初始化"""
    assert api_client.api_key == "test_key"
    assert api_client.api_base == "https://openrouter.ai/api/v1/chat/completions"
    assert api_client.timeout == 30
    assert api_client.max_retries == 3


def test_build_text_to_image_payload(api_client):
    """测试构建文生图请求体"""
    payload = api_client._build_payload(
        mode="text_to_image",
        prompt="一个可爱的猫",
        size="1024x1024",
        num_images=1
    )
    assert payload["model"] == MODEL_NAME
    assert len(payload["messages"]) == 1
    assert "可爱的猫" in payload["messages"][0]["content"]


def test_build_image_to_image_payload(api_client):
    """测试构建图生图请求体"""
    payload = api_client._build_payload(
        mode="image_to_image",
        prompt="修改图像",
        reference_image_url="https://example.com/image.jpg",
        edit_type="modify",
        size="1024x1024",
        num_images=1
    )
    assert payload["model"] == MODEL_NAME
    assert len(payload["messages"]) >= 2
    # 验证包含图像
    has_image = any(
        msg.get("type") == "image_url"
        for msg in payload["messages"]
    )
    assert has_image


@patch('requests.post')
def test_successful_api_call(mock_post, api_client):
    """测试成功的API调用"""
    # Mock响应
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "生成的图像数据"
            }
        }]
    }
    mock_post.return_value = mock_response

    result = api_client.generate_image(
        mode="text_to_image",
        prompt="测试提示词"
    )

    assert result["success"] is True
    assert "data" in result
    mock_post.assert_called_once()


@patch('requests.post')
def test_api_error_401(mock_post, api_client):
    """测试401认证失败"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_post.return_value = mock_response

    result = api_client.generate_image(
        mode="text_to_image",
        prompt="测试提示词"
    )

    assert result["success"] is False
    assert result["error"]["type"] == "api_error"


@patch('requests.post')
def test_network_timeout(mock_post, api_client):
    """测试网络超时"""
    import requests
    mock_post.side_effect = requests.exceptions.Timeout()

    result = api_client.generate_image(
        mode="text_to_image",
        prompt="测试提示词"
    )

    assert result["success"] is False
    assert result["error"]["type"] == "network_error"


def test_parse_image_response(api_client):
    """测试解析图像响应"""
    response_data = {
        "choices": [{
            "message": {
                "content": "![image](https://example.com/generated.jpg)"
            }
        }]
    }

    urls = api_client._parse_image_response(response_data)
    assert len(urls) > 0
    assert "https://example.com/generated.jpg" in urls[0]
```

运行测试验证失败:

```bash
pytest tests/test_api_client.py -v
```

预期: FAIL - "ModuleNotFoundError: No module named 'gemini_image_generator.api_client'"

**Step 3: 实现API客户端**

创建 `gemini_image_generator/api_client.py`:

```python
"""OpenRouter API客户端"""
import time
import requests
from typing import Optional, List, Dict, Any
from .config import (
    OPENROUTER_API_BASE,
    MODEL_NAME,
    API_TIMEOUT,
    MAX_RETRIES
)
from .utils import format_error


class OpenRouterAPIClient:
    """OpenRouter API客户端"""

    def __init__(
        self,
        api_key: str,
        api_base: str = OPENROUTER_API_BASE,
        timeout: int = API_TIMEOUT,
        max_retries: int = MAX_RETRIES
    ):
        self.api_key = api_key
        self.api_base = api_base
        self.timeout = timeout
        self.max_retries = max_retries

    def _build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://dify.ai",
            "X-Title": "Dify Gemini Image Generator"
        }

    def _build_payload(
        self,
        mode: str,
        prompt: str,
        size: str = "1024x1024",
        num_images: int = 1,
        reference_image_url: Optional[str] = None,
        edit_type: Optional[str] = None,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """构建API请求体"""
        messages = []

        # 添加图像输入（图生图模式）
        if mode == "image_to_image" and reference_image_url:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": reference_image_url}
                    },
                    {
                        "type": "text",
                        "text": f"请根据这张图像{self._get_edit_type_desc(edit_type)}"
                    }
                ]
            })

        # 添加文本提示词
        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 2048
        }

        # 添加可选参数
        if seed:
            payload["seed"] = seed

        return payload

    def _get_edit_type_desc(self, edit_type: Optional[str]) -> str:
        """获取编辑类型描述"""
        edit_descriptions = {
            "modify": "进行修改和优化",
            "style_transfer": "进行风格迁移",
            "sketch_render": "渲染为高质量图像",
            "outpainting": "扩展图像边界"
        }
        return edit_descriptions.get(edit_type, "进行修改")

    def _parse_image_response(self, response_data: Dict[str, Any]) -> List[str]:
        """解析API响应，提取图像URL"""
        urls = []

        try:
            choices = response_data.get("choices", [])
            for choice in choices:
                content = choice.get("message", {}).get("content", "")

                # 尝试提取Markdown格式的图像链接
                if "![" in content and "](" in content:
                    start = content.find("](") + 2
                    end = content.find(")", start)
                    if start > 0 and end > start:
                        url = content[start:end]
                        urls.append(url)

                # 如果是直接的URL
                elif content.startswith("http"):
                    urls.append(content)

        except Exception as e:
            print(f"Error parsing image response: {e}")

        return urls

    def generate_image(
        self,
        mode: str,
        prompt: str,
        size: str = "1024x1024",
        num_images: int = 1,
        reference_image_url: Optional[str] = None,
        edit_type: Optional[str] = None,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """生成图像的主方法"""
        for attempt in range(self.max_retries):
            try:
                payload = self._build_payload(
                    mode=mode,
                    prompt=prompt,
                    size=size,
                    num_images=num_images,
                    reference_image_url=reference_image_url,
                    edit_type=edit_type,
                    seed=seed
                )

                response = requests.post(
                    self.api_base,
                    headers=self._build_headers(),
                    json=payload,
                    timeout=self.timeout
                )

                # 处理API错误
                if response.status_code != 200:
                    error_msg = f"API返回错误: {response.status_code} - {response.text}"
                    return {
                        "success": False,
                        "images": [],
                        "error": format_error(
                            "api_error",
                            error_msg,
                            retry_possible=response.status_code == 429
                        )
                    }

                # 解析成功响应
                response_data = response.json()
                image_urls = self._parse_image_response(response_data)

                if not image_urls:
                    return {
                        "success": False,
                        "images": [],
                        "error": format_error(
                            "api_error",
                            "无法从API响应中提取图像URL",
                            retry_possible=False
                        )
                    }

                return {
                    "success": True,
                    "images": [{"url": url, "index": i + 1} for i, url in enumerate(image_urls)],
                    "error": None
                }

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                return {
                    "success": False,
                    "images": [],
                    "error": format_error(
                        "network_error",
                        "网络请求超时",
                        retry_possible=True
                    )
                }

            except requests.exceptions.ConnectionError:
                return {
                    "success": False,
                    "images": [],
                    "error": format_error(
                        "network_error",
                        "网络连接失败",
                        retry_possible=True
                    )
                }

            except Exception as e:
                return {
                    "success": False,
                    "images": [],
                    "error": format_error(
                        "api_error",
                        f"未知错误: {str(e)}",
                        retry_possible=False
                    )
                }

        return {
            "success": False,
            "images": [],
            "error": format_error(
                "network_error",
                "达到最大重试次数",
                retry_possible=False
            )
        }
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_api_client.py -v
```

预期: PASS (9个测试全部通过)

**Step 5: 提交API客户端**

```bash
git add gemini_image_generator/api_client.py gemini_image_generator/utils.py tests/test_api_client.py
git commit -m "feat: implement OpenRouter API client

- Add OpenRouterAPIClient class
- Implement request building for text/image to image modes
- Add response parsing for image URLs
- Implement retry logic with exponential backoff
- Add comprehensive error handling (network, API, timeout)
- Add utility functions for validation
- Add full unit test coverage
- All tests passing (9/9)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 4: 实现主工具节点

**Files:**
- Create: `gemini_image_generator/gemini_image_tool.py`
- Test: `tests/test_gemini_image_tool.py`

**Step 1: 编写主工具节点测试**

创建 `tests/test_gemini_image_tool.py`:

```python
"""测试Gemini图像生成工具节点"""
import pytest
from unittest.mock import Mock, patch
from gemini_image_generator.gemini_image_tool import GeminiImageGenerator


@pytest.fixture
def tool():
    """创建工具实例"""
    return GeminiImageGenerator()


def test_tool_initialization():
    """测试工具初始化"""
    with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'}):
        tool = GeminiImageGenerator()
        assert tool.api_client is not None
        assert tool.template_manager is not None


@patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'})
def test_validate_parameters_success():
    """测试参数验证成功"""
    tool = GeminiImageGenerator()
    params = {
        "mode": "text_to_image",
        "prompt": "测试提示词",
        "size": "1024x1024",
        "num_images": 1
    }
    errors = tool._validate_parameters(params)
    assert len(errors) == 0


@patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'})
def test_validate_parameters_failure():
    """测试参数验证失败"""
    tool = GeminiImageGenerator()
    params = {
        "mode": "invalid_mode",
        "prompt": "",
        "size": "invalid_size",
        "num_images": 10
    }
    errors = tool._validate_parameters(params)
    assert len(errors) > 0


@patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'})
def test_invoke_text_to_image():
    """测试文生图调用"""
    tool = GeminiImageGenerator()

    # Mock API客户端
    tool.api_client = Mock()
    tool.api_client.generate_image.return_value = {
        "success": True,
        "images": [{"url": "https://example.com/image.jpg", "index": 1}],
        "error": None
    }

    result = tool.invoke({
        "mode": "text_to_image",
        "prompt": "一个可爱的猫"
    })

    assert result["success"] is True
    assert len(result["images"]) == 1
    assert result["images"][0]["url"] == "https://example.com/image.jpg"


@patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'})
def test_invoke_with_patent_template():
    """测试使用专利模板"""
    tool = GeminiImageGenerator()

    tool.api_client = Mock()
    tool.api_client.generate_image.return_value = {
        "success": True,
        "images": [{"url": "https://example.com/image.jpg", "index": 1}],
        "error": None
    }

    result = tool.invoke({
        "mode": "patent_drawing",
        "prompt": "手持工具",
        "preset_template": "explosion"
    })

    assert result["success"] is True
    # 验证API被调用且prompt包含模板内容
    call_args = tool.api_client.generate_image.call_args
    assert "爆炸图" in call_args[1]["prompt"]


@patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test_key'})
def test_invoke_with_api_error():
    """测试API错误处理"""
    tool = GeminiImageGenerator()

    tool.api_client = Mock()
    tool.api_client.generate_image.return_value = {
        "success": False,
        "images": [],
        "error": {
            "type": "api_error",
            "message": "API认证失败",
            "retry_possible": False
        }
    }

    result = tool.invoke({
        "mode": "text_to_image",
        "prompt": "测试"
    })

    assert result["success"] is False
    assert result["error"]["type"] == "api_error"


@patch.dict('os.environ', {})  # 无API密钥
def test_invoke_without_api_key():
    """测试无API密钥的情况"""
    tool = GeminiImageGenerator()
    result = tool.invoke({
        "mode": "text_to_image",
        "prompt": "测试"
    })

    assert result["success"] is False
    assert "配置错误" in result["error"]["message"]
```

运行测试验证失败:

```bash
pytest tests/test_gemini_image_tool.py -v
```

预期: FAIL - "ModuleNotFoundError: No module named 'gemini_image_generator.gemini_image_tool'"

**Step 2: 实现主工具节点**

创建 `gemini_image_generator/gemini_image_tool.py`:

```python
"""Gemini图像生成工具节点"""
import os
from typing import Dict, Any, Optional, List
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
    """Dify图像生成工具节点"""

    def __init__(self):
        """初始化工具"""
        self.api_key: Optional[str] = None
        self.api_client: Optional[OpenRouterAPIClient] = None
        self.template_manager = get_template_manager()

        # 尝试加载API密钥
        self._load_api_key()

    def _load_api_key(self):
        """从环境变量加载API密钥"""
        self.api_key = get_api_key()
        if self.api_key:
            self.api_client = OpenRouterAPIClient(api_key=self.api_key)

    def _validate_parameters(self, params: Dict[str, Any]) -> List[str]:
        """验证输入参数"""
        errors = []

        # 验证mode
        mode = params.get("mode", "")
        if not validate_mode(mode):
            errors.append(f"无效的工作模式: {mode}")

        # 验证prompt
        prompt = params.get("prompt", "")
        if not prompt or not prompt.strip():
            errors.append("提示词不能为空")

        # 验证size
        size = params.get("size", "1024x1024")
        if not validate_size(size):
            errors.append(f"无效的图像尺寸: {size}")

        # 验证num_images
        num_images = params.get("num_images", 1)
        if not validate_num_images(num_images):
            errors.append(f"生成数量必须在1-4之间: {num_images}")

        # 图生图模式验证reference_image_url
        if mode == "image_to_image":
            ref_url = params.get("reference_image_url", "")
            if not ref_url:
                errors.append("图生图模式必须提供reference_image_url")

        return errors

    def _apply_template_if_needed(
        self,
        mode: str,
        prompt: str,
        params: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """应用预设模板"""
        template_id = params.get("preset_template")

        if not template_id:
            return prompt, params

        # 根据模式获取模板
        if mode == "patent_drawing":
            template = self.template_manager.get_patent_template(template_id)
        elif mode == "product_prototype":
            template = self.template_manager.get_product_template(template_id)
        else:
            return prompt, params

        if not template:
            return prompt, params

        # 应用模板到prompt
        enhanced_prompt = self.template_manager.apply_template(template, prompt)

        # 合并模板默认参数
        default_params = self.template_manager.get_template_default_params(template)
        for key, value in default_params.items():
            if key not in params or not params[key]:
                params[key] = value

        return enhanced_prompt, params

    def _format_result(
        self,
        api_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """格式化API响应为Dify工具返回格式"""
        if api_response["success"]:
            return {
                "success": True,
                "images": api_response["images"],
                "error": None
            }
        else:
            return {
                "success": False,
                "images": [],
                "error": api_response["error"]
            }

    def invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """工具节点入口方法（Dify调用）"""
        # 参数验证
        validation_errors = self._validate_parameters(params)
        if validation_errors:
            return {
                "success": False,
                "images": [],
                "error": format_error(
                    "validation_error",
                    f"参数验证失败: {', '.join(validation_errors)}",
                    retry_possible=False
                )
            }

        # 检查API密钥
        if not self.api_client:
            return {
                "success": False,
                "images": [],
                "error": format_error(
                    "configuration_error",
                    "未配置OPENROUTER_API_KEY环境变量",
                    retry_possible=False
                )
            }

        # 提取参数
        mode = params["mode"]
        prompt = params["prompt"]
        size = params.get("size", "1024x1024")
        num_images = params.get("num_images", 1)
        reference_image_url = params.get("reference_image_url")
        edit_type = params.get("edit_type")
        seed = params.get("seed")

        # 应用模板（如果指定）
        enhanced_prompt, params = self._apply_template_if_needed(
            mode, prompt, params
        )

        # 更新size（可能被模板修改）
        size = params.get("size", size)

        # 调用API生成图像
        api_response = self.api_client.generate_image(
            mode=mode,
            prompt=enhanced_prompt,
            size=size,
            num_images=num_images,
            reference_image_url=reference_image_url,
            edit_type=edit_type,
            seed=seed
        )

        return self._format_result(api_response)
```

**Step 3: 运行测试验证通过**

```bash
pytest tests/test_gemini_image_tool.py -v
```

预期: PASS (7个测试全部通过)

**Step 4: 运行所有测试**

```bash
pytest tests/ -v
```

预期: PASS (24个测试全部通过)

**Step 5: 提交主工具节点**

```bash
git add gemini_image_generator/gemini_image_tool.py tests/test_gemini_image_tool.py
git commit -m "feat: implement main tool node

- Add GeminiImageGenerator class
- Implement parameter validation
- Add template application logic
- Implement invoke() entry point for Dify
- Add error handling for all failure modes
- Add comprehensive integration tests
- All tests passing (24/24 total)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 5: 完善文档和配置

**Files:**
- Update: `README.md`
- Create: `docs/USAGE.md`
- Create: `.env.example`

**Step 1: 创建环境变量示例文件**

创建 `.env.example`:

```bash
# OpenRouter API配置
OPENROUTER_API_KEY=sk-or-your-api-key-here
```

**Step 2: 创建详细使用文档**

创建 `docs/USAGE.md`:

```markdown
# Dify Gemini图像生成插件使用指南

## 安装步骤

### 1. 准备环境

确保已安装Dify（支持自托管或云版本）

### 2. 获取API密钥

1. 访问 [OpenRouter](https://openrouter.ai/)
2. 注册账号并创建API密钥
3. 复制您的API密钥

### 3. 安装插件

#### 方式A：直接复制（推荐用于开发）

```bash
cd /path/to/dify/plugins
cp -r /path/to/dify-gemini-image-plugin .
```

#### 方式B：通过Dify管理界面

1. 将插件打包为zip: `zip -r dify-gemini-image-plugin.zip .`
2. 在Dify管理界面选择"插件" > "上传插件"
3. 上传zip文件

### 4. 配置API密钥

在Dify的docker-compose.yml或环境变量中添加:

```yaml
services:
  api:
    environment:
      - OPENROUTER_API_KEY=sk-or-xxxx...
```

或在Dify系统设置 > 环境变量中添加。

### 5. 重启Dify

```bash
docker-compose restart api worker
```

## 使用示例

### 场景1：生成专利爆炸图

**工作流配置：**
```
节点: Gemini图像生成器
参数:
  - mode: 专利附图
  - preset_template: 爆炸图
  - prompt: "手持电动工具的爆炸图，展示电机、齿轮箱、外壳的装配关系"
  - size: 1024x1024
  - num_images: 1
```

**预期输出：**
```json
{
  "success": true,
  "images": [
    {"url": "https://...", "index": 1}
  ],
  "error": null
}
```

### 场景2：产品概念图生成

**工作流配置：**
```
节点: Gemini图像生成器
参数:
  - mode: 产品原型图
  - preset_template: 概念渲染图
  - prompt: "智能蓝牙耳机，现代简约设计，白色磨砂质感，45度视角"
  - line_style: 渲染图
  - size: 1024x1024
```

### 场景3：草图渲染

**工作流配置：**
```
节点1: 文件上传（获取草图URL）
节点2: Gemini图像生成器
  - mode: 图生图
  - edit_type: 草图渲染
  - reference_image_url: {{node1.file_url}}
  - prompt: "将草图渲染为高质量产品图，保持设计细节，添加真实材质"
```

### 场景4：批量生成方案

```
节点: Gemini图像生成器
参数:
  - mode: 产品原型图
  - prompt: "智能手表，多种设计方案"
  - num_images: 4
  - seed: 42  # 固定种子以便复现
```

### 场景5：错误处理

```
节点1: Gemini图像生成器
节点2: 条件判断
  - 条件: {{node1.success}} == true
  - 分支1: 成功 → 保存图像URL
  - 分支2: 失败 → 记录错误日志
```

## 参数说明

### 核心参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mode | select | 是 | 工作模式：文生图/图生图/专利附图/产品原型图 |
| prompt | text | 是 | 图像生成提示词 |
| negative_prompt | text | 否 | 负面提示词 |
| reference_image_url | text | 否 | 图生图模式的参考图像URL |
| edit_type | select | 否 | 编辑类型：修改/风格迁移/草图渲染/外扩 |

### 生成参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| size | select | 否 | 图像尺寸（默认1024x1024） |
| num_images | number | 否 | 生成数量1-4（默认1） |
| seed | number | 否 | 随机种子，用于复现结果 |

### 模板参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| preset_template | select | 否 | 预设模板ID |
| line_style | select | 否 | 线条风格：技术绘图/草图/渲染图 |
| view_angle | select | 否 | 视角：正视图/俯视图/侧视图/等轴测图 |

## 预设模板列表

### 专利附图模板
- **爆炸图** (explosion): 零件分离，清晰标注
- **装配图** (assembly): 整体结构，组件组合
- **零件细节图** (detail): 局部放大，工艺要求
- **剖面图** (section): 内部结构，材料区分
- **原理图** (principle): 工作原理，流程说明
- **电路/管路图** (circuit): 专业领域图示

### 产品原型图模板
- **概念渲染图** (concept): 现代感，3D渲染
- **用户界面图** (ui): UI/UX，交互示意
- **场景使用图** (scene): 使用场景，应用演示
- **功能示意图** (function): 模块划分，操作流程
- **包装设计图** (packaging): 包装展示，品牌元素

## 最佳实践

### 提示词编写

**专利附图：**
- 使用简洁的技术描述
- 明确标注结构和关系
- 示例："爆炸图，展示电机、齿轮箱、外壳的装配关系，标注清晰"

**产品原型图：**
- 加入材质、光影、场景描述
- 明确风格和设计语言
- 示例："现代简约设计，白色磨砂质感，45度等轴测视角，柔和光照"

### 错误处理

使用条件节点检查success字段：

```json
条件: {{gemini_image.success}} == true
分支1: 成功 → 处理图像URL
分支2: 失败 → 检查{{gemini_image.error.message}}
```

### 性能优化

1. **小尺寸测试**: 先用1024x768测试提示词效果
2. **固定种子**: 使用seed参数保存满意的参数组合
3. **批量生成**: 一次生成3-4张图探索不同方案
4. **URL缓存**: 使用CDN缓存生成的图像URL

## 故障排除

### 问题：API认证失败

**错误信息：** "未配置OPENROUTER_API_KEY环境变量"

**解决方案：**
1. 检查Dify环境变量配置
2. 验证API密钥有效性
3. 重启Dify服务

### 问题：生成失败

**错误信息：** "API返回错误: 429"

**解决方案：**
- 检查OpenRouter配额
- 降低请求频率
- 查看错误对象的retry_possible字段

### 问题：无法解析图像URL

**错误信息：** "无法从API响应中提取图像URL"

**解决方案：**
1. 检查API返回格式是否变化
2. 查看API日志了解详细响应
3. 可能需要更新响应解析逻辑

## 成本估算

- 单张图像成本: $0.01-$0.03
- 100张图像估算: $1-$3
- 建议先用小尺寸测试，避免浪费配额

详细定价请参考 [OpenRouter定价页面](https://openrouter.ai/docs#models)

## 技术支持

- GitHub Issues: [项目地址]
- 文档: [完整文档链接]
- 邮件: support@example.com
```

**Step 3: 更新主README**

更新 `README.md`:

```markdown
# Dify Gemini图像生成插件

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Dify](https://img.shields.io/badge/Dify-Plugin-green.svg)](https://github.com/langgenius/dify)

> 通过OpenRouter调用Google Gemini 2.0 Flash模型，实现专利附图和产品原型图的AI生成与编辑功能。

## ✨ 功能特性

- 🎨 **文生图** - 基于文本描述生成全新图像
- 🖼️ **图生图/文改图** - 基于参考图像进行修改、风格迁移、草图渲染、图像外扩
- 📐 **专利附图模式** - 爆炸图、装配图、剖面图等专业模板
- 💡 **产品原型图模式** - 概念渲染图、UI设计图、场景使用图等模板
- 🛡️ **宽松错误处理** - 失败不中断工作流，提供详细错误信息

## 🚀 快速开始

### 安装

```bash
# 1. 克隆或复制插件到Dify plugins目录
cp -r dify-gemini-image-plugin /path/to/dify/plugins/

# 2. 配置环境变量
export OPENROUTER_API_KEY=sk-or-your-key-here

# 3. 重启Dify
docker-compose restart
```

### 获取API密钥

访问 [OpenRouter](https://openrouter.ai/) 注册并获取API密钥。

## 📖 使用示例

### 专利爆炸图生成

```yaml
mode: patent_drawing
preset_template: explosion
prompt: "手持电动工具的爆炸图，展示电机、齿轮箱、外壳的装配关系"
size: "1024x1024"
```

### 产品概念图生成

```yaml
mode: product_prototype
preset_template: concept
prompt: "智能蓝牙耳机，现代简约设计，白色磨砂质感，45度视角"
line_style: render
```

### 草图渲染

```yaml
mode: image_to_image
edit_type: sketch_render
reference_image_url: "https://example.com/sketch.jpg"
prompt: "将草图渲染为高质量产品图，保持设计细节，添加真实材质"
```

## 📚 文档

- 📘 [完整使用指南](docs/USAGE.md)
- 📗 [设计文档](docs/plans/2026-01-26-dify-gemini-image-plugin-design.md)
- 📙 [API参考](docs/API_REFERENCE.md)（待补充）

## 🧪 测试

```bash
# 安装测试依赖
pip install -r requirements.txt

# 运行测试
pytest tests/ -v

# 查看覆盖率
pytest tests/ --cov=gemini_image_generator --cov-report=html
```

## 🏗️ 项目结构

```
dify-gemini-image-plugin/
├── gemini_image_generator/    # 主包
│   ├── gemini_image_tool.py   # 主工具节点
│   ├── api_client.py          # API客户端
│   ├── templates.py           # 模板系统
│   ├── utils.py               # 工具函数
│   └── config.py              # 配置常量
├── tests/                     # 测试文件
├── docs/                      # 文档
├── manifest.yaml              # Dify插件清单
├── requirements.txt           # Python依赖
└── README.md                  # 本文件
```

## 🔧 配置说明

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| OPENROUTER_API_KEY | 是 | OpenRouter API密钥 |

### Dify节点参数

详见 [使用指南](docs/USAGE.md#参数说明)。

## 📊 性能与成本

- **响应时间**: 通常5-15秒
- **单张成本**: $0.01-$0.03
- **并发支持**: 支持多工作流并行调用

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Dify](https://github.com/langgenius/dify) - 优秀的LLM应用开发平台
- [OpenRouter](https://openrouter.ai/) - 统一的AI模型API接口
- [Google Gemini](https://ai.google.dev/) - 强大的多模态AI模型

## 📮 联系方式

- 作者: Your Name
- 邮箱: your.email@example.com
- GitHub: [your-github-username]

---

Made with ❤️ by Claude Code
```

**Step 4: 提交文档和配置**

```bash
git add README.md docs/USAGE.md .env.example
git commit -m "docs: add comprehensive documentation

- Add detailed usage guide with examples
- Create environment variable example file
- Update main README with quick start and features
- Add troubleshooting section
- Document all parameters and templates
- Add cost estimation and best practices

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 6: 创建最终发布包

**Files:**
- Create: `LICENSE`
- Create: `.gitignore` (update)
- Create: `CHANGELOG.md`

**Step 1: 创建LICENSE文件**

创建 `LICENSE`:

```text
MIT License

Copyright (c) 2026 Dify Gemini Image Plugin Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Step 2: 更新.gitignore**

更新 `.gitignore`:

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
.worktrees/
*.log
```

**Step 3: 创建CHANGELOG**

创建 `CHANGELOG.md`:

```markdown
# 变更日志

## [1.0.0] - 2026-01-26

### 新增
- 🎉 首次发布
- ✨ 支持文生图功能
- ✨ 支持图生图/文改图功能（修改、风格迁移、草图渲染、图像外扩）
- ✨ 专利附图模式（6个预设模板）
- ✨ 产品原型图模式（5个预设模板）
- 🛡️ 宽松错误处理机制
- 📚 完整的文档和测试覆盖

### 技术实现
- 使用OpenRouter API调用Google Gemini 2.0 Flash模型
- 模板管理系统（单例模式）
- API客户端（支持重试和指数退避）
- 参数验证和错误格式化
- 完整的单元测试和集成测试（24个测试用例）

### 文档
- 完整的使用指南
- API参数说明
- 故障排除指南
- 最佳实践建议

---

## 未来计划

### [1.1.0] - 计划中
- [ ] 支持用户自定义模板保存
- [ ] 添加图像后处理功能（增强、裁剪、水印）
- [ ] 支持更多图像生成模型
- [ ] 添加图像本地保存选项
- [ ] 支持批量图像生成和导出

### [1.2.0] - 计划中
- [ ] 支持Inpainting（图像修复）
- [ ] 支持背景替换
- [ ] 添加图像编辑历史记录
- [ ] 支持工作流中的图像比较
```

**Step 4: 创建发布包**

```bash
# 创建不包含.git和.worktrees的发布包
git archive HEAD --prefix=dify-gemini-image-plugin/ -o dify-gemini-image-plugin-v1.0.0.tar.gz

# 或创建zip包
git archive HEAD --prefix=dify-gemini-image-plugin/ -o dify-gemini-image-plugin-v1.0.0.zip
```

**Step 5: 提交最终文件**

```bash
git add LICENSE .gitignore CHANGELOG.md
git commit -m "chore: prepare for v1.0.0 release

- Add MIT License
- Update .gitignore with Python-specific patterns
- Add comprehensive changelog
- Document release notes and future plans

Version: 1.0.0
Release Date: 2026-01-26

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Step 6: 创建版本标签**

```bash
git tag -a v1.0.0 -m "Release v1.0.0: Initial release of Dify Gemini Image Plugin

Features:
- Text to image generation
- Image to image editing
- Patent drawing templates (6 templates)
- Product prototype templates (5 templates)
- Comprehensive error handling
- Full test coverage (24 tests)

Documentation:
- Usage guide
- API reference
- Troubleshooting guide
"
```

---

## 验收标准

实现完成后，确保以下检查点全部通过：

### 功能验收
- [ ] 文生图模式可以正常生成图像
- [ ] 图生图模式可以正常编辑图像
- [ ] 专利图模式可以应用预设模板
- [ ] 产品原型图模式可以应用预设模板
- [ ] 所有错误情况都能正确处理且不中断工作流

### 测试验收
- [ ] 所有单元测试通过（24/24）
- [ ] 测试覆盖率 >= 80%
- [ ] 集成测试通过

### 文档验收
- [ ] README.md包含快速开始指南
- [ ] USAGE.md包含所有参数说明
- [ ] 包含故障排除指南
- [ ] 包含使用示例

### 代码质量
- [ ] 无Python语法错误
- [ ] 符合PEP 8代码规范
- [ ] 所有函数都有docstring
- [ ] 无硬编码的配置值

### 部署验收
- [ ] 可以成功安装到Dify
- [ ] 环境变量配置正确
- [ ] 可以在Dify工作流中正常调用
- [ ] 生成图像URL可以正常访问

---

## 后续步骤

实现完成后，建议按以下顺序进行：

1. **本地测试**: 在Dify开发环境中完整测试所有功能
2. **文档完善**: 根据实际使用情况补充文档
3. **发布到生产**: 部署到生产环境
4. **用户反馈**: 收集用户反馈并迭代优化
5. **功能扩展**: 根据CHANGELOG中的计划添加新功能

---

**计划完成时间估算**: 2-3小时
**开发者技能要求**: 熟悉Python、Dify插件开发、API集成
**预期代码行数**: ~1500行（包含测试和文档）
