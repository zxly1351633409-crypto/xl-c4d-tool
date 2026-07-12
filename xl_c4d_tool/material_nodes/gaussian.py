"""【节点：OC_高斯光谱 Gaussian Spectrum】
基于波长的高斯分布光谱颜色生成（380-750nm可见光）"""
import bpy
from ..utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_oc_gaussian_spectrum_group():
    group_name = "OC_高斯光谱"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="波长 (nm)", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 550.0
    group.interface.new_socket(name="宽度 (0-100)", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 5.0
    group.interface.new_socket(name="Power", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    nodes = group.nodes
    links = group.links
    node_in = nodes.new("NodeGroupInput")
    node_out = nodes.new("NodeGroupOutput")

    frm_wave = create_frame(nodes, "波长映射", "波长映射: 将nm值(380-750)映射到0-1", (0.3, 0.3, 0.1))
    map_wave = nodes.new("ShaderNodeMapRange")
    map_wave.inputs[1].default_value = 380.0; map_wave.inputs[2].default_value = 750.0
    label_node(map_wave, "波长→0-1(380-750nm)", frm_wave)
    links.new(node_in.outputs[0], map_wave.inputs[0])

    frm_ramp = create_frame(nodes, "光谱色表", "光谱色表: 将0-1值转换为对应波长的颜色", (0.4, 0.2, 0.1))
    ramp = nodes.new("ShaderNodeValToRGB"); ramp.name = "Spectrum_Ramp"
    ramp.color_ramp.interpolation = "EASE"
    label_node(ramp, "可见光谱颜色映射", frm_ramp)
    stops = ramp.color_ramp.elements
    while len(stops) < 7:
        stops.new(0.5)
    stops[0].position = 0.00; stops[0].color = (0.05, 0.0, 0.2, 1.0)
    stops[1].position = 0.16; stops[1].color = (0.0, 0.0, 1.0, 1.0)
    stops[2].position = 0.33; stops[2].color = (0.0, 1.0, 1.0, 1.0)
    stops[3].position = 0.50; stops[3].color = (0.0, 1.0, 0.0, 1.0)
    stops[4].position = 0.66; stops[4].color = (1.0, 1.0, 0.0, 1.0)
    stops[5].position = 0.83; stops[5].color = (1.0, 0.0, 0.0, 1.0)
    stops[6].position = 1.00; stops[6].color = (0.2, 0.0, 0.0, 1.0)
    links.new(map_wave.outputs[0], ramp.inputs[0])

    frm_width = create_frame(nodes, "宽度混合", "宽度混合: 宽度越大越接近白色(宽光谱)", (0.2, 0.3, 0.4))
    map_width = nodes.new("ShaderNodeMapRange")
    map_width.inputs[1].default_value = 0.0; map_width.inputs[2].default_value = 100.0
    map_width.inputs[3].default_value = 0.0; map_width.inputs[4].default_value = 1.0
    label_node(map_width, "宽度→0-1混合因子", frm_width)
    links.new(node_in.outputs[1], map_width.inputs[0])
    mix_white = nodes.new("ShaderNodeMix"); mix_white.data_type = "RGBA"
    mix_white.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
    label_node(mix_white, "光谱色↔白色(宽度混合)", frm_width)
    links.new(map_width.outputs[0], mix_white.inputs[0]); links.new(ramp.outputs[0], mix_white.inputs[6])

    frm_power = create_frame(nodes, "功率缩放", "功率缩放: 控制最终颜色强度", (0.3, 0.1, 0.3))
    math_pow = nodes.new("ShaderNodeVectorMath"); math_pow.operation = "SCALE"
    label_node(math_pow, "颜色×功率", frm_power)
    links.new(mix_white.outputs[2], math_pow.inputs[0]); links.new(node_in.outputs[2], math_pow.inputs[3])
    links.new(math_pow.outputs[0], node_out.inputs[0])

    return group
