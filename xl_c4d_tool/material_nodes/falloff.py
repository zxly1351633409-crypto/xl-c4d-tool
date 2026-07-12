"""【节点：OC_衰减 Falloff】
法线与视线方向/自定义方向的衰减效果（菲涅尔/半角/方向衰减）"""
import bpy
from ..utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_oc_falloff_group():
    group_name = "OC_衰减"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="Mode (0=Eye, 1=90, 2=180)", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="最小值", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="最大值", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="衰减倾斜系数", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="衰减方向", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0, 0, 1)
    group.interface.new_socket(name="Falloff Result", in_out="OUTPUT", socket_type="NodeSocketFloat")
    nodes = group.nodes
    links = group.links
    node_in = nodes.new("NodeGroupInput")
    node_out = nodes.new("NodeGroupOutput")

    frm_geom = create_frame(nodes, "几何数据", "几何数据: 获取法线和位置信息", (0.3, 0.3, 0.1))
    node_geom = nodes.new("ShaderNodeNewGeometry")
    label_node(node_geom, "几何数据(法线/位置)", frm_geom)

    frm_dot = create_frame(nodes, "点乘计算", "点乘计算: 法线·视线方向 = 衰减基础值", (0.2, 0.4, 0.2))
    node_dot = nodes.new("ShaderNodeVectorMath"); node_dot.operation = "DOT_PRODUCT"
    label_node(node_dot, "法线·视线(视线衰减)", frm_dot)
    links.new(node_geom.outputs[1], node_dot.inputs[0]); links.new(node_geom.outputs[4], node_dot.inputs[1])
    node_dot_dir = nodes.new("ShaderNodeVectorMath"); node_dot_dir.operation = "DOT_PRODUCT"
    label_node(node_dot_dir, "法线·自定义方向(方向衰减)", frm_dot)
    node_dir_norm = nodes.new("ShaderNodeVectorMath"); node_dir_norm.operation = "NORMALIZE"
    label_node(node_dir_norm, "归一化方向向量", frm_dot)
    links.new(node_in.outputs[4], node_dir_norm.inputs[0])
    links.new(node_geom.outputs[1], node_dot_dir.inputs[0]); links.new(node_dir_norm.outputs[0], node_dot_dir.inputs[1])

    frm_eye = create_frame(nodes, "视线模式", "视线模式: 1-|法线·视线| = 菲涅尔", (0.4, 0.2, 0.1))
    node_abs = nodes.new("ShaderNodeMath"); node_abs.operation = "ABSOLUTE"
    label_node(node_abs, "取绝对值", frm_eye)
    math_sub_1 = nodes.new("ShaderNodeMath"); math_sub_1.operation = "SUBTRACT"
    math_sub_1.inputs[0].default_value = 1.0
    label_node(math_sub_1, "1-点乘(菲涅尔效果)", frm_eye)
    links.new(node_dot.outputs[1], node_abs.inputs[0]); links.new(node_abs.outputs[0], math_sub_1.inputs[1])

    frm_90 = create_frame(nodes, "90°模式", "90°模式: acos(点乘)/π × 2 = 半角衰减", (0.1, 0.3, 0.4))
    node_acos = nodes.new("ShaderNodeMath"); node_acos.operation = "ARCCOSINE"
    label_node(node_acos, "反余弦(角度)", frm_90)
    math_div_pi = nodes.new("ShaderNodeMath"); math_div_pi.operation = "DIVIDE"
    math_div_pi.inputs[1].default_value = 3.14159
    label_node(math_div_pi, "角度/π(归一化到0-1)", frm_90)
    math_mul_2 = nodes.new("ShaderNodeMath"); math_mul_2.operation = "MULTIPLY"
    math_mul_2.inputs[1].default_value = 2.0
    label_node(math_mul_2, "×2(扩展到0-2范围)", frm_90)
    links.new(node_dot.outputs[1], node_acos.inputs[0])
    links.new(node_acos.outputs[0], math_div_pi.inputs[0]); links.new(math_div_pi.outputs[0], math_mul_2.inputs[0])

    frm_180 = create_frame(nodes, "180°模式", "180°模式: acos(法线·方向)/π = 方向衰减", (0.3, 0.1, 0.4))
    node_acos_dir = nodes.new("ShaderNodeMath"); node_acos_dir.operation = "ARCCOSINE"
    label_node(node_acos_dir, "反余弦(方向角度)", frm_180)
    math_div_pi_dir = nodes.new("ShaderNodeMath"); math_div_pi_dir.operation = "DIVIDE"
    math_div_pi_dir.inputs[1].default_value = 3.14159
    label_node(math_div_pi_dir, "角度/π(0-1)", frm_180)
    links.new(node_dot_dir.outputs[1], node_acos_dir.inputs[0])
    links.new(node_acos_dir.outputs[0], math_div_pi_dir.inputs[0])

    frm_mode = create_frame(nodes, "模式切换", "模式切换: Eye=菲涅尔, 90°=半角, 180°=方向", (0.2, 0.4, 0.4))
    comp_m1 = nodes.new("ShaderNodeMath"); comp_m1.operation = "COMPARE"
    comp_m1.inputs[1].default_value = 1.0; comp_m1.inputs[2].default_value = 0.1
    label_node(comp_m1, "Mode=1?(90°)", frm_mode)
    comp_m2 = nodes.new("ShaderNodeMath"); comp_m2.operation = "COMPARE"
    comp_m2.inputs[1].default_value = 2.0; comp_m2.inputs[2].default_value = 0.1
    label_node(comp_m2, "Mode=2?(180°)", frm_mode)
    mix_m1 = nodes.new("ShaderNodeMix"); mix_m1.data_type = "FLOAT"
    label_node(mix_m1, "混合: 视线/90°", frm_mode)
    mix_m2 = nodes.new("ShaderNodeMix"); mix_m2.data_type = "FLOAT"
    label_node(mix_m2, "混合: 90°/180°", frm_mode)
    links.new(node_in.outputs[0], comp_m1.inputs[0]); links.new(node_in.outputs[0], comp_m2.inputs[0])
    m1_fac, m1_a, m1_b, m1_r = get_mix_f_ports(mix_m1)
    links.new(comp_m1.outputs[0], m1_fac); links.new(math_sub_1.outputs[0], m1_a); links.new(math_mul_2.outputs[0], m1_b)
    m2_fac, m2_a, m2_b, m2_r = get_mix_f_ports(mix_m2)
    links.new(comp_m2.outputs[0], m2_fac); links.new(m1_r, m2_a); links.new(math_div_pi_dir.outputs[0], m2_b)

    frm_output = create_frame(nodes, "输出处理", "输出处理: 幂运算(倾斜系数)→范围映射", (0.3, 0.1, 0.3))
    math_pow = nodes.new("ShaderNodeMath"); math_pow.operation = "POWER"
    label_node(math_pow, "幂运算(倾斜系数控制衰减)", frm_output)
    links.new(m2_r, math_pow.inputs[0]); links.new(node_in.outputs[3], math_pow.inputs[1])
    map_range = nodes.new("ShaderNodeMapRange")
    label_node(map_range, "映射到最小/最大范围", frm_output)
    links.new(math_pow.outputs[0], map_range.inputs[0])
    links.new(node_in.outputs[1], map_range.inputs[3]); links.new(node_in.outputs[2], map_range.inputs[4])
    links.new(map_range.outputs[0], node_out.inputs[0])

    return group
