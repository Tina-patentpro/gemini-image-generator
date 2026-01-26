# Dify Gemini Image Generator Plugin

一个基于 Google Gemini 2.0 Flash 模型的强大图像生成插件，通过 OpenRouter API 调用，集成到 Dify 工作流中。

A powerful image generation plugin using Google's Gemini 2.0 Flash model via OpenRouter API, integrated into Dify workflows.

## 功能特性 (Features)

- **多种生成模式**
  - 文生图 (Text-to-Image): 从文本描述生成高质量图像
  - 图生图/文改图 (Image-to-Image): 基于参考图像进行修改和编辑
  - 专利附图 (Patent Drawing): 生成技术性专利附图
  - 产品原型图 (Product Prototype): 创建产品概念原型

- **灵活的参数配置**
  - 支持多种图像尺寸 (1024x1024, 1024x768, 768x1024, 832x1216, 1216x832)
  - 可自定义生成数量 (1-4张)
  - 负面提示词支持
  - 温度控制 (0.0-1.0)
  - 顶级采样 (Top-P: 0.0-1.0)

- **专利附图专用功能**
  - 多种线条风格: 技术绘图、草图、渲染图
  - 多种视角: 正视图、俯视图、侧视图、等轴测图
  - 自动标注和编号支持

- **图生图编辑功能**
  - 图像修改/编辑
  - 风格迁移
  - 草图渲染
  - 图像外扩

## 安装 (Installation)

### 前置要求 (Prerequisites)

- Python 3.8+
- Dify Platform
- OpenRouter API Key

### 安装步骤 (Installation Steps)

1. 克隆或下载此插件到 Dify 的插件目录：

```bash
cd /path/to/dify/data/plugins
git clone https://github.com/yourusername/dify-gemini-image-plugin.git
cd dify-gemini-image-plugin
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：

在 Dify 的环境配置中添加：

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

或在 Dify 的系统设置中配置 API 密钥。

4. 在 Dify 中启用插件：

重启 Dify 服务，然后在插件管理页面启用 "Gemini Image Generator"。

## 使用方法 (Usage)

### 在 Dify 工作流中使用 (Using in Dify Workflow)

1. **创建新工作流** 或编辑现有工作流

2. **添加 Gemini Image Generator 节点**
   - 在工具列表中找到 "Gemini Image Generator"
   - 将其拖入工作流画布

3. **配置参数**

#### 文生图模式 (Text-to-Image Mode)

```
工作模式: text_to_image
提示词: "A futuristic cityscape at sunset, cyberpunk style"
图像尺寸: 1024x1024
生成数量: 1
温度: 0.8
```

#### 图生图模式 (Image-to-Image Mode)

```
工作模式: image_to_image
编辑类型: style_transfer
参考图像URL: "https://example.com/reference.jpg"
提示词: "Convert this to watercolor style"
图像尺寸: 1024x1024
```

#### 专利附图模式 (Patent Drawing Mode)

```
工作模式: patent_drawing
提示词: "A mechanical device with gears and levers"
线条风格: technical
视角: isometric
图像尺寸: 1024x1024
自动标注: true
```

#### 产品原型图模式 (Product Prototype Mode)

```
工作模式: product_prototype
提示词: "Smart watch with health monitoring features"
线条风格: render
视角: front
图像尺寸: 1024x1024
```

### API 参数说明 (API Parameters)

| 参数 (Parameter) | 类型 (Type) | 说明 (Description) | 必填 (Required) |
|-----------------|------------|-------------------|---------------|
| mode | string | 工作模式: text_to_image, image_to_image, patent_drawing, product_prototype | 是 |
| prompt | string | 图像生成提示词 | 是 |
| size | string | 图像尺寸: 1024x1024, 1024x768, 768x1024, 832x1216, 1216s832 | 否 (默认: 1024x1024) |
| n | integer | 生成数量 (1-4) | 否 (默认: 1) |
| negative_prompt | string | 负面提示词 | 否 |
| temperature | float | 创造性 (0.0-1.0) | 否 (默认: 0.7) |
| top_p | float | 顶级采样 (0.0-1.0) | 否 (默认: 0.9) |

#### 图生图额外参数 (Image-to-Image Additional Parameters)

| 参数 | 类型 | 说明 | 必填 |
|-----|------|------|------|
| edit_type | string | 编辑类型: modify, style_transfer, sketch_render, outpainting | 图生图模式必填 |
| reference_image | string | 参考图像URL | 图生图模式必填 |

#### 专利附图额外参数 (Patent Drawing Additional Parameters)

| 参数 | 类型 | 说明 | 必填 |
|-----|------|------|------|
| line_style | string | 线条风格: technical, sketch, render | 否 (默认: technical) |
| view_angle | string | 视角: front, top, side, isometric | 否 (默认: isometric) |
| auto_label | boolean | 自动标注 | 否 (默认: true) |

## 使用示例 (Examples)

### 示例 1: 文生图 - 生成风景画

**输入:**
```json
{
  "mode": "text_to_image",
  "prompt": "A serene mountain landscape at dawn, with a lake reflecting the mountains, photorealistic style",
  "size": "1024x1024",
  "n": 1,
  "temperature": 0.8
}
```

**输出:**
```json
{
  "success": true,
  "images": [
    {
      "url": "https://storage.example.com/generated/image1.png",
      "revised_prompt": "A serene mountain landscape..."
    }
  ]
}
```

### 示例 2: 图生图 - 风格迁移

**输入:**
```json
{
  "mode": "image_to_image",
  "edit_type": "style_transfer",
  "reference_image": "https://example.com/original.jpg",
  "prompt": "Convert this photo to impressionist oil painting style",
  "size": "1024x1024"
}
```

### 示例 3: 专利附图

**输入:**
```json
{
  "mode": "patent_drawing",
  "prompt": "A novel mechanical transmission system with clutch mechanism",
  "line_style": "technical",
  "view_angle": "isometric",
  "auto_label": true
}
```

### 示例 4: 产品原型

**输入:**
```json
{
  "mode": "product_prototype",
  "prompt": "Ergonomic office chair with lumbar support",
  "line_style": "render",
  "view_angle": "side",
  "n": 2
}
```

## 技术细节 (Technical Details)

### API 端点 (API Endpoint)

- OpenRouter API: `https://openrouter.ai/api/v1/chat/completions`
- 模型: `google/gemini-2.0-flash-exp-image-generation`

