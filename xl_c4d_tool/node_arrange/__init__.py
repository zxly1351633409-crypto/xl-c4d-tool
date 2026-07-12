"""【入口模块：c4d_自动排列节点】
Sugiyama算法自动排列选中节点，支持批量处理
依赖: networkx（如未安装则跳过排列功能，居中功能不受影响）"""
import bpy

from . import keymaps, operators, properties, ui, context_menu


def register() -> None:
    try:
        properties.register()
    except Exception as e:
        print(f"[xl_c4d_tool] 排列节点属性注册失败: {e}")

    try:
        operators.register()
    except Exception as e:
        print(f"[xl_c4d_tool] 排列节点操作符注册失败: {e}")

    try:
        keymaps.register()
    except Exception as e:
        print(f"[xl_c4d_tool] 排列节点快捷键注册失败: {e}")

    try:
        ui.register()
    except Exception as e:
        print(f"[xl_c4d_tool] 排列节点UI注册失败: {e}")

    try:
        context_menu.register()
    except Exception as e:
        print(f"[xl_c4d_tool] 排列节点菜单注册失败: {e}")

    if not operators.HAS_SUGIYAMA:
        print("[xl_c4d_tool] 提示: networkx 未安装，排列功能将不可用，居中功能正常")
        print("[xl_c4d_tool]   安装方法: pip install networkx")


def unregister() -> None:
    try:
        context_menu.unregister()
    except Exception:
        pass
    try:
        ui.unregister()
    except Exception:
        pass
    try:
        keymaps.unregister()
    except Exception:
        pass
    try:
        operators.unregister()
    except Exception:
        pass
    try:
        properties.unregister()
    except Exception:
        pass
