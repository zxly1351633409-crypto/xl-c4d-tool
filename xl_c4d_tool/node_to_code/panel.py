"""【面板：任意节点转代码】
将Blender节点组转为Python代码，含注释解析，可还原为节点组
位置：Node Editor > Sidebar > c4d小工具"""
import bpy
from .operators import (
    NODE2CODE_OT_preview,
    NODE2CODE_OT_convert_current,
    NODE2CODE_OT_convert_all,
    NODE2CODE_OT_convert_blend,
    NODE2CODE_OT_open_output_dir,
)


class NodeToCodeProperties(bpy.types.PropertyGroup):
    """【属性组：节点转代码配置】
    保存：输出路径、代码预览、状态消息"""
    output_path: bpy.props.StringProperty(
        name="输出路径", description="生成的.py文件保存路径", default="", subtype='DIR_PATH')
    preview_code: bpy.props.StringProperty(
        name="代码预览", description="当前编辑器节点组的代码预览", default="")
    blend_filepath: bpy.props.StringProperty(
        name="Blend文件", description="要批量转换的.blend文件路径", default="", subtype='FILE_PATH')
    status_message: bpy.props.StringProperty(name="状态", default="就绪")


class NODE2CODE_PT_main(bpy.types.Panel):
    """【面板：任意节点转代码】
    将Blender节点组转为Python代码，含注释解析，可还原为节点"""
    bl_label = "任意节点转代码"
    bl_idname = "NODE2CODE_PT_main"
    bl_description = "将Blender节点组转为Python代码（含注释/色标/嵌套组），可还原为节点"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "c4d小工具"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.xl_c4d_tool_props
        code_props = context.scene.node_to_code_props

        col = layout.column()
        col.prop(props, "node_to_code_folded", text="展开设置", icon='RIGHTARROW' if props.node_to_code_folded else 'DOWNARROW_HLT', emboss=False, toggle=True)

        if props.node_to_code_folded:
            return

        box = layout.box()
        box.label(text="输出设置", icon='FILE_FOLDER')
        box.prop(code_props, "output_path", text="保存路径")
        if code_props.output_path:
            box.operator(NODE2CODE_OT_open_output_dir.bl_idname, icon='FILE_FOLDER')

        layout.separator()
        box = layout.box()
        box.label(text="当前编辑器", icon='NODETREE')
        box.operator(NODE2CODE_OT_preview.bl_idname, icon='VIEWZOOM')
        box.operator(NODE2CODE_OT_convert_current.bl_idname, icon='EXPORT')

        layout.separator()
        box = layout.box()
        box.label(text="批量转换", icon='FILE_BLEND')
        box.operator(NODE2CODE_OT_convert_all.bl_idname, text="当前文件所有节点组", icon='COLLECTION_NEW')
        box.operator(NODE2CODE_OT_convert_blend.bl_idname, text="选择Blend文件转换", icon='FILEBROWSER')

        if code_props.preview_code:
            layout.separator()
            box = layout.box()
            box.label(text="代码预览", icon='SCRIPT')
            lines = code_props.preview_code.split('\n')
            show_lines = lines[:50]
            for line in show_lines:
                row = box.row()
                row.scale_y = 0.6
                row.label(text=line[:80], icon='NONE')
            if len(lines) > 50:
                box.label(text=f"... 共 {len(lines)} 行 (仅显示前50行)", icon='INFO')

        if code_props.status_message:
            layout.separator()
            layout.label(text=code_props.status_message, icon='CHECKMARK')


classes = (
    NODE2CODE_PT_main,
)


def register():
    bpy.utils.register_class(NodeToCodeProperties)
    if not hasattr(bpy.types.Scene, "node_to_code_props"):
        bpy.types.Scene.node_to_code_props = bpy.props.PointerProperty(type=NodeToCodeProperties)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Scene, "node_to_code_props"):
        del bpy.types.Scene.node_to_code_props
    bpy.utils.unregister_class(NodeToCodeProperties)
