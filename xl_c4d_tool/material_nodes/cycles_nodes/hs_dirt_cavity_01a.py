import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_19_r import pf_grunge_19_r


def hs_dirt_cavity_01a():
    """BL_脏污凹腔 - 凹腔脏污多层混合材质
    基于Principled BSDF，含凹凸开关/凹腔脏污检测"""
    group_name = "BL_脏污凹腔"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="着色器", in_out="INPUT", socket_type="NodeSocketShader")
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.1195, 0.0953, 0.0762, 1.0000)
    group.interface.new_socket(name="凹腔扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0452, 0.0409, 0.0319, 1.0000)
    group.interface.new_socket(name="脏污扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame_001 = create_frame(nodes, "Frame.001", "污渍纹理: 程序化污渍/脏旧纹理")
    frame_002 = create_frame(nodes, "Frame.002", "凹腔: AO采样检测凹面/凸面区域生成遮罩")
    frame_007 = create_frame(nodes, "Frame.007", "输入着色器: 底层材质着色器输入")
    frame_008 = create_frame(nodes, "Frame.008", "粗糙度: 表面粗糙度控制")
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "凹凸: 凹凸贴图效果")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (1278.5, 474.9)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.1435045301914215
    principled_bsdf.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    principled_bsdf.inputs[21].default_value = 1.5
    principled_bsdf.inputs[22].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf.inputs[25].default_value = 0.5
    principled_bsdf.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[30].default_value = 1.3300000429153442
    cavity_012 = nodes.new("ShaderNodeGroup")
    cavity_012.location = (1743.4, -461.2)
    label_node(cavity_012, "", frame_002)
    cavity_012.xl_c4d_gradient_type = '0'
    cavity_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_012.node_tree = cavity()
    cavity_012.inputs[2].default_value = 1.0
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (1568.5, 666.0)
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (763.4, -437.5)
    label_node(group_029, "", frame_002)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_19_r()
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (1357.7, -461.2)
    label_node(map_range, "", frame_002)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = -0.15999998152256012
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (487.9, -130.0)
    label_node(group_030, "", frame_008)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_19_r()
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.2265862673521042
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.6253778338432312
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (-1141.0, 1328.9)
    mix = nodes.new("ShaderNodeMix")
    mix.location = (2135.1, -197.2)
    label_node(mix, "", frame_002)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[7].default_value = (0.0873, 0.0194, 0.0129, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    cavity_013 = nodes.new("ShaderNodeGroup")
    cavity_013.location = (1327.0, -102.3)
    label_node(cavity_013, "", frame_002)
    cavity_013.xl_c4d_gradient_type = '0'
    cavity_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_013.node_tree = cavity()
    cavity_013.inputs[2].default_value = 1.0
    math = nodes.new("ShaderNodeMath")
    math.location = (764.8, -112.1)
    label_node(math, "", frame_002)
    math.operation = 'DIVIDE'
    math.use_clamp = False
    math.inputs[0].default_value = 0.8700001239776611
    math.inputs[2].default_value = 0.5
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1022.5, -174.3)
    label_node(bump, "", frame)
    bump.invert = False
    bump.inputs[1].default_value = 0.009999999776482582
    bump.inputs[2].default_value = 1.0
    bump.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.33836817741394043
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.6858007311820984
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (732.5, -283.7)
    label_node(color_ramp_001, "", frame)
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 6:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.0
    color_ramp_002.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.12311187386512756
    color_ramp_002.color_ramp.elements[1].color = (0.25, 0.25, 0.25, 1.0)
    color_ramp_002.color_ramp.elements[2].position = 0.18844419717788696
    color_ramp_002.color_ramp.elements[2].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[3].position = 0.2203551083803177
    color_ramp_002.color_ramp.elements[3].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[4].position = 0.2522660195827484
    color_ramp_002.color_ramp.elements[4].color = (0.5, 0.5, 0.5, 1.0)
    color_ramp_002.color_ramp.elements[5].position = 0.44410908222198486
    color_ramp_002.color_ramp.elements[5].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (2105.9, -130.0)
    label_node(color_ramp_002, "", frame_008)
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (357.4, 455.2)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_031 = nodes.new("ShaderNodeGroup")
    group_031.location = (519.1, -315.8)
    label_node(group_031, "", frame_001)
    group_031.xl_c4d_gradient_type = '0'
    group_031.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_031.node_tree = pf_grunge_19_r()
    cavity_014 = nodes.new("ShaderNodeGroup")
    cavity_014.location = (1261.2, -167.8)
    label_node(cavity_014, "", frame_001)
    cavity_014.xl_c4d_gradient_type = '0'
    cavity_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_014.node_tree = cavity()
    cavity_014.inputs[2].default_value = 10.0
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.22054386138916016
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.43806666135787964
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (860.3, -315.8)
    label_node(color_ramp_003, "", frame_001)
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (1744.1, -197.2)
    label_node(mix_002, "", frame_002)
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (357.4, 757.5)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (1351.4, -281.6)
    label_node(hue_saturation_value, "", frame_002)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 0.11000001430511475
    hue_saturation_value.inputs[2].default_value = 0.06000000238418579
    hue_saturation_value.inputs[3].default_value = 1.0
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1675.8, -351.7)
    label_node(reroute_001, "", frame_002)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1498.9, -264.1)
    label_node(reroute_002, "", frame_002)
    reroute_002.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (575.2, -713.1)
    label_node(reroute_003, "", frame_002)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1498.9, -713.1)
    label_node(reroute_004, "", frame_002)
    reroute_004.socket_idname = 'NodeSocketFloat'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1390.7, 724.0)
    reroute_005.socket_idname = 'NodeSocketFloat'
    reroute = nodes.new("NodeReroute")
    reroute.location = (1053.2, 377.2)
    reroute.socket_idname = 'NodeSocketColor'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (1216.5, 313.7)
    reroute_007.socket_idname = 'NodeSocketVector'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (306.5, 1538.9)
    reroute_006.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-685.9, 1296.1)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (1009.3, -264.0)
    label_node(reroute_009, "", frame_002)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (1595.4, -394.3)
    label_node(reroute_010, "", frame_002)
    reroute_010.socket_idname = 'NodeSocketColor'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (1621.5, -372.7)
    label_node(reroute_011, "", frame_002)
    reroute_011.socket_idname = 'NodeSocketColor'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (1195.6, -203.5)
    label_node(reroute_012, "", frame_002)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1009.3, -182.1)
    label_node(reroute_013, "", frame_002)
    reroute_013.socket_idname = 'NodeSocketFloat'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1145.5, -591.5)
    label_node(reroute_015, "", frame_002)
    reroute_015.socket_idname = 'NodeSocketColor'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (1585.2, -561.7)
    label_node(reroute_016, "", frame_002)
    reroute_016.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (1636.5, -540.7)
    label_node(reroute_017, "", frame_002)
    reroute_017.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (2135.8, -493.7)
    label_node(reroute_019, "", frame_002)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (2004.3, -372.9)
    label_node(reroute_021, "", frame_002)
    reroute_021.socket_idname = 'NodeSocketColor'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (2030.7, -352.6)
    label_node(reroute_022, "", frame_002)
    reroute_022.socket_idname = 'NodeSocketColor'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (915.9, -314.2)
    label_node(reroute_024, "", frame_008)
    reroute_024.socket_idname = 'NodeSocketColor'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (764.6, -164.5)
    label_node(reroute_025, "", frame_008)
    reroute_025.socket_idname = 'NodeSocketColor'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1039.0, -314.1)
    label_node(reroute_026, "", frame_008)
    reroute_026.socket_idname = 'NodeSocketColor'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (-1235.3, 1145.2)
    reroute_027.socket_idname = 'NodeSocketColor'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (223.9, 279.3)
    reroute_023.socket_idname = 'NodeSocketColor'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (109.1, 256.7)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (-284.8, 300.9)
    reroute_029.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (-606.3, 56.8)
    reroute_030.socket_idname = 'NodeSocketFloat'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (-497.0, -95.4)
    reroute_031.socket_idname = 'NodeSocketColor'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (-73.0, 890.7)
    reroute_032.socket_idname = 'NodeSocketColor'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (594.2, -238.1)
    label_node(reroute_034, "", frame_002)
    reroute_034.socket_idname = 'NodeSocketFloat'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (305.5, -101.7)
    label_node(percentage_to_0_1, "百分比转0-1", frame_008)
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[3].default_value = 0.009999999776482582
    percentage_to_0_1.inputs[4].default_value = 0.75
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_1.location = (221.3, -102.2)
    label_node(percentage_to_0_1_1, "百分比转0-1", frame_001)
    percentage_to_0_1_1.clamp = True
    percentage_to_0_1_1.interpolation_type = 'LINEAR'
    percentage_to_0_1_1.data_type = 'FLOAT'
    percentage_to_0_1_1.inputs[2].default_value = 100.0
    percentage_to_0_1_1.inputs[3].default_value = 0.009999999776482582
    percentage_to_0_1_1.inputs[4].default_value = 0.1899999976158142
    percentage_to_0_1_1.inputs[5].default_value = 4.0
    percentage_to_0_1_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_2 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_2.location = (223.3, -356.8)
    label_node(percentage_to_0_1_2, "百分比转0-1", frame_001)
    percentage_to_0_1_2.clamp = True
    percentage_to_0_1_2.interpolation_type = 'LINEAR'
    percentage_to_0_1_2.data_type = 'FLOAT'
    percentage_to_0_1_2.inputs[2].default_value = 100.0
    percentage_to_0_1_2.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1_2.inputs[4].default_value = 1.0
    percentage_to_0_1_2.inputs[5].default_value = 4.0
    percentage_to_0_1_2.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (533.0, -248.7)
    label_node(reroute_018, "", frame_001)
    reroute_018.socket_idname = 'NodeSocketFloat'
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (1168.0, -267.7)
    label_node(reroute_035, "", frame_001)
    reroute_035.socket_idname = 'NodeSocketColor'
    percentage_to_0_1_3 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_3.location = (224.2, -206.9)
    label_node(percentage_to_0_1_3, "百分比转0-1", frame_002)
    percentage_to_0_1_3.clamp = True
    percentage_to_0_1_3.interpolation_type = 'LINEAR'
    percentage_to_0_1_3.data_type = 'FLOAT'
    percentage_to_0_1_3.inputs[2].default_value = 100.0
    percentage_to_0_1_3.inputs[3].default_value = 0.009999999776482582
    percentage_to_0_1_3.inputs[4].default_value = 0.30000001192092896
    percentage_to_0_1_3.inputs[5].default_value = 4.0
    percentage_to_0_1_3.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_4 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_4.location = (223.5, -452.2)
    label_node(percentage_to_0_1_4, "百分比转0-1", frame_002)
    percentage_to_0_1_4.clamp = True
    percentage_to_0_1_4.interpolation_type = 'LINEAR'
    percentage_to_0_1_4.data_type = 'FLOAT'
    percentage_to_0_1_4.inputs[2].default_value = 100.0
    percentage_to_0_1_4.inputs[3].default_value = 0.009999999776482582
    percentage_to_0_1_4.inputs[4].default_value = 2.069999933242798
    percentage_to_0_1_4.inputs[5].default_value = 4.0
    percentage_to_0_1_4.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_4.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_4.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (1188.5, -264.0)
    label_node(reroute_033, "", frame_002)
    reroute_033.socket_idname = 'NodeSocketColor'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1285.4, -424.6)
    label_node(reroute_036, "", frame_002)
    reroute_036.socket_idname = 'NodeSocketColor'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (782.5, -101.7)
    label_node(hs_bump_control, "", frame)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (457.7, -283.5)
    label_node(group_032, "", frame)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = pf_grunge_19_r()
    percentage_to_0_1_5 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_5.location = (267.7, -285.1)
    label_node(percentage_to_0_1_5, "百分比转0-1", frame)
    percentage_to_0_1_5.clamp = True
    percentage_to_0_1_5.interpolation_type = 'LINEAR'
    percentage_to_0_1_5.data_type = 'FLOAT'
    percentage_to_0_1_5.inputs[2].default_value = 100.0
    percentage_to_0_1_5.inputs[3].default_value = 0.20000000298023224
    percentage_to_0_1_5.inputs[4].default_value = 1.25
    percentage_to_0_1_5.inputs[5].default_value = 4.0
    percentage_to_0_1_5.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_5.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_5.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_5.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_5.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_5.inputs[11].default_value = (4.0000, 4.0000, 4.0000)

    # === 节点连接 ===
    links.new(mix_001.outputs[2], principled_bsdf.inputs[0])
    links.new(reroute_022.outputs[0], mix.inputs[0])
    links.new(reroute_029.outputs[0], mix_001.inputs[0])
    links.new(reroute_007.outputs[0], principled_bsdf.inputs[5])
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[2])
    links.new(reroute_023.outputs[0], mix_001.inputs[6])
    links.new(reroute_034.outputs[0], math.inputs[1])
    links.new(reroute.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_026.outputs[0], color_ramp_002.inputs[0])
    links.new(reroute_027.outputs[0], color_ramp.inputs[0])
    links.new(reroute_015.outputs[0], map_range.inputs[0])
    links.new(reroute_021.outputs[0], mix.inputs[6])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(reroute_019.outputs[0], map_range_001.inputs[0])
    links.new(reroute_010.outputs[0], mix_002.inputs[7])
    links.new(reroute_036.outputs[0], hue_saturation_value.inputs[4])
    links.new(map_range_001.outputs[0], reroute_005.inputs[0])
    links.new(reroute_033.outputs[0], reroute_002.inputs[0])
    links.new(reroute_003.outputs[0], reroute_004.inputs[0])
    links.new(reroute_011.outputs[0], mix_002.inputs[6])
    links.new(reroute_001.outputs[0], mix_002.inputs[0])
    links.new(reroute_028.outputs[0], mix_001.inputs[7])
    links.new(reroute_005.outputs[0], mix_shader.inputs[0])
    links.new(input_node.outputs[0], mix_shader.inputs[1])
    links.new(reroute_006.outputs[0], reroute.inputs[0])
    links.new(bump.outputs[0], reroute_007.inputs[0])
    links.new(color_ramp_002.outputs[0], reroute_006.inputs[0])
    links.new(color_ramp.outputs[0], reroute_008.inputs[0])
    links.new(input_node.outputs[5], reroute_009.inputs[0])
    links.new(hue_saturation_value.outputs[0], reroute_010.inputs[0])
    links.new(reroute_002.outputs[0], reroute_011.inputs[0])
    links.new(math.outputs[0], reroute_013.inputs[0])
    links.new(map_range.outputs[0], reroute_016.inputs[0])
    links.new(reroute_004.outputs[0], reroute_017.inputs[0])
    links.new(mix_002.outputs[2], reroute_021.inputs[0])
    links.new(reroute_008.outputs[0], reroute_022.inputs[0])
    links.new(reroute_025.outputs[0], reroute_024.inputs[0])
    links.new(reroute_024.outputs[0], reroute_026.inputs[0])
    links.new(reroute_026.outputs[0], reroute_027.inputs[0])
    links.new(reroute_032.outputs[0], reroute_023.inputs[0])
    links.new(reroute_031.outputs[0], reroute_028.inputs[0])
    links.new(reroute_030.outputs[0], reroute_029.inputs[0])
    links.new(input_node.outputs[8], reroute_031.inputs[0])
    links.new(mix.outputs[2], reroute_032.inputs[0])
    links.new(percentage_to_0_1_4.outputs[0], reroute_034.inputs[0])
    links.new(input_node.outputs[1], percentage_to_0_1.inputs[0])
    links.new(input_node.outputs[9], percentage_to_0_1_1.inputs[0])
    links.new(input_node.outputs[10], percentage_to_0_1_2.inputs[0])
    links.new(percentage_to_0_1_1.outputs[0], reroute_018.inputs[0])
    links.new(color_ramp_003.outputs[0], reroute_035.inputs[0])
    links.new(percentage_to_0_1_4.outputs[0], reroute_003.inputs[0])
    links.new(input_node.outputs[6], percentage_to_0_1_4.inputs[0])
    links.new(input_node.outputs[7], percentage_to_0_1_3.inputs[0])
    links.new(reroute_009.outputs[0], reroute_033.inputs[0])
    links.new(reroute_033.outputs[0], reroute_036.inputs[0])
    links.new(reroute_016.outputs[0], cavity_012.inputs[1])
    links.new(reroute_017.outputs[0], cavity_012.inputs[0])
    links.new(cavity_012.outputs[0], reroute_019.inputs[0])
    links.new(reroute_013.outputs[0], cavity_013.inputs[0])
    links.new(reroute_012.outputs[0], cavity_013.inputs[1])
    links.new(cavity_013.outputs[0], reroute_001.inputs[0])
    links.new(reroute_035.outputs[0], cavity_014.inputs[1])
    links.new(cavity_014.outputs[0], reroute_030.inputs[0])
    links.new(reroute_018.outputs[0], cavity_014.inputs[0])
    links.new(group_029.outputs[0], reroute_012.inputs[0])
    links.new(group_029.outputs[0], reroute_015.inputs[0])
    links.new(percentage_to_0_1_3.outputs[0], group_029.inputs[0])
    links.new(group_030.outputs[0], reroute_025.inputs[0])
    links.new(percentage_to_0_1.outputs[0], group_030.inputs[0])
    links.new(group_031.outputs[0], color_ramp_003.inputs[0])
    links.new(percentage_to_0_1_2.outputs[0], group_031.inputs[0])
    links.new(input_node.outputs[4], hs_bump_control.inputs[1])
    links.new(input_node.outputs[2], hs_bump_control.inputs[0])
    links.new(input_node.outputs[3], percentage_to_0_1_5.inputs[0])
    links.new(percentage_to_0_1_5.outputs[0], group_032.inputs[0])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(group_032.outputs[0], color_ramp_001.inputs[0])
    links.new(color_ramp_001.outputs[0], bump.inputs[3])

    return group