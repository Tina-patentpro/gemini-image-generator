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
