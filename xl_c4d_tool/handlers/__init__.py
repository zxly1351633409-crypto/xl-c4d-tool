"""插件持久化处理器。"""

from . import boolean_display


def register():
    boolean_display.register()


def unregister():
    boolean_display.unregister()
