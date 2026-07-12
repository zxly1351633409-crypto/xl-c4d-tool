"""【节点：OC_曲率 Curvature】
基于AO检测凹面/凸面曲率，支持全局/自身/其他物体模式"""
import bpy
from ..utils.node_utils import get_mix_f_ports, create_frame, label_node, build_object_mode_switcher


def create_oc_curvature_group():
    group_name = "OC_曲率"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="Mode (0=All, 1=Concave, 2=Convex)", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Strength", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="Radius", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="Radius map", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="Tolerance", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="Spread", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="Invert normal", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="Obj Mode (0=All,1=Self,2=Others)", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Curvature", in_out="OUTPUT", socket_type="NodeSocketFloat")
    nodes = group.nodes
    links = group.links
    node_in = nodes.new("NodeGroupInput")
    node_out = nodes.new("NodeGroupOutput")

    frm_radius = create_frame(nodes, "半径计算", "半径计算: 基础半径 × 半径贴图", (0.3, 0.3, 0.1))
    math_radius = nodes.new("ShaderNodeMath")
    math_radius.operation = "MULTIPLY"
    label_node(math_radius, "半径 × 贴图", frm_radius)
    links.new(node_in.outputs[2], math_radius.inputs[0])
    links.new(node_in.outputs[3], math_radius.inputs[1])

    frm_ao = create_frame(nodes, "AO采样", "AO采样: 4组AO检测凹面/凸面 × 全局/自身", (0.4, 0.2, 0.1))
    ao_conc_all = nodes.new("ShaderNodeAmbientOcclusion")
    ao_conc_all.inside = False
    label_node(ao_conc_all, "凹面-全局AO", frm_ao)
    ao_conc_self = nodes.new("ShaderNodeAmbientOcclusion")
    ao_conc_self.inside = False
    ao_conc_self.only_local = True
    label_node(ao_conc_self, "凹面-自身AO", frm_ao)
    ao_conv_all = nodes.new("ShaderNodeAmbientOcclusion")
    ao_conv_all.inside = True
    label_node(ao_conv_all, "凸面-全局AO", frm_ao)
    ao_conv_self = nodes.new("ShaderNodeAmbientOcclusion")
    ao_conv_self.inside = True
    ao_conv_self.only_local = True
    label_node(ao_conv_self, "凸面-自身AO", frm_ao)
    for n in [ao_conc_all, ao_conc_self, ao_conv_all, ao_conv_self]:
        links.new(math_radius.outputs[0], n.inputs[1])

    frm_obj_mode = create_frame(nodes, "物体模式切换", "物体模式: 根据Obj Mode选择全局/自身/其他", (0.2, 0.4, 0.4))
    raw_concave = build_object_mode_switcher(nodes, links, node_in.outputs[8], ao_conc_all.outputs[0], ao_conc_self.outputs[0], frm_obj_mode)
    raw_convex = build_object_mode_switcher(nodes, links, node_in.outputs[8], ao_conv_all.outputs[0], ao_conv_self.outputs[0], frm_obj_mode)

    frm_invert = create_frame(nodes, "反转处理", "反转: 1-AO值 得到凹/凸遮罩", (0.2, 0.3, 0.5))
    inv_conc = nodes.new("ShaderNodeMath")
    inv_conc.operation = "SUBTRACT"
    inv_conc.inputs[0].default_value = 1.0
    label_node(inv_conc, "1-凹面AO(凹面遮罩)", frm_invert)
    inv_conv = nodes.new("ShaderNodeMath")
    inv_conv.operation = "SUBTRACT"
    inv_conv.inputs[0].default_value = 1.0
    label_node(inv_conv, "1-凸面AO(凸面遮罩)", frm_invert)
    links.new(raw_concave, inv_conc.inputs[1])
    links.new(raw_convex, inv_conv.inputs[1])

    frm_normal = create_frame(nodes, "法线反转", "法线反转: 根据开关交换凹/凸", (0.3, 0.2, 0.4))
    mix_sw_conc = nodes.new("ShaderNodeMix"); mix_sw_conc.data_type = "FLOAT"
    label_node(mix_sw_conc, "凹面/凸面交换", frm_normal)
    mix_sw_conv = nodes.new("ShaderNodeMix"); mix_sw_conv.data_type = "FLOAT"
    label_node(mix_sw_conv, "凸面/凹面交换", frm_normal)
    sw1_f, sw1_a, sw1_b, sw1_r = get_mix_f_ports(mix_sw_conc)
    sw2_f, sw2_a, sw2_b, sw2_r = get_mix_f_ports(mix_sw_conv)
    links.new(node_in.outputs[7], sw1_f); links.new(inv_conc.outputs[0], sw1_a); links.new(inv_conv.outputs[0], sw1_b)
    links.new(node_in.outputs[7], sw2_f); links.new(inv_conv.outputs[0], sw2_a); links.new(inv_conc.outputs[0], sw2_b)
    math_all = nodes.new("ShaderNodeMath"); math_all.operation = "MAXIMUM"
    label_node(math_all, "取最大值(凹+凸合并)", frm_normal)
    links.new(sw1_r, math_all.inputs[0]); links.new(sw2_r, math_all.inputs[1])

    frm_mode = create_frame(nodes, "模式切换", "模式切换: All=最大值, Concave=凹面, Convex=凸面", (0.1, 0.4, 0.2))
    comp_m1 = nodes.new("ShaderNodeMath"); comp_m1.operation = "COMPARE"
    comp_m1.inputs[1].default_value = 1.0; comp_m1.inputs[2].default_value = 0.1
    label_node(comp_m1, "Mode=1?(凹面)", frm_mode)
    comp_m2 = nodes.new("ShaderNodeMath"); comp_m2.operation = "COMPARE"
    comp_m2.inputs[1].default_value = 2.0; comp_m2.inputs[2].default_value = 0.1
    label_node(comp_m2, "Mode=2?(凸面)", frm_mode)
    mix_m1 = nodes.new("ShaderNodeMix"); mix_m1.data_type = "FLOAT"
    label_node(mix_m1, "混合: 全部/凹面", frm_mode)
    mix_m2 = nodes.new("ShaderNodeMix"); mix_m2.data_type = "FLOAT"
    label_node(mix_m2, "混合: 凹面/凸面", frm_mode)
    m1_f, m1_a, m1_b, m1_r = get_mix_f_ports(mix_m1)
    m2_f, m2_a, m2_b, m2_r = get_mix_f_ports(mix_m2)
    links.new(node_in.outputs[0], comp_m1.inputs[0]); links.new(node_in.outputs[0], comp_m2.inputs[0])
    links.new(comp_m1.outputs[0], m1_f); links.new(math_all.outputs[0], m1_a); links.new(sw1_r, m1_b)
    links.new(comp_m2.outputs[0], m2_f); links.new(m1_r, m2_a); links.new(sw2_r, m2_b)

    frm_output = create_frame(nodes, "输出处理", "输出处理: 偏移→容差/扩散映射→强度", (0.3, 0.1, 0.3))
    math_offset = nodes.new("ShaderNodeMath"); math_offset.operation = "ADD"
    label_node(math_offset, "加偏移量", frm_output)
    map_range = nodes.new("ShaderNodeMapRange"); map_range.clamp = False
    label_node(map_range, "容差/扩散映射", frm_output)
    math_str = nodes.new("ShaderNodeMath"); math_str.operation = "MULTIPLY"
    label_node(math_str, "乘以强度", frm_output)
    links.new(m2_r, math_offset.inputs[0]); links.new(node_in.outputs[4], math_offset.inputs[1])
    links.new(math_offset.outputs[0], map_range.inputs[0])
    links.new(node_in.outputs[5], map_range.inputs[1]); links.new(node_in.outputs[6], map_range.inputs[2])
    links.new(map_range.outputs[0], math_str.inputs[0]); links.new(node_in.outputs[1], math_str.inputs[1])
    links.new(math_str.outputs[0], node_out.inputs[0])

    return group
