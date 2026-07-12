"""【节点：C4D_云层材质】
给平面使用的轻量程序化云层：云疏密、云块大小、过渡、颜色和透明度均可直接调节。"""
import bpy

from ..utils.node_utils import create_frame, label_node


CLOUD_GROUP_VERSION = 2


def _new_input(group, name, socket_type, default, min_value=None, max_value=None, description=""):
    socket = group.interface.new_socket(name=name, in_out="INPUT", socket_type=socket_type)
    if description:
        socket.description = description
    try:
        socket.default_value = default
    except Exception:
        pass
    if min_value is not None:
        try:
            socket.min_value = min_value
        except Exception:
            pass
    if max_value is not None:
        try:
            socket.max_value = max_value
        except Exception:
            pass
    return socket


def _new_output(group, name, socket_type, description=""):
    socket = group.interface.new_socket(name=name, in_out="OUTPUT", socket_type=socket_type)
    if description:
        socket.description = description
    return socket


def _node(nodes, node_type, label, location, frame=None):
    node = nodes.new(node_type)
    node.location = location
    label_node(node, label, frame)
    return node


def _input(node, name, fallback_index=None):
    socket = node.inputs.get(name)
    if socket is None and fallback_index is not None and fallback_index < len(node.inputs):
        socket = node.inputs[fallback_index]
    return socket


def _output(node, name, fallback_index=None):
    socket = node.outputs.get(name)
    if socket is None and fallback_index is not None and fallback_index < len(node.outputs):
        socket = node.outputs[fallback_index]
    return socket


def _set_default(socket, value):
    if socket is not None:
        try:
            socket.default_value = value
        except Exception:
            pass


def _set_clamp(node, enabled=True):
    for attr in ("clamp", "use_clamp"):
        if hasattr(node, attr):
            try:
                setattr(node, attr, enabled)
            except Exception:
                pass


def _retire_old_group(group_name):
    group = bpy.data.node_groups.get(group_name)
    if group is None:
        return None
    if group.get("_xl_cloud_version") == CLOUD_GROUP_VERSION:
        return group
    group.name = f"{group_name}_旧版"
    return None


