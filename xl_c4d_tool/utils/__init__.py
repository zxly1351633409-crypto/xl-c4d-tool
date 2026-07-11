"""【工具模块：工具函数导出】日志/着色器/节点发现"""
from .logger import logger
from .shading import set_shading_for_all_areas, generate_random_color, get_all_collections
from .node_discovery import get_node_data, resolve_tree_type, get_category_color_prop_name, get_category_folded_prop_name
from . import icon_manager


def register():
    icon_manager.register()


def unregister():
    icon_manager.unregister()
