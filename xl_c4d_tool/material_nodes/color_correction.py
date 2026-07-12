"""【节点：OC_颜色校正 Color Correction】
调节亮度/对比度/色相/饱和度/伽马/曝光/反相的完整色彩校正"""
import bpy
from ..utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_oc_color_correction_group():
    group_name = "OC_颜色校正"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="Texture (纹理)", in_out="INPUT", socket_type="NodeSocketColor").default_value = (1.0, 1.0, 1.0, 1.0)
    group.interface.new_socket(name="亮度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="色相", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="饱和度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="对比度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="伽马", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="曝光", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="反相", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="Color Result", in_out="OUTPUT", socket_type="NodeSocketColor")
    nodes = group.nodes
    links = group.links
    node_in = nodes.new("NodeGroupInput")
    node_out = nodes.new("NodeGroupOutput")

    frm_hsv = create_frame(nodes, "HSV调整", "HSV调整: 色相偏移+饱和度+亮度控制", (0.4, 0.3, 0.1))
    node_hsv = nodes.new("ShaderNodeHueSaturation")
    label_node(node_hsv, "色相/饱和度/亮度", frm_hsv)
    math_hue_add = nodes.new("ShaderNodeMath"); math_hue_add.operation = "ADD"
    math_hue_add.inputs[1].default_value = 0.5
    label_node(math_hue_add, "色相+0.5(偏移到正确范围)", frm_hsv)
    links.new(node_in.outputs[2], math_hue_add.inputs[0])
    links.new(math_hue_add.outputs[0], node_hsv.inputs[0])
    links.new(node_in.outputs[3], node_hsv.inputs[1]); links.new(node_in.outputs[1], node_hsv.inputs[2])
    links.new(node_in.outputs[0], node_hsv.inputs[4])

    frm_bc = create_frame(nodes, "亮度对比度", "亮度对比度: 调整画面明暗对比", (0.2, 0.3, 0.4))
    node_bc = nodes.new("ShaderNodeBrightContrast")
    label_node(node_bc, "亮度/对比度", frm_bc)
    math_cont = nodes.new("ShaderNodeMath"); math_cont.operation = "SUBTRACT"
    math_cont.inputs[1].default_value = 1.0
    label_node(math_cont, "对比度-1(归一化)", frm_bc)
    links.new(node_in.outputs[4], math_cont.inputs[0])
    links.new(math_cont.outputs[0], node_bc.inputs[2]); links.new(node_hsv.outputs[0], node_bc.inputs[0])

    frm_exp = create_frame(nodes, "曝光控制", "曝光控制: 2^曝光值×颜色", (0.3, 0.2, 0.4))
    math_exp_pow = nodes.new("ShaderNodeMath"); math_exp_pow.operation = "POWER"
    math_exp_pow.inputs[0].default_value = 2.0
    label_node(math_exp_pow, "2^曝光值", frm_exp)
    node_exp_mix = nodes.new("ShaderNodeMix"); node_exp_mix.data_type = "RGBA"
    node_exp_mix.blend_type = "MULTIPLY"; node_exp_mix.inputs[0].default_value = 1.0
    label_node(node_exp_mix, "颜色×曝光系数", frm_exp)
    links.new(node_in.outputs[6], math_exp_pow.inputs[1])
    links.new(node_bc.outputs[0], node_exp_mix.inputs[6]); links.new(math_exp_pow.outputs[0], node_exp_mix.inputs[7])

    frm_gamma = create_frame(nodes, "伽马校正", "伽马校正: 调整中间调亮度", (0.2, 0.4, 0.3))
    node_gamma = nodes.new("ShaderNodeGamma")
    label_node(node_gamma, "伽马校正", frm_gamma)
    links.new(node_exp_mix.outputs[2], node_gamma.inputs[0]); links.new(node_in.outputs[5], node_gamma.inputs[1])

    frm_inv = create_frame(nodes, "反相开关", "反相开关: 根据开关选择正常/反相输出", (0.4, 0.1, 0.3))
    node_inv = nodes.new("ShaderNodeInvert"); node_inv.inputs[0].default_value = 1.0
    label_node(node_inv, "反相处理", frm_inv)
    links.new(node_gamma.outputs[0], node_inv.inputs[1])
    mix_sw = nodes.new("ShaderNodeMix"); mix_sw.data_type = "RGBA"; mix_sw.blend_type = "MIX"
    label_node(mix_sw, "最终混合(反相开关)", frm_inv)
    links.new(node_in.outputs[7], mix_sw.inputs[0])
    links.new(node_gamma.outputs[0], mix_sw.inputs[6]); links.new(node_inv.outputs[0], mix_sw.inputs[7])
    links.new(mix_sw.outputs[2], node_out.inputs[0])

    return group
