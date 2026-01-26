# Dify Gemini Image Generator Plugin

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Dify](https://img.shields.io/badge/Dify-Compatible-orange.svg)

一个基于 Google Gemini 2.0 Flash 模型的强大图像生成插件，通过 OpenRouter API 调用，集成到 Dify 工作流中。

A powerful image generation plugin using Google's Gemini 2.0 Flash model via OpenRouter API, integrated into Dify workflows.

[English](#english) | [中文](#中文)

</div>

---

## 中文

## 功能特性

### 核心功能

- **文生图** 🎨
  - 从文本描述生成高质量图像
  - 支持创意设计和商业应用
  - 可调节创造性和多样性

- **图生图/文改图** 🖼️
  - 基于参考图像进行修改和编辑
  - 支持风格迁移、草图渲染、图像外扩
  - 保持原图结构的同时应用新风格

- **专利附图** 📐
  - 生成技术性专利附图
  - 多种线条风格（技术绘图、草图、渲染图）
  - 多种视角（正视图、俯视图、侧视图、等轴测图）
  - 自动标注和编号支持

- **产品原型图** 📦
  - 创建产品概念原型
  - 适用于工业设计和产品展示
  - 支持多视角批量生成

### 高级特性

- **灵活的参数配置** ⚙️
  - 5种图像尺寸：1024x1024, 1024x768, 768x1024, 832x1216, 1216x832
  - 生成数量：1-4张
  - 负面提示词支持
  - 温度控制 (0.0-1.0)
  - 顶级采样 (Top-P: 0.0-1.0)

- **智能重试机制** 🔄
  - 自动重试失败的请求（最多3次）
  - 网络超时保护
  - 详细的错误信息返回

- **高质量输出** ✨
  - 使用 Google Gemini 2.0 Flash 最新的图像生成模型
  - 支持 8K 级别的高分辨率图像
  - 专业级的产品摄影效果

## 快速开始 (Quick Start)

### 前置要求

- Python 3.8+
- Dify Platform（本地或云端）
- OpenRouter API Key（[获取指南](https://openrouter.ai/））

### 安装步骤

#### 1. 克隆插件

```bash
cd /path/to/dify/data/plugins
git clone https://github.com/yourusername/dify-gemini-image-plugin.git
cd dify-gemini-image-plugin
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# OPENROUTER_API_KEY=sk-or-your-actual-api-key-here
```

或在 Dify 的系统设置中添加环境变量 `OPENROUTER_API_KEY`。

#### 4. 重启 Dify 服务

```bash
# Docker 部署
docker-compose restart

# 本地部署
pkill -f dify && ./start.sh
```

#### 5. 验证安装

登录 Dify，创建新工作流，在工具列表中查找 "Gemini Image Generator"。

## 使用方法

### 基础用法

在 Dify 工作流中：

1. **添加节点**：在工具列表中找到 "Gemini Image Generator" 并拖入画布
2. **配置参数**：根据需求选择工作模式和参数
3. **运行工作流**：执行工作流生成图像

### 使用示例

#### 示例 1：文生图 - 产品摄影

```json
{
  "mode": "text_to_image",
  "prompt": "高端蓝牙耳机，放在大理石桌面上，柔和窗光，产品摄影风格",
  "size": "1024x1024",
  "n": 1,
  "temperature": 0.7
}
```

#### 示例 2：专利附图 - 机械装置

```json
{
  "mode": "patent_drawing",
  "prompt": "齿轮传动系统，包括输入轴、输出轴和离合器机构",
  "line_style": "technical",
  "view_angle": "isometric",
  "size": "1024x1024",
  "auto_label": true
}
```

#### 示例 3：产品原型 - 智能手表

```json
{
  "mode": "product_prototype",
  "prompt": "智能手表，方形表盘，金属边框，真皮表带",
  "line_style": "render",
  "view_angle": "front",
  "size": "1024x1024",
  "n": 2
}
```

#### 示例 4：图生图 - 风格迁移

```json
{
  "mode": "image_to_image",
  "edit_type": "style_transfer",
  "reference_image": "https://example.com/original.jpg",
  "prompt": "将这张照片转换为印象派油画风格",
  "size": "1024x1024"
}
```

### 核心参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `mode` | 工作模式：text_to_image, image_to_image, patent_drawing, product_prototype | 必填 |
| `prompt` | 图像生成提示词 | 必填 |
| `size` | 图像尺寸：1024x1024, 1024x768, 768x1024, 832x1216, 1216x832 | 1024x1024 |
| `n` | 生成数量 (1-4) | 1 |
| `temperature` | 创造性 (0.0-1.0) | 0.7 |
| `negative_prompt` | 负面提示词 | 无 |

## 文档

详细使用指南请查看：[docs/USAGE.md](docs/USAGE.md)

包含内容：
- 完整安装指南
- 5种使用场景详解
- 所有参数说明
- 预设模板列表
- 最佳实践
- 故障排除
- 成本估算

## 测试

运行测试套件：

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_gemini_tool.py

# 查看测试覆盖率
pytest --cov=gemini_image_generator tests/
```

## 项目结构

```
dify-gemini-image-plugin/
├── gemini_image_generator/    # 主要代码
│   ├── __init__.py           # 包初始化
│   ├── config.py             # 配置常量
│   ├── gemini_image_tool.py  # 核心工具实现
│   └── utils.py              # 工具函数
├── tests/                     # 测试套件
│   ├── __init__.py
│   └── test_gemini_tool.py   # 单元测试
├── docs/                      # 文档
│   └── USAGE.md              # 详细使用指南
├── manifest.yaml              # Dify 插件清单
├── requirements.txt           # Python 依赖
├── .env.example              # 环境变量模板
├── README.md                 # 项目说明
└── .gitignore
```

## 配置

### 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API 密钥 | `sk-or-v1-xxxxx` |

### Dify 集成配置

在 `manifest.yaml` 中配置插件元数据：

```yaml
version: 1.0.0
author: Your Name
name: gemini_image_generator
label:
  en_US: Gemini Image Generator
  zh_Hans: Gemini 图像生成器
description:
  en_US: Generate images using Google Gemini 2.0 Flash
  zh_Hans: 使用 Google Gemini 2.0 Flash 生成图像
```

## 性能与成本

### 生成速度

- 单张图像：5-15 秒
- 批量生成（4张）：15-45 秒
- 专利附图：8-20 秒

### 成本估算

基于 OpenRouter 定价（2026-01）：

| 图像尺寸 | 单张成本 |
|----------|----------|
| 1024x1024 | $0.015 |
| 1024x768 | $0.012 |
| 768x1024 | $0.012 |
| 832x1216 | $0.015 |
| 1216x832 | $0.015 |

**示例：** 生成 100 张产品图（1024x768）约 $1.20

详细成本分析请查看：[docs/USAGE.md#成本估算](docs/USAGE.md#成本估算)

## 技术细节

### API 端点

- **OpenRouter API:** `https://openrouter.ai/api/v1/chat/completions`
- **模型:** `google/gemini-2.0-flash-exp-image-generation`

### 错误处理

- API 密钥验证
- 网络超时重试（最多3次）
- 参数验证
- 详细的错误信息返回
- 部分失败处理

### 性能优化

- 请求超时：30秒
- 自动重试机制
- 连接池复用
- 响应缓存支持（可选）

更多问题请查看：[docs/USAGE.md#故障排除](docs/USAGE.md#故障排除)

## 贡献

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 致谢

- [Dify](https://github.com/langgenius/dify) - 强大的 LLM 应用开发平台
- [OpenRouter](https://openrouter.ai/) - 统一的 AI API 接口
- [Google Gemini](https://ai.google.dev/) - 先进的图像生成模型

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- GitHub Issues: [提交问题](https://github.com/yourusername/dify-gemini-image-plugin/issues)
- Email: your-email@example.com

---

## English

## Features

### Core Functions

- **Text-to-Image** 🎨
  - Generate high-quality images from text descriptions
  - Support for creative design and commercial applications
  - Adjustable creativity and diversity

- **Image-to-Image** 🖼️
  - Modify and edit based on reference images
  - Support for style transfer, sketch rendering, outpainting
  - Maintain original structure while applying new styles

- **Patent Drawing** 📐
  - Generate technical patent drawings
  - Multiple line styles (technical, sketch, render)
  - Multiple viewing angles (front, top, side, isometric)
  - Auto-labeling and numbering support

- **Product Prototype** 📦
  - Create product concept prototypes
  - Suitable for industrial design and product presentation
  - Multi-angle batch generation

### Advanced Features

- **Flexible Parameter Configuration** ⚙️
  - 5 image sizes: 1024x1024, 1024x768, 768x1024, 832x1216, 1216x832
  - Generation count: 1-4 images
  - Negative prompt support
  - Temperature control (0.0-1.0)
  - Top-P sampling (0.0-1.0)

- **Smart Retry Mechanism** 🔄
  - Auto-retry failed requests (up to 3 times)
  - Network timeout protection
  - Detailed error message returns

- **High-Quality Output** ✨
  - Using Google Gemini 2.0 Flash latest image generation model
  - Support 8K level high-resolution images
  - Professional product photography effects

## Quick Start

### Prerequisites

- Python 3.8+
- Dify Platform (local or cloud)
- OpenRouter API Key ([Get Guide](https://openrouter.ai/))

### Installation Steps

#### 1. Clone Plugin

```bash
cd /path/to/dify/data/plugins
git clone https://github.com/yourusername/dify-gemini-image-plugin.git
cd dify-gemini-image-plugin
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure API Key

```bash
# Copy environment variable template
cp .env.example .env

# Edit .env file, add your API Key
# OPENROUTER_API_KEY=sk-or-your-actual-api-key-here
```

Or add environment variable `OPENROUTER_API_KEY` in Dify system settings.

#### 4. Restart Dify Service

```bash
# Docker deployment
docker-compose restart

# Local deployment
pkill -f dify && ./start.sh
```

#### 5. Verify Installation

Login to Dify, create new workflow, find "Gemini Image Generator" in tool list.

## Usage

### Basic Usage

In Dify workflow:

1. **Add Node**: Find "Gemini Image Generator" in tool list and drag to canvas
2. **Configure Parameters**: Select work mode and parameters as needed
3. **Run Workflow**: Execute workflow to generate images

### Usage Examples

#### Example 1: Text-to-Image - Product Photography

```json
{
  "mode": "text_to_image",
  "prompt": "Premium Bluetooth headphones on marble table, soft window light, product photography style",
  "size": "1024x1024",
  "n": 1,
  "temperature": 0.7
}
```

#### Example 2: Patent Drawing - Mechanical Device

```json
{
  "mode": "patent_drawing",
  "prompt": "Gear transmission system with input shaft, output shaft and clutch mechanism",
  "line_style": "technical",
  "view_angle": "isometric",
  "size": "1024x1024",
  "auto_label": true
}
```

#### Example 3: Product Prototype - Smart Watch

```json
{
  "mode": "product_prototype",
  "prompt": "Smart watch with square dial, metal bezel, leather strap",
  "line_style": "render",
  "view_angle": "front",
  "size": "1024x1024",
  "n": 2
}
```

#### Example 4: Image-to-Image - Style Transfer

```json
{
  "mode": "image_to_image",
  "edit_type": "style_transfer",
  "reference_image": "https://example.com/original.jpg",
  "prompt": "Convert this photo to impressionist oil painting style",
  "size": "1024x1024"
}
```

### Core Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mode` | Work mode: text_to_image, image_to_image, patent_drawing, product_prototype | Required |
| `prompt` | Image generation prompt | Required |
| `size` | Image size: 1024x1024, 1024x768, 768x1024, 832x1216, 1216x832 | 1024x1024 |
| `n` | Generation count (1-4) | 1 |
| `temperature` | Creativity (0.0-1.0) | 0.7 |
| `negative_prompt` | Negative prompt | None |

## Documentation

For detailed usage guide, see: [docs/USAGE.md](docs/USAGE.md)

Contents:
- Complete installation guide
- 5 usage scenarios explained
- All parameter descriptions
- Preset template lists
- Best practices
- Troubleshooting
- Cost estimation

## Testing

Run test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_gemini_tool.py

# View test coverage
pytest --cov=gemini_image_generator tests/
```

## Project Structure

```
dify-gemini-image-plugin/
├── gemini_image_generator/    # Main code
│   ├── __init__.py           # Package init
│   ├── config.py             # Config constants
│   ├── gemini_image_tool.py  # Core tool implementation
│   └── utils.py              # Utility functions
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_gemini_tool.py   # Unit tests
├── docs/                      # Documentation
│   └── USAGE.md              # Detailed usage guide
├── manifest.yaml              # Dify plugin manifest
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── README.md                 # Project description
└── .gitignore
```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | `sk-or-v1-xxxxx` |

### Dify Integration Config

Configure plugin metadata in `manifest.yaml`:

```yaml
version: 1.0.0
author: Your Name
name: gemini_image_generator
label:
  en_US: Gemini Image Generator
  zh_Hans: Gemini 图像生成器
description:
  en_US: Generate images using Google Gemini 2.0 Flash
  zh_Hans: 使用 Google Gemini 2.0 Flash 生成图像
```

## Performance & Cost

### Generation Speed

- Single image: 5-15 seconds
- Batch generation (4 images): 15-45 seconds
- Patent drawing: 8-20 seconds

### Cost Estimation

Based on OpenRouter pricing (2026-01):

| Image Size | Cost Per Image |
|------------|----------------|
| 1024x1024 | $0.015 |
| 1024x768 | $0.012 |
| 768x1024 | $0.012 |
| 832x1216 | $0.015 |
| 1216x832 | $0.015 |

**Example:** 100 product images (1024x768) costs approximately $1.20

For detailed cost analysis, see: [docs/USAGE.md#成本估算](docs/USAGE.md#成本估算)

## Technical Details

### API Endpoint

- **OpenRouter API:** `https://openrouter.ai/api/v1/chat/completions`
- **Model:** `google/gemini-2.0-flash-exp-image-generation`

### Error Handling

- API key validation
- Network timeout retry (up to 3 times)
- Parameter validation
- Detailed error message returns
- Partial failure handling

### Performance Optimization

- Request timeout: 30 seconds
- Auto-retry mechanism
- Connection pool reuse
- Response cache support (optional)

## FAQ

### Q: How to get OpenRouter API Key?

A: Visit [OpenRouter](https://openrouter.ai/) to register and create API Key.

### Q: What image sizes are supported?

A: Supports 1024x1024, 1024x768, 768x1024, 832x1216, 1216x832.

### Q: How long does it take to generate an image?

A: Typically 5-15 seconds, depending on prompt complexity and network conditions.

### Q: How to improve generation quality?

A:
- Use detailed, specific prompts
- Adjust temperature appropriately (0.7-0.9 usually works well)
- Add negative prompts to exclude unwanted elements
- For professional drawings, use patent drawing mode with appropriate line style

For more questions, see: [docs/USAGE.md#故障排除](docs/USAGE.md#故障排除)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- [Dify](https://github.com/langgenius/dify) - Powerful LLM application development platform
- [OpenRouter](https://openrouter.ai/) - Unified AI API interface
- [Google Gemini](https://ai.google.dev/) - Advanced image generation model

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contact

- GitHub Issues: [Submit Issue](https://github.com/yourusername/dify-gemini-image-plugin/issues)
- Email: your-email@example.com
