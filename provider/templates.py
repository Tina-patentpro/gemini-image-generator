"""预设模板管理系统

提供专利附图和产品原型绘图的预设模板。
"""

from typing import Dict, List, Optional, Any


class TemplateManager:
    """模板管理器 - 单例模式"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # 专利附图模板
        self._patent_templates = {
            "explosion": {
                "id": "explosion",
                "name": "爆炸图",
                "type": "patent",
                "description": "展示产品各部件的分解组合关系",
                "prompt_prefix": "请绘制一张专业的爆炸图，展示",
                "prompt_suffix": "的内部结构和各部件的装配关系。要求：\n"
                               "1. 清晰展示各部件的分解位置\n"
                               "2. 标注主要部件名称\n"
                               "3. 使用等轴测视角\n"
                               "4. 线条简洁清晰，符合专利附图规范",
                "default_params": {
                    "style": "technical",
                    "view": "isometric",
                    "detail_level": "medium"
                }
            },
            "assembly": {
                "id": "assembly",
                "name": "装配图",
                "type": "patent",
                "description": "展示产品整体装配后的外观和结构",
                "prompt_prefix": "请绘制一张装配图，展示",
                "prompt_suffix": "的整体外观和结构特征。要求：\n"
                               "1. 展示产品完整装配状态\n"
                               "2. 标注主要结构和功能部件\n"
                               "3. 使用正视图或侧视图\n"
                               "4. 符合专利附图的简洁规范",
                "default_params": {
                    "style": "technical",
                    "view": "front",
                    "detail_level": "high"
                }
            },
            "detail": {
                "id": "detail",
                "name": "细节放大图",
                "type": "patent",
                "description": "展示产品关键部位的细节结构",
                "prompt_prefix": "请绘制一张细节放大图，展示",
                "prompt_suffix": "的关键部位结构。要求：\n"
                               "1. 放大比例适中，清晰可见\n"
                               "2. 标注细节特征和尺寸\n"
                               "3. 使用剖面或局部放大\n"
                               "4. 线条精细，符合专利附图规范",
                "default_params": {
                    "style": "technical",
                    "view": "detail",
                    "detail_level": "high"
                }
            },
            "section": {
                "id": "section",
                "name": "剖面图",
                "type": "patent",
                "description": "展示产品内部结构的剖面关系",
                "prompt_prefix": "请绘制一张剖面图，展示",
                "prompt_suffix": "的内部结构。要求：\n"
                               "1. 清晰展示内部层次关系\n"
                               "2. 标注主要内部部件\n"
                               "3. 使用适当的剖切位置\n"
                               "4. 符合专利附图的剖面规范",
                "default_params": {
                    "style": "technical",
                    "view": "section",
                    "detail_level": "medium"
                }
            },
            "principle": {
                "id": "principle",
                "name": "原理图",
                "type": "patent",
                "description": "展示产品的工作原理和机制",
                "prompt_prefix": "请绘制一张原理图，展示",
                "prompt_suffix": "的工作原理。要求：\n"
                               "1. 清晰展示工作流程\n"
                               "2. 标注关键步骤和部件\n"
                               "3. 使用箭头和符号表示动作\n"
                               "4. 简洁明了，易于理解",
                "default_params": {
                    "style": "schematic",
                    "view": "diagram",
                    "detail_level": "low"
                }
            },
            "circuit": {
                "id": "circuit",
                "name": "电路图",
                "type": "patent",
                "description": "展示电子产品的电路连接关系",
                "prompt_prefix": "请绘制一张电路图，展示",
                "prompt_suffix": "的电路连接关系。要求：\n"
                               "1. 清晰展示电路结构\n"
                               "2. 标注主要元件和连接\n"
                               "3. 使用标准电路符号\n"
                               "4. 符合电气原理图规范",
                "default_params": {
                    "style": "schematic",
                    "view": "circuit",
                    "detail_level": "high"
                }
            }
        }

        # 产品原型模板
        self._product_templates = {
            "concept": {
                "id": "concept",
                "name": "概念设计",
                "type": "product",
                "description": "产品的概念设计和创意表达",
                "prompt_prefix": "请设计一个",
                "prompt_suffix": "的概念设计图。要求：\n"
                               "1. 展现创新和未来感\n"
                               "2. 突出核心功能特点\n"
                               "3. 使用现代简洁的设计风格\n"
                               "4. 适合产品展示和宣传",
                "default_params": {
                    "style": "modern",
                    "quality": "high",
                    "detail_level": "medium"
                }
            },
            "ui": {
                "id": "ui",
                "name": "界面设计",
                "type": "product",
                "description": "软件产品的用户界面设计",
                "prompt_prefix": "请设计",
                "prompt_suffix": "的用户界面。要求：\n"
                               "1. 界面简洁美观\n"
                               "2. 符合现代UI设计规范\n"
                               "3. 突出主要功能模块\n"
                               "4. 注重用户体验和交互",
                "default_params": {
                    "style": "modern_ui",
                    "quality": "high",
                    "detail_level": "high"
                }
            },
            "scene": {
                "id": "scene",
                "name": "使用场景",
                "type": "product",
                "description": "产品在实际使用场景中的应用",
                "prompt_prefix": "请绘制",
                "prompt_suffix": "的使用场景图。要求：\n"
                               "1. 展示真实使用环境\n"
                               "2. 突出产品功能和价值\n"
                               "3. 场景自然真实\n"
                               "4. 适合产品推广和营销",
                "default_params": {
                    "style": "realistic",
                    "quality": "high",
                    "detail_level": "medium"
                }
            },
            "function": {
                "id": "function",
                "name": "功能演示",
                "type": "product",
                "description": "展示产品核心功能的运作方式",
                "prompt_prefix": "请绘制",
                "prompt_suffix": "的功能演示图。要求：\n"
                               "1. 清晰展示功能流程\n"
                               "2. 突出关键操作步骤\n"
                               "3. 使用示意图或插图风格\n"
                               "4. 简洁易懂，便于说明",
                "default_params": {
                    "style": "illustration",
                    "quality": "medium",
                    "detail_level": "medium"
                }
            },
            "packaging": {
                "id": "packaging",
                "name": "包装设计",
                "type": "product",
                "description": "产品的包装和外观设计",
                "prompt_prefix": "请设计",
                "prompt_suffix": "的包装方案。要求：\n"
                               "1. 包装美观大方\n"
                               "2. 符合品牌调性\n"
                               "3. 突出产品特点\n"
                               "4. 适合市场销售",
                "default_params": {
                    "style": "commercial",
                    "quality": "high",
                    "detail_level": "medium"
                }
            }
        }

    def get_patent_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取专利附图模板

        Args:
            template_id: 模板ID

        Returns:
            模板字典，如果不存在返回None
        """
        return self._patent_templates.get(template_id)

    def get_product_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取产品原型模板

        Args:
            template_id: 模板ID

        Returns:
            模板字典，如果不存在返回None
        """
        return self._product_templates.get(template_id)

    def apply_template(self, template: Dict[str, Any], user_prompt: str) -> str:
        """应用模板到用户提示词

        Args:
            template: 模板字典
            user_prompt: 用户输入的提示词

        Returns:
            完整的提示词
        """
        prompt = f"{template['prompt_prefix']} {user_prompt} {template['prompt_suffix']}"
        return prompt

    def list_all_templates(self) -> List[Dict[str, Any]]:
        """列出所有模板

        Returns:
            所有模板的列表
        """
        all_templates = []
        all_templates.extend(list(self._patent_templates.values()))
        all_templates.extend(list(self._product_templates.values()))
        return all_templates

    def list_patent_templates(self) -> List[Dict[str, Any]]:
        """列出所有专利附图模板

        Returns:
            专利模板列表
        """
        return list(self._patent_templates.values())

    def list_product_templates(self) -> List[Dict[str, Any]]:
        """列出所有产品原型模板

        Returns:
            产品模板列表
        """
        return list(self._product_templates.values())


# 全局单例实例
_template_manager: Optional[TemplateManager] = None


def get_template_manager() -> TemplateManager:
    """获取模板管理器单例

    Returns:
        TemplateManager实例
    """
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager
