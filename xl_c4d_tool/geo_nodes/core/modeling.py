"""【节点组：Modeling — 建模转换】
将曲线转为建模空间：重采样→位置重映射→曲线转网格→网格转曲线"""
import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .change_direction import create_change_direction_group


def create_modeling_group():
    group_name = "Modeling"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Curves", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    frm_main = create_frame(nodes, "建模转换", "建模转换: 重采样→方向变换→位置重映射→曲线转网格→删除→网格转曲线", (0.3, 0.3, 0.1))

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-634.3, 78.7)
    reroute_001.socket_idname = 'NodeSocketGeometry'
    index = nodes.new("GeometryNodeInputIndex")
    index.location = (-132.2, -119.4)
    label_node(index, "索引", frm_main)
    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.location = (-554.3, 63.7)
    label_node(index_001, "索引", frm_main)
    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.location = (-572.6, 179.1)
    label_node(curve_line, "创建直线", frm_main)
    curve_line.mode = 'POINTS'
    curve_line.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    curve_line.inputs[1].default_value = (0.0000, 0.0000, 1.0000)
    curve_line.inputs[2].default_value = (0.0000, 0.0000, 1.0000)
    curve_line.inputs[3].default_value = 1.0
    position = nodes.new("GeometryNodeInputPosition")
    position.location = (-355.9, -17.0)
    label_node(position, "位置数据", frm_main)
    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.location = (253.6, 190.5)
    label_node(curve_to_mesh, "曲线转网格", frm_main)
    curve_to_mesh.inputs[2].default_value = 1.0
    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.location = (658.4, 206.5)
    label_node(mesh_to_curve, "网格转曲线", frm_main)
    mesh_to_curve.mode = 'EDGES'
    mesh_to_curve.inputs[1].default_value = True
    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.location = (447.3, 211.8)
    label_node(delete_geometry, "删除多余边", frm_main)
    delete_geometry.mode = 'ALL'
    delete_geometry.domain = 'EDGE'
    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.location = (-356.0, 233.2)
    label_node(resample_curve, "重采样曲线", frm_main)
    resample_curve.keep_last_segment = False
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = 'Count'
    resample_curve.inputs[4].default_value = 0.10099999606609344
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (55.0, -5.3)
    label_node(math_003, "取模运算", frm_main)
    math_003.operation = 'MODULO'
    math_003.use_clamp = False
    math_003.inputs[2].default_value = 0.5
    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.location = (56.0, 248.3)
    label_node(set_position_001, "设置位置", frm_main)
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = (0.0000, 0.0000, 0.0000)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (48.2, -178.8)
    label_node(math_001, "减法运算", frm_main)
    math_001.operation = 'SUBTRACT'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 1.0
    math_001.inputs[2].default_value = 0.5
    compare = nodes.new("FunctionNodeCompare")
    compare.location = (255.5, 32.2)
    label_node(compare, "比较相等", frm_main)
    compare.operation = 'EQUAL'
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    grp_change_dir = nodes.new("GeometryNodeGroup")
    grp_change_dir.location = (-351.0, -131.4)
    label_node(grp_change_dir, "方向变换", frm_main)
    grp_change_dir.node_tree = create_change_direction_group()
    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.location = (-572.6, -29.8)
    label_node(domain_size, "域大小", frm_main)
    domain_size.component = 'CURVE'
    采样编号 = nodes.new("GeometryNodeSampleIndex")
    label_node(采样编号, "采样位置", frm_main)
    采样编号.data_type = 'FLOAT_VECTOR'
    采样编号.domain = 'POINT'
    采样编号.clamp = True

    links.new(mesh_to_curve.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[0], reroute_001.inputs[0])
    links.new(curve_line.outputs[0], resample_curve.inputs[0])
    links.new(采样编号.outputs[0], set_position_001.inputs[2])
    links.new(position.outputs[0], 采样编号.inputs[1])
    links.new(grp_change_dir.outputs[0], 采样编号.inputs[2])
    links.new(domain_size.outputs[0], grp_change_dir.inputs[1])
    links.new(domain_size.outputs[0], resample_curve.inputs[3])
    links.new(curve_to_mesh.outputs[0], delete_geometry.inputs[0])
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(index.outputs[0], math_003.inputs[0])
    links.new(domain_size.outputs[4], math_003.inputs[1])
    links.new(math_003.outputs[0], compare.inputs[0])
    links.new(math_003.outputs[0], compare.inputs[2])
    links.new(compare.outputs[0], delete_geometry.inputs[1])
    links.new(domain_size.outputs[4], grp_change_dir.inputs[2])
    links.new(index_001.outputs[0], grp_change_dir.inputs[0])
    links.new(set_position_001.outputs[0], curve_to_mesh.inputs[0])
    links.new(resample_curve.outputs[0], set_position_001.inputs[0])
    links.new(domain_size.outputs[4], math_001.inputs[0])
    links.new(math_001.outputs[0], compare.inputs[3])
    links.new(reroute_001.outputs[0], domain_size.inputs[0])
    links.new(reroute_001.outputs[0], 采样编号.inputs[0])

    return group
