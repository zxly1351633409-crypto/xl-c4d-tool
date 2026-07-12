import bpy
from ..utils.logger import logger


def update_mist_start(self, context):
    if context.scene.world:
        try:
            context.scene.world.mist_settings.start = self.mist_start
        except AttributeError:
            pass


def update_mist_depth(self, context):
    if context.scene.world:
        try:
            context.scene.world.mist_settings.depth = self.mist_depth
        except AttributeError:
            pass


def update_mist_falloff(self, context):
    if context.scene.world:
        try:
            context.scene.world.mist_settings.falloff = self.mist_falloff
        except AttributeError:
            pass


class XlC4dToolProperties(bpy.types.PropertyGroup):
    mist_start: bpy.props.FloatProperty(
        name="起始距离", default=5.0, min=0.0,
        description="雾场起始距离", update=update_mist_start
    )
    mist_depth: bpy.props.FloatProperty(
        name="深度", default=25.0, min=0.0,
        description="雾场深度", update=update_mist_depth
    )
    mist_falloff: bpy.props.EnumProperty(
        name="衰减",
        items=[
            ('QUADRATIC', "二次", "二次衰减"),
            ('LINEAR', "线性", "线性衰减"),
            ('INVERSE_QUADRATIC', "反向二次", "反向二次衰减"),
        ],
        default='QUADRATIC',
        description="雾场衰减类型",
        update=update_mist_falloff
    )
    current_mode: bpy.props.EnumProperty(
        name="当前模式",
        items=[
            ('NORMAL', "正常", "正常视图模式"),
            ('MATERIAL_ID', "材质ID", "材质ID效果模式"),
            ('MIST', "雾场", "雾场效果模式"),
            ('LAYER_ID', "物体ID", "物体ID图效果模式"),
        ],
        default='NORMAL',
        description="当前视图模式"
    )
    expand_layer_id: bpy.props.BoolProperty(name="物体ID图", default=False)
    expand_material_id: bpy.props.BoolProperty(name="材质ID", default=False)
    expand_mist: bpy.props.BoolProperty(name="雾场", default=False)
    expand_claymate: bpy.props.BoolProperty(name="一键粘土", default=False)
    expand_collection_instance: bpy.props.BoolProperty(name="集合实例转材质", default=False)
    expand_c4d_tools: bpy.props.BoolProperty(name="C4D工具", default=True)
    show_object_outline: bpy.props.BoolProperty(name="显示物体轮廓", default=False)
    align_use_active: bpy.props.BoolProperty(name="使用活动物体", default=False)
    new_object_suffix: bpy.props.StringProperty(name="新物体后缀", default="_new")
    skip_prefix: bpy.props.StringProperty(name="跳过集合前缀", default="莫动——")

    active_tab: bpy.props.EnumProperty(
        name="活动标签页",
        items=[
            ('MODIFIERS', "修改器库", "选择并赋予 C4D 节点组"),
            ('EFFECTS', "效果模式", "效果模式设置"),
            ('TOOLS', "C4D工具", "C4D小功能"),
        ],
        default='MODIFIERS'
    )

    modifier_search: bpy.props.StringProperty(
        name="搜索修改器", description="按中文名称或描述搜索节点组", default=""
    )
    modifier_category: bpy.props.EnumProperty(
        name="分类",
        items=[
            ('ALL', "全部", "显示全部节点组"),
            ('生成器', "生成器", "参数化生成器与样条生成"),
            ('建模工具', "建模工具", "布尔、连接、细分、对称等"),
            ('克隆器', "克隆器", "MoGraph 克隆与实例"),
            ('效果器', "效果器", "MoGraph 效果器"),
            ('域', "域", "Fields 域与域修改"),
            ('散布', "散布", "散布系统"),
            ('变形器', "变形器", "C4D 风格变形器"),
            ('动画', "动画", "运动与动画处理"),
            ('其他', "其他", "其他工具节点组"),
        ],
        default='生成器',
    )
    modifier_stack_folded: bpy.props.BoolProperty(name="修改器栈折叠", default=False)

    node_to_code_folded: bpy.props.BoolProperty(name="折叠任意节点转代码", default=True)
    material_nodes_folded: bpy.props.BoolProperty(name="折叠材质节点助手", default=True)
    geo_nodes_folded: bpy.props.BoolProperty(name="折叠几何节点助手", default=True)
    node_arrange_folded: bpy.props.BoolProperty(name="折叠自动排列节点", default=True)


classes = [
    XlC4dToolProperties,
]


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    if not hasattr(bpy.types.Scene, "xl_c4d_tool_props"):
        bpy.types.Scene.xl_c4d_tool_props = bpy.props.PointerProperty(type=XlC4dToolProperties)
    logger.info("属性注册完成")


def unregister():
    if hasattr(bpy.types.Scene, "xl_c4d_tool_props"):
        del bpy.types.Scene.xl_c4d_tool_props
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("属性注销完成")
