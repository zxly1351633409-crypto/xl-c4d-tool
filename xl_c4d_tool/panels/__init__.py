"""【入口模块：面板】统一注册所有面板
- main_panel: 3D View > c4d小工具 (效果/C4D工具/节点设置)
- node_panel: Node Editor > 快捷节点 / c4d小工具"""
from .main_panel import register as register_main, unregister as unregister_main
from .node_panel import register as register_node, unregister as unregister_node


def register():
    register_main()
    register_node()


def unregister():
    unregister_node()
    unregister_main()
