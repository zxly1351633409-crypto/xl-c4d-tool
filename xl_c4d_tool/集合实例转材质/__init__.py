"""集合实例转材质模块
将选中的集合实例自动转为可上材质的几何节点平面
"""
from . import operators


def register():
    operators.register()


def unregister():
    operators.unregister()
