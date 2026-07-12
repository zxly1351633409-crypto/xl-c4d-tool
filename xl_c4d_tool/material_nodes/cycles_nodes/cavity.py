import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def cavity():
    """节点组: Cavity
    凹腔检测遮罩 — 基于AO采样识别凹面/凸面区域，生成遮罩用于脏污/磨损效果合成"""
    group_name = "Cavity"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="采样距离", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="遮罩强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="值", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    math = nodes.new("ShaderNodeMath")
    math.location = (517.2, 57.1)
    math.operation = 'MULTIPLY_ADD'
    math.use_clamp = True
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (350.7, 52.3)
    math_001.operation = 'ADD'
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (163.5, -123.7)
    math_003.operation = 'SUBTRACT'
    math_003.use_clamp = False
    math_003.inputs[0].default_value = 1.0
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (143.9, 144.5)
    math_004.operation = 'SUBTRACT'
    math_004.use_clamp = False
    math_004.inputs[0].default_value = 1.0
    math_004.inputs[2].default_value = 0.5
    ambient_occlusion = nodes.new("ShaderNodeAmbientOcclusion")
    ambient_occlusion.location = (-54.6, -118.6)
    ambient_occlusion.samples = 32
    ambient_occlusion.inside = False
    ambient_occlusion.only_local = False
    ambient_occlusion.inputs[0].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (-297.7, -81.2)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (-536.8, -170.1)
    math_005.operation = 'DIVIDE'
    math_005.use_clamp = False
    math_005.inputs[1].default_value = 10.0
    math_005.inputs[2].default_value = 0.5
    ambient_occlusion_001 = nodes.new("ShaderNodeAmbientOcclusion")
    ambient_occlusion_001.location = (-58.8, 184.0)
    ambient_occlusion_001.samples = 32
    ambient_occlusion_001.inside = False
    ambient_occlusion_001.only_local = False
    ambient_occlusion_001.inputs[0].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (-298.9, 211.4)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.location = (-790.9, -0.0)

    # === 节点连接 ===
    links.new(math_001.outputs[0], math.inputs[0])
    links.new(ambient_occlusion.outputs[1], math_003.inputs[1])
    links.new(math_004.outputs[0], math_001.inputs[0])
    links.new(math_003.outputs[0], math_001.inputs[1])
    links.new(map_range.outputs[0], ambient_occlusion.inputs[1])
    links.new(ambient_occlusion_001.outputs[1], math_004.inputs[1])
    links.new(map_range_001.outputs[0], ambient_occlusion_001.inputs[1])
    links.new(input_node.outputs[2], math.inputs[1])
    links.new(input_node.outputs[0], map_range_001.inputs[4])
    links.new(input_node.outputs[0], math_005.inputs[0])
    links.new(math_005.outputs[0], map_range.inputs[4])
    links.new(input_node.outputs[1], map_range.inputs[0])
    links.new(input_node.outputs[1], map_range_001.inputs[0])
    links.new(geometry.outputs[1], ambient_occlusion.inputs[2])
    links.new(geometry.outputs[1], ambient_occlusion_001.inputs[2])
    links.new(math.outputs[0], output_node.inputs[0])

    return group