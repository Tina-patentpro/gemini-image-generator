# Dify Gemini图像生成插件设计文档

**日期：** 2026-01-26
**作者：** Claude Code
**状态：** 设计阶段

## 1. 概述

### 1.1 项目目标
开发一个Dify插件，通过OpenRouter调用Google Gemini 2.0 Flash图像生成模型，实现专利附图和产品原型图的AI生成与编辑功能。

### 1.2 核心功能
- **文生图**：基于文本描述生成全新图像
- **图生图/文改图**：基于参考图像进行修改、风格迁移、草图渲染、图像外扩
- **专利附图专用模式**：提供爆炸图、装配图、剖面图等专业模板
- **产品原型图模式**：提供概念渲染图、UI设计图、场景使用图等模板

### 1.3 技术栈
- Python 3.10+
- Dify Tool Plugin API
- OpenRouter API（Google Gemini 2.0 Flash模型）
- requests、pydantic

## 2. 架构设计

### 2.1 整体架构
采用**统一多功能节点**设计，通过模式参数切换不同功能。

**核心组件：**
- `GeminiImageGenerator`：主工具节点类，处理所有图像生成逻辑
- `OpenRouterAPIClient`：封装API调用、认证、重试逻辑
- `TemplateManager`：管理预设模板和参数
- `ImageProcessor`：处理不同模式的输入输出流程

### 2.2 数据流
```
Dify工作流 → 节点参数验证 → 模式路由 → 模板应用 → API调用
→ 响应解析 → 错误处理 → 返回结果（JSON格式）
```

### 2.3 模式切换逻辑
- `text_to_image`：纯文本生成图像
- `image_to_image`：基于参考图像编辑
- `patent_drawing`：专利图模式 + 自动应用专业模板
- `product_prototype`：原型图模式 + 自动应用设计模板

## 3. 节点参数设计

### 3.1 核心参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| mode | select | 是 | 工作模式选择 |
| prompt | text | 是 | 图像生成提示词 |
| negative_prompt | text | 否 | 负面提示词 |
| reference_image_url | text | 否 | 图生图模式的参考图像URL |
| edit_type | select | 否 | 编辑类型（修改/风格迁移/草图渲染/外扩） |

### 3.2 生成参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| size | select | 否 | 图像尺寸（默认1024x1024） |
| num_images | number | 否 | 生成数量1-4（默认1） |
| seed | number | 否 | 随机种子，用于复现 |

### 3.3 专利/原型图专用参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| preset_template | select | 否 | 预设模板（爆炸图/装配图/概念图等） |
| line_style | select | 否 | 线条风格（技术绘图/草图/渲染图） |
| view_angle | select | 否 | 视角（正视图/俯视图/等轴测图） |

### 3.4 输出格式
```json
{
  "success": true,
  "images": [
    {"url": "https://...", "index": 1}
  ],
  "error": null
}
```

## 4. 预设模板系统

### 4.1 专利附图模板（6-8个）
- **爆炸图**：零件分离、清晰标注、装配关系
- **装配图**：整体结构、组件组合
- **零件细节图**：局部放大、工艺要求
- **剖面图**：内部结构、材料区分
- **原理图**：工作原理、流程说明
- **电路/管路图**：专业领域图示

### 4.2 产品原型图模板（5-6个）
- **概念渲染图**：现代感、3D渲染
- **用户界面图**：UI/UX、交互示意
- **场景使用图**：使用场景、应用演示
- **功能示意图**：模块划分、操作流程
- **包装设计图**：包装展示、品牌元素

### 4.3 模板实现
- 存储在`templates.py`中的Python字典结构
- 每个模板包含：基础prompt、推荐参数、示例说明
- 支持模板叠加和自定义覆盖

## 5. API集成与错误处理

### 5.1 认证机制
- 使用Dify系统级环境变量`OPENROUTER_API_KEY`
- 节点初始化时验证密钥有效性
- 支持密钥轮换和更新

### 5.2 API调用封装
- 模型：`google/gemini-2.0-flash-exp-image-generation`
- 端点：OpenRouter Chat Completions API
- 超时：30秒
- 重试：最多3次，指数退避

### 5.3 宽松错误处理
**错误类型：**
- 网络错误（超时、连接失败）
- API错误（认证、配额、内容审核）
- 验证错误（参数无效、URL格式错误）

**错误响应：**
```json
{
  "success": false,
  "images": [],
  "error": {
    "type": "api_error|validation_error|network_error",
    "message": "详细错误信息",
    "retry_possible": true
  }
}
```

**处理策略：**
- 不抛出异常，确保工作流继续
- 错误信息通过error字段传递
- 建议配合条件节点检查success字段

## 6. 项目结构

```
dify-gemini-image-plugin/
├── manifest.yaml              # Dify插件清单
├── gemini_image_generator/    # 主包
│   ├── __init__.py
│   ├── gemini_image_tool.py   # 主工具类
│   ├── api_client.py          # API客户端
│   ├── templates.py           # 模板定义
│   ├── utils.py               # 工具函数
│   └── config.py              # 配置常量
├── requirements.txt           # 依赖
├── README.md                  # 文档
└── tests/                     # 测试
    ├── test_api_client.py
    └── test_templates.py
```

## 7. 测试策略

### 7.1 单元测试
- API客户端：Mock响应，测试成功/失败场景
- 模板系统：验证加载和合并逻辑

### 7.2 集成测试场景
1. 文生图基础流程
2. 图生图编辑（修改、风格迁移、草图渲染、外扩）
3. 专利图模式（应用爆炸图模板）
4. 批量生成（num_images=3）
5. 错误恢复（无效API密钥、超时）
6. 参数验证（边界值测试）

### 7.3 测试工具
- pytest + pytest-mock
- Dify开发环境进行真实测试

## 8. 部署与使用

### 8.1 安装步骤
1. 复制插件到Dify plugins目录
2. 配置`OPENROUTER_API_KEY`环境变量
3. 在Dify中重启或重新加载插件

### 8.2 使用示例
**专利爆炸图生成：**
```
mode: 专利附图
preset_template: 爆炸图
prompt: "手持电动工具的爆炸图，展示电机、齿轮箱、外壳的装配关系"
size: 1024x1024
```

**产品概念图生成：**
```
mode: 产品原型图
preset_template: 概念渲染图
prompt: "智能蓝牙耳机，现代简约设计，白色磨砂质感，45度视角"
```

**草图渲染：**
```
mode: 图生图
edit_type: 草图渲染
reference_image_url: [草图URL]
prompt: "将草图渲染为高质量产品图，保持设计细节，添加真实材质"
```

## 9. 性能与成本

### 9.1 成本估算
- 预估每张图像：$0.01-$0.03
- 建议先用小尺寸测试prompt效果
- 批量生成适合探索设计方案

### 9.2 性能优化
- API超时控制避免长时间等待
- 重试机制平衡成功率和响应时间
- 建议使用CDN缓存生成的图像URL

## 10. 未来扩展

- 支持用户自定义模板保存
- 添加更多图像编辑模式（inpainting、背景替换）
- 集成其他图像生成模型（Midjourney、Stable Diffusion）
- 支持图像本地保存和多格式导出
- 添加图像后处理（增强、裁剪、水印）
