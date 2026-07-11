"""【xl_c4d_tool — C4D 风格 Blender 工具集 v3.4 公开核心版】

公开核心包含修改器库、图像置换 2.0、场景辅助、Node Preview、
集合实例转材质和四边重拓扑入口。分发范围与第三方许可见仓库文档。
"""

bl_info = {
    "name": "xl_c4d_tool",
    "author": "xl",
    "version": (3, 4, 0),
    "blender": (5, 1, 0),
    "location": "3D View > c4d小工具 / Node Editor > c4d小工具 / 编辑器菜单栏",
    "description": "C4D风格工具集：莫兰迪节点库、四边重拓扑、场景整理与完整节点浏览器",
    "category": "3D View",
}

import bpy
from . import panels
from . import operators
from . import properties
from . import utils
from . import preferences
from . import handlers

from . import node_preview
from . import geo_nodes
from . import 集合实例转材质
from . import 重拓扑

sub_modules = [
    utils,
    preferences,
    properties,
    operators,
    handlers,
    重拓扑,
    node_preview,
    geo_nodes,
    集合实例转材质,
    panels,
]


def register():
    for mod in sub_modules:
        mod.register()


def unregister():
    for mod in reversed(sub_modules):
        mod.unregister()
