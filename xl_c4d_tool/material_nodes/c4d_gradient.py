"""【节点：C4D_渐变 C4D Gradient】
11种渐变投影类型（2D:U/V/斜/锥/圆/方/星/四角 + 3D:线性/柱面/球面）"""
import bpy
from ..utils.node_utils import get_mix_f_ports, create_frame, label_node


GRADIENT_TYPES = [
    ("0", "二维 - U", "2D-U: 沿U方向线性渐变"),
    ("1", "二维 - V", "2D-V: 沿V方向线性渐变"),
    ("2", "二维 - 斜向", "2D-对角线: U+V方向的45°渐变"),
    ("3", "二维 - 锥形", "2D-锥形: 从中心向外放射状渐变"),
    ("4", "二维 - 圆形", "2D-圆形: 基于到中心距离的圆形渐变"),
    ("5", "二维 - 方形", "2D-方形: 基于到中心最大轴距离的方形渐变"),
    ("6", "二维 - 星形", "2D-星形: 基于到中心绝对值之和的菱形渐变"),
    ("7", "二维 - 四角", "2D-四角: U×V乘积渐变(四角分布)"),
    ("8", "三维 - 线性", "3D-线性: 沿X方向线性渐变"),
    ("9", "三维 - 柱面", "3D-柱面: 基于XY平面距离的圆柱渐变"),
    ("10", "三维 - 球面", "3D-球面: 基于3D距离的球形渐变"),
]


