"""XL 物理天空操作符。"""

from __future__ import annotations

import bpy

from .core import (
    apply_preset_to_nodes,
    apply_preset_to_settings,
    ensure_psa_graph,
    ensure_world,
    load_preset,
)


class WORLD_OT_xl_setup_atmosphere(bpy.types.Operator):
    bl_idname = "world.xl_setup_atmosphere"
    bl_label = "物理天空"
    bl_description = "创建或更新 XL 物理天空节点链，内置 PSA 节点组与中文独立控制"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        world = ensure_world(context)
        settings = world.xl_atmosphere_settings
        ensure_psa_graph(context, settings)
        self.report({"INFO"}, "XL 物理天空已创建/更新")
        return {"FINISHED"}


class WORLD_OT_xl_apply_atmosphere_preset(bpy.types.Operator):
    bl_idname = "world.xl_apply_atmosphere_preset"
    bl_label = "应用天空预设"
    bl_description = "把选中的 PSA 预设应用到 XL 物理天空"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        world = ensure_world(context)
        settings = world.xl_atmosphere_settings
        if not settings.preset or settings.preset == "NONE":
            self.report({"WARNING"}, "没有可用预设")
            return {"CANCELLED"}
        preset_data = load_preset(settings.preset)
        apply_preset_to_settings(settings, preset_data)
        ensure_psa_graph(context, settings)
        apply_preset_to_nodes(context, preset_data)
        self.report({"INFO"}, f"已应用天空预设: {settings.preset}")
        return {"FINISHED"}


class WORLD_OT_xl_refresh_atmosphere(bpy.types.Operator):
    bl_idname = "world.xl_refresh_atmosphere"
    bl_label = "刷新物理天空"
    bl_description = "按当前面板参数重新写入天空节点和太阳"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        world = ensure_world(context)
        ensure_psa_graph(context, world.xl_atmosphere_settings)
        self.report({"INFO"}, "物理天空参数已刷新")
        return {"FINISHED"}


classes = (
    WORLD_OT_xl_setup_atmosphere,
    WORLD_OT_xl_apply_atmosphere_preset,
    WORLD_OT_xl_refresh_atmosphere,
)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)

