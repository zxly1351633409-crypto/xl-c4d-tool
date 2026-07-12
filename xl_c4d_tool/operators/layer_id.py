import bpy
from ..utils.logger import logger
from ..utils.shading import generate_random_color, get_all_collections, set_shading_for_all_areas


def _sync_gn_material_if_plane(obj, material):
    """如果物体是GN材质平面, 同步其修改器材质槽
    通过检测 '集合实例材质' 修改器来判断
    """
    mod = obj.modifiers.get("集合实例材质")
    if mod is None or mod.node_group is None:
        return False

    ng = mod.node_group
    mat_socket_id = None
    for item in ng.interface.items_tree:
        if item.in_out == 'INPUT' and item.socket_type == 'NodeSocketMaterial':
            mat_socket_id = item.identifier
            break

    if mat_socket_id is None:
        return False

    try:
        mod[mat_socket_id] = material
        logger.debug(f"GN平面[{obj.name}]材质槽同步为 {material.name}")
        return True
    except Exception as e:
        logger.warning(f"GN平面[{obj.name}]材质槽同步失败: {e}")
        return False


class OBJECT_OT_layer_id_setup(bpy.types.Operator):
    bl_idname = "object.xl_layer_id_setup"
    bl_label = "物体ID图"
    bl_description = "按集合赋予不同颜色材质，输出物体ID图效果"
    bl_options = {'REGISTER', 'UNDO'}

    confirm: bpy.props.BoolProperty(
        name="我已另存为新工程，确认清除材质",
        default=False
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        box = layout.box()
        box.label(text="⚠ 警告：此操作将清除所有材质与材质槽！", icon='ERROR')
        box.label(text="请先【另存为】新工程后再执行此操作！")
        box.separator()
        box.prop(self, "confirm")
        box.label(text="勾选后点击确定继续，否则点击取消", icon='INFO')

    def execute(self, context):
        if not self.confirm:
            self.report({'WARNING'}, "未确认，操作已取消")
            logger.warning("物体ID图：用户未确认，操作取消")
            return {'CANCELLED'}

        props = context.scene.xl_c4d_tool_props
        skip_prefix = props.skip_prefix if props else "莫动——"

        logger.info("===== 开始物体ID图设置 =====")
        logger.info(f"跳过集合前缀: {skip_prefix}")

        skipped_objects = self._get_skipped_objects(context, skip_prefix)
        logger.info(f"跳过前缀集合中的物体数量: {len(skipped_objects)}")

        logger.info("Step 1: 清除非跳过集合物体的材质和材质槽")
        cleared_count = 0
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj not in skipped_objects:
                if obj.data.materials:
                    obj.data.materials.clear()
                    cleared_count += 1
        logger.info(f"已清除 {cleared_count} 个物体的材质")

        logger.info("Step 2: 按集合赋予材质（跳过前缀集合及其子集合，跳过自动材质集）")
        collections = get_all_collections(context.scene)
        material_count = 0
        skipped_col_names = set()

        for col, col_path in collections:
            if self._is_collection_skipped(col, col_path, skip_prefix, skipped_col_names):
                logger.info(f"跳过集合: {col.name}（前缀匹配或为跳过集合的子集合）")
                continue
            # 跳过自动生成的材质集（{实例名}_材质集），避免双重赋材质
            if col.name.endswith("_材质集"):
                logger.debug(f"跳过自动材质集: {col.name}")
                continue

            mat_name = f"ID_{col.name}"
            mat = bpy.data.materials.get(mat_name)
            if not mat:
                mat = bpy.data.materials.new(name=mat_name)
                logger.info(f"创建材质: {mat_name}")

            color = generate_random_color()
            mat.diffuse_color = (*color, 1.0)
            mat.use_nodes = False

            for obj in col.all_objects:
                if obj.type == 'MESH' and obj not in skipped_objects:
                    if mat.name not in [m.name for m in obj.data.materials if m]:
                        obj.data.materials.append(mat)
                        material_count += 1
                    logger.debug(f"赋予材质 {mat_name} -> {obj.name}")
                    # 同步GN材质槽：如果此物体是GN材质平面，一并设置修改器材质输入
                    _sync_gn_material_if_plane(obj, mat)

        logger.info(f"已赋予 {material_count} 个物体材质")

        logger.info("Step 3: 切换视图着色方式")
        show_outline = props.show_object_outline if props else False
        set_shading_for_all_areas(
            context,
            light='FLAT',
            color_type='MATERIAL',
            shading_type='SOLID',
            show_object_outline=show_outline
        )

        logger.info("Step 4: 切换渲染引擎为工作台")
        context.scene.render.engine = 'BLENDER_WORKBENCH'

        if props:
            props.current_mode = 'LAYER_ID'

        logger.info("===== 物体ID图设置完成 =====")
        self.report({'INFO'}, f"物体ID图设置完成，已处理 {material_count} 个物体")
        return {'FINISHED'}

    def _get_skipped_objects(self, context, skip_prefix):
        skipped = set()
        for col, col_path in get_all_collections(context.scene):
            path_parts = col_path.split('/')
            if any(part.startswith(skip_prefix) for part in path_parts):
                for obj in col.all_objects:
                    skipped.add(obj)
        return skipped

    def _is_collection_skipped(self, col, col_path, skip_prefix, skipped_col_names):
        path_parts = col_path.split('/')
        return any(part.startswith(skip_prefix) for part in path_parts)


classes = [
    OBJECT_OT_layer_id_setup,
]


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    logger.info("物体ID图操作符注册完成")


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("物体ID图操作符注销完成")
