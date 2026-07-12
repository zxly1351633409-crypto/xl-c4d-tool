import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def perlin_noise_main002():
    """节点组: Perlin Noise Main.002
    柏林噪声主生成器002 — 多层柏林噪声叠加，提供缩放/细节/粗糙度等参数控制"""
    group_name = "Perlin Noise Main.002"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="向量", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="W", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 5.0
    group.interface.new_socket(name="细节", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 15.0
    group.interface.new_socket(name="维度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="间隙度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 2.0
    group.interface.new_socket(name="偏移", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="增益", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 90.0
    group.interface.new_socket(name="最小值", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="最大值", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="系数", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    musgrave_texture = nodes.new("ShaderNodeTexNoise")
    musgrave_texture.location = (-518.2, 0.0)
    musgrave_texture.noise_dimensions = '3D'
    musgrave_texture.noise_type = 'RIDGED_MULTIFRACTAL'
    musgrave_texture.normalize = False
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (-253.6, 0.0)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math = nodes.new("ShaderNodeMath")
    math.location = (-518.2, -320.0)
    math.operation = 'MINIMUM'
    math.use_clamp = False
    math.inputs[1].default_value = 14.0
    math.inputs[2].default_value = 0.5
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (-518.2, -360.0)
    math_001.operation = 'SUBTRACT'
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (-518.2, -400.0)
    math_002.operation = 'GREATER_THAN'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 1.0
    math_002.inputs[2].default_value = 0.5
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (-518.2, -520.0)
    math_003.operation = 'MAXIMUM'
    math_003.use_clamp = False
    math_003.inputs[1].default_value = -9.999999747378752e-06
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (-518.2, -480.0)
    math_004.operation = 'MULTIPLY'
    math_004.use_clamp = False
    math_004.inputs[1].default_value = -1.0
    math_004.inputs[2].default_value = 0.5
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (-518.2, -440.0)
    math_005.operation = 'POWER'
    math_005.use_clamp = False
    math_005.inputs[2].default_value = 0.5
    math_006 = nodes.new("ShaderNodeMath")
    math_006.location = (-518.2, -560.0)
    math_006.operation = 'MAXIMUM'
    math_006.use_clamp = False
    math_006.inputs[1].default_value = -9.999999747378752e-06
    math_006.inputs[2].default_value = 0.5
    math_007 = nodes.new("ShaderNodeMath")
    math_007.location = (-1028.7, 266.0)
    math_007.operation = 'GREATER_THAN'
    math_007.use_clamp = False
    math_007.inputs[2].default_value = 0.5
    math_008 = nodes.new("ShaderNodeMath")
    math_008.location = (-1207.0, 219.0)
    math_008.operation = 'ABSOLUTE'
    math_008.use_clamp = False
    math_008.inputs[1].default_value = 0.5
    math_008.inputs[2].default_value = 0.5
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (-1383.6, 276.9)
    texture_coordinate_001.from_instancer = False
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (-811.0, 282.4)
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
    links.new(musgrave_texture.outputs[0], map_range.inputs[0])
    links.new(map_range.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[1], musgrave_texture.inputs[1])
    links.new(input_node.outputs[2], musgrave_texture.inputs[2])
    links.new(input_node.outputs[6], musgrave_texture.inputs[6])
    links.new(input_node.outputs[7], musgrave_texture.inputs[7])
    links.new(input_node.outputs[8], map_range.inputs[1])
    links.new(input_node.outputs[9], map_range.inputs[2])
    links.new(input_node.outputs[3], math_001.inputs[0])
    links.new(math_001.outputs[0], math.inputs[0])
    links.new(math.outputs[0], musgrave_texture.inputs[3])
    links.new(input_node.outputs[3], math_002.inputs[0])
    links.new(math_002.outputs[0], math_001.inputs[1])
    links.new(input_node.outputs[4], math_003.inputs[0])
    links.new(math_003.outputs[0], math_004.inputs[0])
    links.new(math_004.outputs[0], math_005.inputs[1])
    links.new(math_005.outputs[0], musgrave_texture.inputs[4])
    links.new(input_node.outputs[5], math_006.inputs[0])
    links.new(math_006.outputs[0], math_005.inputs[0])
    links.new(math_006.outputs[0], musgrave_texture.inputs[5])
    links.new(math_007.outputs[0], mix_006.inputs[0])
    links.new(texture_coordinate_001.outputs[0], mix_006.inputs[6])
    links.new(math_008.outputs[0], math_007.inputs[0])
    links.new(input_node.outputs[0], math_008.inputs[0])
    links.new(input_node.outputs[0], mix_006.inputs[7])
    links.new(mix_006.outputs[2], musgrave_texture.inputs[0])

    return group