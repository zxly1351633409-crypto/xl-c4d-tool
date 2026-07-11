"""【节点组：Handle — 控制柄】
生成控制柄几何体，存储手柄类型/位置/缩放/细分属性"""
import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node


def create_handle_group():
    group_name = "Handle"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="手柄类型", in_out="INPUT", socket_type="NodeSocketInt").default_value = 0
    group.interface.new_socket(name="左边位置", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="右边位置", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="缩放手柄", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="细分", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    frm_main = create_frame(nodes, "控制柄属性", "控制柄属性: 依次存储use_sub/sub_type/sub_left_pos/sub_right_pos/sub_div/sub_handle_scale", (0.3, 0.3, 0.1))

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.location = (720.1, 314.6)
    label_node(store_named_attribute_002, "存储手柄类型", frm_main)
    store_named_attribute_002.data_type = 'INT'
    store_named_attribute_002.domain = 'CURVE'
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = 'sub_type'
    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.location = (541.2, 314.6)
    label_node(store_named_attribute_001, "存储使用子曲线", frm_main)
    store_named_attribute_001.data_type = 'BOOLEAN'
    store_named_attribute_001.domain = 'CURVE'
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = 'use_sub'
    store_named_attribute_001.inputs[3].default_value = True
    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.location = (896.9, 314.6)
    label_node(store_named_attribute_003, "存储左位置", frm_main)
    store_named_attribute_003.data_type = 'FLOAT_VECTOR'
    store_named_attribute_003.domain = 'CURVE'
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = 'sub_left_pos'
    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.location = (1078.5, 314.6)
    label_node(store_named_attribute_004, "存储右位置", frm_main)
    store_named_attribute_004.data_type = 'FLOAT_VECTOR'
    store_named_attribute_004.domain = 'CURVE'
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = 'sub_right_pos'
    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.location = (1261.1, 314.6)
    label_node(store_named_attribute_005, "存储细分数", frm_main)
    store_named_attribute_005.data_type = 'INT'
    store_named_attribute_005.domain = 'CURVE'
    store_named_attribute_005.inputs[1].default_value = True
    store_named_attribute_005.inputs[2].default_value = 'sub_div'
    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.location = (1454.4, 314.6)
    label_node(store_named_attribute, "存储缩放", frm_main)
    store_named_attribute.data_type = 'FLOAT_VECTOR'
    store_named_attribute.domain = 'CURVE'
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = 'sub_handle_scale'

    links.new(store_named_attribute_005.outputs[0], store_named_attribute.inputs[0])
    links.new(input_node.outputs[0], store_named_attribute_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_002.inputs[0])
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(store_named_attribute_003.outputs[0], store_named_attribute_004.inputs[0])
    links.new(store_named_attribute_004.outputs[0], store_named_attribute_005.inputs[0])
    links.new(input_node.outputs[1], store_named_attribute_002.inputs[3])
    links.new(input_node.outputs[2], store_named_attribute_003.inputs[3])
    links.new(input_node.outputs[3], store_named_attribute_004.inputs[3])
    links.new(input_node.outputs[5], store_named_attribute_005.inputs[3])
    links.new(store_named_attribute.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[4], store_named_attribute.inputs[3])

    return group
