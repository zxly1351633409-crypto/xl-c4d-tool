import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_20b_r import pf_grunge_20b_r
from .pf_grunge_22d_r import pf_grunge_22d_r


def hs_rust_01a():
    """BL_生锈 - 铁锈材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/锈蚀混合"""
    group_name = "BL_生锈"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="基础着色器", in_out="INPUT", socket_type="NodeSocketShader")
    group.interface.new_socket(name="颜色: 材质颜色通道", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.1301, 0.0666, 0.0382, 1.0000)
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="损伤变体A", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="损伤变体B", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="损伤扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame_004 = create_frame(nodes, "Frame.004", "输入: 外部数据输入")
    frame_001 = create_frame(nodes, "Frame.001", "损伤A: 第一层损伤/磨损效果")
    frame_002 = create_frame(nodes, "Frame.002", "损伤B: 第二层损伤/磨损效果")

    # === 节点创建 ===
    principled_bsdf_004 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_004.location = (-190.8, -137.4)
    principled_bsdf_004.distribution = 'MULTI_GGX'
    principled_bsdf_004.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_004.inputs[1].default_value = 0.09969788789749146
    principled_bsdf_004.inputs[3].default_value = 1.5
    principled_bsdf_004.inputs[4].default_value = 1.0
    principled_bsdf_004.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_004.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_004.inputs[11].default_value = 1.399999976158142
    principled_bsdf_004.inputs[13].default_value = 0.5
    principled_bsdf_004.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_004.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_004.inputs[20].default_value = 0.029999999329447746
    principled_bsdf_004.inputs[21].default_value = 1.5
    principled_bsdf_004.inputs[22].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_004.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_004.inputs[25].default_value = 0.5
    principled_bsdf_004.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_004.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_004.inputs[30].default_value = 1.3300000429153442
    mix_shader_002 = nodes.new("ShaderNodeMixShader")
    mix_shader_002.location = (491.3, -90.6)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (-1268.4, 798.8)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[1].default_value = 0.09999999403953552
    map_range_003.inputs[2].default_value = 1.0
    map_range_003.inputs[3].default_value = 0.3600001037120819
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix = nodes.new("ShaderNodeMix")
    mix.location = (-1234.4, -156.1)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.3444109261035919
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.483384370803833
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (848.3, -350.4)
    label_node(color_ramp_001, "", frame_002)
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (-1846.5, -296.6)
    hue_saturation_value.inputs[0].default_value = 0.47999998927116394
    hue_saturation_value.inputs[1].default_value = 2.0
    hue_saturation_value.inputs[2].default_value = 2.0
    hue_saturation_value.inputs[3].default_value = 1.0
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.3293052911758423
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.40181222558021545
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (848.3, -102.4)
    label_node(color_ramp, "", frame_002)
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (519.9, -102.4)
    label_node(group_035, "", frame_002)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = pf_grunge_22d_r()
    group_035.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (519.9, -102.9)
    label_node(group_036, "", frame_001)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_20b_r()
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (-755.8, 1190.6)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[7].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.2628399729728699
    color_ramp_002.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.35649481415748596
    color_ramp_002.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (843.8, -102.9)
    label_node(color_ramp_002, "", frame_001)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-497.3, -260.9)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    bump.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (329.9, -102.9)
    label_node(percentage_to_0_1, "百分比转0-1", frame_001)
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1.inputs[4].default_value = 0.6200000047683716
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_1.location = (945.6, -834.9)
    label_node(percentage_to_0_1_1, "百分比转0-1", frame_002)
    percentage_to_0_1_1.clamp = True
    percentage_to_0_1_1.interpolation_type = 'LINEAR'
    percentage_to_0_1_1.data_type = 'FLOAT'
    percentage_to_0_1_1.inputs[2].default_value = 100.0
    percentage_to_0_1_1.inputs[3].default_value = 1.2000000476837158
    percentage_to_0_1_1.inputs[5].default_value = 4.0
    percentage_to_0_1_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_2 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_2.location = (329.9, -102.4)
    label_node(percentage_to_0_1_2, "百分比转0-1", frame_002)
    percentage_to_0_1_2.clamp = True
    percentage_to_0_1_2.interpolation_type = 'LINEAR'
    percentage_to_0_1_2.data_type = 'FLOAT'
    percentage_to_0_1_2.inputs[2].default_value = 100.0
    percentage_to_0_1_2.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1_2.inputs[4].default_value = 0.5
    percentage_to_0_1_2.inputs[5].default_value = 4.0
    percentage_to_0_1_2.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (-1408.5, 419.8)
    reroute.socket_idname = 'NodeSocketColor'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-879.2, 420.3)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (-620.2, 420.2)
    reroute_002.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (-380.0, 1157.4)
    reroute_003.socket_idname = 'NodeSocketColor'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (254.7, -148.9)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (256.2, -189.1)
    reroute_005.socket_idname = 'NodeSocketShader'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-1472.3, 581.9)
    reroute_006.socket_idname = 'NodeSocketFloat'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-1445.6, -351.5)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-1658.7, -538.4)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-545.2, -402.2)
    reroute_009.socket_idname = 'NodeSocketColor'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (-919.8, -402.5)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-546.1, -341.5)
    reroute_010.socket_idname = 'NodeSocketFloat'
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.3444109261035919
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.483384370803833
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (848.3, -593.7)
    label_node(color_ramp_003, "", frame_002)
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (550.1, -585.9)
    label_node(group_037, "", frame_002)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_22d_r()
    group_037.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_3.location = (360.1, -585.9)
    label_node(percentage_to_0_1_3, "百分比转0-1", frame_002)
    percentage_to_0_1_3.clamp = True
    percentage_to_0_1_3.interpolation_type = 'LINEAR'
    percentage_to_0_1_3.data_type = 'FLOAT'
    percentage_to_0_1_3.inputs[2].default_value = 100.0
    percentage_to_0_1_3.inputs[3].default_value = 0.5
    percentage_to_0_1_3.inputs[4].default_value = 2.0
    percentage_to_0_1_3.inputs[5].default_value = 4.0
    percentage_to_0_1_3.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-1009.1, 178.5)
    reroute_011.socket_idname = 'NodeSocketColor'

    # === 节点连接 ===
    links.new(reroute_004.outputs[0], mix_shader_002.inputs[0])
    links.new(mix.outputs[2], principled_bsdf_004.inputs[0])
    links.new(hue_saturation_value.outputs[0], mix.inputs[6])
    links.new(color_ramp.outputs[0], map_range_003.inputs[0])
    links.new(principled_bsdf_004.outputs[0], mix_shader_002.inputs[1])
    links.new(reroute.outputs[0], mix.inputs[0])
    links.new(map_range_003.outputs[0], mix_001.inputs[6])
    links.new(color_ramp_002.outputs[0], mix_001.inputs[0])
    links.new(reroute_002.outputs[0], principled_bsdf_004.inputs[2])
    links.new(mix_shader_002.outputs[0], output_node.inputs[0])
    links.new(bump.outputs[0], principled_bsdf_004.inputs[5])
    links.new(reroute_009.outputs[0], bump.inputs[3])
    links.new(reroute_005.outputs[0], mix_shader_002.inputs[2])
    links.new(input_node.outputs[5], percentage_to_0_1.inputs[0])
    links.new(reroute_006.outputs[0], map_range_003.inputs[4])
    links.new(input_node.outputs[6], percentage_to_0_1_2.inputs[0])
    links.new(reroute_007.outputs[0], mix.inputs[7])
    links.new(color_ramp_001.outputs[0], reroute.inputs[0])
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], reroute_002.inputs[0])
    links.new(mix_001.outputs[2], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], reroute_004.inputs[0])
    links.new(input_node.outputs[0], reroute_005.inputs[0])
    links.new(percentage_to_0_1_1.outputs[0], reroute_006.inputs[0])
    links.new(reroute_008.outputs[0], reroute_007.inputs[0])
    links.new(input_node.outputs[1], hue_saturation_value.inputs[4])
    links.new(input_node.outputs[1], reroute_008.inputs[0])
    links.new(group_036.outputs[0], color_ramp_002.inputs[0])
    links.new(percentage_to_0_1.outputs[0], group_036.inputs[0])
    links.new(group_035.outputs[0], color_ramp.inputs[0])
    links.new(group_035.outputs[0], color_ramp_001.inputs[0])
    links.new(percentage_to_0_1_2.outputs[0], group_035.inputs[1])
    links.new(reroute_011.outputs[0], reroute_009.inputs[0])
    links.new(reroute_010.outputs[0], bump.inputs[0])
    links.new(input_node.outputs[4], hs_bump_control.inputs[1])
    links.new(input_node.outputs[2], hs_bump_control.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_010.inputs[0])
    links.new(input_node.outputs[7], percentage_to_0_1_1.inputs[0])
    links.new(percentage_to_0_1_3.outputs[0], group_037.inputs[1])
    links.new(group_037.outputs[0], color_ramp_003.inputs[0])
    links.new(color_ramp_003.outputs[0], reroute_011.inputs[0])
    links.new(input_node.outputs[3], percentage_to_0_1_3.inputs[0])

    return group