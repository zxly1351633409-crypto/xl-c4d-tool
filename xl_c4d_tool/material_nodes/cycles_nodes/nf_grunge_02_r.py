import bpy
import os
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def nf_grunge_02_r():
    """节点组: NF_Grunge_02_R
    噪声污渍纹理02 — 基于噪声生成的脏污/磨损效果，用于粗糙度和凹凸混合"""
    group_name = "NF_Grunge_02_R"
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
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (-400.4, 0.8)
    texture_coordinate_001.from_instancer = False
    vector_transform_001 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_001.location = (-210.4, 0.8)
    vector_transform_001.vector_type = 'VECTOR'
    vector_transform_001.convert_from = 'WORLD'
    vector_transform_001.convert_to = 'WORLD'
    mapping_001 = nodes.new("ShaderNodeMapping")
    mapping_001.location = (-20.4, 0.8)
    mapping_001.vector_type = 'POINT'
    mapping_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.image = bpy.data.images.load(os.path.join(os.path.dirname(__file__), 'textures', 'NF_Grunge_02_R.tga'))
    image_texture.location = (282.1, 0.8)
    image_texture.projection = 'BOX'
    image_texture.interpolation = 'Linear'
    image_texture.projection_blend = 0.8761329054832458
    image_texture.extension = 'REPEAT'

    # === 节点连接 ===
    links.new(input_node.outputs[0], mapping_001.inputs[3])
    links.new(texture_coordinate_001.outputs[3], vector_transform_001.inputs[0])
    links.new(vector_transform_001.outputs[0], mapping_001.inputs[0])
    links.new(mapping_001.outputs[0], image_texture.inputs[0])
    links.new(image_texture.outputs[0], output_node.inputs[0])

    return group