"""C4D 式布尔操作对象显示联动。"""

from __future__ import annotations

import bpy
from bpy.app.handlers import persistent


FLAG = "_xl_c4d_boolean_operand"
ORIGINAL_DISPLAY = "_xl_c4d_boolean_display"
ORIGINAL_NAME = "_xl_c4d_boolean_name"
ORIGINAL_RENDER = "_xl_c4d_boolean_render"
LEGACY_RAY_VISIBILITY = "_xl_c4d_boolean_ray_visibility"
_busy = False
TARGET_PREFIXES = ("XL_布尔", "XL_连接", "XL_融球")
LEGACY_KEYS = ("_xl_wire", "_xl_wire_disp", "_xl_wire_name", "_xl_wire_hr")


def _boolean_operands():
    operands = set()
    for owner in bpy.data.objects:
        for modifier in owner.modifiers:
            group = getattr(modifier, "node_group", None)
            if modifier.type != "NODES" or group is None:
                continue
            if not group.name.startswith(TARGET_PREFIXES) or not modifier.show_viewport:
                continue
            for item in group.interface.items_tree:
                if getattr(item, "item_type", "") != "SOCKET" or item.in_out != "INPUT":
                    continue
                value = modifier.get(item.identifier)
                if item.socket_type == "NodeSocketObject" and value is not None:
                    operands.add(value)
                elif item.socket_type == "NodeSocketCollection" and value is not None:
                    operands.update(value.all_objects)
    return operands


def _restore_legacy_ray_visibility(obj):
    saved = obj.get(LEGACY_RAY_VISIBILITY, {})
    for attr, value in saved.items():
        if hasattr(obj, attr):
            setattr(obj, attr, bool(value))
    if LEGACY_RAY_VISIBILITY in obj:
        del obj[LEGACY_RAY_VISIBILITY]


def update_boolean_operand_display(*_args):
    global _busy
    if _busy:
        return
    _busy = True
    try:
        operands = _boolean_operands()
        for obj in operands:
            if not obj.get(FLAG):
                if obj.get("_xl_wire"):
                    obj[ORIGINAL_DISPLAY] = obj.get("_xl_wire_disp", "SOLID")
                    obj[ORIGINAL_NAME] = bool(obj.get("_xl_wire_name", False))
                    obj[ORIGINAL_RENDER] = bool(obj.get("_xl_wire_hr", False))
                else:
                    obj[ORIGINAL_DISPLAY] = obj.display_type
                    obj[ORIGINAL_NAME] = bool(obj.show_name)
                    obj[ORIGINAL_RENDER] = bool(obj.hide_render)
                obj[FLAG] = True
            elif obj.get("_xl_wire"):
                # 迁移旧 blend 内嵌处理器保存的真实原始状态。
                obj[ORIGINAL_DISPLAY] = obj.get("_xl_wire_disp", obj.get(ORIGINAL_DISPLAY, "SOLID"))
                obj[ORIGINAL_NAME] = bool(obj.get("_xl_wire_name", obj.get(ORIGINAL_NAME, False)))
                obj[ORIGINAL_RENDER] = bool(obj.get("_xl_wire_hr", obj.get(ORIGINAL_RENDER, False)))
            _restore_legacy_ray_visibility(obj)
            obj.display_type = "WIRE"
            obj.show_name = True
            obj.hide_render = True

        for obj in list(bpy.data.objects):
            if not obj.get(FLAG) or obj in operands:
                continue
            obj.display_type = obj.get(ORIGINAL_DISPLAY, "SOLID")
            obj.show_name = bool(obj.get(ORIGINAL_NAME, False))
            obj.hide_render = bool(obj.get(ORIGINAL_RENDER, False))
            _restore_legacy_ray_visibility(obj)
            for key in (FLAG, ORIGINAL_DISPLAY, ORIGINAL_NAME, ORIGINAL_RENDER, *LEGACY_KEYS):
                if key in obj:
                    del obj[key]
    finally:
        _busy = False


@persistent
def _depsgraph_handler(*args):
    update_boolean_operand_display(*args)


@persistent
def _load_handler(*args):
    update_boolean_operand_display(*args)


def register():
    # 兼容旧 blend 内嵌脚本，避免两个同名逻辑互相争用。
    for handler in list(bpy.app.handlers.depsgraph_update_post):
        if getattr(handler, "__name__", "") == "_xl_wire_handler":
            bpy.app.handlers.depsgraph_update_post.remove(handler)
    if _depsgraph_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(_depsgraph_handler)
    if _load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(_load_handler)
    # 插件启用阶段 bpy.data 可能处于 _RestrictData；等待正常上下文的依赖图事件再扫描。


def unregister():
    if _depsgraph_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_depsgraph_handler)
    if _load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_load_handler)
    # 禁用插件时不把操作对象永久留在线框状态。
    for obj in list(bpy.data.objects):
        if obj.get(FLAG):
            obj.display_type = obj.get(ORIGINAL_DISPLAY, "SOLID")
            obj.show_name = bool(obj.get(ORIGINAL_NAME, False))
            obj.hide_render = bool(obj.get(ORIGINAL_RENDER, False))
            _restore_legacy_ray_visibility(obj)
            for key in (FLAG, ORIGINAL_DISPLAY, ORIGINAL_NAME, ORIGINAL_RENDER, *LEGACY_KEYS):
                if key in obj:
                    del obj[key]
