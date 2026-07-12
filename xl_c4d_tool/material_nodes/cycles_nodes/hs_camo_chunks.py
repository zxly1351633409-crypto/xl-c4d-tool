import bpy
import os
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def hs_camo_chunks():
    """BL_迷彩块状 - 块状迷彩图案
    基于Principled BSDF，含凹凸开关/迷彩纹理生成"""
    group_name = "BL_迷彩块状"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1000.0
    group.interface.new_socket(name="位置", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="Chunks", in_out="OUTPUT", socket_type="NodeSocketColor")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (20.2, 344.1)
    mapping.vector_type = 'POINT'
    mapping.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    texture_coordinate = nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (-372.3, 404.3)
    texture_coordinate.from_instancer = False
    vector_transform = nodes.new("ShaderNodeVectorTransform")
    vector_transform.location = (-169.8, 435.6)
    vector_transform.vector_type = 'VECTOR'
    vector_transform.convert_from = 'WORLD'
    vector_transform.convert_to = 'WORLD'
    math = nodes.new("ShaderNodeMath")
    math.location = (-169.8, 184.2)
    math.operation = 'DIVIDE'
    math.use_clamp = False
    math.inputs[1].default_value = 1000.0
    math.inputs[2].default_value = 0.5
    image_texture = nodes.new("ShaderNodeTexImage")
    image_texture.image = bpy.data.images.load(os.path.join(os.path.dirname(__file__), 'textures', 'HS_Camo_Chunks.tga'))
    image_texture.location = (210.2, 556.8)
    image_texture.projection = 'BOX'
    image_texture.interpolation = 'Linear'
    image_texture.extension = 'REPEAT'
    reroute = nodes.new("NodeReroute")
    reroute.location = (-169.8, 242.2)
    reroute.socket_idname = 'NodeSocketVectorTranslation'

    # === 节点连接 ===
    links.new(texture_coordinate.outputs[3], vector_transform.inputs[0])
    links.new(vector_transform.outputs[0], mapping.inputs[0])
    links.new(math.outputs[0], mapping.inputs[3])
    links.new(input_node.outputs[0], math.inputs[0])
    links.new(mapping.outputs[0], image_texture.inputs[0])
    links.new(image_texture.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[1], reroute.inputs[0])
    links.new(reroute.outputs[0], mapping.inputs[1])

    return group