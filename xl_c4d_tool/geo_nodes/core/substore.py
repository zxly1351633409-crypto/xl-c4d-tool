"""【节点组：SubStore — 属性存储/读取器】
通过Sample Index从曲线几何体中读取已存储的细分命名属性。
读取的属性包括：sub_type（类型）、sub_left_pos（左位置）、sub_right_pos（右位置）、
sub_handle_scale（控制柄缩放）、sub_div（细分计数）、use_sub（启用细分标志）。
是Subdivide节点组的内部子模块，为细分流程提供属性读写支持。"""
import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_substore_group():
    group_name = "SubStore"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    group.interface.new_socket(name="Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Enable", in_out="OUTPUT", socket_type="NodeSocketBool")
    group.interface.new_socket(name="Type", in_out="OUTPUT", socket_type="NodeSocketInt")
    group.interface.new_socket(name="Left Position", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Right Position", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Handle Scale", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Subdivde", in_out="OUTPUT", socket_type="NodeSocketInt")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.location = (453.1, -99.7)
    named_attribute_002.data_type = 'FLOAT_VECTOR'
    named_attribute_002.inputs[0].default_value = 'sub_right_pos'
    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.location = (690.3, -78.1)
    named_attribute_003.data_type = 'INT'
    named_attribute_003.inputs[0].default_value = 'sub_div'
    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.location = (-0.6, -94.6)
    named_attribute.data_type = 'INT'
    named_attribute.inputs[0].default_value = 'sub_type'
    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.location = (238.0, -95.9)
    named_attribute_001.data_type = 'FLOAT_VECTOR'
    named_attribute_001.inputs[0].default_value = 'sub_left_pos'
    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.location = (913.3, -85.5)
    named_attribute_004.data_type = 'BOOLEAN'
    named_attribute_004.inputs[0].default_value = 'use_sub'
    reroute = nodes.new("NodeReroute")
    reroute.location = (-97.3, 23.6)
    reroute.socket_idname = 'NodeSocketInt'
    named_attribute_005 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.location = (1156.1, -60.0)
    named_attribute_005.data_type = 'FLOAT_VECTOR'
    named_attribute_005.inputs[0].default_value = 'sub_handle_scale'
    采样编号 = nodes.new("GeometryNodeSampleIndex")
    采样编号.data_type = 'INT'
    采样编号.domain = 'CURVE'
    采样编号.clamp = True
    采样编号_001 = nodes.new("GeometryNodeSampleIndex")
    采样编号_001.data_type = 'INT'
    采样编号_001.domain = 'CURVE'
    采样编号_001.clamp = True
    采样编号_002 = nodes.new("GeometryNodeSampleIndex")
    采样编号_002.data_type = 'FLOAT_VECTOR'
    采样编号_002.domain = 'CURVE'
    采样编号_002.clamp = True
    采样编号_003 = nodes.new("GeometryNodeSampleIndex")
    采样编号_003.data_type = 'FLOAT_VECTOR'
    采样编号_003.domain = 'CURVE'
    采样编号_003.clamp = True
    采样编号_004 = nodes.new("GeometryNodeSampleIndex")
    采样编号_004.data_type = 'BOOLEAN'
    采样编号_004.domain = 'CURVE'
    采样编号_004.clamp = True
    采样编号_005 = nodes.new("GeometryNodeSampleIndex")
    采样编号_005.data_type = 'FLOAT_VECTOR'
    采样编号_005.domain = 'CURVE'
    采样编号_005.clamp = True

    links.new(input_node.outputs[0], 采样编号.inputs[0])
    links.new(采样编号.outputs[0], output_node.inputs[1])
    links.new(named_attribute.outputs[0], 采样编号.inputs[1])
    links.new(input_node.outputs[0], 采样编号_003.inputs[0])
    links.new(named_attribute_001.outputs[0], 采样编号_003.inputs[1])
    links.new(采样编号_003.outputs[0], output_node.inputs[2])
    links.new(input_node.outputs[0], 采样编号_002.inputs[0])
    links.new(named_attribute_002.outputs[0], 采样编号_002.inputs[1])
    links.new(采样编号_002.outputs[0], output_node.inputs[3])
    links.new(reroute.outputs[0], 采样编号.inputs[2])
    links.new(reroute.outputs[0], 采样编号_003.inputs[2])
    links.new(reroute.outputs[0], 采样编号_002.inputs[2])
    links.new(input_node.outputs[0], 采样编号_001.inputs[0])
    links.new(reroute.outputs[0], 采样编号_001.inputs[2])
    links.new(named_attribute_003.outputs[0], 采样编号_001.inputs[1])
    links.new(采样编号_001.outputs[0], output_node.inputs[5])
    links.new(input_node.outputs[0], 采样编号_004.inputs[0])
    links.new(reroute.outputs[0], 采样编号_004.inputs[2])
    links.new(named_attribute_004.outputs[0], 采样编号_004.inputs[1])
    links.new(采样编号_004.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[1], reroute.inputs[0])
    links.new(input_node.outputs[0], 采样编号_005.inputs[0])
    links.new(reroute.outputs[0], 采样编号_005.inputs[2])
    links.new(named_attribute_005.outputs[0], 采样编号_005.inputs[1])
    links.new(采样编号_005.outputs[0], output_node.inputs[4])

    return group
