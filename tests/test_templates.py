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
    assert template["id"] == "explosion"
    assert template["type"] == "patent"


def test_get_product_template():
    """测试获取产品模板"""
    manager = get_template_manager()
    template = manager.get_product_template("concept")
    assert template is not None
    assert template["id"] == "concept"
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
