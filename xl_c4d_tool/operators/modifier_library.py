"""将 C4D 节点组作为几何节点修改器赋予所选对象。"""

from __future__ import annotations

import bpy
from bpy.props import StringProperty

from ..handlers.boolean_display import update_boolean_operand_display
from ..utils.modifier_library import ensure_node_group


SUPPORTED_OBJECT_TYPES = {"MESH", "CURVE", "FONT", "SURFACE", "POINTCLOUD", "VOLUME"}


class OBJECT_OT_xl_apply_c4d_node_group(bpy.types.Operator):
    bl_idname = "object.xl_apply_c4d_node_group"
    bl_label = "赋予 C4D 节点组"
    bl_description = "把所选节点组作为几何节点修改器添加到所有已选对象"
    bl_options = {"REGISTER", "UNDO"}

    group_name: StringProperty(name="节点组")
    tooltip: StringProperty(options={"HIDDEN"})

    @classmethod
    def description(cls, _context, properties):
        return properties.tooltip or cls.bl_description

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and any(
            obj.type in SUPPORTED_OBJECT_TYPES for obj in context.selected_objects
        )

    def execute(self, context):
        targets = [obj for obj in context.selected_objects if obj.type in SUPPORTED_OBJECT_TYPES]
        active = context.view_layer.objects.active
        try:
            group = ensure_node_group(self.group_name)
        except (OSError, RuntimeError) as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        applied = 0
        for obj in targets:
            modifier = obj.modifiers.new(name=group.name.replace("XL_", "", 1), type="NODES")
            modifier.node_group = group
            applied += 1

        for obj in targets:
            obj.select_set(True)
        if active is not None and active.name in context.view_layer.objects:
            context.view_layer.objects.active = active

        if not applied:
            self.report({"WARNING"}, "请选择网格、曲线、文字、曲面、点云或体积对象")
            return {"CANCELLED"}

        update_boolean_operand_display()
        self.report({"INFO"}, f"已为 {applied} 个对象添加：{group.name}")
        return {"FINISHED"}


class OBJECT_OT_xl_duplicate_modifier(bpy.types.Operator):
    bl_idname = "object.xl_duplicate_modifier"
    bl_label = "复制修改器"
    bl_description = "复制当前修改器并保留所有节点接口参数"
    bl_options = {"REGISTER", "UNDO"}

    modifier_name: StringProperty()

    def execute(self, context):
        obj = context.active_object
        source = obj.modifiers.get(self.modifier_name) if obj else None
        if source is None:
            return {"CANCELLED"}
        try:
            with context.temp_override(object=obj, active_object=obj):
                bpy.ops.object.modifier_copy(modifier=source.name)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class PREFERENCES_OT_xl_open_addon(bpy.types.Operator):
    bl_idname = "preferences.xl_open_addon"
    bl_label = "打开插件偏好设置"
    bl_description = "打开 Blender 偏好设置；搜索 xl_c4d_tool 可调整节点浏览器"

    def execute(self, _context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        return {"FINISHED"}


classes = (
    OBJECT_OT_xl_apply_c4d_node_group,
    OBJECT_OT_xl_duplicate_modifier,
    PREFERENCES_OT_xl_open_addon,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
