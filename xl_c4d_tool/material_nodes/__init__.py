"""【入口模块：材质节点助手】材质节点组注册与注销"""
import bpy
from . import operators
from . import panel
from . import properties
from . import cycles_operators


def register():
    properties.register()
    for cls in operators.classes + panel.classes + cycles_operators.cy_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(operators.classes + panel.classes + cycles_operators.cy_classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    properties.unregister()
