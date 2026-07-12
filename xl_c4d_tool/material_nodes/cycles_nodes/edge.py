import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def edge():
    """节点组: Edge
    边缘纹理映射 — 对边缘检测结果进行范围映射和强度控制处理"""
    group_name = "Edge"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="范围", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    group.interface.new_socket(name="强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="结果", in_out="OUTPUT", socket_type="NodeSocketFloat")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 节点创建 ===
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (364.7, 61.1)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[1].default_value = 0.9900000095367432
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (109.3, 88.0)
    vector_math.operation = 'DOT_PRODUCT'
    vector_math.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[3].default_value = 1.0
    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.location = (-162.2, -148.8)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (-161.8, 108.3)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    math = nodes.new("ShaderNodeMath")
    math.location = (-364.7, 123.2)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5

    # === 节点连接 ===
    links.new(bevel.outputs[0], vector_math.inputs[0])
    links.new(math.outputs[0], bevel.inputs[0])
    links.new(vector_math.outputs[1], map_range.inputs[0])
    links.new(geometry.outputs[1], vector_math.inputs[1])
    links.new(map_range.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[0], math.inputs[0])
    links.new(input_node.outputs[1], math.inputs[1])
    links.new(input_node.outputs[2], map_range.inputs[3])

    return group