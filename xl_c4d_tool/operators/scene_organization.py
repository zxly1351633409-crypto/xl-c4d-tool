"""XL 原生场景整理、环境、材质与建模工具。

这些操作使用 Blender 公共 API 独立实现，用于吸收用户所给参考插件中的通用工作流，
不依赖或复制参考插件代码。
"""

from __future__ import annotations

from mathutils import Vector

import bpy
import bmesh


def _unique_name(base, existing):
    if base not in existing:
        return base
    index = 1
    while f"{base}.{index:03d}" in existing:
        index += 1
    return f"{base}.{index:03d}"


class OBJECT_OT_xl_group_to_empty(bpy.types.Operator):
    bl_idname = "object.xl_group_to_empty"
    bl_label = "分组"
    bl_description = "创建空物体分组并严格保持所选物体的当前位置"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = [obj for obj in context.selected_objects]
        if not objects:
            return {"CANCELLED"}
        center = sum((obj.matrix_world.translation for obj in objects), Vector()) / len(objects)
        empty = bpy.data.objects.new(_unique_name("XL_分组", bpy.data.objects), None)
        empty.empty_display_type = "CUBE"
        empty.empty_display_size = max(0.25, max((obj.dimensions.length for obj in objects), default=1.0) * 0.15)
        context.collection.objects.link(empty)
        empty.location = center
        for obj in objects:
            world = obj.matrix_world.copy()
            obj.parent = empty
            obj.matrix_parent_inverse = empty.matrix_world.inverted()
            obj.matrix_world = world
        for obj in objects:
            obj.select_set(False)
        empty.select_set(True)
        context.view_layer.objects.active = empty
        return {"FINISHED"}


class OBJECT_OT_xl_ungroup_keep_transform(bpy.types.Operator):
    bl_idname = "object.xl_ungroup_keep_transform"
    bl_label = "解组"
    bl_description = "清除所选物体父级并保持当前世界位置、旋转和缩放"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        changed = 0
        for obj in context.selected_objects:
            if obj.parent is None:
                continue
            world = obj.matrix_world.copy()
            obj.parent = None
            obj.matrix_world = world
            changed += 1
        self.report({"INFO"}, f"已解除 {changed} 个物体的父级")
        return {"FINISHED"}


class OBJECT_OT_xl_parent_to_active(bpy.types.Operator):
    bl_idname = "object.xl_parent_to_active"
    bl_label = "设父级"
    bl_description = "把其他所选物体设为活动物体的子级并保持世界变换"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        parent = context.active_object
        if parent is None:
            return {"CANCELLED"}
        for obj in context.selected_objects:
            if obj == parent:
                continue
            world = obj.matrix_world.copy()
            obj.parent = parent
            obj.matrix_world = world
        return {"FINISHED"}


class OBJECT_OT_xl_collection_from_selection(bpy.types.Operator):
    bl_idname = "object.xl_collection_from_selection"
    bl_label = "建集合"
    bl_description = "新建集合并把所选物体移动进去，同时从原集合移除"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = list(context.selected_objects)
        if not objects:
            return {"CANCELLED"}
        collection = bpy.data.collections.new(_unique_name("XL_集合", bpy.data.collections))
        context.scene.collection.children.link(collection)
        for obj in objects:
            old_collections = list(obj.users_collection)
            if collection.objects.get(obj.name) is None:
                collection.objects.link(obj)
            for old_collection in old_collections:
                if old_collection != collection and old_collection.objects.get(obj.name) is not None:
                    old_collection.objects.unlink(obj)
        collection.color_tag = "COLOR_05"
        self.report({"INFO"}, f"已把 {len(objects)} 个物体移动到 {collection.name}")
        return {"FINISHED"}


class OBJECT_OT_xl_toggle_display_mode(bpy.types.Operator):
    bl_idname = "object.xl_toggle_display_mode"
    bl_label = "线框切换"
    bl_description = "在所选物体的线框与实体显示间切换，并同步名称显示"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for obj in context.selected_objects:
            wire = obj.display_type != "WIRE"
            obj.display_type = "WIRE" if wire else "TEXTURED"
            obj.show_name = wire
            obj.show_wire = wire
        return {"FINISHED"}


