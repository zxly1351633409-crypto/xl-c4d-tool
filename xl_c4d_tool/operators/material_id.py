import bpy
from ..utils.logger import logger
from ..utils.shading import generate_random_color, set_shading_for_all_areas


class OBJECT_OT_material_id_mode(bpy.types.Operator):
    bl_idname = "object.xl_material_id_mode"
    bl_label = "材质ID"
    bl_description = "切换到材质ID效果模式，为所有材质赋予随机视图显示颜色"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.xl_c4d_tool_props
        logger.info("===== 开始材质ID模式设置 =====")

        logger.info("Step 1: 切换视图着色方式")
        show_outline = props.show_object_outline if props else False
        set_shading_for_all_areas(
            context,
            light='FLAT',
            color_type='MATERIAL',
            shading_type='SOLID',
            show_object_outline=show_outline
        )

        logger.info("Step 2: 切换渲染引擎为工作台")
        context.scene.render.engine = 'BLENDER_WORKBENCH'

        logger.info("Step 3: 设置所有材质的视图显示颜色")
        mat_count = 0
        for mat in bpy.data.materials:
            if mat.users > 0:
                color = generate_random_color()
                mat.diffuse_color = (*color, 1.0)
                mat_count += 1
                logger.debug(f"设置材质颜色: {mat.name}")

        if props:
            props.current_mode = 'MATERIAL_ID'

        logger.info(f"===== 材质ID模式设置完成，已处理 {mat_count} 个材质 =====")
        self.report({'INFO'}, f"材质ID模式已激活，已设置 {mat_count} 个材质颜色")
        return {'FINISHED'}


class OBJECT_OT_normal_from_material_id(bpy.types.Operator):
    bl_idname = "object.xl_normal_from_material_id"
    bl_label = "正常"
    bl_description = "从材质ID模式切换回正常视图模式"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.xl_c4d_tool_props
        logger.info("===== 从材质ID模式切换回正常模式 =====")

        set_shading_for_all_areas(
            context,
            light='STUDIO',
            color_type='OBJECT',
            shading_type='SOLID',
            show_object_outline=False
        )

        context.scene.render.engine = 'CYCLES'
        logger.info("渲染引擎切换为CYCLES")

        if props:
            props.current_mode = 'NORMAL'

        logger.info("===== 切换回正常模式完成 =====")
        self.report({'INFO'}, "已切换回正常视图模式")
        return {'FINISHED'}


classes = [
    OBJECT_OT_material_id_mode,
    OBJECT_OT_normal_from_material_id,
]


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    logger.info("材质ID操作符注册完成")


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("材质ID操作符注销完成")
