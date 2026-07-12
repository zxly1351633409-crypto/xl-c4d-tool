import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .hs_camo_dazzle import hs_camo_dazzle as _create_camo_dazzle


def shader_nodetree():
    """节点组: Shader Nodetree
    Shader节点树容器 — 提供标准Shader输出结构框架"""
    group_name = "Shader Nodetree"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.location = (200.0, 100.0)
    material_output.is_active_output = True
    material_output.target = 'ALL'
    material_output.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    camo_dazzle_node = nodes.new("ShaderNodeGroup")
    camo_dazzle_node.location = (0.6, 102.3)
    camo_dazzle_node.xl_c4d_gradient_type = '0'
    camo_dazzle_node.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    camo_dazzle_node.node_tree = _create_camo_dazzle()
    camo_dazzle_node.inputs[0].default_value = 1000.0
    camo_dazzle_node.inputs[1].default_value = (0.0000, 0.0000, 0.0000)

    # === 节点连接 ===
    links.new(camo_dazzle_node.outputs[0], material_output.inputs[0])

    return group