class MESH_OT_xl_smart_extrude(bpy.types.Operator):
    """智能挤出（自研 bmesh 实现，吸收参考插件交互逻辑，不复制其代码）。

    参照 C4D / Smart Extrude 的行为：
      - 沿法向挤出所选面（整体平均法向 或 各自法向）；
      - 单位修复：距离以场景长度单位输入（unit='LENGTH'，自动按 scale_length 换算）；
      - 翻转方向；
      - 仅流形：删除挤出后留在内部的原面，保持网格干净/水密（C4D 挖洞观感）；
      - 智能清理：按阈值合并重合顶点（等效原生自动合并）。
    交互：执行后用 F9 重做面板（含单位输入框）即时调距离/选项。
    """

    bl_idname = "mesh.xl_smart_extrude"
    bl_label = "智能挤出"
    bl_description = "沿法向智能挤出所选面：整体/各自法向、翻转、仅流形清理、按场景单位输入距离"
    bl_options = {"REGISTER", "UNDO"}

    distance: bpy.props.FloatProperty(
        name="距离",
        description="沿法向的挤出距离（按场景长度单位输入，自动换算）",
        default=1.0,
        unit="LENGTH",
    )
    mode: bpy.props.EnumProperty(
        name="法向模式",
        description="整体=沿所选面平均法向一起挤出；各自=每个面沿自身法向独立挤出",
        items=[
            ("REGION", "整体法向", "所有选中面作为一个区域，沿平均法向一起挤出"),
            ("INDIVIDUAL", "各自法向", "每个选中面沿自身法向独立挤出（适合曲面、多朝向面）"),
        ],
        default="REGION",
    )
    flip: bpy.props.BoolProperty(
        name="翻转方向",
        description="反向挤出（向内/向下）",
        default=False,
    )
    only_manifold: bpy.props.BoolProperty(
        name="仅流形(删内壁)",
        description="删除挤出后留在内部的原面，保持网格水密干净（关闭则保留原面=经典挤出）",
        default=True,
    )
    merge_distance: bpy.props.FloatProperty(
        name="合并阈值",
        description="挤出后按此距离合并重合顶点，自动清理重叠几何（智能清理）",
        default=0.0001,
        min=0.0,
        unit="LENGTH",
        precision=5,
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and context.mode == "EDIT_MESH"

    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        sel_faces = [f for f in bm.faces if f.select]
        if not sel_faces:
            self.report({"WARNING"}, "未选择任何面")
            return {"CANCELLED"}

        d = -self.distance if self.flip else self.distance

        if self.mode == "INDIVIDUAL":
            res = bmesh.ops.extrude_discrete_faces(bm, faces=sel_faces)
            new_faces = res["faces"]
            for f in new_faces:
                f.normal_update()
                vec = f.normal * d
                for v in f.verts:
                    v.co += vec
            new_sel = new_faces
        else:
            avg = Vector((0.0, 0.0, 0.0))
            for f in sel_faces:
                avg += f.normal
            if avg.length > 1e-9:
                avg.normalize()
            res = bmesh.ops.extrude_face_region(bm, geom=sel_faces)
            new_verts = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
            new_faces = [e for e in res["geom"] if isinstance(e, bmesh.types.BMFace)]
            bmesh.ops.translate(bm, verts=new_verts, vec=avg * d)
            if self.only_manifold:
                bmesh.ops.delete(bm, geom=sel_faces, context="FACES_ONLY")
            new_sel = new_faces

        if self.merge_distance > 0.0:
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=self.merge_distance)

        for f in bm.faces:
            f.select = False
        for f in new_sel:
            if f.is_valid:
                f.select = True
        bm.normal_update()
        bmesh.update_edit_mesh(me)
        return {"FINISHED"}

    def invoke(self, context, _event):
        # 立即按当前距离执行；用户用 F9 重做面板（含单位框）即时微调
        return self.execute(context)


class NODE_OT_xl_toggle_preview(bpy.types.Operator):
    bl_idname = "node.xl_toggle_preview"
    bl_label = "切换节点预览"
    bl_description = "切换所选节点自身支持的预览区域"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        nodes = getattr(context, "selected_nodes", ())
        changed = 0
        for node in nodes:
            if hasattr(node, "show_preview"):
                node.show_preview = not node.show_preview
                changed += 1
        self.report({"INFO"}, f"已切换 {changed} 个节点预览")
        return {"FINISHED"}


def draw_node_preview_menu(self, context):
    if getattr(context, "selected_nodes", None):
        self.layout.operator(NODE_OT_xl_toggle_preview.bl_idname, icon="IMAGE_DATA")


classes = (
    OBJECT_OT_xl_group_to_empty, OBJECT_OT_xl_ungroup_keep_transform,
    OBJECT_OT_xl_parent_to_active, OBJECT_OT_xl_collection_from_selection,
    OBJECT_OT_xl_toggle_display_mode,
    MESH_OT_xl_smart_extrude, NODE_OT_xl_toggle_preview,
)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    bpy.types.NODE_MT_context_menu.append(draw_node_preview_menu)


def unregister():
    try:
        bpy.types.NODE_MT_context_menu.remove(draw_node_preview_menu)
    except (ValueError, RuntimeError):
        pass
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
