"""【节点：OC_RGB光谱 RGBSpectrum】
直接输出纯RGB颜色到材质通道，支持N面板预设切换"""
import bpy
from ..utils.node_utils import create_frame, label_node


def create_oc_rgbspectrum_group():
    group_name = "OC_RGB光谱"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group.interface.new_socket(name="Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    nodes = group.nodes
    links = group.links

    frm_main = create_frame(nodes, "RGB颜色输出", "RGB颜色输出: 直接输出纯色到材质通道", (0.3, 0.2, 0.4))
    output_node = nodes.new("NodeGroupOutput")
    output_node.location = (200, 0)
    label_node(output_node, "组输出", frm_main)

    rgb_node = nodes.new("ShaderNodeRGB")
    rgb_node.name = "RGB"
    rgb_node.label = "RGB Color"
    rgb_node.location = (0, 0)
    rgb_node.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    label_node(rgb_node, "RGB纯色(可编辑)", frm_main)

    links.new(rgb_node.outputs[0], output_node.inputs[0])

    return group
