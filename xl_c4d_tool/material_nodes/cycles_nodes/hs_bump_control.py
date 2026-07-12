import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def hs_bump_control():
    """BL_凹凸控制 - 凹凸效果开关
    控制凹凸贴图的开/关及强度缩放，可按百分比调节"""
    group_name = "BL_凹凸控制"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="强度%", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket(name="最大值", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.4000000059604645
    group.interface.new_socket(name="值", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (53.1, 101.6)
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    math_003.inputs[2].default_value = 0.5
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (-149.4, 101.6)
    label_node(percentage_to_0_1, "百分比转0-1")
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (-149.4, 132.1)
    reroute.socket_idname = 'NodeSocketBool'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-9.4, 132.1)
    reroute_001.socket_idname = 'NodeSocketBool'

    # === 节点连接 ===
    links.new(input_node.outputs[1], percentage_to_0_1.inputs[0])
    links.new(math_003.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[2], percentage_to_0_1.inputs[4])
    links.new(percentage_to_0_1.outputs[0], math_003.inputs[1])
    links.new(input_node.outputs[0], reroute.inputs[0])
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], math_003.inputs[0])

    return group