def create_c4d_gradient_group():
    group_name = "C4D_渐变"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Type", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="Color Result", in_out="OUTPUT", socket_type="NodeSocketColor")
    nodes = group.nodes
    links = group.links
    node_in = nodes.new("NodeGroupInput")
    node_out = nodes.new("NodeGroupOutput")

    frm_input = create_frame(nodes, "输入处理", "输入处理: 分离UV坐标和中心偏移", (0.3, 0.3, 0.1))
    sep_uv = nodes.new("ShaderNodeSeparateXYZ")
    label_node(sep_uv, "分离UVW坐标", frm_input)
    links.new(node_in.outputs["Vector"], sep_uv.inputs[0])
    vec_sub = nodes.new("ShaderNodeVectorMath"); vec_sub.operation = "SUBTRACT"
    vec_sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    label_node(vec_sub, "减去中心点(0.5,0.5,0.5)", frm_input)
    links.new(node_in.outputs["Vector"], vec_sub.inputs[0])
    sep_sub = nodes.new("ShaderNodeSeparateXYZ")
    label_node(sep_sub, "分离偏移后坐标", frm_input)
    links.new(vec_sub.outputs[0], sep_sub.inputs[0])

    frm_2d = create_frame(nodes, "2D渐变", "2D渐变: 基于UV平面的7种投影方式", (0.2, 0.4, 0.2))
    val0 = sep_uv.outputs[0]
    val1 = sep_uv.outputs[1]
    add2 = nodes.new("ShaderNodeMath"); add2.operation = "ADD"
    label_node(add2, "U+V(斜向基础)", frm_2d)
    links.new(sep_uv.outputs[0], add2.inputs[0]); links.new(sep_uv.outputs[1], add2.inputs[1])
    mul2 = nodes.new("ShaderNodeMath"); mul2.operation = "MULTIPLY"; mul2.inputs[1].default_value = 0.5
    label_node(mul2, "×0.5(归一化斜向)", frm_2d)
    links.new(add2.outputs[0], mul2.inputs[0])
    val2 = mul2.outputs[0]

    grad_conic = nodes.new("ShaderNodeTexGradient"); grad_conic.gradient_type = "RADIAL"
    label_node(grad_conic, "锥形渐变(径向)", frm_2d)
    links.new(vec_sub.outputs[0], grad_conic.inputs[0])
    val3 = grad_conic.outputs[0]

    len4 = nodes.new("ShaderNodeVectorMath"); len4.operation = "LENGTH"
    label_node(len4, "2D长度(到中心距离)", frm_2d)
    comb4 = nodes.new("ShaderNodeCombineXYZ")
    label_node(comb4, "重组XY偏移", frm_2d)
    links.new(sep_sub.outputs[0], comb4.inputs[0]); links.new(sep_sub.outputs[1], comb4.inputs[1])
    links.new(comb4.outputs[0], len4.inputs[0])
    mul4 = nodes.new("ShaderNodeMath"); mul4.operation = "MULTIPLY"; mul4.inputs[1].default_value = 2.0
    label_node(mul4, "×2(扩展到0-1范围)", frm_2d)
    links.new(len4.outputs[1], mul4.inputs[0]); val4 = mul4.outputs[0]

    abs5x = nodes.new("ShaderNodeMath"); abs5x.operation = "ABSOLUTE"
    label_node(abs5x, "|X偏移|", frm_2d); links.new(sep_sub.outputs[0], abs5x.inputs[0])
    abs5y = nodes.new("ShaderNodeMath"); abs5y.operation = "ABSOLUTE"
    label_node(abs5y, "|Y偏移|", frm_2d); links.new(sep_sub.outputs[1], abs5y.inputs[0])
    max5 = nodes.new("ShaderNodeMath"); max5.operation = "MAXIMUM"
    label_node(max5, "max(|X|,|Y|)(方形)", frm_2d)
    links.new(abs5x.outputs[0], max5.inputs[0]); links.new(abs5y.outputs[0], max5.inputs[1])
    mul5 = nodes.new("ShaderNodeMath"); mul5.operation = "MULTIPLY"; mul5.inputs[1].default_value = 2.0
    label_node(mul5, "×2(方形范围)", frm_2d); links.new(max5.outputs[0], mul5.inputs[0])
    val5 = mul5.outputs[0]

    add6 = nodes.new("ShaderNodeMath"); add6.operation = "ADD"
    label_node(add6, "|X|+|Y|(星形/菱形)", frm_2d)
    links.new(abs5x.outputs[0], add6.inputs[0]); links.new(abs5y.outputs[0], add6.inputs[1])
    mul6 = nodes.new("ShaderNodeMath"); mul6.operation = "MULTIPLY"; mul6.inputs[1].default_value = 2.0
    label_node(mul6, "×2(星形范围)", frm_2d); links.new(add6.outputs[0], mul6.inputs[0])
    val6 = mul6.outputs[0]

    mul7 = nodes.new("ShaderNodeMath"); mul7.operation = "MULTIPLY"
    label_node(mul7, "U×V(四角分布)", frm_2d)
    links.new(sep_uv.outputs[0], mul7.inputs[0]); links.new(sep_uv.outputs[1], mul7.inputs[1])
    val7 = mul7.outputs[0]

    frm_3d = create_frame(nodes, "3D渐变", "3D渐变: 基于三维空间的3种投影方式", (0.2, 0.2, 0.5))
    val8 = sep_uv.outputs[0]
    val9 = mul4.outputs[0]

    len10 = nodes.new("ShaderNodeVectorMath"); len10.operation = "LENGTH"
    label_node(len10, "3D长度(球面距离)", frm_3d)
    links.new(vec_sub.outputs[0], len10.inputs[0])
    mul10 = nodes.new("ShaderNodeMath"); mul10.operation = "MULTIPLY"; mul10.inputs[1].default_value = 2.0
    label_node(mul10, "×2(球面范围)", frm_3d); links.new(len10.outputs[1], mul10.inputs[0])
    val10 = mul10.outputs[0]

    frm_switch = create_frame(nodes, "类型切换", "类型切换: 根据Type值选择11种渐变之一", (0.4, 0.2, 0.3))
    vals = [val0, val1, val2, val3, val4, val5, val6, val7, val8, val9, val10]
    last_output = vals[0]

    for i in range(1, 11):
        comp = nodes.new("ShaderNodeMath"); comp.operation = "COMPARE"
        comp.inputs[1].default_value = i; comp.inputs[2].default_value = 0.1
        label_node(comp, f"Type={i}?({GRADIENT_TYPES[i][1]})", frm_switch)
        links.new(node_in.outputs["Type"], comp.inputs[0])
        mix = nodes.new("ShaderNodeMix"); mix.data_type = "FLOAT"
        label_node(mix, f"切换到{GRADIENT_TYPES[i][1]}", frm_switch)
        f_fac, f_a, f_b, f_res = get_mix_f_ports(mix)
        links.new(comp.outputs[0], f_fac); links.new(last_output, f_a); links.new(vals[i], f_b)
        last_output = f_res

    frm_output = create_frame(nodes, "颜色输出", "颜色输出: 将渐变值转换为颜色", (0.3, 0.1, 0.3))
    ramp = nodes.new("ShaderNodeValToRGB"); ramp.name = "C4D_Gradient_Ramp"
    label_node(ramp, "颜色渐变(可编辑色带)", frm_output)
    links.new(last_output, ramp.inputs[0])
    color_out = ramp.outputs[0]
    if len(node_out.inputs) > 0:
        links.new(color_out, node_out.inputs[0])

    return group
