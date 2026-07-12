"""【节点：OC_污渍 Dirt Noise】
基于环境光遮蔽(AO)生成污垢/脏旧效果，支持边缘提取和噪波混合"""
import bpy
from ..utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_oc_dirt_noise_group():
    group_name = "OC_污渍"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="半径", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="细节/扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="提取边缘", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="噪波贴图", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="噪波强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="反转输出", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="Dirt Texture (污垢遮罩)", in_out="OUTPUT", socket_type="NodeSocketFloat")
    nodes = group.nodes
    links = group.links
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")

    frm_ao = create_frame(nodes, "AO采样", "AO采样: 用环境光遮蔽检测污垢与边缘", (0.4, 0.2, 0.1))
    ao_dirt = nodes.new("ShaderNodeAmbientOcclusion")
    ao_dirt.inside = False
    label_node(ao_dirt, "外部AO(检测污垢/凹陷)", frm_ao)
    ao_edge = nodes.new("ShaderNodeAmbientOcclusion")
    ao_edge.inside = True
    label_node(ao_edge, "内部AO(检测边缘/凸起)", frm_ao)
    links.new(input_node.outputs[0], ao_dirt.inputs[1])
    links.new(input_node.outputs[0], ao_edge.inputs[1])

    frm_edge = create_frame(nodes, "边缘提取", "边缘提取: 根据开关混合污垢与边缘", (0.2, 0.4, 0.2))
    mix_edge = nodes.new("ShaderNodeMix")
    mix_edge.data_type = "FLOAT"
    label_node(mix_edge, "边缘混合(开=边缘,关=污垢)", frm_edge)
    e_fac, e_a, e_b, e_res = get_mix_f_ports(mix_edge)
    links.new(input_node.outputs[3], e_fac)
    links.new(ao_dirt.outputs[1], e_a)
    links.new(ao_edge.outputs[1], e_b)

    frm_process = create_frame(nodes, "强度处理", "强度处理: 反转→映射→幂运算控制衰减", (0.2, 0.2, 0.5))
    math_inv = nodes.new("ShaderNodeMath")
    math_inv.operation = "SUBTRACT"
    math_inv.inputs[0].default_value = 1.0
    label_node(math_inv, "1-结果(反转遮罩)", frm_process)
    links.new(e_res, math_inv.inputs[1])
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.inputs[3].default_value = 4.0
    label_node(map_range, "映射范围(扩散→幂指数)", frm_process)
    links.new(input_node.outputs[2], map_range.inputs[0])
    math_pow = nodes.new("ShaderNodeMath")
    math_pow.operation = "POWER"
    label_node(math_pow, "幂运算(控制衰减曲线)", frm_process)
    links.new(math_inv.outputs[0], math_pow.inputs[0])
    links.new(map_range.outputs[0], math_pow.inputs[1])

    frm_noise = create_frame(nodes, "噪波混合", "噪波混合: 用噪波贴图打破均匀感", (0.4, 0.3, 0.1))
    mix_noise = nodes.new("ShaderNodeMix")
    mix_noise.data_type = "FLOAT"
    label_node(mix_noise, "噪波混合(1=完全替换)", frm_noise)
    n_fac, n_a, n_b, n_res = get_mix_f_ports(mix_noise)
    links.new(input_node.outputs[5], n_fac)
    n_a.default_value = 1.0
    links.new(input_node.outputs[4], n_b)
    math_apply = nodes.new("ShaderNodeMath")
    math_apply.operation = "MULTIPLY"
    label_node(math_apply, "应用噪波到遮罩", frm_noise)
    links.new(math_pow.outputs[0], math_apply.inputs[0])
    links.new(n_res, math_apply.inputs[1])

    frm_output = create_frame(nodes, "输出处理", "输出处理: 强度控制→反转开关→最终输出", (0.3, 0.1, 0.3))
    math_str = nodes.new("ShaderNodeMath")
    math_str.operation = "MULTIPLY"
    label_node(math_str, "乘以强度", frm_output)
    links.new(math_apply.outputs[0], math_str.inputs[0])
    links.new(input_node.outputs[1], math_str.inputs[1])
    node_inv_out = nodes.new("ShaderNodeInvert")
    node_inv_out.inputs[0].default_value = 1.0
    label_node(node_inv_out, "反转输出", frm_output)
    links.new(math_str.outputs[0], node_inv_out.inputs[1])
    mix_final = nodes.new("ShaderNodeMix")
    mix_final.data_type = "FLOAT"
    label_node(mix_final, "最终混合(反转开关)", frm_output)
    f_fac, f_a, f_b, f_res = get_mix_f_ports(mix_final)
    links.new(input_node.outputs[6], f_fac)
    links.new(math_str.outputs[0], f_a)
    links.new(node_inv_out.outputs[0], f_b)
    links.new(f_res, output_node.inputs[0])

    return group
