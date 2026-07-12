import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def hs_chipping():
    """BL_油漆剥落遮罩_内部 - 油漆材质内部遮罩
    供 BL_油漆01 内部调用，不作为独立材质按钮暴露。"""
    group_name = "BL_油漆剥落遮罩_内部"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="百分比%", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="遮罩", in_out="OUTPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="颜色: 材质颜色通道", in_out="OUTPUT", socket_type="NodeSocketColor")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    mapping_003 = nodes.new("ShaderNodeMapping")
    mapping_003.location = (-131.1, -189.5)
    mapping_003.vector_type = 'POINT'
    mapping_003.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping_003.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_003.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_003 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_003.location = (-131.1, -158.3)
    texture_coordinate_003.from_instancer = False
    vector_transform_004 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_004.location = (-131.1, -127.0)
    vector_transform_004.vector_type = 'VECTOR'
    vector_transform_004.convert_from = 'OBJECT'
    vector_transform_004.convert_to = 'OBJECT'
    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.location = (-131.1, 151.9)
    noise_texture_002.noise_dimensions = '3D'
    noise_texture_002.noise_type = 'FBM'
    noise_texture_002.normalize = True
    noise_texture_002.inputs[3].default_value = 12.850000381469727
    noise_texture_002.inputs[4].default_value = 0.5
    noise_texture_002.inputs[5].default_value = 2.4800000190734863
    noise_texture_002.inputs[7].default_value = 1.0
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'EASE'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.6909090280532837
    color_ramp_003.color_ramp.elements[0].color = (0.19130007922649384, 0.09814079105854034, 0.06471572071313858, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.6999999284744263
    color_ramp_003.color_ramp.elements[1].color = (0.11610929667949677, 0.07029114663600922, 0.0548812560737133, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (55.0, -53.4)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (312.0, 189.5)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 0.5
    map_range_001.inputs[3].default_value = 0.009999990463256836
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'CONSTANT'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.027272727340459824
    color_ramp_002.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.6909091472625732
    color_ramp_002.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (57.1, 154.5)
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (-312.0, 33.1)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = 1.0
    map_range_013.inputs[4].default_value = 10.0
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)

    # === 节点连接 ===
    links.new(noise_texture_002.outputs[0], color_ramp_002.inputs[0])
    links.new(texture_coordinate_003.outputs[3], vector_transform_004.inputs[0])
    links.new(color_ramp_002.outputs[0], map_range_001.inputs[0])
    links.new(map_range_013.outputs[0], noise_texture_002.inputs[2])
    links.new(vector_transform_004.outputs[0], mapping_003.inputs[0])
    links.new(noise_texture_002.outputs[0], color_ramp_003.inputs[0])
    links.new(mapping_003.outputs[0], noise_texture_002.inputs[0])
    links.new(input_node.outputs[0], map_range_013.inputs[0])
    links.new(color_ramp_003.outputs[0], output_node.inputs[1])
    links.new(map_range_001.outputs[0], output_node.inputs[0])

    return group
