"""【入口模块：几何节点助手】放样节点组注册与注销"""
from . import panel
from . import operators


def register():
    operators.register()
    panel.register()


def unregister():
    panel.unregister()
    operators.unregister()
