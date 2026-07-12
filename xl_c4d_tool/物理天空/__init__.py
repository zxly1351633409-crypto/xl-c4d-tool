"""【入口模块：物理天空】PSA 节点组中文包装与独立控制。"""

from . import operators
from . import panel
from . import properties
from . import handlers


def register():
    properties.register()
    operators.register()
    panel.register()
    handlers.register()


def unregister():
    handlers.unregister()
    panel.unregister()
    operators.unregister()
    properties.unregister()
