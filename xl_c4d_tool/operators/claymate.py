from __future__ import annotations

import os

import bpy


ADDON_ROOT = os.path.dirname(os.path.dirname(__file__))
CLAYMATE_BLEND = os.path.join(ADDON_ROOT, "assets", "Claymate.blend")
CLAYMATE_PREFIX = "Claymate"


def get_claymate_nodegroup():
    for group in bpy.data.node_groups:
        if group.name.startswith(CLAYMATE_PREFIX):
            return group

    if os.path.exists(CLAYMATE_BLEND):
        existing = set(bpy.data.node_groups.keys())
        with bpy.data.libraries.load(CLAYMATE_BLEND, link=False) as (data_from, data_to):
            if CLAYMATE_PREFIX in data_from.node_groups:
                data_to.node_groups = [CLAYMATE_PREFIX]
        for group in bpy.data.node_groups:
            if group.name.startswith(CLAYMATE_PREFIX) and group.name not in existing:
                return group

    group = bpy.data.node_groups.new(CLAYMATE_PREFIX, "ShaderNodeTree")
    group.interface.new_socket("Base Color", in_out="INPUT", socket_type="NodeSocketColor")
    group.interface.new_socket("Roughness", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket("Metallic", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket("Enable", in_out="INPUT", socket_type="NodeSocketBool")
    group.interface.new_socket("Clay Color", in_out="INPUT", socket_type="NodeSocketColor")
    group.interface.new_socket("Base Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    group.interface.new_socket("Roughness", in_out="OUTPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket("Metallic", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes, links = group.nodes, group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    mix = nodes.new("ShaderNodeMixRGB")
    mix.name = "CM Mix"
    mix.blend_type = "MIX"
    mix.location = (220, 80)
    group_input.location = (0, 0)
    group_output.location = (440, 0)

    links.new(group_input.outputs["Enable"], mix.inputs[0])
    links.new(group_input.outputs["Base Color"], mix.inputs[1])
    links.new(group_input.outputs["Clay Color"], mix.inputs[2])
    links.new(mix.outputs[0], group_output.inputs["Base Color"])
    links.new(group_input.outputs["Roughness"], group_output.inputs["Roughness"])
    links.new(group_input.outputs["Metallic"], group_output.inputs["Metallic"])
    group_input.outputs["Enable"].default_value = True
    group_input.outputs["Clay Color"].default_value = (0.8, 0.7, 0.6, 1.0)
    return group


def active_claymate_group():
    for group in bpy.data.node_groups:
        if group.name.startswith(CLAYMATE_PREFIX):
            return group
    return None


def _ensure_basic_materials(context):
    material = bpy.data.materials.get("XL_粘土默认材质")
    if material is None:
        material = bpy.data.materials.new("XL_粘土默认材质")
        material.use_nodes = True

    targets = list(context.selected_objects) or list(context.scene.objects)
    for obj in targets:
        if obj.type != "MESH":
            continue
        if not obj.data.materials:
            obj.data.materials.append(material)


def dissolve_claymate_nodes(remove_group=True):
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.node_tree:
            continue

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes_to_remove = []
        links_to_restore = []

        for node in nodes:
            if node.type != "GROUP" or not node.node_tree or not node.node_tree.name.startswith(CLAYMATE_PREFIX):
                continue

            principled = None
            for output in node.outputs:
                for link in output.links:
                    if link.to_node.type == "BSDF_PRINCIPLED":
                        principled = link.to_node
                        break
                if principled:
                    break
            if principled is None:
                nodes_to_remove.append(node)
                continue

            base_color = node.inputs["Base Color"].links[0].from_socket if node.inputs["Base Color"].is_linked else None
            roughness = node.inputs["Roughness"].links[0].from_socket if node.inputs["Roughness"].is_linked else None
            metallic = node.inputs["Metallic"].links[0].from_socket if node.inputs["Metallic"].is_linked else None
            links_to_restore.append((principled, base_color, roughness, metallic))
            nodes_to_remove.append(node)

        for node in nodes_to_remove:
            nodes.remove(node)

        for principled, base_color, roughness, metallic in links_to_restore:
            if base_color:
                links.new(base_color, principled.inputs["Base Color"])
            if roughness:
                links.new(roughness, principled.inputs["Roughness"])
            if metallic:
                links.new(metallic, principled.inputs["Metallic"])

    if remove_group:
        for group in list(bpy.data.node_groups):
            if group.name.startswith(CLAYMATE_PREFIX):
                bpy.data.node_groups.remove(group)


def enable_claymate(context):
    dissolve_claymate_nodes(remove_group=False)
    _ensure_basic_materials(context)
    group = get_claymate_nodegroup()
    if group is None:
        return 0

    changed = 0
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.node_tree:
            continue
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        for principled in [node for node in nodes if node.type == "BSDF_PRINCIPLED"]:
            base_source = _source_or_value_node(mat, principled, "Base Color", "ShaderNodeRGB", 120)
            rough_source = _source_or_value_node(mat, principled, "Roughness", "ShaderNodeValue", 0)
            metal_source = _source_or_value_node(mat, principled, "Metallic", "ShaderNodeValue", -120)

            clay = nodes.new("ShaderNodeGroup")
            clay.node_tree = group
            clay.name = "XL_一键粘土"
            clay.label = "XL_一键粘土"
            clay.location = (principled.location.x - 220, principled.location.y)
            links.new(base_source, clay.inputs["Base Color"])
            links.new(rough_source, clay.inputs["Roughness"])
            links.new(metal_source, clay.inputs["Metallic"])
            links.new(clay.outputs["Base Color"], principled.inputs["Base Color"])
            links.new(clay.outputs["Roughness"], principled.inputs["Roughness"])
            links.new(clay.outputs["Metallic"], principled.inputs["Metallic"])
            changed += 1
    return changed


def _source_or_value_node(mat, principled, socket_name, node_type, y_offset):
    socket = principled.inputs[socket_name]
    if socket.is_linked:
        return socket.links[0].from_socket

    node = mat.node_tree.nodes.new(node_type)
    node.location = (principled.location.x - 520, principled.location.y + y_offset)
    if node_type == "ShaderNodeRGB":
        node.outputs[0].default_value = socket.default_value
    else:
        node.outputs[0].default_value = socket.default_value
    return node.outputs[0]


class OBJECT_OT_xl_claymate_enable(bpy.types.Operator):
    bl_idname = "object.xl_claymate_enable"
    bl_label = "一键粘土"
    bl_description = "给场景材质加入 Claymate 粘土效果节点"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        count = enable_claymate(context)
        self.report({"INFO"}, f"已启用粘土效果：{count} 个 Principled BSDF")
        return {"FINISHED"}


class OBJECT_OT_xl_claymate_dissolve(bpy.types.Operator):
    bl_idname = "object.xl_claymate_dissolve"
    bl_label = "移除粘土"
    bl_description = "移除 Claymate 粘土效果节点并恢复原材质连接"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, _context):
        dissolve_claymate_nodes(remove_group=True)
        self.report({"INFO"}, "已移除粘土效果")
        return {"FINISHED"}


classes = (
    OBJECT_OT_xl_claymate_enable,
    OBJECT_OT_xl_claymate_dissolve,
)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
