import bpy
from ..utils.logger import logger
from ..utils.shading import _iter_view3d_spaces


class OBJECT_OT_mist_mode(bpy.types.Operator):
    bl_idname = "object.xl_mist_mode"
    bl_label = "雾场"
    bl_description = "切换到雾场效果模式（Eevee引擎）"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.xl_c4d_tool_props
        screen = context.screen
        logger.info("===== 开始雾场模式设置 =====")
        logger.info(f"当前屏幕: {screen.name}")

        logger.info("Step 1: 切换渲染引擎为EEVEE")
        context.scene.render.engine = 'BLENDER_EEVEE'

        logger.info("Step 2: 启用视图层的雾场通道")
        for vl in context.scene.view_layers:
            try:
                vl.use_pass_mist = True
                logger.info(f"视图层 {vl.name} 雾场通道已启用")
            except AttributeError:
                logger.warning("无法启用雾场通道")

        logger.info("Step 3: 设置雾场参数")
        world = context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            context.scene.world = world
            logger.info("创建新的世界环境")

        if world:
            try:
                mist = world.mist_settings
                if props:
                    mist.start = props.mist_start
                    mist.depth = props.mist_depth
                    mist.falloff = props.mist_falloff
                    logger.info(f"雾场参数: 起始={mist.start}, 深度={mist.depth}, 衰减={mist.falloff}")
            except AttributeError:
                logger.warning("无法设置雾场参数")

        logger.info(f"Step 4: 设置屏幕[{screen.name}]所有3D视口为渲染模式 + 雾场通道 + 禁用合成器")
        for area, space in _iter_view3d_spaces(screen):
            space.shading.type = 'RENDERED'
            try:
                space.shading.render_pass = 'MIST'
                logger.info(f"渲染通道已设置为 MIST")
            except AttributeError as e:
                logger.warning(f"设置渲染通道失败: {e}")
            try:
                space.shading.use_compositor = 'DISABLED'
                logger.info(f"合成器已禁用")
            except AttributeError as e:
                logger.warning(f"禁用合成器失败: {e}")

        if props:
            props.current_mode = 'MIST'

        logger.info("===== 雾场模式设置完成 =====")
        self.report({'INFO'}, "雾场模式已激活（Eevee）")
        return {'FINISHED'}


class OBJECT_OT_normal_from_mist(bpy.types.Operator):
    bl_idname = "object.xl_normal_from_mist"
    bl_label = "正常"
    bl_description = "从雾场模式切换回正常视图模式"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.xl_c4d_tool_props
        screen = context.screen
        logger.info("===== 从雾场模式切换回正常模式 =====")
        logger.info(f"当前屏幕: {screen.name}")

        logger.info(f"Step 1: 恢复屏幕[{screen.name}]的渲染通道为合并结果、启用合成器、切回实体模式")
        for area, space in _iter_view3d_spaces(screen):
            try:
                space.shading.render_pass = 'COMBINED'
            except AttributeError:
                pass
            try:
                space.shading.use_compositor = 'ALWAYS'
            except AttributeError:
                pass
            space.shading.type = 'SOLID'

        context.scene.render.engine = 'BLENDER_EEVEE'
        logger.info("渲染引擎切换为EEVEE")

        if props:
            props.current_mode = 'NORMAL'

        logger.info("===== 切换回正常模式完成 =====")
        self.report({'INFO'}, "已切换回正常视图模式")
        return {'FINISHED'}


classes = [
    OBJECT_OT_mist_mode,
    OBJECT_OT_normal_from_mist,
]


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    logger.info("雾场操作符注册完成")


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("雾场操作符注销完成")
