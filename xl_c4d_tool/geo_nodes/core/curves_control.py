"""【节点组：Curves Control — 曲线控制与细分】
放样流程核心控制：Bezier转换→手柄设置→细分/重采样→U向闭合"""
import bpy
from ...utils.node_utils import create_frame, label_node
from .subdivide import create_subdivide_group


def create_curves_control_group():
    group_name = "Curves Control"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    group.interface.new_socket(name="Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Sources", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="U Resolution", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Each | Total", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="U Cyclic", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="Curves", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    frm_type = create_frame(nodes, "手柄类型设置", "手柄类型设置: 判断类型→设置自动/对齐手柄", (0.3, 0.3, 0.1))
    frm_pos = create_frame(nodes, "手柄位置设置", "手柄位置设置: 切线方向→缩放→左右手柄位置", (0.2, 0.4, 0.2))
    frm_output = create_frame(nodes, "输出处理", "输出处理: 分辨率→U向闭合→细分/重采样→切换输出", (0.3, 0.1, 0.3))

    set_handle_type = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type.location = (-148.3, 55.7)
    label_node(set_handle_type, "设置手柄类型①", frm_type)
    set_handle_type.handle_type = 'AUTO'
    set_handle_type_001 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_001.location = (131.9, 49.8)
    label_node(set_handle_type_001, "设置手柄类型②", frm_type)
    set_handle_type_001.handle_type = 'AUTO'
    set_handle_type_003 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_003.location = (651.6, 47.9)
    label_node(set_handle_type_003, "设置手柄类型④", frm_type)
    set_handle_type_003.handle_type = 'AUTO'
    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.location = (-135.4, -125.3)
    label_node(compare_001, "类型==1?", frm_type)
    compare_001.operation = 'EQUAL'
    compare_001.data_type = 'INT'
    compare_001.mode = 'ELEMENT'
    compare_001.inputs[3].default_value = 1
    compare = nodes.new("FunctionNodeCompare")
    compare.location = (-414.2, -125.3)
    label_node(compare, "类型==0?", frm_type)
    compare.operation = 'EQUAL'
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.location = (398.2, -114.8)
    label_node(compare_003, "类型==3?", frm_type)
    compare_003.operation = 'EQUAL'
    compare_003.data_type = 'INT'
    compare_003.mode = 'ELEMENT'
    compare_003.inputs[3].default_value = 3
    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.location = (147.6, -124.1)
    label_node(compare_002, "类型==2?", frm_type)
    compare_002.operation = 'EQUAL'
    compare_002.data_type = 'INT'
    compare_002.mode = 'ELEMENT'
    compare_002.inputs[3].default_value = 2
    set_handle_positions_005 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_005.location = (863.2, 56.2)
    label_node(set_handle_positions_005, "设置左手柄位置", frm_pos)
    set_handle_positions_005.mode = 'LEFT'
    set_handle_positions_005.inputs[1].default_value = True
    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.location = (395.2, -293.4)
    label_node(vector_math_001, "缩放切线方向", frm_pos)
    vector_math_001.operation = 'SCALE'
    vector_math_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    vector_math_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math_001.inputs[3].default_value = -1.0
    reroute = nodes.new("NodeReroute")
    reroute.location = (216.8, -353.6)
    reroute.socket_idname = 'NodeSocketVector'
    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.location = (862.6, -146.1)
    label_node(vector_math_002, "右手柄偏移", frm_pos)
    vector_math_002.operation = 'MULTIPLY_ADD'
    vector_math_002.inputs[3].default_value = 1.0
    curve_handle_positions = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions.location = (381.5, -525.8)
    label_node(curve_handle_positions, "手柄位置数据", frm_pos)
    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.location = (386.5, -452.0)
    label_node(curve_tangent, "曲线切线", frm_pos)
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (648.2, -149.3)
    label_node(vector_math, "左手柄偏移", frm_pos)
    vector_math.operation = 'MULTIPLY_ADD'
    vector_math.inputs[3].default_value = 1.0
    set_handle_type_002 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_002.location = (395.9, 57.3)
    label_node(set_handle_type_002, "设置手柄类型③", frm_type)
    set_handle_type_002.handle_type = 'AUTO'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1933.4, -77.3)
    reroute_001.socket_idname = 'NodeSocketInt'
    subdivide_curve = nodes.new("GeometryNodeSubdivideCurve")
    subdivide_curve.location = (2017.8, 112.3)
    label_node(subdivide_curve, "细分曲线", frm_output)
    set_handle_positions_004 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_004.location = (1088.2, 70.1)
    label_node(set_handle_positions_004, "设置右手柄位置", frm_pos)
    set_handle_positions_004.mode = 'RIGHT'
    set_handle_positions_004.inputs[1].default_value = True
    set_spline_cyclic_004 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_004.location = (1769.3, 63.4)
    label_node(set_spline_cyclic_004, "设置U向闭合", frm_output)
    set_spline_cyclic_004.inputs[1].default_value = True
    set_spline_resolution_003 = nodes.new("GeometryNodeSetSplineResolution")
    set_spline_resolution_003.location = (1340.4, 62.1)
    label_node(set_spline_resolution_003, "设置分辨率", frm_output)
    set_spline_resolution_003.inputs[1].default_value = True
    set_spline_resolution_003.inputs[2].default_value = 1
    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.location = (1557.7, 68.7)
    label_node(switch_001, "分辨率/手柄切换", frm_output)
    switch_001.input_type = 'GEOMETRY'
    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.location = (2016.0, -27.7)
    label_node(resample_curve, "重采样曲线", frm_output)
    resample_curve.keep_last_segment = False
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = 'Count'
    resample_curve.inputs[4].default_value = 0.10000000149011612
    switch = nodes.new("GeometryNodeSwitch")
    switch.location = (2233.5, 88.4)
    label_node(switch, "细分/重采样切换", frm_output)
    switch.input_type = 'GEOMETRY'
    set_spline_type_002 = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type_002.location = (-413.4, 63.3)
    label_node(set_spline_type_002, "转为Bezier", frm_type)
    set_spline_type_002.spline_type = 'BEZIER'
    set_spline_type_002.inputs[1].default_value = True
    grp_subdivide = nodes.new("GeometryNodeGroup")
    grp_subdivide.location = (-657.2, -52.8)
    label_node(grp_subdivide, "细分处理", frm_type)
    grp_subdivide.node_tree = create_subdivide_group()

    links.new(input_node.outputs[0], set_spline_type_002.inputs[0])
    links.new(grp_subdivide.outputs[1], set_handle_positions_005.inputs[3])
    links.new(grp_subdivide.outputs[2], set_handle_positions_004.inputs[3])
    links.new(set_handle_positions_005.outputs[0], set_handle_positions_004.inputs[0])
    links.new(set_handle_positions_004.outputs[0], set_spline_resolution_003.inputs[0])
    links.new(switch_001.outputs[0], set_spline_cyclic_004.inputs[0])
    links.new(set_handle_type.outputs[0], set_handle_type_001.inputs[0])
    links.new(set_handle_type_001.outputs[0], set_handle_type_002.inputs[0])
    links.new(set_handle_type_002.outputs[0], set_handle_type_003.inputs[0])
    links.new(compare.outputs[0], set_handle_type.inputs[1])
    links.new(compare_001.outputs[0], set_handle_type_001.inputs[1])
    links.new(compare_002.outputs[0], set_handle_type_002.inputs[1])
    links.new(compare_003.outputs[0], set_handle_type_003.inputs[1])
    links.new(set_spline_type_002.outputs[0], set_handle_type.inputs[0])
    links.new(grp_subdivide.outputs[4], compare.inputs[2])
    links.new(grp_subdivide.outputs[4], compare_001.inputs[2])
    links.new(grp_subdivide.outputs[4], compare_002.inputs[2])
    links.new(grp_subdivide.outputs[4], compare_003.inputs[2])
    links.new(set_handle_type_003.outputs[0], set_handle_positions_005.inputs[0])
    links.new(set_spline_cyclic_004.outputs[0], subdivide_curve.inputs[0])
    links.new(reroute_001.outputs[0], subdivide_curve.inputs[1])
    links.new(input_node.outputs[2], grp_subdivide.inputs[1])
    links.new(input_node.outputs[4], set_spline_cyclic_004.inputs[2])
    links.new(input_node.outputs[1], grp_subdivide.inputs[0])
    links.new(curve_tangent.outputs[0], vector_math.inputs[0])
    links.new(vector_math_001.outputs[0], vector_math.inputs[1])
    links.new(curve_handle_positions.outputs[0], vector_math.inputs[2])
    links.new(vector_math.outputs[0], set_handle_positions_005.inputs[2])
    links.new(reroute.outputs[0], vector_math_001.inputs[0])
    links.new(curve_tangent.outputs[0], vector_math_002.inputs[0])
    links.new(curve_handle_positions.outputs[1], vector_math_002.inputs[2])
    links.new(vector_math_002.outputs[0], set_handle_positions_004.inputs[2])
    links.new(grp_subdivide.outputs[3], reroute.inputs[0])
    links.new(reroute.outputs[0], vector_math_002.inputs[1])
    links.new(set_spline_cyclic_004.outputs[0], resample_curve.inputs[0])
    links.new(grp_subdivide.outputs[0], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], resample_curve.inputs[3])
    links.new(subdivide_curve.outputs[0], switch.inputs[1])
    links.new(switch.outputs[0], output_node.inputs[0])
    links.new(resample_curve.outputs[0], switch.inputs[2])
    links.new(set_spline_resolution_003.outputs[0], switch_001.inputs[1])
    links.new(set_handle_positions_004.outputs[0], switch_001.inputs[2])
    links.new(input_node.outputs[3], switch_001.inputs[0])
    links.new(input_node.outputs[3], switch.inputs[0])
    links.new(input_node.outputs[3], grp_subdivide.inputs[2])

    return group
