"""【面板：c4d_材质节点助手】
位置：Node Editor > Sidebar > c4d小工具（仅着色器编辑器可用）
功能：快速添加OC/C4D/BL风格材质节点组，2列布局"""
import bpy
from .operators import (
    NODE_OT_xl_add_oc_dirt,
    NODE_OT_xl_add_oc_curvature,
    NODE_OT_xl_add_oc_color_correction,
    NODE_OT_xl_add_oc_falloff,
    NODE_OT_xl_add_oc_gaussian_spectrum,
    NODE_OT_xl_add_c4d_gradient,
    NODE_OT_xl_add_oc_rgbspectrum,
    NODE_OT_xl_add_c4d_cloud_layer,
)
from .cycles_operators import OP_DEFS


_CY_CATEGORIES = [
    ("BL_金属", [0, 1, 2, 3, 4, 5], 'MATPLANE'),
    ("BL_油漆", [6, 7, 8, 9, 10, 11], 'BRUSH_DATA'),
    ("BL_玻璃", [12, 13, 14], 'SHADING_BBOX'),
    ("BL_塑料/橡胶", [15, 16, 17], 'MESH_CYLINDER'),
    ("BL_生锈/边缘", [18, 19], 'EDGESEL'),
    ("BL_脏污", [20, 21], 'MATERIAL'),
    ("BL_凹凸", [22], 'MOD_BUILD'),
    ("BL_迷彩", [23, 24, 25, 26], 'COLOR'),
]


class NODE_PT_xl_material_assistant(bpy.types.Panel):
    bl_label = "c4d_材质节点助手"
    bl_idname = "NODE_PT_xl_material_assistant"
    bl_description = "快速添加Cycles材质节点组（金属/油漆/玻璃/塑料/橡胶/生锈/边缘/脏污/迷彩）及Octane纹理效果节点"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "c4d小工具"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'NODE_EDITOR' and context.space_data.tree_type is not None

    def draw(self, context):
        layout = self.layout
        props = context.scene.xl_c4d_tool_props
        tree_type = context.space_data.tree_type

        if tree_type != 'ShaderNodeTree':
            box = layout.box()
            box.label(text="⚠ 此面板仅对着色器编辑器有效", icon='ERROR')
            return

        layout.prop(props, "material_nodes_folded", text="", icon='RIGHTARROW' if props.material_nodes_folded else 'DOWNARROW_HLT', emboss=False, toggle=True)
        if props.material_nodes_folded:
            return

        if context.object is None:
            layout.label(text="请先选择物体", icon="ERROR")
            return

        # C4D 云层 - 可折叠
        header, panel = layout.panel("c4d_cloud_layer", default_closed=False)
        header.label(text="C4D_云层", icon='MOD_NOISE')
        if panel:
            grid = panel.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
            grid.operator(NODE_OT_xl_add_c4d_cloud_layer.bl_idname, text="云层材质", icon="MOD_NOISE")

        if not getattr(context.object, "active_material", None):
            layout.label(text="其他材质节点需要先添加材质", icon="INFO")
            return

        # OC 纹理效果 - 可折叠
        header, panel = layout.panel("oc_texture", default_closed=True)
        header.label(text="OC_纹理效果", icon='TEXTURE')
        if panel:
            grid = panel.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
            grid.operator(NODE_OT_xl_add_oc_dirt.bl_idname, text="污渍", icon="MOD_NOISE")
            grid.operator(NODE_OT_xl_add_oc_curvature.bl_idname, text="曲率", icon="SMOOTHCURVE")
            grid.operator(NODE_OT_xl_add_oc_falloff.bl_idname, text="衰减", icon="SPHERECURVE")

        # OC 颜色处理 - 可折叠
        header, panel = layout.panel("oc_color", default_closed=True)
        header.label(text="OC_颜色处理", icon='COLOR')
        if panel:
            grid = panel.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
            grid.operator(NODE_OT_xl_add_oc_color_correction.bl_idname, text="颜色校正", icon="COLOR")
            grid.operator(NODE_OT_xl_add_oc_gaussian_spectrum.bl_idname, text="高斯光谱", icon="LIGHT_SUN")
            grid.operator(NODE_OT_xl_add_oc_rgbspectrum.bl_idname, text="RGB光谱", icon="COLOR")
            grid.operator(NODE_OT_xl_add_c4d_gradient.bl_idname, text="渐变", icon="COLOR")

        # BL 类别 - 可折叠
        for cat_name, indices, icon_name in _CY_CATEGORIES:
            header, panel = layout.panel(f"bl_{cat_name}", default_closed=True)
            header.label(text=cat_name, icon=icon_name)
            if panel:
                grid = panel.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
                for idx in indices:
                    bl_idname, bl_label, bl_desc, _ = OP_DEFS[idx]
                    display_name = bl_label.replace("BL_", "")
                    grid.operator(bl_idname, text=display_name)

        # 节点交互控件 — 点击已创建的OC节点后在N面板显示操作控件
        active_node = context.active_node
        if active_node and active_node.type == "GROUP" and active_node.node_tree:
            nt_name = active_node.node_tree.name
            if "C4D_渐变" in nt_name:
                box = layout.box()
                box.label(text="C4D 渐变设置:", icon='NODE_TEXTURE')
                box.prop(active_node, "xl_c4d_gradient_type", text="投影类型")
                ramp = active_node.node_tree.nodes.get("C4D_Gradient_Ramp")
                if ramp:
                    box.template_color_ramp(ramp, "color_ramp")
            elif "高斯光谱" in nt_name:
                box = layout.box()
                box.label(text="光谱图预览:", icon='COLOR')
                ramp = active_node.node_tree.nodes.get("Spectrum_Ramp")
                if ramp:
                    box.template_color_ramp(ramp, "color_ramp")
            elif "RGB光谱" in nt_name:
                box = layout.box()
                box.label(text="RGB 颜色设置:", icon='COLOR')
                rgb_node = active_node.node_tree.nodes.get("RGB")
                if rgb_node:
                    box.template_color_picker(rgb_node.outputs[0], "default_value", value_slider=True)
                    box.prop(active_node, "xl_rgbspectrum_preset", text="预设", icon='PRESET')

classes = (
    NODE_PT_xl_material_assistant,
)
