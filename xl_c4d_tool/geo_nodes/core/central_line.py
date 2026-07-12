"""【节点组：Central Line — 中线生成】
计算曲线骨架中线，用于放样路径提取"""
import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_central_line_group():
    group_name = "Central line"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    group.interface.new_socket(name="Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    frm_main = create_frame(nodes, "中线生成", "中线生成: 创建直线→重采样→采样位置→设置位置", (0.3, 0.3, 0.1))

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.location = (-223.4, -169.5)
    label_node(position_002, "位置数据", frm_main)
    curve_line_001 = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_001.location = (-200.7, 72.6)
    label_node(curve_line_001, "创建直线", frm_main)
    curve_line_001.mode = 'POINTS'
    curve_line_001.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    curve_line_001.inputs[1].default_value = (0.0000, 0.0000, 1.0000)
    curve_line_001.inputs[2].default_value = (0.0000, 0.0000, 1.0000)
    curve_line_001.inputs[3].default_value = 1.0
    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.location = (24.4, 169.5)
    label_node(resample_curve_002, "重采样曲线", frm_main)
    resample_curve_002.keep_last_segment = False
    resample_curve_002.inputs[1].default_value = True
    resample_curve_002.inputs[2].default_value = 'Count'
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    domain_size_002 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_002.location = (-224.6, -2.0)
    label_node(domain_size_002, "曲线域大小", frm_main)
    domain_size_002.component = 'CURVE'
    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.location = (238.7, 153.9)
    label_node(set_position_002, "设置位置", frm_main)
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[3].default_value = (0.0000, 0.0000, 0.0000)
    采样编号 = nodes.new("GeometryNodeSampleIndex")
    label_node(采样编号, "采样位置", frm_main)
    采样编号.data_type = 'FLOAT_VECTOR'
    采样编号.domain = 'CURVE'
    采样编号.clamp = True
    编号 = nodes.new("GeometryNodeInputIndex")
    label_node(编号, "索引", frm_main)

    links.new(input_node.outputs[0], domain_size_002.inputs[0])
    links.new(set_position_002.outputs[0], output_node.inputs[0])
    links.new(curve_line_001.outputs[0], resample_curve_002.inputs[0])
    links.new(domain_size_002.outputs[4], resample_curve_002.inputs[3])
    links.new(resample_curve_002.outputs[0], set_position_002.inputs[0])
    links.new(采样编号.outputs[0], set_position_002.inputs[2])
    links.new(position_002.outputs[0], 采样编号.inputs[1])
    links.new(input_node.outputs[0], 采样编号.inputs[0])
    links.new(编号.outputs[0], 采样编号.inputs[2])

    return group
