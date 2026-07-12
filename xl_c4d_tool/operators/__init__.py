"""【入口模块：操作符】统一注册所有操作符
- layer_id: 物体ID图效果
- material_id: 材质ID效果
- mist: 雾场效果
- c4d_tools: C4D小工具(样条线/对齐)
- side_add_nodes: 快捷节点搜索与添加"""
from .layer_id import register as register_layer_id, unregister as unregister_layer_id
from .material_id import register as register_material_id, unregister as unregister_material_id
from .mist import register as register_mist, unregister as unregister_mist
from .c4d_tools import register as register_c4d_tools, unregister as unregister_c4d_tools
from .side_add_nodes import register as register_side_add_nodes, unregister as unregister_side_add_nodes
from .modifier_library import register as register_modifier_library, unregister as unregister_modifier_library
from .node_description import register as register_node_description, unregister as unregister_node_description
from .encoding_tools import register as register_encoding_tools, unregister as unregister_encoding_tools
from .scene_organization import register as register_scene_organization, unregister as unregister_scene_organization
from .claymate import register as register_claymate, unregister as unregister_claymate


def register():
    register_layer_id()
    register_material_id()
    register_mist()
    register_c4d_tools()
    register_side_add_nodes()
    register_modifier_library()
    register_node_description()
    register_encoding_tools()
    register_scene_organization()
    register_claymate()


def unregister():
    unregister_claymate()
    unregister_scene_organization()
    unregister_encoding_tools()
    unregister_node_description()
    unregister_modifier_library()
    unregister_side_add_nodes()
    unregister_c4d_tools()
    unregister_mist()
    unregister_material_id()
    unregister_layer_id()