### 错误处理 (Error Handling)

插件包含完善的错误处理机制：
- API 密钥验证
- 网络超时重试 (最多3次)
- 参数验证
- 详细的错误信息返回

### 性能优化 (Performance)

- 请求超时: 30秒
- 自动重试机制
- 连接池复用
- 响应缓存支持

## 依赖项 (Dependencies)

```
requests>=2.31.0
pydantic>=2.0.0
pytest>=7.4.0
pytest-mock>=3.11.0
```

## 开发 (Development)

### 运行测试 (Run Tests)

```bash
pytest tests/
```

### 代码结构 (Code Structure)

```
gemini_image_generator/
├── __init__.py           # 包初始化
├── config.py             # 配置常量
├── gemini_image_tool.py  # 主要工具实现
└── utils.py              # 工具函数

tests/
├── __init__.py
├── test_gemini_tool.py   # 工具测试
└── fixtures/             # 测试数据
```

## 常见问题 (FAQ)

### Q: 如何获取 OpenRouter API Key?

A: 访问 [OpenRouter](https://openrouter.ai/) 注册账号并创建 API Key。

### Q: 支持哪些图像尺寸?

A: 支持 1024x1024, 1024x768, 768x1024, 832x1216, 1216x832 五种尺寸。

### Q: 生成一张图片需要多长时间?

A: 通常在 5-15 秒之间，取决于提示词的复杂度和网络状况。

### Q: 如何提高生成质量?

A:
- 使用详细、具体的提示词
- 合理调整温度参数 (0.7-0.9 通常效果较好)
- 添加负面提示词排除不需要的元素
- 对于专业图稿，使用专利附图模式并选择合适的线条风格

## 许可证 (License)

MIT License

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！

## 联系方式 (Contact)

- GitHub Issues: https://github.com/yourusername/dify-gemini-image-plugin/issues
- Email: your-email@example.com

## 更新日志 (Changelog)

### v1.0.0 (2025-01-26)
- 初始版本发布
- 支持四种生成模式
- 完整的参数配置
- 专利附图专用功能
