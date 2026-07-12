import bpy
import os
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from .batch import (
    batch_process_current_editor,
    batch_process_current_file,
    batch_process_blend_file,
    preview_current_editor,
)
from .generator import generate_group_code
from .parser import parse_current_editor_group


class NODE2CODE_OT_preview(bpy.types.Operator):
    """【操作符：预览代码】
    功能：预览当前节点编辑器中节点组的Python代码"""
    bl_idname = "node2code.preview"
    bl_label = "预览代码"
    bl_description = "预览当前节点编辑器中节点组的Python代码"

    def execute(self, context):
        code, err = preview_current_editor()
        if err:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}
        props = context.scene.node_to_code_props
        props.preview_code = code
        props.status_message = "预览已生成"
        self.report({'INFO'}, "代码预览已生成")
        return {'FINISHED'}


class NODE2CODE_OT_convert_current(bpy.types.Operator):
    """【操作符：转换当前节点组】
    功能：将当前节点编辑器中的节点组转为Python代码并保存"""
    bl_idname = "node2code.convert_current"
    bl_label = "转换当前节点组"
    bl_description = "将当前节点编辑器中的节点组转为Python代码并保存"

    def execute(self, context):
        props = context.scene.node_to_code_props
        output_dir = props.output_path
        if not output_dir:
            self.report({'ERROR'}, "请先设置输出路径")
            return {'CANCELLED'}
        success, msg = batch_process_current_editor(output_dir)
        if not success:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}
        props.status_message = msg
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class NODE2CODE_OT_convert_all(bpy.types.Operator):
    """【操作符：转换当前文件所有节点组】
    功能：将当前.blend文件中所有节点组转为Python代码"""
    bl_idname = "node2code.convert_all"
    bl_label = "转换当前文件所有节点组"
    bl_description = "将当前.blend文件中所有节点组转为Python代码并保存"

    def execute(self, context):
        props = context.scene.node_to_code_props
        output_dir = props.output_path
        if not output_dir:
            self.report({'ERROR'}, "请先设置输出路径")
            return {'CANCELLED'}
        success, msg = batch_process_current_file(output_dir)
        if not success:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}
        props.status_message = msg
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class NODE2CODE_OT_convert_blend(bpy.types.Operator, ImportHelper):
    """【操作符：选择Blend文件批量转换】
    功能：选择一个.blend文件，转换其中所有节点组"""
    bl_idname = "node2code.convert_blend"
    bl_label = "选择Blend文件批量转换"
    bl_description = "选择一个.blend文件，转换其中所有节点组"
    filename_ext = ".blend"
    filter_glob: StringProperty(default="*.blend", options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.node_to_code_props
        output_dir = props.output_path
        if not output_dir:
            self.report({'ERROR'}, "请先设置输出路径")
            return {'CANCELLED'}
        success, msg = batch_process_blend_file(self.filepath, output_dir)
        if not success:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}
        props.status_message = msg
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class NODE2CODE_OT_open_output_dir(bpy.types.Operator):
    """【操作符：打开输出目录】
    功能：在文件管理器中打开输出目录"""
    bl_idname = "node2code.open_output_dir"
    bl_label = "打开输出目录"
    bl_description = "在文件管理器中打开输出目录"

    def execute(self, context):
        props = context.scene.node_to_code_props
        output_dir = props.output_path
        if not output_dir or not os.path.isdir(output_dir):
            self.report({'ERROR'}, "输出目录不存在")
            return {'CANCELLED'}
        import subprocess
        import platform
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(f'explorer "{output_dir}"')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', output_dir])
            else:
                subprocess.Popen(['xdg-open', output_dir])
        except Exception as e:
            self.report({'ERROR'}, f"无法打开目录: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}


classes = (
    NODE2CODE_OT_preview,
    NODE2CODE_OT_convert_current,
    NODE2CODE_OT_convert_all,
    NODE2CODE_OT_convert_blend,
    NODE2CODE_OT_open_output_dir,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
