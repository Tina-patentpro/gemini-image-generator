# Dify Gemini Image Generator Plugin - 使用指南

## 目录 (Table of Contents)

1. [安装指南](#安装指南)
2. [使用场景示例](#使用场景示例)
3. [参数详细说明](#参数详细说明)
4. [预设模板列表](#预设模板列表)
5. [最佳实践](#最佳实践)
6. [故障排除](#故障排除)
7. [成本估算](#成本估算)
8. [技术支持](#技术支持)

---

## 安装指南

### 第一步：准备工作

#### 系统要求
- Python 3.8 或更高版本
- pip 包管理器
- Dify Platform（本地或云端）
- 至少 1GB 可用磁盘空间

#### 检查 Python 版本
```bash
python --version
# 或
python3 --version
```

### 第二步：获取 OpenRouter API Key

1. **注册 OpenRouter 账号**
   - 访问 [OpenRouter 官网](https://openrouter.ai/)
   - 点击 "Sign Up" 创建账号
   - 验证邮箱

2. **生成 API Key**
   - 登录后进入 Settings
   - 选择 "API Keys" 标签
   - 点击 "Create New Key"
   - 复制生成的 API Key（格式：`sk-or-...`）

3. **充值账户**
   - Gemini 2.0 Flash 图像生成按使用量计费
   - 建议先充值 $5-10 测试
   - 查看定价：https://openrouter.ai/docs/models

### 第三步：安装插件

#### 方法一：通过 Git 克隆（推荐）

```bash
# 进入 Dify 插件目录
cd /path/to/dify/data/plugins

# 克隆插件仓库
git clone https://github.com/yourusername/dify-gemini-image-plugin.git

# 进入插件目录
cd dify-gemini-image-plugin

# 安装 Python 依赖
pip install -r requirements.txt
```

#### 方法二：手动下载

1. 从 GitHub 下载 ZIP 文件
2. 解压到 Dify 的 `data/plugins/` 目录
3. 重命名文件夹为 `dify-gemini-image-plugin`
4. 安装依赖：

```bash
cd /path/to/dify/data/plugins/dify-gemini-image-plugin
pip install -r requirements.txt
```

### 第四步：配置环境变量

#### 方法一：通过 .env 文件（开发环境）

```bash
# 在插件根目录创建 .env 文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# OPENROUTER_API_KEY=sk-or-your-actual-api-key-here
```

#### 方法二：通过 Dify 系统设置（生产环境）

1. 登录 Dify 管理后台
2. 进入 "Settings" → "Environment Variables"
3. 添加新的环境变量：
   - Name: `OPENROUTER_API_KEY`
   - Value: 你的 API Key
4. 保存设置

### 第五步：重启 Dify 服务

#### Docker 部署

```bash
# 停止容器
docker-compose down

# 重新构建并启动
docker-compose up -d

# 查看日志确认启动成功
docker-compose logs -f dify-web
```

#### 本地部署

```bash
# 停止服务
pkill -f dify

# 重新启动
cd /path/to/dify
python app.py
# 或使用启动脚本
./start.sh
```

### 第六步：验证安装

1. 登录 Dify
2. 创建新工作流
3. 在工具列表中查找 "Gemini Image Generator"
4. 如果能看到该工具，说明安装成功

---

## 使用场景示例

### 场景一：专利附图生成

#### 使用案例
机械工程师需要为新型传动装置申请专利，需要生成技术性附图。

#### 参数配置

**输入参数：**
```json
{
  "mode": "patent_drawing",
  "prompt": "一种新型齿轮传动系统，包括输入轴、输出轴、中间齿轮组和离合器机构",
  "line_style": "technical",
  "view_angle": "isometric",
  "size": "1024x1024",
  "auto_label": true,
  "n": 1
}
```

**输出示例：**
```json
{
  "success": true,
  "mode": "patent_drawing",
  "images": [
    {
      "url": "https://storage.example.com/patent_drawing_001.png",
      "revised_prompt": "Technical patent drawing of gear transmission system..."
    }
  ],
  "metadata": {
    "line_style": "technical",
    "view_angle": "isometric",
    "labels": ["1", "2", "3", "4", "5"],
    "generation_time": "8.3s"
  }
}
```

#### 提示词优化技巧

**基础版：**
```
齿轮传动系统
```

**优化版：**
```
一种新型齿轮传动系统，包括：
- 输入轴（左侧）
- 输出轴（右侧）
- 三个中间齿轮形成齿轮组
- 电磁离合器机构
- 所有部件标注零件编号
- 等轴测视图，技术绘图风格
```

### 场景二：产品原型设计

#### 使用案例
工业设计师需要快速生成产品概念图，用于客户演示。

#### 参数配置

**输入参数：**
```json
{
  "mode": "product_prototype",
  "prompt": "智能手环，带有心率监测、血氧检测、GPS定位功能，现代简约设计",
  "line_style": "render",
  "view_angle": "front",
  "size": "1024x1024",
  "n": 2,
  "temperature": 0.8
}
```

**输出示例：**
```json
{
  "success": true,
  "mode": "product_prototype",
  "images": [
    {
      "url": "https://storage.example.com/prototype_001.png",
      "revised_prompt": "Product prototype render of smart fitness tracker..."
    },
    {
      "url": "https://storage.example.com/prototype_002.png",
      "revised_prompt": "Product prototype render of smart fitness tracker..."
    }
  ],
  "metadata": {
    "line_style": "render",
    "view_angle": "front",
    "generation_time": "15.7s"
  }
}
```

#### 多视角批量生成

```json
{
  "mode": "product_prototype",
  "prompt": "智能蓝牙音箱，圆柱形设计，金属质感",
  "line_style": "render",
  "size": "1024x1024",
  "n": 4,
  "temperature": 0.9
}
```

**说明：** 高温度值（0.9）会生成4个不同的设计变体。

### 场景三：草图渲染

#### 使用案例
设计师手绘产品草图，需要快速渲染成效果图。

#### 参数配置

**输入参数：**
```json
{
  "mode": "image_to_image",
  "edit_type": "sketch_render",
  "reference_image": "https://example.com/sketch.jpg",
  "prompt": "将这个草图渲染成高质量产品效果图，添加材质、光影和细节",
  "size": "1024x1024",
  "n": 1
}
```

**工作流程：**
1. 上传手绘草图到图床或 Dify 文件管理
2. 获取图片 URL
3. 配置图生图参数
4. 执行生成

### 场景四：批量生成营销图片

#### 使用案例
电商需要为一款新产品生成多个角度的营销图片。

#### 参数配置

**输入参数：**
```json
{
  "mode": "text_to_image",
  "prompt": "高端蓝牙耳机，放在木质桌面上，柔和的自然光，产品摄影风格",
  "size": "1024x1024",
  "n": 4,
  "temperature": 0.7,
  "negative_prompt": "低质量、模糊、过度曝光、水印、文字"
}
```

**优化策略：**
- 使用负面提示词排除质量问题
- 调整温度到 0.7 获得平衡的多样性和质量
- 一次生成4张，选择最好的使用

### 场景五：错误处理和重试

#### 使用案例
在生产环境中处理 API 错误和超时。

#### 错误处理示例

**输入参数：**
```json
{
  "mode": "text_to_image",
  "prompt": "A beautiful landscape",
  "size": "1024x1024"
}
```

**可能的错误响应：**

```json
{
  "success": false,
  "error": "api_key_invalid",
  "message": "OpenRouter API key is invalid or missing. Please check your environment variables.",
  "details": {
    "timestamp": "2026-01-26T10:30:00Z",
    "request_id": "req_123456"
  }
}
```

**常见错误处理：**

1. **API Key 无效**
   - 检查环境变量配置
   - 验证 API Key 是否过期
   - 确认账户余额充足

2. **网络超时**
   - 插件会自动重试3次
   - 如持续失败，检查网络连接
   - 考虑增加超时时间

3. **参数验证失败**
   - 检查必需参数是否提供
   - 验证参数格式是否正确
   - 查看错误消息中的详细信息

---

## 参数详细说明

### 通用参数（所有模式）

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 可选值 |
|--------|------|------|--------|------|--------|
| `mode` | string | 是 | 无 | 工作模式 | `text_to_image`<br>`image_to_image`<br>`patent_drawing`<br>`product_prototype` |
| `prompt` | string | 是 | 无 | 图像生成提示词 | 任意文本描述<br>建议：详细、具体、结构化 |
| `size` | string | 否 | `1024x1024` | 图像尺寸（像素） | `1024x1024`<br>`1024x768`<br>`768x1024`<br>`832x1216`<br>`1216x832` |
| `n` | integer | 否 | `1` | 生成数量 | `1`-`4` |
| `negative_prompt` | string | 否 | 无 | 负面提示词 | 需要排除的元素描述 |
| `temperature` | float | 否 | `0.7` | 创造性/随机性 | `0.0`-`1.0`<br>（0=确定性，1=高随机性） |
| `top_p` | float | 否 | `0.9` | 核采样参数 | `0.0`-`1.0`<br>（控制词汇多样性） |

### 图生图模式专用参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 可选值 |
|--------|------|------|--------|------|--------|
| `edit_type` | string | 是（图生图） | 无 | 编辑类型 | `modify` - 图像修改<br>`style_transfer` - 风格迁移<br>`sketch_render` - 草图渲染<br>`outpainting` - 图像外扩 |
| `reference_image` | string | 是（图生图） | 无 | 参考图像URL | 公网可访问的图片URL<br>支持格式：JPG, PNG, WebP |

### 专利附图模式专用参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 可选值 |
|--------|------|------|--------|------|--------|
| `line_style` | string | 否 | `technical` | 线条风格 | `technical` - 技术绘图<br>`sketch` - 草图<br>`render` - 渲染图 |
| `view_angle` | string | 否 | `isometric` | 视角 | `front` - 正视图<br>`top` - 俯视图<br>`side` - 侧视图<br>`isometric` - 等轴测图 |
| `auto_label` | boolean | 否 | `true` | 自动标注 | `true` - 自动添加编号<br>`false` - 不添加 |

### 产品原型模式专用参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 可选值 |
|--------|------|------|--------|------|--------|
| `line_style` | string | 否 | `render` | 线条风格 | `render` - 渲染图<br>`technical` - 技术绘图<br>`sketch` - 草图 |
| `view_angle` | string | 否 | `front` | 视角 | `front` - 正视图<br>`top` - 俯视图<br>`side` - 侧视图<br>`isometric` - 等轴测图 |

### 参数使用示例

#### 文生图 - 基础配置
```json
{
  "mode": "text_to_image",
  "prompt": "一只可爱的柯基犬坐在草地上"
}
```

#### 文生图 - 高级配置
```json
{
  "mode": "text_to_image",
  "prompt": "一只可爱的柯基犬坐在阳光明媚的草地上，春天，背景有樱花树，专业宠物摄影，浅景深",
  "size": "1024x768",
  "n": 2,
  "temperature": 0.8,
  "top_p": 0.95,
  "negative_prompt": "模糊、低质量、变形、多余肢体"
}
```

#### 专利附图 - 完整配置
```json
{
  "mode": "patent_drawing",
  "prompt": "可调节高度的办公椅，包括座椅、靠背、扶手、气压杆和五星脚",
  "line_style": "technical",
  "view_angle": "isometric",
  "size": "1024x1024",
  "n": 1,
  "auto_label": true
}
```

---

## 预设模板列表

### 专利附图模板

#### 模板 1：机械装置
```json
{
  "mode": "patent_drawing",
  "line_style": "technical",
  "view_angle": "isometric",
  "auto_label": true,
  "size": "1024x1024"
}
```

**适用场景：** 传动系统、发动机、机械结构

**提示词示例：**
```
齿轮传动系统，包括输入轴、输出轴、齿轮组和离合器
```

#### 模板 2：电子设备
```json
{
  "mode": "patent_drawing",
  "line_style": "technical",
  "view_angle": "front",
  "auto_label": true,
  "size": "1024x768"
}
```

**适用场景：** 电路板、电子元件、连接器

**提示词示例：**
```
电路板布局，包括微处理器、存储器、电源管理模块和接口
```

#### 模板 3：容器结构
```json
{
  "mode": "patent_drawing",
  "line_style": "technical",
  "view_angle": "side",
  "auto_label": true,
  "size": "768x1024"
}
```

**适用场景：** 瓶子、盒子、包装容器

**提示词示例：**
```
新型饮料瓶，包括瓶身、瓶盖、标签区域和防滑纹理
```

### 产品原型模板

#### 模板 1：消费电子
```json
{
  "mode": "product_prototype",
  "line_style": "render",
  "view_angle": "front",
  "size": "1024x1024",
  "temperature": 0.8,
  "n": 2
}
```

**适用场景：** 智能手表、耳机、手机配件

**提示词示例：**
```
智能手表，方形表盘，金属边框，真皮表带，现代简约设计
```

#### 模板 2：家具设计
```json
{
  "mode": "product_prototype",
  "line_style": "render",
  "view_angle": "isometric",
  "size": "1024x1024",
  "temperature": 0.7,
  "n": 1
}
```

**适用场景：** 椅子、桌子、沙发

**提示词示例：**
```
人体工学办公椅，网状靠背，可调节扶手，黑色设计
```

#### 模板 3：交通工具
```json
{
  "mode": "product_prototype",
  "line_style": "render",
  "view_angle": "side",
  "size": "1216x832",
  "temperature": 0.9,
  "n": 3
}
```

**适用场景：** 自行车、电动车、滑板车

**提示词示例：**
```
电动自行车，流线型车架，隐藏式电池，前后轮碟刹
```

### 文生图创意模板

#### 模板 1：产品摄影
```json
{
  "mode": "text_to_image",
  "size": "1024x1024",
  "n": 1,
  "temperature": 0.7
}
```

**提示词结构：**
```
[产品名称] + [摆放场景] + [光线条件] + [摄影风格]
```

**示例：**
```
高端蓝牙耳机，放在大理石桌面上，柔和窗光，产品摄影风格，浅景深
```

#### 模板 2：概念艺术
```json
{
  "mode": "text_to_image",
  "size": "1024x1024",
  "n": 4,
  "temperature": 0.95
}
```

**提示词结构：**
```
[主体] + [风格/流派] + [细节描述] + [氛围/情绪]
```

**示例：**
```
未来派城市建筑，赛博朋克风格，霓虹灯效，飞行汽车，雨夜氛围
```

#### 模板 3：插画风格
```json
{
  "mode": "text_to_image",
  "size": "1024x768",
  "n": 1,
  "temperature": 0.8
}
```

**提示词结构：**
```
[场景] + [艺术风格] + [色彩方案] + [构图方式]
```

**示例：**
```
儿童阅读书籍，温馨房间，水彩插画风格，暖色调，特写视角
```

### 图生图编辑模板

#### 模板 1：风格迁移
```json
{
  "mode": "image_to_image",
  "edit_type": "style_transfer",
  "size": "1024x1024",
  "n": 1
}
```

**提示词示例：**
```
将这张照片转换为印象派油画风格
```

#### 模板 2：草图渲染
```json
{
  "mode": "image_to_image",
  "edit_type": "sketch_render",
  "size": "1024x1024",
  "n": 1
}
```

**提示词示例：**
```
将这个产品草图渲染成高质量效果图，添加金属材质和环境光
```

#### 模板 3：图像外扩
```json
{
  "mode": "image_to_image",
  "edit_type": "outpainting",
  "size": "1024x1024",
  "n": 1
}
```

**提示词示例：**
```
向四周扩展图像，添加与原场景匹配的内容
```

---

## 最佳实践

### 1. 提示词编写技巧

#### 结构化提示词

**推荐的提示词结构：**
```
[主体描述] + [细节特征] + [风格/质量] + [技术参数]
```

**示例：**

❌ **不好的提示词：**
```
一个杯子
```

✅ **好的提示词：**
```
陶瓷咖啡杯，白色，简约现代设计，圆柄，250ml容量，产品摄影风格，专业布光，浅景深
```

#### 使用具体描述

**包含的要素：**
- **材质：** 陶瓷、金属、塑料、木质、玻璃
- **颜色：** 具体颜色名称（如：深蓝色、米白色）
- **风格：** 现代简约、复古、工业风、科技感
- **场景：** 室内、室外、自然光、摄影棚
- **角度：** 俯视、平视、仰视、特写

**示例：**
```
机械键盘，87键布局，铝合金边框，RGB背光，悬浮式键帽，放在木质办公桌上，45度角拍摄
```

#### 添加质量关键词

**提升质量的词汇：**
- `专业摄影` (professional photography)
- `高分辨率` (high resolution)
- `细节丰富` (highly detailed)
- `8K` (8K quality)
- `电影级光效` (cinematic lighting)
- `浅景深` (shallow depth of field)

**示例：**
```
智能手表，专业产品摄影，8K分辨率，影棚布光，浅景深，细节清晰
```

#### 使用负面提示词

**常见需要排除的元素：**
```
低质量、模糊、变形、水印、文字、多余肢体、不对称
```

**完整示例：**
```json
{
  "prompt": "一只金毛寻回犬坐在草地上，阳光明媚",
  "negative_prompt": "低质量、模糊、变形、卡通风格、水印、文字、糟糕的解剖结构"
}
```

### 2. 参数调优策略

#### Temperature（温度）调优

| Temperature 值 | 效果 | 适用场景 |
|----------------|------|----------|
| `0.0 - 0.3` | 高度确定性，结果稳定 | 需要精确控制，批量生成一致性图片 |
| `0.4 - 0.6` | 平衡确定性和多样性 | 一般用途，产品展示 |
| `0.7 - 0.9` | 较高创造性 | 创意设计，艺术创作 |
| `0.95 - 1.0` | 高度随机性 | 探索性创作，灵感启发 |

**示例：**
```json
// 稳定生成产品图
{
  "prompt": "蓝牙耳机",
  "temperature": 0.3
}

// 创意设计探索
{
  "prompt": "未来派耳机概念设计",
  "temperature": 0.95
}
```

#### Top-P 调优

| Top-P 值 | 效果 | 适用场景 |
|----------|------|----------|
| `0.8 - 0.9` | 保守采样 | 需要高质量和一致性 |
| `0.9 - 0.95` | 平衡采样 | 一般用途（推荐） |
| `0.95 - 1.0` | 激进采样 | 需要多样性和创造力 |

**建议：** 通常保持默认值 `0.9`，除非有特殊需求。

#### 图像尺寸选择

| 尺寸 | 宽高比 | 适用场景 |
|------|--------|----------|
| `1024x1024` | 1:1 | 正方形构图，社交媒体，产品主图 |
| `1024x768` | 4:3 | 横向构图，演示文稿，横幅 |
| `768x1024` | 3:4 | 纵向构图，手机壁纸，海报 |
| `832x1216` | 9:16 | 竖屏视频封面，Instagram Stories |
| `1216x832` | 16:9 | 横屏视频封面，YouTube 缩略图 |

### 3. 批量生成策略

#### 生成多个变体

**场景：** 需要从同一提示词生成多个不同的结果。

**方法：**
```json
{
  "prompt": "智能手表概念设计",
  "n": 4,
  "temperature": 0.9
}
```

**说明：** 高温度（0.9）+ 生成数量（4）= 4个不同设计方案

#### 生成一致性结果

**场景：** 需要多个角度但风格统一的图片。

**方法：**
```json
// 第一次生成
{
  "prompt": "蓝牙耳机，正视图，产品摄影",
  "temperature": 0.3,
  "n": 1
}

// 第二次生成（相同温度）
{
  "prompt": "蓝牙耳机，侧视图，产品摄影",
  "temperature": 0.3,
  "n": 1
}

// 第三次生成（相同温度）
{
  "prompt": "蓝牙耳机，俯视图，产品摄影",
  "temperature": 0.3,
  "n": 1
}
```

### 4. 错误处理最佳实践

#### 重试策略

插件内置自动重试机制（最多3次），但你可以手动实现：

**在 Dify 工作流中：**
1. 添加"条件判断"节点
2. 检查返回结果的 `success` 字段
3. 如果 `false`，则循环回重试
4. 设置最大重试次数（建议3次）

#### 超时处理

**默认超时：** 30秒

**如果经常超时：**
- 检查网络连接
- 简化提示词
- 减少生成数量
- 考虑使用更小的图像尺寸

#### API 配额管理

**监控使用量：**
```python
# 查看返回的 metadata
{
  "images": [...],
  "metadata": {
    "tokens_used": 12345,
    "estimated_cost": 0.012
  }
}
```

**成本控制建议：**
- 设置每月使用限额
- 优先使用小尺寸测试（1024x768）
- 批量生成前先单张测试效果

### 5. 性能优化

#### 减少等待时间

**方法1：使用较小的图像尺寸**
```json
{
  "size": "1024x768"  // 比 1024x1024 快约20%
}
```

**方法2：降低生成数量**
```json
{
  "n": 1  // 单张生成最快
}
```

**方法3：简化提示词**
```
// 慢
"a very detailed and intricate futuristic cityscape with flying cars, neon lights, robots, and holographic advertisements at sunset..."

// 快
"futuristic city with flying cars and neon lights"
```

#### 提高成功率

**关键因素：**
1. **清晰的提示词** - 避免歧义
2. **合理的参数** - 不要追求极端温度
3. **稳定的网络** - 确保连接质量
4. **充足的配额** - 保持账户余额

---

## 故障排除

### 问题 1：安装失败

#### 症状
```bash
ERROR: Could not find a version that satisfies the requirement pydantic
```

#### 解决方案

**检查 Python 版本：**
```bash
python --version
# 必须是 3.8 或更高
```

**升级 pip：**
```bash
pip install --upgrade pip
```

**使用虚拟环境：**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 问题 2：插件不显示

#### 症状
在 Dify 工具列表中找不到 "Gemini Image Generator"

#### 解决方案

**检查插件目录：**
```bash
ls /path/to/dify/data/plugins/dify-gemini-image-plugin
```

**检查 manifest.yaml：**
```bash
cat manifest.yaml
```

确保文件存在且格式正确。

**重启 Dify：**
```bash
docker-compose restart
# 或
pkill -f dify && ./start.sh
```

**查看日志：**
```bash
docker-compose logs dify-worker | grep gemini
```

### 问题 3：API Key 错误

#### 症状
```json
{
  "success": false,
  "error": "api_key_invalid",
  "message": "OpenRouter API key is invalid or missing"
}
```

#### 解决方案

**验证环境变量：**
```bash
echo $OPENROUTER_API_KEY
```

**检查 .env 文件：**
```bash
cat .env
# 确保格式正确，无引号
OPENROUTER_API_KEY=sk-or-xxxxx
```

**在 Dify 中重新配置：**
1. 进入 Settings → Environment Variables
2. 删除旧的 `OPENROUTER_API_KEY`
3. 添加新的值
4. 保存并重启服务

### 问题 4：生成失败

#### 症状
```json
{
  "success": false,
  "error": "generation_failed",
  "message": "Failed to generate image"
}
```

#### 可能原因和解决方案

**原因1：提示词包含违规内容**
- 检查提示词是否符合内容政策
- 移除敏感词汇

**原因2：网络超时**
```json
{
  "timeout": 60  // 增加超时时间（秒）
}
```

**原因3：API 配额不足**
- 登录 OpenRouter 检查余额
- 充值账户

**原因4：模型不可用**
- 检查 OpenRouter 状态页面
- 稍后重试

### 问题 5：图像质量不佳

#### 症状
生成的图像模糊、变形或不符预期

#### 解决方案

**优化提示词：**
```
// 添加质量关键词
"产品摄影，高分辨率，专业布光，8K质量"
```

**调整参数：**
```json
{
  "temperature": 0.8,  // 提高创造性
  "top_p": 0.95
}
```

**使用负面提示词：**
```json
{
  "negative_prompt": "低质量、模糊、变形、水印"
}
```

**尝试不同模式：**
- 如果生成产品图，使用 `product_prototype` 模式
- 如果生成技术图，使用 `patent_drawing` 模式

### 问题 6：生成速度慢

#### 症状
单次生成超过 30 秒

#### 解决方案

**减小图像尺寸：**
```json
{
  "size": "1024x768"  // 而非 1024x1024
}
```

**减少生成数量：**
```json
{
  "n": 1
}
```

**简化提示词：**
```
// 移除冗余描述
```

**检查网络：**
```bash
ping openrouter.ai
traceroute openrouter.ai
```

### 问题 7：批量生成部分失败

#### 症状
请求生成 4 张，只返回了 2 张

#### 解决方案

这是正常行为。API 可能部分成功：

```json
{
  "success": true,
  "images": [/* 2张图片 */],
  "metadata": {
    "requested": 4,
    "generated": 2,
    "note": "Some images failed to generate"
  }
}
```

**建议：**
- 接收已生成的图片
- 对失败的图片重新发起请求

---

## 成本估算

### OpenRouter 定价

**Gemini 2.0 Flash 图像生成**（截至 2026-01）

| 图像尺寸 | 输入成本 | 输出成本 |
|----------|---------|---------|
| 1024x1024 | $0.002/张 | $0.015/张 |
| 1024x768 | $0.0015/张 | $0.012/张 |
| 768x1024 | $0.0015/张 | $0.012/张 |
| 832x1216 | $0.002/张 | $0.015/张 |
| 1216x832 | $0.002/张 | $0.015/张 |

**注意：** 价格可能变动，请以 [OpenRouter 定价页面](https://openrouter.ai/docs/models) 为准。

### 使用场景成本计算

#### 场景 1：专利附图

**需求：** 生成 10 张专利附图

**配置：**
```json
{
  "mode": "patent_drawing",
  "size": "1024x1024",
  "n": 1
}
```

**计算：**
- 单张成本：$0.015
- 总成本：$0.015 × 10 = **$0.15**

#### 场景 2：产品原型批量生成

**需求：** 为 5 个产品生成设计稿，每个产品 4 个方案

**配置：**
```json
{
  "mode": "product_prototype",
  "size": "1024x1024",
  "n": 4
}
```

**计算：**
- 单次请求（4张）：$0.015 × 4 = $0.06
- 5个产品：$0.06 × 5 = **$0.30**

#### 场景 3：电商营销图片

**需求：** 为 100 个产品生成营销图片，每个产品 2 张

**配置：**
```json
{
  "mode": "text_to_image",
  "size": "1024x768",  // 使用较小尺寸节省成本
  "n": 2
}
```

**计算：**
- 单张成本：$0.012
- 单次请求（2张）：$0.012 × 2 = $0.024
- 100个产品：$0.024 × 100 = **$2.40**

### 成本优化建议

#### 策略 1：使用合适尺寸

**成本对比：**
- 1024x1024: $0.015/张
- 1024x768: $0.012/张（节省 20%）

**建议：** 除非需要正方形，否则使用 1024x768

#### 策略 2：分批测试

**工作流程：**
1. 先用小尺寸测试：`1024x768` + `n: 1`
2. 确认提示词效果
3. 再批量生成：`1024x1024` + `n: 4`

**节省：** 避免浪费在大规模测试上

#### 策略 3：控制生成数量

**问题：** 一次生成 4 张，可能只需要 1 张

**解决方案：**
```json
// 测试阶段
{ "n": 1 }

// 确认后批量
{ "n": 4 }
```

#### 策略 4：使用缓存

**在 Dify 工作流中：**
1. 检查是否已生成过相同提示词
2. 如果有，直接使用缓存
3. 避免重复生成

**节省：** 可能节省 50-80% 成本

### 预算规划示例

#### 小型项目（个人使用）

**需求：**
- 每月生成 100 张图片
- 主要用于个人项目

**预估成本：**
- 100 张 × $0.012 = **$1.20/月**

**建议充值：** $5（可用 4 个月）

#### 中型项目（小团队）

**需求：**
- 每月生成 1000 张图片
- 用于产品设计和营销

**预估成本：**
- 1000 张 × $0.012 = **$12/月**

**建议充值：** $50（可用 4 个月）

#### 大型项目（企业级）

**需求：**
- 每月生成 10000 张图片
- 大规模电商和营销

**预估成本：**
- 10000 张 × $0.012 = **$120/月**

**建议充值：** $500（可用 4 个月）

**联系 OpenRouter：** 可能获得企业折扣

---

## 技术支持

### 获取帮助

#### 1. 文档资源

- **GitHub README:** [项目主页](https://github.com/yourusername/dify-gemini-image-plugin)
- **使用指南:** 本文档
- **API 文档:** [OpenRouter API Docs](https://openrouter.ai/docs)
- **Dify 文档:** [Dify 官方文档](https://docs.dify.ai/)

#### 2. 社区支持

**GitHub Issues:**
- 报告 Bug: [提交 Issue](https://github.com/yourusername/dify-gemini-image-plugin/issues/new?template=bug_report.md)
- 功能请求: [提交 Issue](https://github.com/yourusername/dify-gemini-image-plugin/issues/new?template=feature_request.md)
- 使用问题: [提交 Issue](https://github.com/yourusername/dify-gemini-image-plugin/issues/new?template=question.md)

**Discord 社区:**
- Dify 官方 Discord: [加入链接](https://discord.gg/dify)
- 插件讨论频道: #plugin-development

#### 3. 联系方式

**项目维护者：**
- Email: your-email@example.com
- Twitter: @yourusername
- GitHub: @yourusername

**商业支持：**
如需企业级支持、定制开发或技术培训，请联系：enterprise@example.com

### 常用资源

#### OpenRouter 相关

- **官网:** https://openrouter.ai/
- **控制台:** https://openrouter.ai/console
- **API 文档:** https://openrouter.ai/docs
- **定价页面:** https://openrouter.ai/docs/models
- **状态页面:** https://status.openrouter.ai/

#### Dify 相关

- **官网:** https://dify.ai/
- **文档:** https://docs.dify.ai/
- **GitHub:** https://github.com/langgenius/dify
- **社区论坛:** https://community.dify.ai/

#### Google Gemini 相关

- **官网:** https://ai.google.dev/
- **模型文档:** https://ai.google.dev/gemini-api/docs
- **示例库:** https://ai.google.dev/gemini-api/libraries

### 贡献指南

#### 如何贡献

我们欢迎各种形式的贡献：

**1. 报告问题**
- 使用 GitHub Issues 模板
- 提供详细的复现步骤
- 附上日志和截图

**2. 提交代码**
1. Fork 项目仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

**3. 改进文档**
- 修正错别字
- 添加使用示例
- 翻译文档
- 更新过时信息

**4. 分享经验**
- 写博客文章
- 制作视频教程
- 在社区分享你的工作流
- 帮助其他用户

#### 代码规范

**Python 代码风格：**
- 遵循 PEP 8
- 使用类型注解
- 添加文档字符串
- 编写单元测试

**提交信息规范：**
```
<type>: <subject>

<body>

<footer>
```

**类型（type）：**
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

**示例：**
```
feat: add batch image generation support

- Add batch_size parameter
- Implement concurrent processing
- Add progress callback

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

### 致谢

感谢以下开源项目和社区：

- [Dify](https://github.com/langgenius/dify) - 强大的 LLM 应用开发平台
- [OpenRouter](https://openrouter.ai/) - 统一的 AI API 接口
- [Google Gemini](https://ai.google.dev/) - 先进的图像生成模型
- 所有贡献者和用户的支持

---

## 附录

### A. 完整配置示例

#### 示例 1：完整工作流配置

```yaml
workflow:
  name: "产品图片生成工作流"
  nodes:
    - id: "input"
      type: "start"
      data:
        prompt: "{{用户输入的产品描述}}"

    - id: "generate_image"
      type: "tool"
      tool: "gemini_image_generator"
      data:
        mode: "product_prototype"
        prompt: "{{input.prompt}}"
        line_style: "render"
        view_angle: "front"
        size: "1024x1024"
        n: 2
        temperature: 0.8

    - id: "output"
      type: "end"
      data:
        images: "{{generate_image.images}}"
```

### B. 错误代码参考

| 错误代码 | 说明 | 解决方案 |
|----------|------|----------|
| `api_key_invalid` | API Key 无效或缺失 | 检查环境变量配置 |
| `api_key_quota_exceeded` | API 配额超限 | 充值账户 |
| `invalid_parameter` | 参数验证失败 | 检查参数格式和值 |
| `network_error` | 网络连接错误 | 检查网络连接，稍后重试 |
| `timeout` | 请求超时 | 简化提示词或增加超时时间 |
| `generation_failed` | 生成失败 | 检查提示词，稍后重试 |
| `content_policy_violation` | 违反内容政策 | 修改提示词内容 |
| `model_unavailable` | 模型不可用 | 检查 OpenRouter 状态 |
| `rate_limit_exceeded` | 超过速率限制 | 降低请求频率 |
| `invalid_image_url` | 图像 URL 无效 | 检查 URL 可访问性 |

### C. 版本历史

#### v1.0.0 (2026-01-26)
- 初始版本发布
- 支持四种生成模式
- 完整的参数配置
- 专利附图专用功能
- 图生图编辑功能
- 自动重试机制
- 完善的错误处理

---

**文档更新日期:** 2026-01-26
**文档版本:** 1.0.0
**维护者:** Dify Gemini Image Plugin Team
