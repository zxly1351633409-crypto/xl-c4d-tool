import bpy
import os
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def pf_grunge_09_r():
    """节点组: PF_Grunge_09_R
    程序化污渍纹理09 — 生成无缝平铺的脏污/磨损图案，支持缩放控制"""
    group_name = "PF_Grunge_09_R"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="缩放", in_out="INPUT", socket_type="NodeSocketVector").default_value = (1.0000, 1.0000, 1.0000)
    group.interface.new_socket(name="Location", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="颜色: 材质颜色通道", in_out="OUTPUT", socket_type="NodeSocketColor")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (-887.2, -10.5)
    texture_coordinate_001.from_instancer = False
    mapping_001 = nodes.new("ShaderNodeMapping")
    mapping_001.location = (-347.3, -30.7)
    mapping_001.vector_type = 'VECTOR'
    mapping_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.image = bpy.data.images.load(os.path.join(os.path.dirname(__file__), 'textures', 'PF_Grunge_09_R.tga'))
    image_texture.location = (-85.2, -29.7)
    image_texture.projection = 'BOX'
    image_texture.interpolation = 'Linear'
    image_texture.projection_blend = 0.5
    image_texture.extension = 'REPEAT'
    vector_transform = nodes.new("ShaderNodeVectorTransform")
    vector_transform.location = (-704.6, -10.4)
    vector_transform.vector_type = 'VECTOR'
    vector_transform.convert_from = 'WORLD'
    vector_transform.convert_to = 'WORLD'
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (-527.3, -9.6)
    vector_math.operation = 'ADD'
    vector_math.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[3].default_value = 1.0

    # === 节点连接 ===
    links.new(mapping_001.outputs[0], image_texture.inputs[0])
    links.new(input_node.outputs[0], mapping_001.inputs[3])
    links.new(image_texture.outputs[0], output_node.inputs[0])
    links.new(vector_math.outputs[0], mapping_001.inputs[0])
    links.new(texture_coordinate_001.outputs[3], vector_transform.inputs[0])
    links.new(vector_transform.outputs[0], vector_math.inputs[0])
    links.new(input_node.outputs[1], vector_math.inputs[1])

    return group