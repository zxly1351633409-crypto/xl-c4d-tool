import bpy
import os
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def pf_grunge_25_r():
    """节点组: PF_Grunge_25_R
    程序化污渍纹理25 — 生成无缝平铺的脏污/磨损图案，支持缩放控制"""
    group_name = "PF_Grunge_25_R"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="缩放", in_out="INPUT", socket_type="NodeSocketVector").default_value = (1.0000, 1.0000, 1.0000)
    group.interface.new_socket(name="颜色: 材质颜色通道", in_out="OUTPUT", socket_type="NodeSocketColor")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.image = bpy.data.images.load(os.path.join(os.path.dirname(__file__), 'textures', 'PF_Grunge_25_R.tga'))
    image_texture.location = (227.2, 49.7)
    image_texture.projection = 'BOX'
    image_texture.interpolation = 'Linear'
    image_texture.projection_blend = 1.0
    image_texture.extension = 'REPEAT'
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (24.7, 49.7)
    mapping.vector_type = 'POINT'
    mapping.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    texture_coordinate = nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (-355.3, 7.6)
    texture_coordinate.from_instancer = False
    vector_transform = nodes.new("ShaderNodeVectorTransform")
    vector_transform.location = (-165.3, 7.6)
    vector_transform.vector_type = 'POINT'
    vector_transform.convert_from = 'WORLD'
    vector_transform.convert_to = 'WORLD'

    # === 节点连接 ===
    links.new(mapping.outputs[0], image_texture.inputs[0])
    links.new(vector_transform.outputs[0], mapping.inputs[0])
    links.new(texture_coordinate.outputs[3], vector_transform.inputs[0])
    links.new(input_node.outputs[0], mapping.inputs[3])
    links.new(image_texture.outputs[0], output_node.inputs[0])

    return group