"""集合实例转材质模块 - 操作符
将选中的集合实例转为可上材质的几何节点平面
每个选中实例独立创建一个平面
"""
import bpy
from ..utils.logger import logger


def _get_collection_instance_empty(obj):
    """判断物体是否为集合实例(Empty且instance_type='COLLECTION'), 返回源集合"""
    if obj.type != 'EMPTY':
        return None
    if obj.instance_type != 'COLLECTION':
        return None
    if obj.instance_collection is None:
        return None
    return obj.instance_collection


def _get_selected_instances(context):
    """获取选中物体中的集合实例, 返回列表 [(empty_obj, source_collection), ...]"""
    instances = []
    for obj in context.selected_objects:
        source_col = _get_collection_instance_empty(obj)
        if source_col is None:
            continue
        instances.append((obj, source_col))
    return instances


def _find_material_plane_by_instance(instance_empty):
    """按实例名查找材质平面
    命名规则: {instance_name}_材质平面
    """
    plane_name = f"{instance_empty.name}_材质平面"
    return bpy.data.objects.get(plane_name)


def _build_gn_node_tree(plane, instance_empty, source_collection):
    """在平面上构建几何节点树
    结构: GroupInput(材质) → ObjectInfo(引用实例) → RealizeInstances → SetMaterial → GroupOutput
    """
    ng_name = f"GN_{instance_empty.name}_材质"

    # 检查是否已有同名节点组
    if ng_name in bpy.data.node_groups:
        ng = bpy.data.node_groups[ng_name]
    else:
        ng = bpy.data.node_groups.new(ng_name, "GeometryNodeTree")

        # 清空默认节点
        ng.nodes.clear()

        # 定义接口: Material 材质输入, Geometry 输出
        ng.interface.clear()
        mat_socket = ng.interface.new_socket(
            name="材质", in_out="INPUT", socket_type="NodeSocketMaterial"
        )
        geo_in = ng.interface.new_socket(
            name="几何体", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        geo_out = ng.interface.new_socket(
            name="几何体", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

        nodes = ng.nodes
        links = ng.links

        # Group Input / Output
        group_in = nodes.new("NodeGroupInput")
        group_in.location = (-400, 0)
        group_out = nodes.new("NodeGroupOutput")
        group_out.location = (400, 0)

        # Object Info — 引用该实例空物体
        obj_info = nodes.new("GeometryNodeObjectInfo")
        obj_info.location = (-100, 0)
        obj_info.inputs["Object"].default_value = instance_empty

        # Realize Instances
        realize = nodes.new("GeometryNodeRealizeInstances")
        realize.location = (100, 0)

        # Set Material
        set_mat = nodes.new("GeometryNodeSetMaterial")
        set_mat.location = (250, 0)

        # 连线
        links.new(group_in.outputs[mat_socket.identifier], set_mat.inputs["Material"])
        links.new(obj_info.outputs["Geometry"], realize.inputs["Geometry"])
        links.new(realize.outputs["Geometry"], set_mat.inputs["Geometry"])
        links.new(set_mat.outputs["Geometry"], group_out.inputs[geo_out.identifier])

        logger.info(f"创建几何节点组: {ng_name}")

    # 在平面上添加 GN 修改器
    modifier = plane.modifiers.new(name="集合实例材质", type='NODES')
    modifier.node_group = ng

    return modifier


def _hide_instance(empty_obj):
    """隐藏集合实例(视口+渲染)"""
    empty_obj.hide_viewport = True
    empty_obj.hide_render = True


class OBJECT_OT_collection_instance_to_material(bpy.types.Operator):
    bl_idname = "object.xl_collection_instance_to_material"
    bl_label = "集合实例转材质"
    bl_description = (
        "将选中的集合实例转为可上材质的几何节点平面。\n"
        "每个选中实例独立创建一个平面。"
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        instances = _get_selected_instances(context)
        if not instances:
            self.report({'WARNING'}, "请选择至少一个集合实例（空物体且实例类型为集合）")
            return {'CANCELLED'}

        created_planes = 0
        hidden_instances = 0
        reused_planes = 0

        for instance_empty, source_col in instances:
            # 检查是否已有该实例的材质平面
            existing_plane = _find_material_plane_by_instance(instance_empty)
            if existing_plane:
                mod = existing_plane.modifiers.get("集合实例材质")
                if not mod or not mod.node_group:
                    _build_gn_node_tree(existing_plane, instance_empty, source_col)
                _hide_instance(instance_empty)
                hidden_instances += 1
                reused_planes += 1
                # 确保实例也链入平面所在集合
                for col in existing_plane.users_collection:
                    if instance_empty.name not in col.objects:
                        col.objects.link(instance_empty)
                        break
                logger.info(
                    f"实例[{instance_empty.name}]已有材质平面[{existing_plane.name}]，跳过创建"
                )
                continue

            # 新建平面 (以实例名命名)
            plane_name = f"{instance_empty.name}_材质平面"
            plane_data = bpy.data.meshes.new(plane_name)
            plane = bpy.data.objects.new(plane_name, plane_data)

            # 放到实例位置
            plane.location = instance_empty.location
            plane.rotation_euler = instance_empty.rotation_euler
            plane.scale = instance_empty.scale

            # 创建专属新集合，把实例和平面放一起
            coll_name = f"{instance_empty.name}_材质集"
            if coll_name in bpy.data.collections:
                new_coll = bpy.data.collections[coll_name]
            else:
                new_coll = bpy.data.collections.new(coll_name)
                # 挂到场景主集合下
                context.scene.collection.children.link(new_coll)

            new_coll.objects.link(plane)
            new_coll.objects.link(instance_empty)
            created_planes += 1

            # 构建GN
            _build_gn_node_tree(plane, instance_empty, source_col)

            # 隐藏实例
            _hide_instance(instance_empty)
            hidden_instances += 1

            logger.info(
                f"创建材质平面 [{plane_name}] → 引用实例[{instance_empty.name}]，源集合[{source_col.name}]"
            )

        msg_parts = []
        if created_planes:
            msg_parts.append(f"创建 {created_planes} 个材质平面")
        if reused_planes:
            msg_parts.append(f"复用 {reused_planes} 个已有平面")
        msg_parts.append(f"隐藏 {hidden_instances} 个集合实例")

        msg = "，".join(msg_parts)
        self.report({'INFO'}, msg)
        logger.info(f"===== 集合实例转材质完成: {msg} =====")
        return {'FINISHED'}


class OBJECT_OT_restore_collection_instances(bpy.types.Operator):
    bl_idname = "object.xl_restore_collection_instances"
    bl_label = "恢复集合实例"
    bl_description = "恢复被隐藏的集合实例显示，并清理材质平面"
    bl_options = {'REGISTER', 'UNDO'}

    remove_planes: bpy.props.BoolProperty(
        name="同时删除材质平面",
        description="勾选后删除自动生成的材质平面及其几何节点",
        default=False,
    )

    def execute(self, context):
        restored = 0
        removed_planes = 0

        # 恢复所有被隐藏的集合实例
        for obj in bpy.data.objects:
            if obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION':
                if obj.instance_collection is not None:
                    if obj.hide_viewport or obj.hide_render:
                        obj.hide_viewport = False
                        obj.hide_render = False
                        restored += 1

        # 删除材质平面
        if self.remove_planes:
            to_remove = []
            for obj in bpy.data.objects:
                if obj.name.endswith("_材质平面"):
                    mod = obj.modifiers.get("集合实例材质")
                    if mod:
                        to_remove.append(obj)

            for obj in to_remove:
                mesh = obj.data
                bpy.data.objects.remove(obj, do_unlink=True)
                if mesh and mesh.users == 0:
                    bpy.data.meshes.remove(mesh)
                removed_planes += 1

            # 清理孤立节点组
            for ng in list(bpy.data.node_groups):
                if ng.name.startswith("GN_") and ng.name.endswith("_材质"):
                    if ng.users == 0:
                        bpy.data.node_groups.remove(ng)

        msg = f"恢复 {restored} 个集合实例"
        if removed_planes:
            msg += f"，删除 {removed_planes} 个材质平面"
        self.report({'INFO'}, msg)
        logger.info(f"===== 恢复集合实例完成: {msg} =====")
        return {'FINISHED'}


classes = [
    OBJECT_OT_collection_instance_to_material,
    OBJECT_OT_restore_collection_instances,
]


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    logger.info("集合实例转材质操作符注册完成")


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("集合实例转材质操作符注销完成")
