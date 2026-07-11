"""【节点组：Subdivide — 曲线细分处理】
对输入曲线进行细分/重采样控制：根据U Resolution参数计算细分数量，
支持Each（每段独立）和Total（总段数）两种细分模式。
内部通过SubStore子存储读写各控制点的细分属性（类型/左右位置/控制柄缩放）。
输出细分后的count、左右位置、控制柄缩放及类型信息，供Curves Control调用。"""
import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .substore import create_substore_group


def create_subdivide_group():
    group_name = "Subdivide"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    group.interface.new_socket(name="Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="U Resolution", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Each | Total", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="count", in_out="OUTPUT", socket_type="NodeSocketInt")
    group.interface.new_socket(name="Left Position", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Right Position", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Handle Scale", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Type", in_out="OUTPUT", socket_type="NodeSocketInt")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    math = nodes.new("ShaderNodeMath")
    math.location = (-448.2, -32.8)
    math.operation = 'ADD'
    math.use_clamp = False
    math.inputs[1].default_value = 1.0
    math.inputs[2].default_value = 0.5
    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.location = (-260.0, -32.8)
    compare_001.operation = 'EQUAL'
    compare_001.data_type = 'INT'
    compare_001.mode = 'ELEMENT'
    index_004 = nodes.new("GeometryNodeInputIndex")
    index_004.location = (-877.0, -38.0)
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (-677.0, -35.9)
    math_005.operation = 'MODULO'
    math_005.use_clamp = False
    math_005.inputs[2].default_value = 0.5
    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.location = (-879.2, -110.5)
    domain_size.component = 'CURVE'
    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.location = (-68.0, -32.8)
    switch_001.input_type = 'INT'
    group_006 = nodes.new("GeometryNodeGroup")
    group_006.location = (170.0, -88.0)
    group_006.node_tree = create_substore_group()
    group_005 = nodes.new("GeometryNodeGroup")
    group_005.location = (168.4, 204.9)
    group_005.node_tree = create_substore_group()
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (594.7, 30.7)
    math_002.operation = 'ADD'
    math_002.use_clamp = False
    math_002.inputs[2].default_value = 0.5
    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.location = (383.2, 184.4)
    boolean_math.operation = 'OR'
    switch = nodes.new("GeometryNodeSwitch")
    switch.location = (596.6, 220.6)
    switch.input_type = 'INT'
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (817.1, 190.2)
    math_004.operation = 'ADD'
    math_004.use_clamp = False
    math_004.inputs[2].default_value = 0.5
    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.location = (1059.6, 234.2)
    switch_002.input_type = 'INT'

    links.new(input_node.outputs[0], group_005.inputs[0])
    links.new(input_node.outputs[1], switch.inputs[1])
    links.new(group_005.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], switch.inputs[0])
    links.new(math.outputs[0], compare_001.inputs[0])
    links.new(math.outputs[0], compare_001.inputs[2])
    links.new(compare_001.outputs[0], switch_001.inputs[0])
    links.new(math.outputs[0], switch_001.inputs[1])
    links.new(switch_001.outputs[0], group_006.inputs[1])
    links.new(math_005.outputs[0], group_005.inputs[1])
    links.new(group_006.outputs[0], boolean_math.inputs[1])
    links.new(group_005.outputs[5], math_002.inputs[0])
    links.new(group_006.outputs[5], math_002.inputs[1])
    links.new(switch.outputs[0], math_004.inputs[0])
    links.new(math_002.outputs[0], math_004.inputs[1])
    links.new(index_004.outputs[0], math_005.inputs[0])
    links.new(math_005.outputs[0], math.inputs[0])
    links.new(domain_size.outputs[4], math_005.inputs[1])
    links.new(domain_size.outputs[4], compare_001.inputs[3])
    links.new(input_node.outputs[0], group_006.inputs[0])
    links.new(group_005.outputs[1], output_node.inputs[4])
    links.new(group_005.outputs[2], output_node.inputs[1])
    links.new(group_005.outputs[3], output_node.inputs[2])
    links.new(group_005.outputs[4], output_node.inputs[3])
    links.new(switch_002.outputs[0], output_node.inputs[0])
    links.new(math_004.outputs[0], switch_002.inputs[1])
    links.new(input_node.outputs[2], switch_002.inputs[0])
    links.new(input_node.outputs[1], switch_002.inputs[2])
    links.new(input_node.outputs[0], domain_size.inputs[0])

    return group
