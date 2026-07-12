"""XL 四边重拓扑：QRemeshify/QuadWild 的中文安全封装。"""

from __future__ import annotations

import math
import os
from pathlib import Path

import bmesh
import bpy
import mathutils

from .vendor_qremeshify.lib import Quadwild, QWException
from .vendor_qremeshify.util import bisect, exporter, importer


bl_info = {
    "name": "XL 四边重拓扑",
    "description": "基于 QuadWild/QuadPatches 的离线四边面重拓扑",
    "author": "XL C4D Replication Project; QRemeshify by ksami",
    "version": (0, 1, 0),
    "blender": (5, 1, 0),
    "location": "3D 视图 > 侧栏 > C4D工具 > XL 四边重拓扑",
    "category": "Mesh",
}


def _quality_preset_update(self, _context):
    values = {
        "PREVIEW": (True, False, True, 1.8, 25),
        "BALANCED": (True, True, True, 1.0, 90),
        "DETAIL": (True, True, True, 0.55, 240),
    }.get(self.quality_preset)
    if values is None:
        return
    self.preprocess, self.smoothing, self.detect_sharp, self.density, self.solver_time = values


class XLRT_Properties(bpy.types.PropertyGroup):
    quality_preset: bpy.props.EnumProperty(
        name="质量预设",
        description="按用途设置面尺寸、平滑与求解时间；选自定义可逐项调整",
        items=(
            ("PREVIEW", "快速预览", "更大的四边面与短时求解，先检查流向"),
            ("BALANCED", "均衡", "适合大多数模型的质量与速度平衡"),
            ("DETAIL", "细节优先", "保留更多曲面细节，耗时与面数更高"),
            ("CUSTOM", "自定义", "保留下面的手动参数"),
        ),
        default="BALANCED",
        update=_quality_preset_update,
    )
    preprocess: bpy.props.BoolProperty(
        name="预处理",
        description="先修复、简化并三角化输入，适合大多数网格",
        default=True,
    )
    smoothing: bpy.props.BoolProperty(
        name="结果平滑",
        description="四边化后执行表面平滑与回投影",
        default=True,
    )
    detect_sharp: bpy.props.BoolProperty(
        name="保留锐边",
        description="识别角度、边界、缝合边、材质边界和雕刻面组边界",
        default=True,
    )
    sharp_angle: bpy.props.FloatProperty(
        name="锐边角度",
        description="超过该夹角的边作为重拓扑方向约束",
        subtype="ANGLE",
        default=math.radians(35.0),
        min=0.0,
        max=math.pi,
    )
    density: bpy.props.FloatProperty(
        name="面尺寸倍率",
        description="1 为均衡；大于 1 面更大更少，小于 1 面更小更多",
        default=1.0,
        min=0.05,
        max=10.0,
        soft_min=0.25,
        soft_max=4.0,
    )
    apply_modifiers: bpy.props.BoolProperty(
        name="包含当前修改器",
        description="以视口中修改器计算后的形体作为重拓扑输入；原修改器不会被应用或删除",
        default=True,
    )
    symmetry_x: bpy.props.BoolProperty(name="X", description="只计算X轴正侧并添加镜像", default=False)
    symmetry_y: bpy.props.BoolProperty(name="Y", description="只计算Y轴正侧并添加镜像", default=False)
    symmetry_z: bpy.props.BoolProperty(name="Z", description="只计算Z轴正侧并添加镜像", default=False)
    hide_original: bpy.props.BoolProperty(
        name="隐藏原物体",
        description="成功生成后隐藏原始对象；原网格不会被删除",
        default=True,
    )
    use_cache: bpy.props.BoolProperty(
        name="仅重算四边化",
        description="复用同名对象上次的方向场和路径缓存；修改网格后请关闭",
        default=False,
    )
    output_suffix: bpy.props.StringProperty(
        name="输出后缀",
        description="生成对象名称后缀",
        default="四边重拓扑",
    )
    solver_time: bpy.props.IntProperty(
        name="求解时限",
        description="整数优化的最大时间；低模通常远低于此值（QRemeshify 默认 200）",
        default=200,
        min=5,
        max=3600,
        subtype="TIME",
    )
    show_advanced: bpy.props.BoolProperty(
        name="高级设置",
        description="显示缓存、求解时限和输出命名",
        default=False,
    )


def _safe_mesh_name(name: str) -> str:
    clean = "".join("_" if c in "\\/:*?<>|" else c for c in name).strip()
    return clean or "XL_Retopology"


