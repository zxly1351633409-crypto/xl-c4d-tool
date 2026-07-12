import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def all_edges():
    """节点组: All Edges
    边缘检测遮罩 — 基于Bevel法线检测识别模型边缘，生成边缘磨损遮罩"""
    group_name = "All Edges"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="检测距离", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.020000001415610313
    group.interface.new_socket(name="纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="遮罩强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 4.0
    group.interface.new_socket(name="遮罩", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (-367.4, 77.1)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (-60.8, 21.9)
    vector_math.operation = 'DOT_PRODUCT'
    vector_math.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[3].default_value = 1.0
    math = nodes.new("ShaderNodeMath")
    math.location = (-524.5, 78.7)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (93.1, 75.7)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[1].default_value = 0.9900000095367432
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[4].default_value = -0.20000000298023224
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.location = (-365.1, -131.6)
    reroute = nodes.new("NodeReroute")
    reroute.location = (-524.2, -115.9)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-153.0, -79.0)
    reroute_001.socket_idname = 'NodeSocketVector'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (-152.3, -58.8)
    reroute_002.socket_idname = 'NodeSocketVector'

    # === 节点连接 ===
    links.new(map_range.outputs[0], output_node.inputs[0])
    links.new(reroute_002.outputs[0], vector_math.inputs[0])
    links.new(vector_math.outputs[1], map_range.inputs[0])
    links.new(input_node.outputs[0], math.inputs[0])
    links.new(math.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[1], math.inputs[1])
    links.new(reroute.outputs[0], map_range.inputs[3])
    links.new(reroute_001.outputs[0], vector_math.inputs[1])
    links.new(input_node.outputs[2], reroute.inputs[0])
    links.new(geometry.outputs[1], reroute_001.inputs[0])
    links.new(bevel.outputs[0], reroute_002.inputs[0])

    return group