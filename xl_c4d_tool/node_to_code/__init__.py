"""【入口模块：任意节点转代码】操作符与面板注册"""
from . import operators
from . import panel


def register():
    operators.register()
    panel.register()


def unregister():
    panel.unregister()
    operators.unregister()
