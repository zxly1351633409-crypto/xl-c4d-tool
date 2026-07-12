import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def white_splashes():
    """节点组: White Splashes
    白色飞溅噪声 — 生成3D噪声驱动的白色飞溅图案纹理"""
    group_name = "White Splashes"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="值", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="结果", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.location = (258.1, 242.1)
    noise_texture_001.noise_dimensions = '3D'
    noise_texture_001.noise_type = 'FBM'
    noise_texture_001.normalize = True
    noise_texture_001.inputs[3].default_value = 10.0
    noise_texture_001.inputs[5].default_value = 1.8300000429153442
    noise_texture_001.inputs[7].default_value = 1.0
    noise_texture_001.inputs[8].default_value = 0.25
    mapping_001 = nodes.new("ShaderNodeMapping")
    mapping_001.location = (60.6, 243.8)
    mapping_001.vector_type = 'POINT'
    mapping_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (-303.2, 183.2)
    texture_coordinate_001.from_instancer = False
    vector_transform_001 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_001.location = (-141.4, 301.1)
    vector_transform_001.vector_type = 'VECTOR'
    vector_transform_001.convert_from = 'WORLD'
    vector_transform_001.convert_to = 'WORLD'
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (617.7, -33.7)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'STEPPED'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 2.049999952316284
    map_range_003.inputs[5].default_value = 6.900000095367432
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (258.1, -171.6)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = -6.0
    math_001.inputs[2].default_value = 0.5
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (258.1, -42.1)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 0.9300001263618469
    math_002.inputs[2].default_value = 0.5
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (258.1, -301.1)
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    math_003.inputs[1].default_value = 32.0
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (-136.8, 141.2)
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False
    math_004.inputs[0].default_value = 8.0
    math_004.inputs[2].default_value = 0.5
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (-136.8, -16.3)
    math_005.operation = 'DIVIDE'
    math_005.use_clamp = False
    math_005.inputs[1].default_value = 30.0
    math_005.inputs[2].default_value = 0.5
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (-484.7, 142.4)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 6.0
    map_range_004.inputs[4].default_value = 3.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_006 = nodes.new("ShaderNodeMath")
    math_006.location = (-484.5, -96.6)
    math_006.operation = 'GREATER_THAN'
    math_006.use_clamp = False
    math_006.inputs[1].default_value = 0.009999999776482582
    math_006.inputs[2].default_value = 0.5
    math_007 = nodes.new("ShaderNodeMath")
    math_007.location = (-307.4, -14.9)
    math_007.operation = 'MULTIPLY'
    math_007.use_clamp = False
    math_007.inputs[2].default_value = 0.5
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (-486.6, -247.5)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 1.0
    map_range_005.inputs[4].default_value = 0.8399999737739563
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (-27.6, -282.9)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (206.7, -275.4)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (-606.8, -203.3)
    reroute_002.socket_idname = 'NodeSocketFloat'

    # === 节点连接 ===
    links.new(math_004.outputs[0], noise_texture_001.inputs[2])
    links.new(reroute_001.outputs[0], math_003.inputs[0])
    links.new(math_001.outputs[0], map_range_003.inputs[3])
    links.new(noise_texture_001.outputs[0], map_range_003.inputs[0])
    links.new(math_005.outputs[0], reroute_001.inputs[0])
    links.new(texture_coordinate_001.outputs[3], vector_transform_001.inputs[0])
    links.new(map_range_005.outputs[0], reroute.inputs[0])
    links.new(math_007.outputs[0], math_005.inputs[0])
    links.new(reroute_001.outputs[0], math_002.inputs[0])
    links.new(reroute.outputs[0], noise_texture_001.inputs[4])
    links.new(vector_transform_001.outputs[0], mapping_001.inputs[0])
    links.new(math_003.outputs[0], map_range_003.inputs[4])
    links.new(math_007.outputs[0], math_004.inputs[1])
    links.new(mapping_001.outputs[0], noise_texture_001.inputs[0])
    links.new(math_006.outputs[0], math_007.inputs[1])
    links.new(reroute_001.outputs[0], math_001.inputs[0])
    links.new(map_range_004.outputs[0], math_007.inputs[0])
    links.new(math_002.outputs[0], map_range_003.inputs[1])
    links.new(reroute_002.outputs[0], map_range_004.inputs[0])
    links.new(reroute_002.outputs[0], math_006.inputs[0])
    links.new(reroute_002.outputs[0], map_range_005.inputs[0])
    links.new(map_range_003.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[0], reroute_002.inputs[0])

    return group