def _count_faces(mesh: bpy.types.Mesh) -> dict[str, int]:
    counts = {"tri": 0, "quad": 0, "ngon": 0}
    for poly in mesh.polygons:
        size = len(poly.vertices)
        if size == 3:
            counts["tri"] += 1
        elif size == 4:
            counts["quad"] += 1
        else:
            counts["ngon"] += 1
    return counts


class XLRT_OT_quad_remesh(bpy.types.Operator):
    """将活动网格离线重拓扑为以四边面为主的新对象"""

    bl_idname = "object.xl_quad_remesh"
    bl_label = "生成四边重拓扑"
    bl_description = "运行 QuadWild/QuadPatches；原物体始终保留"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and context.mode == "OBJECT"

    def execute(self, context):
        props = context.scene.xlrt_props
        obj = context.active_object
        if obj is None or obj.type != "MESH" or not obj.data.polygons:
            self.report({"ERROR"}, "请选择一个包含面的网格对象")
            return {"CANCELLED"}

        sharp_degrees = math.degrees(props.sharp_angle)
        mesh_path = os.path.join(bpy.app.tempdir, f"XL_{_safe_mesh_name(obj.name)}.obj")
        engine = Quadwild(mesh_path)
        bm = None
        evaluated_obj = None
        try:
            if not props.use_cache:
                if props.apply_modifiers:
                    depsgraph = context.evaluated_depsgraph_get()
                    evaluated_obj = obj.evaluated_get(depsgraph)
                    evaluated_mesh = evaluated_obj.to_mesh()
                    transform_obj = evaluated_obj
                else:
                    evaluated_mesh = obj.data
                    transform_obj = obj
                bm = bmesh.new()
                bm.from_mesh(evaluated_mesh)

                if transform_obj.rotation_mode == "QUATERNION":
                    rot = transform_obj.rotation_quaternion
                else:
                    rot = transform_obj.rotation_euler
                matrix = mathutils.Matrix.LocRotScale(None, rot, transform_obj.scale)
                bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)

                if props.symmetry_x or props.symmetry_y or props.symmetry_z:
                    bisect.bisect_on_axes(bm, props.symmetry_x, props.symmetry_y, props.symmetry_z)

                if props.detect_sharp:
                    face_sets = bm.faces.layers.int.get(".sculpt_face_set")
                    bm.edges.ensure_lookup_table()
                    for edge in bm.edges:
                        angle_sharp = math.degrees(edge.calc_face_angle(0.0)) > sharp_degrees
                        material_boundary = (
                            len(edge.link_faces) > 1
                            and edge.link_faces[0].material_index != edge.link_faces[1].material_index
                        )
                        face_set_boundary = (
                            face_sets is not None
                            and len(edge.link_faces) > 1
                            and edge.link_faces[0][face_sets] != edge.link_faces[1][face_sets]
                        )
                        if angle_sharp or edge.is_boundary or edge.seam or material_boundary or face_set_boundary:
                            edge.smooth = False

                # 注意：随包的 QuadWild 构建要求输入为纯三角网格，即使开启预处理，
                # remeshAndField 也需要先三角化，否则会报 "remeshAndField failed"。
                bmesh.ops.triangulate(bm, faces=list(bm.faces), quad_method="SHORT_EDGE", ngon_method="BEAUTY")
                exporter.export_mesh(bm, mesh_path)
                if props.detect_sharp:
                    exporter.export_sharp_features(bm, engine.sharp_path, sharp_degrees)

                engine.remeshAndField(props.preprocess, props.detect_sharp, sharp_degrees)
                if not engine.trace():
                    raise QWException("方向场路径追踪失败")

            result_code = engine.quadrangulate(
                props.smoothing,
                props.density,
                0,
                0.005,
                "LEASTSQUARES",
                props.solver_time,
                0.0,
                0.4,
                True,
                True,
                True,
                0.9,
                True,
                0.1,
                True,
                False,
                False,
                True,
                True,
                "SIMPLE",
                "DEFAULT",
                [3.0, 5.0, 10.0, 20.0, 30.0, 60.0, 90.0, 120.0],
                [0.005, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
            )
            if result_code < 0:
                raise QWException(f"四边化求解返回错误码 {result_code}")

            final_path = engine.output_smoothed_path if props.smoothing else engine.output_path
            final_mesh = importer.import_mesh(final_path)
            final_mesh.name = f"{obj.data.name}_{props.output_suffix}"
            if props.smoothing:
                for polygon in final_mesh.polygons:
                    polygon.use_smooth = True
            final_obj = bpy.data.objects.new(f"{obj.name}_{props.output_suffix}", final_mesh)
            target_collections = list(obj.users_collection) or [context.collection]
            for collection in target_collections:
                collection.objects.link(final_obj)
            final_obj.location = obj.location

            for slot in obj.material_slots:
                if slot.material is not None:
                    final_mesh.materials.append(slot.material)

            if props.symmetry_x or props.symmetry_y or props.symmetry_z:
                mirror = final_obj.modifiers.new("重拓扑对称", "MIRROR")
                mirror.use_axis[0] = props.symmetry_x
                mirror.use_axis[1] = props.symmetry_y
                mirror.use_axis[2] = props.symmetry_z
                mirror.use_clip = True
                mirror.merge_threshold = 0.001

            for selected in list(context.selected_objects):
                selected.select_set(False)
            final_obj.select_set(True)
            context.view_layer.objects.active = final_obj
            if props.hide_original:
                obj.hide_set(True)

            counts = _count_faces(final_mesh)
            self.report(
                {"INFO"},
                f"完成：{len(final_mesh.vertices)}点 / {len(final_mesh.polygons)}面，"
                f"四边面 {counts['quad']}，三角面 {counts['tri']}，N边面 {counts['ngon']}",
            )
            return {"FINISHED"}
        except (QWException, OSError, RuntimeError, ValueError) as exc:
            self.report({"ERROR"}, f"四边重拓扑失败：{exc}")
            return {"CANCELLED"}
        finally:
            if bm is not None:
                bm.free()
            if evaluated_obj is not None:
                evaluated_obj.to_mesh_clear()


def _draw_retopology_settings(layout, props):
    layout.use_property_split = True
    layout.use_property_decorate = False

    general = layout.box()
    general.label(text="① 质量与输入", icon="MESH_GRID")
    general.prop(props, "quality_preset")
    general.prop(props, "apply_modifiers")
    general.prop(props, "preprocess")
    general.prop(props, "smoothing")
    general.prop(props, "density")
    general.label(text="倍率越小，四边面越密；建议先用“快速预览”检查流向", icon="INFO")

    sharp = layout.box()
    sharp.label(text="② 特征与对称", icon="MOD_EDGESPLIT")
    sharp.prop(props, "detect_sharp")
    if props.detect_sharp:
        sharp.prop(props, "sharp_angle")
    row = sharp.row(align=True)
    row.prop(props, "symmetry_x", toggle=True)
    row.prop(props, "symmetry_y", toggle=True)
    row.prop(props, "symmetry_z", toggle=True)

    output = layout.box()
    output.label(text="③ 输出", icon="OUTPUT")
    output.prop(props, "hide_original")
    output.prop(props, "show_advanced", toggle=True)
    if props.show_advanced:
        output.prop(props, "output_suffix")
        output.prop(props, "use_cache")
        output.prop(props, "solver_time")
        output.label(text="仅重算四边化只适用于源网格未改变的再次求解", icon="INFO")
    layout.label(text="一次性工具；生成新对象，不删除原网格", icon="INFO")


class XLRT_OT_open_dialog(bpy.types.Operator):
    """打开四边重拓扑设置，确认后开始求解"""

    bl_idname = "object.xlrt_open_dialog"
    bl_label = "XL 四边重拓扑"
    bl_description = "打开四边重拓扑设置；确认后运行 QuadWild/QuadPatches"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return XLRT_OT_quad_remesh.poll(context)

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(
            self,
            width=440,
            title="XL 四边重拓扑",
            confirm_text="开始重拓扑",
        )

    def draw(self, context):
        _draw_retopology_settings(self.layout, context.scene.xlrt_props)

    def execute(self, _context):
        return bpy.ops.object.xl_quad_remesh()


class XLRT_PT_main(bpy.types.Panel):
    bl_idname = "XLRT_PT_main"
    bl_label = "XL 四边重拓扑"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "C4D工具"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def draw(self, context):
        layout = self.layout
        props = context.scene.xlrt_props
        _draw_retopology_settings(layout, props)
        layout.operator(XLRT_OT_quad_remesh.bl_idname, icon="MESH_GRID")


CLASSES = (XLRT_Properties, XLRT_OT_quad_remesh, XLRT_OT_open_dialog)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.xlrt_props = bpy.props.PointerProperty(type=XLRT_Properties)


def unregister():
    if hasattr(bpy.types.Scene, "xlrt_props"):
        del bpy.types.Scene.xlrt_props
    for cls in reversed(CLASSES):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