def create_c4d_cloud_layer_group():
    group_name = "C4D_云层材质"
    existing = _retire_old_group(group_name)
    if existing is not None:
        return existing

    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    group["_xl_cloud_version"] = CLOUD_GROUP_VERSION
    try:
        group.color_tag = "TEXTURE"
    except Exception:
        pass

    _new_input(group, "云疏密", "NodeSocketFloat", 0.58, 0.0, 1.0, "0 更稀疏，1 更密集。")
    _new_input(group, "云块大小", "NodeSocketFloat", 2.4, 0.05, 20.0, "数值越大，云块越大。")
    _new_input(group, "云层过渡", "NodeSocketFloat", 0.28, 0.01, 1.0, "控制云边缘软硬。")
    _new_input(group, "云细节", "NodeSocketFloat", 7.0, 0.0, 14.0, "噪声细节层级，数值越高边缘越丰富。")
    _new_input(group, "云扭曲", "NodeSocketFloat", 0.12, 0.0, 2.0, "噪声扰动强度。")
    _new_input(group, "云颜色", "NodeSocketColor", (1.0, 0.96, 0.88, 1.0), description="云层亮部颜色。")
    _new_input(group, "阴影颜色", "NodeSocketColor", (0.36, 0.48, 0.62, 1.0), description="云层暗部颜色。")
    _new_input(group, "透明度", "NodeSocketFloat", 0.72, 0.0, 1.0, "整体透明度。")
    _new_input(group, "亮度", "NodeSocketFloat", 1.0, 0.0, 3.0, "云层颜色亮度。")

    _new_output(group, "云层材质", "NodeSocketShader", "可直接连接到材质输出 Surface。")
    _new_output(group, "颜色", "NodeSocketColor", "云层颜色结果。")
    _new_output(group, "透明度", "NodeSocketFloat", "透明遮罩结果。")
    _new_output(group, "遮罩", "NodeSocketFloat", "原始云层遮罩。")

    nodes = group.nodes
    links = group.links
    node_in = nodes.new("NodeGroupInput")
    label_node(node_in, "读取云层参数")
    node_in.location = (-1120, 80)
    node_out = nodes.new("NodeGroupOutput")
    label_node(node_out, "输出材质/遮罩")
    node_out.location = (1020, 80)

    frame_coord = create_frame(nodes, "XL_语义_01", "01｜接口/坐标\n生成坐标与云块大小转换", (0.12, 0.12, 0.16))
    frame_noise = create_frame(nodes, "XL_语义_02", "02｜云形遮罩\n单噪声核心，降低拖动重算压力", (0.12, 0.12, 0.16))
    frame_color = create_frame(nodes, "XL_语义_03", "03｜颜色/受光\n暗部与亮部颜色混合", (0.12, 0.12, 0.16))
    frame_shader = create_frame(nodes, "XL_语义_04", "04｜透明材质输出\n透明与漫射云层混合", (0.12, 0.12, 0.16))

    texcoord = _node(nodes, "ShaderNodeTexCoord", "生成坐标", (-900, 220), frame_coord)
    mapping = _node(nodes, "ShaderNodeMapping", "坐标映射", (-700, 220), frame_coord)
    size_safe = _node(nodes, "ShaderNodeMath", "保护云块大小下限", (-900, -80), frame_coord)
    size_safe.operation = "MAXIMUM"
    _set_default(size_safe.inputs[1], 0.05)
    scale_div = _node(nodes, "ShaderNodeMath", "18 / 云块大小", (-700, -80), frame_coord)
    scale_div.operation = "DIVIDE"
    _set_default(scale_div.inputs[0], 18.0)

    noise = _node(nodes, "ShaderNodeTexNoise", "云形噪声", (-500, 120), frame_noise)
    _set_default(_input(noise, "Roughness"), 0.58)
    threshold = _node(nodes, "ShaderNodeMath", "1 - 云疏密", (-500, -170), frame_noise)
    threshold.operation = "SUBTRACT"
    _set_default(threshold.inputs[0], 1.0)
    edge_safe = _node(nodes, "ShaderNodeMath", "保护过渡下限", (-500, -340), frame_noise)
    edge_safe.operation = "MAXIMUM"
    _set_default(edge_safe.inputs[1], 0.01)
    edge_max = _node(nodes, "ShaderNodeMath", "阈值 + 过渡", (-300, -250), frame_noise)
    edge_max.operation = "ADD"
    mask_range = _node(nodes, "ShaderNodeMapRange", "云层遮罩", (-90, 20), frame_noise)
    _set_clamp(mask_range, True)
    _set_default(mask_range.inputs[3], 0.0)
    _set_default(mask_range.inputs[4], 1.0)
    opacity_mul = _node(nodes, "ShaderNodeMath", "遮罩 x 透明度", (130, 20), frame_noise)
    opacity_mul.operation = "MULTIPLY"
    _set_clamp(opacity_mul, True)

    color_mix = _node(nodes, "ShaderNodeMixRGB", "阴影色/云色混合", (130, 280), frame_color)
    color_bright = _node(nodes, "ShaderNodeMixRGB", "颜色亮度", (390, 280), frame_color)
    color_bright.blend_type = "MULTIPLY"
    _set_default(color_bright.inputs["Fac"], 1.0)
    bright_color = _node(nodes, "ShaderNodeCombineColor", "亮度转 RGB 倍率", (130, 500), frame_color)
    _set_default(_input(bright_color, "Alpha", 3), 1.0)

    transparent = _node(nodes, "ShaderNodeBsdfTransparent", "透明区域", (580, -180), frame_shader)
    diffuse = _node(nodes, "ShaderNodeBsdfDiffuse", "云层漫射 - 接受灯光", (580, 120), frame_shader)
    _set_default(_input(diffuse, "Roughness"), 0.74)
    mix_shader = _node(nodes, "ShaderNodeMixShader", "透明/云层混合", (820, 20), frame_shader)

    links.new(_output(texcoord, "Generated", 0), _input(mapping, "Vector", 0))
    links.new(_output(mapping, "Vector", 0), _input(noise, "Vector", 0))
    links.new(node_in.outputs["云块大小"], size_safe.inputs[0])
    links.new(size_safe.outputs[0], scale_div.inputs[1])
    links.new(scale_div.outputs[0], _input(noise, "Scale", 2))
    links.new(node_in.outputs["云细节"], _input(noise, "Detail", 3))
    links.new(node_in.outputs["云扭曲"], _input(noise, "Distortion"))

    links.new(node_in.outputs["云疏密"], threshold.inputs[1])
    links.new(node_in.outputs["云层过渡"], edge_safe.inputs[0])
    links.new(threshold.outputs[0], edge_max.inputs[0])
    links.new(edge_safe.outputs[0], edge_max.inputs[1])
    links.new(_output(noise, "Fac", 0), mask_range.inputs[0])
    links.new(threshold.outputs[0], mask_range.inputs[1])
    links.new(edge_max.outputs[0], mask_range.inputs[2])
    links.new(mask_range.outputs[0], opacity_mul.inputs[0])
    links.new(node_in.outputs["透明度"], opacity_mul.inputs[1])

    links.new(mask_range.outputs[0], color_mix.inputs["Fac"])
    links.new(node_in.outputs["阴影颜色"], color_mix.inputs["Color1"])
    links.new(node_in.outputs["云颜色"], color_mix.inputs["Color2"])
    links.new(color_mix.outputs["Color"], color_bright.inputs["Color1"])
    for index in range(3):
        links.new(node_in.outputs["亮度"], bright_color.inputs[index])
    links.new(bright_color.outputs["Color"], color_bright.inputs["Color2"])
    links.new(color_bright.outputs["Color"], _input(diffuse, "Color"))

    links.new(_output(transparent, "BSDF", 0), mix_shader.inputs[1])
    links.new(_output(diffuse, "BSDF", 0), mix_shader.inputs[2])
    links.new(opacity_mul.outputs[0], mix_shader.inputs[0])

    links.new(_output(mix_shader, "Shader", 0), node_out.inputs["云层材质"])
    links.new(color_bright.outputs["Color"], node_out.inputs["颜色"])
    links.new(opacity_mul.outputs[0], node_out.inputs["透明度"])
    links.new(mask_range.outputs[0], node_out.inputs["遮罩"])

    return group
