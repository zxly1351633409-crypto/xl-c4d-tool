"""【xl_c4d_tool — C4D风格Blender工具集 v3.4】
整合功能模块:
    C4D修改器库       — 选择物体后一键赋予项目节点组，按功能分类与搜索
    四边重拓扑        — QuadWild/QuadPatches 中文安全界面
    布尔显示联动      — 布尔操作对象自动线框+名称，解除引用后还原
    效果模式           — 雾效/材质ID/物体ID/集合实例转材质 (3D View > c4d小工具)
    C4D工具           — 提取样条线/对齐物体/对齐原点 (3D View > c4d小工具)
    节点设置           — 已迁移到插件偏好设置
    快捷节点           — 搜索/分类/收藏/最近/自动补全 (Node Editor)
    材质节点助手       — OC/C4D风格材质节点组 (仅着色器编辑器可用，2列显示)
    几何节点助手       — 全部 C4D 项目节点组，C4D层级折叠、彩色图标与鼠标放置
    任意节点转代码     — 节点组→Python代码 转换/预览/批量处理 (初始折叠)
    自动排列节点       — Sugiyama算法排列节点 (编辑器菜单栏+快捷键)
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

from . import node_to_code
from . import node_preview
from . import material_nodes
from . import geo_nodes
from . import 集合实例转材质
from . import 重拓扑

try:
    from . import node_arrange
    HAS_NODE_ARRANGE = True
except Exception as e:
    HAS_NODE_ARRANGE = False
    print(f"[xl_c4d_tool] 自动排列节点模块加载失败: {e}")
    print("[xl_c4d_tool]   不影响其他功能使用")

sub_modules = [
    utils,
    preferences,
    properties,
    operators,
    handlers,
    重拓扑,
    node_to_code,
    node_preview,
    material_nodes,
    geo_nodes,
    集合实例转材质,
    panels,
]
if HAS_NODE_ARRANGE:
    sub_modules.append(node_arrange)


def register():
    for mod in sub_modules:
        mod.register()


def unregister():
    for mod in reversed(sub_modules):
        mod.unregister()
