"""【工具模块：节点工具函数】
公共函数：端口获取 / 注释框创建 / 节点标签 / 物体模式切换器"""
import bpy


def get_mix_f_ports(n):
    """获取 Mix 节点的关键端口: [Factor, A, B, Result]"""
    return [i for i in n.inputs if i.type == 'VALUE' and not i.hide][0:3] + [
        [o for o in n.outputs if o.type == 'VALUE' and not o.hide][0]
    ]


def create_frame(nodes, name, label, color=(0.3, 0.3, 0.3), parent=None):
    """创建注释框(Frame)节点并设置颜色和标签"""
    frame = nodes.new("NodeFrame")
    frame.name = name
    frame.label = label
    frame.use_custom_color = True
    frame.color = color
    if parent:
        frame.parent = parent
    return frame


def label_node(node, label, parent_frame=None):
    """给节点设置标签并挂到指定Frame下"""
    node.label = label
    if parent_frame is not None:
        node.parent = parent_frame
    return node


def build_object_mode_switcher(nodes, links, mode_sock, ao_all, ao_self, parent_frame=None):
    """构建物体模式切换器：根据Mode(0=全部/1=自身/2=其他)混合AO结果"""
    sub1 = nodes.new("ShaderNodeMath")
    sub1.operation = "SUBTRACT"
    label_node(sub1, "自身AO - 全局AO", parent_frame)
    links.new(ao_self, sub1.inputs[0])
    links.new(ao_all, sub1.inputs[1])

    sub2 = nodes.new("ShaderNodeMath")
    sub2.operation = "SUBTRACT"
    sub2.inputs[0].default_value = 1.0
    label_node(sub2, "1 - 差值(其他物体)", parent_frame)
    links.new(sub1.outputs[0], sub2.inputs[1])

    comp1 = nodes.new("ShaderNodeMath")
    comp1.operation = "COMPARE"
    comp1.inputs[1].default_value = 1.0
    comp1.inputs[2].default_value = 0.1
    label_node(comp1, "模式=1?(仅自身)", parent_frame)
    links.new(mode_sock, comp1.inputs[0])

    mix1 = nodes.new("ShaderNodeMix")
    mix1.data_type = "FLOAT"
    label_node(mix1, "混合: 全局/自身", parent_frame)
    m1_fac, m1_a, m1_b, m1_res = get_mix_f_ports(mix1)
    links.new(comp1.outputs[0], m1_fac)
    links.new(ao_all, m1_a)
    links.new(ao_self, m1_b)

    comp2 = nodes.new("ShaderNodeMath")
    comp2.operation = "COMPARE"
    comp2.inputs[1].default_value = 2.0
    comp2.inputs[2].default_value = 0.1
    label_node(comp2, "模式=2?(仅其他)", parent_frame)
    links.new(mode_sock, comp2.inputs[0])

    mix2 = nodes.new("ShaderNodeMix")
    mix2.data_type = "FLOAT"
    label_node(mix2, "混合: 自身/其他", parent_frame)
    m2_fac, m2_a, m2_b, m2_res = get_mix_f_ports(mix2)
    links.new(comp2.outputs[0], m2_fac)
    links.new(m1_res, m2_a)
    links.new(sub2.outputs[0], m2_b)

    return m2_res
