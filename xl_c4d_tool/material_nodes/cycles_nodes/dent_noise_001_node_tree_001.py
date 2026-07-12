import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def dent_noise001_node_tree001():
    """节点组: Dent Noise.001
    凹陷噪声纹理001变体1 — 模拟表面凹陷/点蚀效果的程序化纹理"""
    group_name = "Dent Noise.001_node_tree.001"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="向量", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="W", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 5.0
    group.interface.new_socket(name="细节", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="畸变", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="值", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    noise_texture_008 = nodes.new("ShaderNodeTexNoise")
    noise_texture_008.location = (-1680.0, 0.0)
    noise_texture_008.noise_dimensions = '3D'
    noise_texture_008.noise_type = 'FBM'
    noise_texture_008.normalize = True
    noise_texture_008.inputs[4].default_value = 0.5
    noise_texture_008.inputs[5].default_value = 2.0
    noise_texture_008.inputs[7].default_value = 1.0
    mix_008 = nodes.new("ShaderNodeMix")
    mix_008.location = (-1470.0, 0.0)
    mix_008.data_type = 'RGBA'
    mix_008.factor_mode = 'UNIFORM'
    mix_008.blend_type = 'SUBTRACT'
    mix_008.clamp_factor = True
    mix_008.clamp_result = False
    mix_008.inputs[0].default_value = 1.0
    mix_008.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_008.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[7].default_value = (0.5000, 0.5000, 0.5000, 1.0000)
    mix_008.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    separate_rgb_003 = nodes.new("ShaderNodeSeparateColor")
    separate_rgb_003.location = (-1260.0, 0.0)
    separate_rgb_003.mode = 'RGB'
    math_058 = nodes.new("ShaderNodeMath")
    math_058.location = (-840.0, 0.0)
    math_058.operation = 'MAXIMUM'
    math_058.use_clamp = False
    math_058.inputs[2].default_value = 0.5
    math_060 = nodes.new("ShaderNodeMath")
    math_060.location = (-1050.0, 0.0)
    math_060.operation = 'ABSOLUTE'
    math_060.use_clamp = False
    math_060.inputs[1].default_value = 0.5
    math_060.inputs[2].default_value = 0.5
    math_061 = nodes.new("ShaderNodeMath")
    math_061.location = (-840.0, -217.2)
    math_061.operation = 'ABSOLUTE'
    math_061.use_clamp = False
    math_061.inputs[1].default_value = 0.5
    math_061.inputs[2].default_value = 0.5
    math_062 = nodes.new("ShaderNodeMath")
    math_062.location = (-1050.0, -195.6)
    math_062.operation = 'ABSOLUTE'
    math_062.use_clamp = False
    math_062.inputs[1].default_value = 0.5
    math_062.inputs[2].default_value = 0.5
    math_063 = nodes.new("ShaderNodeMath")
    math_063.location = (-420.0, 0.0)
    math_063.operation = 'MULTIPLY'
    math_063.use_clamp = False
    math_063.inputs[1].default_value = 2.0
    math_063.inputs[2].default_value = 0.5
    math_064 = nodes.new("ShaderNodeMath")
    math_064.location = (-630.0, 0.0)
    math_064.operation = 'MAXIMUM'
    math_064.use_clamp = False
    math_064.inputs[2].default_value = 0.5
    math_065 = nodes.new("ShaderNodeMath")
    math_065.location = (-210.0, 0.0)
    math_065.operation = 'POWER'
    math_065.use_clamp = False
    math_065.inputs[1].default_value = 2.5
    math_065.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (-2125.5, 184.7)
    math_004.operation = 'GREATER_THAN'
    math_004.use_clamp = False
    math_004.inputs[2].default_value = 0.5
    math_006 = nodes.new("ShaderNodeMath")
    math_006.location = (-2325.3, 110.1)
    math_006.operation = 'ABSOLUTE'
    math_006.use_clamp = False
    math_006.inputs[1].default_value = 0.5
    math_006.inputs[2].default_value = 0.5
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (-2511.0, 232.4)
    texture_coordinate_001.from_instancer = False
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (-1920.1, 178.1)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)

    # === 节点连接 ===
    links.new(noise_texture_008.outputs[1], mix_008.inputs[6])
    links.new(separate_rgb_003.outputs[0], math_060.inputs[0])
    links.new(mix_008.outputs[2], separate_rgb_003.inputs[0])
    links.new(math_058.outputs[0], math_064.inputs[0])
    links.new(separate_rgb_003.outputs[1], math_062.inputs[0])
    links.new(separate_rgb_003.outputs[2], math_061.inputs[0])
    links.new(math_064.outputs[0], math_063.inputs[0])
    links.new(math_060.outputs[0], math_058.inputs[0])
    links.new(math_062.outputs[0], math_058.inputs[1])
    links.new(math_061.outputs[0], math_064.inputs[1])
    links.new(math_063.outputs[0], math_065.inputs[0])
    links.new(input_node.outputs[2], noise_texture_008.inputs[2])
    links.new(math_065.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[3], noise_texture_008.inputs[3])
    links.new(input_node.outputs[4], noise_texture_008.inputs[8])
    links.new(input_node.outputs[1], noise_texture_008.inputs[1])
    links.new(math_004.outputs[0], mix_006.inputs[0])
    links.new(texture_coordinate_001.outputs[0], mix_006.inputs[6])
    links.new(math_006.outputs[0], math_004.inputs[0])
    links.new(mix_006.outputs[2], noise_texture_008.inputs[0])
    links.new(input_node.outputs[0], mix_006.inputs[7])
    links.new(input_node.outputs[0], math_006.inputs[0])

    return group