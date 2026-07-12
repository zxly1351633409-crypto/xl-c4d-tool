"""【节点组：Change Direction — 索引方向重映射】
根据Direction参数重新计算每个截面曲线的索引映射值，
用于控制放样截面的排列方向。支持正向/反向/交替等多方向排列模式。
算法: Index % Direction → 取模 × Total → + Index → / Direction"""
import bpy
from ...utils.node_utils import create_frame, label_node


def create_change_direction_group():
    """【节点组：Change Direction — 索引方向重映射】
    根据"方向(Direction)"参数重新计算每个截面的索引映射值。
    算法: Index % Direction → 取模 × Total → + Index → / Direction"""
    group_name = "Change Direction"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Total", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Direction", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Index", in_out="OUTPUT", socket_type="NodeSocketFloat")
    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    frm_main = create_frame(nodes, "索引重映射", "索引重映射: Index%Direction→×Total→+Index→/Direction", (0.3, 0.3, 0.1))

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-311.4, 44.0)
    reroute_001.socket_idname = 'NodeSocketInt'
    reroute = nodes.new("NodeReroute")
    reroute.location = (-314.1, -168.3)
    reroute.socket_idname = 'NodeSocketInt'

    math = nodes.new("ShaderNodeMath")
    math.location = (-221.8, 46.1)
    label_node(math, "取模(Index%Direction)", frm_main)
    math.operation = 'MODULO'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5

    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (-21.7, 46.1)
    label_node(math_002, "乘法(×Total)", frm_main)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False

    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (165.4, 46.1)
    label_node(math_001, "加法(+Index)", frm_main)
    math_001.operation = 'ADD'
    math_001.use_clamp = False

    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (351.7, 46.1)
    label_node(math_005, "除法(/Direction)", frm_main)
    math_005.operation = 'DIVIDE'
    math_005.use_clamp = False

    links.new(math_005.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[1], math_002.inputs[1])
    links.new(input_node.outputs[2], reroute.inputs[0])
    links.new(input_node.outputs[0], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], math.inputs[0])
    links.new(math.outputs[0], math_002.inputs[0])
    links.new(math_002.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], math_005.inputs[0])
    links.new(reroute_001.outputs[0], math_001.inputs[1])
    links.new(reroute.outputs[0], math_005.inputs[1])
    links.new(reroute.outputs[0], math.inputs[1])

    return group
