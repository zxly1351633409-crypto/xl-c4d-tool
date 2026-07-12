import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_02_r import pf_grunge_02_r
from .pf_grunge_18d_r import pf_grunge_18d_r
from .pf_grunge_22_r import pf_grunge_22_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_22c_r import pf_grunge_22c_r


def hs_metal_03a():
    """BL_金属03 - 旧化氧化金属材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损/凹腔脏污"""
    group_name = "BL_金属03"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="边缘磨损_随机", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_额外细节", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_变色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0782, 0.1070, 0.0762, 1.0000)
    group.interface.new_socket(name="油漆_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_边缘淡化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "油漆: 油漆材质基础设置")
    frame_001 = create_frame(nodes, "Frame.001", "粗糙度缩放: 控制粗糙度贴图的缩放比例")
    frame_002 = create_frame(nodes, "Frame.002", "凹凸缩放: 控制凹凸贴图的缩放大小", (0.25, 0.16, 0.36))
    frame_003 = create_frame(nodes, "Frame.003", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_004 = create_frame(nodes, "Frame.004", "边缘碎裂: 边缘剥落和碎裂效果的遮罩")
    frame_005 = create_frame(nodes, "Frame.005", "凹凸控制: 百分比映射0-1控制凹凸强度")
    frame_006 = create_frame(nodes, "Frame.006", "倒角控制: 控制倒角效果的强度和范围")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (1139.5, 21.0)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[1].default_value = 0.22727271914482117
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.40454545617103577
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
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (1618.2, -674.5)
    label_node(mix_003, "", frame)
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = True
    mix_003.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_003.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (528.1, -886.8)
    label_node(group_037, "", frame)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_22c_r()
    cavity_012 = nodes.new("ShaderNodeGroup")
    cavity_012.location = (1186.2, -790.9)
    label_node(cavity_012, "", frame)
    cavity_012.xl_c4d_gradient_type = '0'
    cavity_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_012.node_tree = cavity()
    cavity_012.inputs[2].default_value = 0.5
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (823.8, -789.1)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = False
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 0.75
    map_range_001.inputs[3].default_value = -0.559999942779541
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (1186.2, -551.1)
    label_node(all_edges_014, "", frame)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 1.0
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (528.1, -595.8)
    label_node(group_030, "", frame)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_02_r()
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (823.8, -499.1)
    label_node(map_range, "", frame)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = -0.19999998807907104
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (1309.5, -1254.6)
    label_node(hue_saturation_value, "", frame)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 0.4000000059604645
    hue_saturation_value.inputs[2].default_value = 3.0
    hue_saturation_value.inputs[3].default_value = 1.0
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (1863.4, -674.5)
    label_node(mix_004, "", frame)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = True
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    hue_saturation_value_001 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_001.location = (1309.4, -1418.8)
    label_node(hue_saturation_value_001, "", frame)
    hue_saturation_value_001.inputs[0].default_value = 0.5
    hue_saturation_value_001.inputs[1].default_value = 0.20000000298023224
    hue_saturation_value_001.inputs[2].default_value = 1.2000000476837158
    hue_saturation_value_001.inputs[3].default_value = 1.0
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.13595128059387207
    color_ramp.color_ramp.elements[0].color = (0.1711277961730957, 0.1711277961730957, 0.1711277961730957, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.8217525482177734
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (725.4, -141.3)
    label_node(color_ramp, "", frame_001)
    group_038 = nodes.new("ShaderNodeGroup")
    group_038.location = (499.3, -241.7)
    label_node(group_038, "", frame_001)
    group_038.xl_c4d_gradient_type = '0'
    group_038.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_038.node_tree = pf_grunge_18d_r()
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-514.3, -605.5)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (436.8, -102.3)
    label_node(bevel, "", frame_006)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (2156.3, -674.5)
    label_node(mix_005, "", frame)
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    mix_005.blend_type = 'COLOR'
    mix_005.clamp_factor = True
    mix_005.clamp_result = True
    mix_005.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_005.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[7].default_value = (0.2967, 0.3083, 0.2446, 1.0000)
    mix_005.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_031 = nodes.new("ShaderNodeGroup")
    group_031.location = (1186.2, -302.5)
    label_node(group_031, "", frame)
    group_031.xl_c4d_gradient_type = '0'
    group_031.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_031.node_tree = pf_grunge_22c_r()
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.07194454222917557
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.336363822221756
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (1574.3, -305.4)
    label_node(color_ramp_001, "", frame)
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (3436.8, 130.8)
    all_edges_015 = nodes.new("ShaderNodeGroup")
    all_edges_015.location = (1065.1, -257.1)
    label_node(all_edges_015, "", frame_003)
    all_edges_015.xl_c4d_gradient_type = '0'
    all_edges_015.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_015.node_tree = all_edges()
    all_edges_015.inputs[2].default_value = 1.0
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (486.0, -363.3)
    label_node(group_032, "", frame_003)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = pf_grunge_02_r()
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (796.6, -363.0)
    label_node(map_range_002, "", frame_003)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 1.0
    map_range_002.inputs[3].default_value = -0.6800000071525574
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_016 = nodes.new("ShaderNodeGroup")
    all_edges_016.location = (1059.6, -457.5)
    label_node(all_edges_016, "", frame_003)
    all_edges_016.xl_c4d_gradient_type = '0'
    all_edges_016.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_016.node_tree = all_edges()
    all_edges_016.inputs[2].default_value = 1.0
    mix = nodes.new("ShaderNodeMix")
    mix.location = (1305.2, -379.3)
    label_node(mix, "", frame_003)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[6].default_value = (0.0534, 0.0132, 0.0136, 1.0000)
    mix.inputs[7].default_value = (0.1241, 0.0874, 0.0714, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (2739.6, -146.6)
    bump_001.invert = False
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (1312.6, -1030.5)
    label_node(mix_006, "", frame)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = True
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[7].default_value = (0.1384, 0.0316, 0.0263, 1.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_033 = nodes.new("ShaderNodeGroup")
    group_033.location = (445.0, -85.5)
    label_node(group_033, "", frame_002)
    group_033.xl_c4d_gradient_type = '0'
    group_033.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_033.node_tree = pf_grunge_22_r()
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.3564954400062561
    color_ramp_002.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.64090895652771
    color_ramp_002.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (677.6, -35.6)
    label_node(color_ramp_002, "", frame_002)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (1139.5, -484.6)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[2].default_value = 0.6000000238418579
    principled_bsdf_002.inputs[3].default_value = 1.5
    principled_bsdf_002.inputs[4].default_value = 1.0
    principled_bsdf_002.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_002.inputs[11].default_value = 1.399999976158142
    principled_bsdf_002.inputs[13].default_value = 0.5
    principled_bsdf_002.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_002.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_002.inputs[20].default_value = 0.029999999329447746
    principled_bsdf_002.inputs[21].default_value = 1.5
    principled_bsdf_002.inputs[22].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_002.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_002.inputs[25].default_value = 0.5
    principled_bsdf_002.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_002.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_002.inputs[30].default_value = 1.3300000429153442
    all_edges_017 = nodes.new("ShaderNodeGroup")
    all_edges_017.location = (1080.9, -284.0)
    label_node(all_edges_017, "", frame_004)
    all_edges_017.xl_c4d_gradient_type = '0'
    all_edges_017.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_017.node_tree = all_edges()
    all_edges_017.inputs[2].default_value = 1.0
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (521.5, -444.8)
    label_node(group_034, "", frame_004)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_22b_r()
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (812.9, -348.5)
    label_node(map_range_003, "", frame_004)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 1.0
    map_range_003.inputs[3].default_value = -0.9800000190734863
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (1595.8, 69.5)
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (-63.3, -166.5)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'COLOR'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[6].default_value = (0.0865, 0.0414, 0.0162, 1.0000)
    mix_001.inputs[7].default_value = (0.0672, 0.0169, 0.0099, 1.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (3046.5, -20.3)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[2].default_value = 0.5
    principled_bsdf_001.inputs[3].default_value = 1.5
    principled_bsdf_001.inputs[4].default_value = 1.0
    principled_bsdf_001.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_001.inputs[11].default_value = 1.399999976158142
    principled_bsdf_001.inputs[13].default_value = 0.5
    principled_bsdf_001.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_001.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001.inputs[20].default_value = 0.029999999329447746
    principled_bsdf_001.inputs[21].default_value = 1.5
    principled_bsdf_001.inputs[22].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_001.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001.inputs[25].default_value = 0.5
    principled_bsdf_001.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_001.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_001.inputs[30].default_value = 1.3300000429153442
    reroute = nodes.new("NodeReroute")
    reroute.location = (1286.7, -1393.3)
    label_node(reroute, "", frame)
    reroute.socket_idname = 'NodeSocketColor'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1863.7, -826.1)
    reroute_002.socket_idname = 'NodeSocketVector'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1021.3, -1184.4)
    label_node(reroute_004, "", frame)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (2391.5, -299.0)
    reroute_006.socket_idname = 'NodeSocketFloat'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (2247.1, -71.3)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (2391.5, 71.1)
    reroute_008.socket_idname = 'NodeSocketFloat'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1461.3, -290.8)
    label_node(reroute_005, "", frame_003)
    reroute_005.socket_idname = 'NodeSocketFloat'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-48.9, -636.5)
    reroute_009.socket_idname = 'NodeSocketVector'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1286.7, -1204.9)
    label_node(reroute_001, "", frame)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (1286.7, -1558.2)
    label_node(reroute_010, "", frame)
    reroute_010.socket_idname = 'NodeSocketColor'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-3390.7, -680.6)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1826.3, -827.5)
    label_node(reroute_003, "", frame)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1826.3, -850.9)
    label_node(reroute_013, "", frame)
    reroute_013.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (1826.3, -872.7)
    label_node(reroute_014, "", frame)
    reroute_014.socket_idname = 'NodeSocketColor'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1826.3, -591.3)
    label_node(reroute_015, "", frame)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (-373.0, -320.4)
    reroute_016.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (1016.2, -382.7)
    label_node(reroute_017, "", frame_004)
    reroute_017.socket_idname = 'NodeSocketFloat'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (-1059.3, 223.1)
    reroute_018.socket_idname = 'NodeSocketColor'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (1094.8, -135.1)
    reroute_019.socket_idname = 'NodeSocketVector'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (1094.8, -640.4)
    reroute_020.socket_idname = 'NodeSocketVector'
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (301.5, -446.2)
    label_node(map_range_004, "", frame)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.4699999690055847
    map_range_004.inputs[4].default_value = 2.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (320.1, -101.9)
    label_node(map_range_005, "", frame_001)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.1599999964237213
    map_range_005.inputs[4].default_value = 0.5299999713897705
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (498.1, -479.0)
    label_node(reroute_021, "", frame)
    reroute_021.socket_idname = 'NodeSocketFloat'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (498.1, -965.8)
    label_node(reroute_022, "", frame)
    reroute_022.socket_idname = 'NodeSocketFloat'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (498.1, -674.2)
    label_node(reroute_023, "", frame)
    reroute_023.socket_idname = 'NodeSocketFloat'
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (277.4, -59.9)
    label_node(map_range_006, "", frame_002)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.20000000298023224
    map_range_006.inputs[4].default_value = 1.5
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1569.3, -851.2)
    label_node(reroute_026, "", frame)
    reroute_026.socket_idname = 'NodeSocketColor'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (1569.3, -872.5)
    label_node(reroute_027, "", frame)
    reroute_027.socket_idname = 'NodeSocketColor'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (1947.3, -338.3)
    label_node(reroute_028, "", frame)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (2092.7, -850.3)
    label_node(reroute_029, "", frame)
    reroute_029.socket_idname = 'NodeSocketColor'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (2106.9, -827.0)
    label_node(reroute_030, "", frame)
    reroute_030.socket_idname = 'NodeSocketColor'
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (652.5, -102.4)
    label_node(map_range_007, "", frame)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.029999999329447746
    map_range_007.inputs[4].default_value = 1.7999999523162842
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (1187.1, -516.7)
    label_node(math_002, "", frame)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 0.20000000298023224
    math_002.inputs[2].default_value = 0.5
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1143.1, -523.1)
    label_node(reroute_031, "", frame)
    reroute_031.socket_idname = 'NodeSocketFloat'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (1143.1, -871.2)
    label_node(reroute_032, "", frame)
    reroute_032.socket_idname = 'NodeSocketFloat'
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (1046.8, -890.6)
    label_node(reroute_033, "", frame)
    reroute_033.socket_idname = 'NodeSocketFloat'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (1143.1, -136.6)
    label_node(reroute_034, "", frame)
    reroute_034.socket_idname = 'NodeSocketFloat'
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (1046.8, -650.5)
    label_node(reroute_035, "", frame)
    reroute_035.socket_idname = 'NodeSocketFloat'
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (651.4, -345.4)
    label_node(map_range_008, "", frame)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.10000000149011612
    map_range_008.inputs[4].default_value = 25.0
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (796.6, -153.8)
    label_node(math_001, "", frame_003)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 0.5
    math_001.inputs[2].default_value = 0.5
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (812.7, -101.8)
    label_node(map_range_009, "", frame_004)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[3].default_value = 0.009999999776482582
    map_range_009.inputs[4].default_value = 0.1900000274181366
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (739.9, -134.9)
    label_node(reroute_036, "", frame_003)
    reroute_036.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (935.6, -135.8)
    label_node(reroute_037, "", frame_003)
    reroute_037.socket_idname = 'NodeSocketFloat'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (739.9, -258.0)
    label_node(reroute_038, "", frame_003)
    reroute_038.socket_idname = 'NodeSocketFloat'
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (559.8, -102.1)
    label_node(map_range_010, "", frame_003)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[4].default_value = -0.10999998450279236
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (318.2, -363.4)
    label_node(map_range_011, "", frame_003)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = 0.5299999713897705
    map_range_011.inputs[4].default_value = 2.0
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    bump_002 = nodes.new("ShaderNodeBump")
    bump_002.location = (898.4, -606.7)
    bump_002.invert = True
    bump_002.inputs[1].default_value = 1.0
    bump_002.inputs[2].default_value = 1.9600000381469727
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (245.8, 415.8)
    reroute_011.socket_idname = 'NodeSocketFloat'
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'CONSTANT'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.00906344410032034
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.40785497426986694
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (522.8, -512.4)
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (343.1, -826.1)
    reroute_039.socket_idname = 'NodeSocketVector'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (2391.6, -321.1)
    reroute_040.socket_idname = 'NodeSocketVector'
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (475.8, -770.2)
    reroute_041.socket_idname = 'NodeSocketVector'
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (245.8, -694.6)
    reroute_042.socket_idname = 'NodeSocketFloat'
    reroute_043 = nodes.new("NodeReroute")
    reroute_043.location = (1033.2, -199.8)
    reroute_043.socket_idname = 'NodeSocketColor'
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (358.2, -307.0)
    label_node(map_range_012, "", frame_004)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.05000000074505806
    map_range_012.inputs[4].default_value = 0.23000004887580872
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_044 = nodes.new("NodeReroute")
    reroute_044.location = (308.3, -230.7)
    label_node(reroute_044, "", frame_004)
    reroute_044.socket_idname = 'NodeSocketFloatPercentage'
    reroute_045 = nodes.new("NodeReroute")
    reroute_045.location = (308.3, -437.7)
    label_node(reroute_045, "", frame_004)
    reroute_045.socket_idname = 'NodeSocketFloatPercentage'
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (246.8, -102.3)
    label_node(map_range_013, "", frame_006)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = 0.0010000000474974513
    map_range_013.inputs[4].default_value = 0.009999999776482582
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (-502.0, -31.5)
    reroute_024.socket_idname = 'NodeSocketColor'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (346.1, -101.7)
    label_node(hs_bump_control, "", frame_005)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (-752.6, -676.3)
    reroute_025.socket_idname = 'NodeSocketColor'
    reroute_046 = nodes.new("NodeReroute")
    reroute_046.location = (1553.1, 12.1)
    reroute_046.socket_idname = 'NodeSocketFloat'
    reroute_047 = nodes.new("NodeReroute")
    reroute_047.location = (1553.1, 417.8)
    reroute_047.socket_idname = 'NodeSocketFloat'
    reroute_048 = nodes.new("NodeReroute")
    reroute_048.location = (870.1, -687.3)
    reroute_048.socket_idname = 'NodeSocketFloat'
    reroute_050 = nodes.new("NodeReroute")
    reroute_050.location = (870.1, -456.3)
    reroute_050.socket_idname = 'NodeSocketFloat'
    reroute_051 = nodes.new("NodeReroute")
    reroute_051.location = (1590.3, -456.3)
    reroute_051.socket_idname = 'NodeSocketFloat'
    reroute_052 = nodes.new("NodeReroute")
    reroute_052.location = (1033.2, -536.7)
    reroute_052.socket_idname = 'NodeSocketColor'
    reroute_053 = nodes.new("NodeReroute")
    reroute_053.location = (1947.7, -228.0)
    reroute_053.socket_idname = 'NodeSocketFloat'
    reroute_055 = nodes.new("NodeReroute")
    reroute_055.location = (-752.6, -456.3)
    reroute_055.socket_idname = 'NodeSocketFloat'
    reroute_049 = nodes.new("NodeReroute")
    reroute_049.location = (-681.8, -769.4)
    reroute_049.socket_idname = 'NodeSocketVector'

    # === 节点连接 ===
    links.new(mix_shader_001.outputs[0], mix_shader.inputs[1])
    links.new(group_037.outputs[0], map_range_001.inputs[0])
    links.new(group_031.outputs[0], color_ramp_001.inputs[0])
    links.new(reroute_030.outputs[0], mix_005.inputs[0])
    links.new(reroute_046.outputs[0], mix_shader_001.inputs[0])
    links.new(reroute_029.outputs[0], mix_005.inputs[6])
    links.new(group_033.outputs[0], color_ramp_002.inputs[0])
    links.new(reroute_020.outputs[0], principled_bsdf_002.inputs[5])
    links.new(reroute_004.outputs[0], mix_006.inputs[0])
    links.new(reroute_019.outputs[0], principled_bsdf.inputs[5])
    links.new(color_ramp.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_001.outputs[0], mix_006.inputs[6])
    links.new(group_038.outputs[0], color_ramp.inputs[0])
    links.new(principled_bsdf_002.outputs[0], mix_shader_001.inputs[2])
    links.new(reroute_006.outputs[0], bump_001.inputs[3])
    links.new(reroute_014.outputs[0], mix_004.inputs[7])
    links.new(reroute_040.outputs[0], bump_001.inputs[4])
    links.new(reroute_010.outputs[0], hue_saturation_value_001.inputs[4])
    links.new(reroute_003.outputs[0], mix_004.inputs[0])
    links.new(reroute_013.outputs[0], mix_004.inputs[6])
    links.new(reroute_016.outputs[0], mix_001.inputs[0])
    links.new(principled_bsdf.outputs[0], mix_shader_001.inputs[1])
    links.new(reroute.outputs[0], hue_saturation_value.inputs[4])
    links.new(reroute_027.outputs[0], mix_003.inputs[7])
    links.new(reroute_052.outputs[0], principled_bsdf_002.inputs[0])
    links.new(reroute_049.outputs[0], bump.inputs[4])
    links.new(reroute_026.outputs[0], mix_003.inputs[6])
    links.new(reroute_024.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_007.outputs[0], principled_bsdf_001.inputs[0])
    links.new(bump_001.outputs[0], principled_bsdf_001.inputs[5])
    links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[2])
    links.new(reroute_039.outputs[0], reroute_002.inputs[0])
    links.new(color_ramp_002.outputs[0], reroute_004.inputs[0])
    links.new(reroute_008.outputs[0], reroute_006.inputs[0])
    links.new(mix.outputs[2], reroute_007.inputs[0])
    links.new(reroute_005.outputs[0], reroute_008.inputs[0])
    links.new(reroute_008.outputs[0], mix_shader.inputs[0])
    links.new(bump.outputs[0], reroute_009.inputs[0])
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_010.inputs[0])
    links.new(reroute_004.outputs[0], reroute_012.inputs[0])
    links.new(reroute_015.outputs[0], reroute_003.inputs[0])
    links.new(mix_003.outputs[2], reroute_013.inputs[0])
    links.new(hue_saturation_value_001.outputs[0], reroute_014.inputs[0])
    links.new(map_range_003.outputs[0], reroute_017.inputs[0])
    links.new(reroute_017.outputs[0], reroute_016.inputs[0])
    links.new(mix_005.outputs[2], reroute_018.inputs[0])
    links.new(bump_002.outputs[0], reroute_020.inputs[0])
    links.new(reroute_020.outputs[0], reroute_019.inputs[0])
    links.new(reroute_022.outputs[0], group_037.inputs[0])
    links.new(map_range_005.outputs[0], group_038.inputs[0])
    links.new(input_node.outputs[10], map_range_005.inputs[0])
    links.new(input_node.outputs[8], map_range_004.inputs[0])
    links.new(map_range_004.outputs[0], reroute_021.inputs[0])
    links.new(reroute_023.outputs[0], reroute_022.inputs[0])
    links.new(reroute_021.outputs[0], reroute_023.inputs[0])
    links.new(map_range_006.outputs[0], group_033.inputs[0])
    links.new(input_node.outputs[3], map_range_006.inputs[0])
    links.new(mix_006.outputs[2], reroute_026.inputs[0])
    links.new(hue_saturation_value.outputs[0], reroute_027.inputs[0])
    links.new(color_ramp_001.outputs[0], reroute_028.inputs[0])
    links.new(mix_004.outputs[2], reroute_029.inputs[0])
    links.new(reroute_028.outputs[0], reroute_030.inputs[0])
    links.new(reroute_031.outputs[0], math_002.inputs[0])
    links.new(input_node.outputs[9], map_range_007.inputs[0])
    links.new(reroute_034.outputs[0], reroute_031.inputs[0])
    links.new(reroute_031.outputs[0], reroute_032.inputs[0])
    links.new(map_range_001.outputs[0], reroute_033.inputs[0])
    links.new(map_range_007.outputs[0], reroute_034.inputs[0])
    links.new(map_range.outputs[0], reroute_035.inputs[0])
    links.new(input_node.outputs[7], reroute.inputs[0])
    links.new(reroute_021.outputs[0], map_range_008.inputs[0])
    links.new(map_range_008.outputs[0], group_031.inputs[0])
    links.new(reroute_038.outputs[0], math_001.inputs[0])
    links.new(reroute_044.outputs[0], map_range_009.inputs[0])
    links.new(map_range_010.outputs[0], reroute_036.inputs[0])
    links.new(reroute_036.outputs[0], reroute_037.inputs[0])
    links.new(reroute_036.outputs[0], reroute_038.inputs[0])
    links.new(input_node.outputs[5], map_range_010.inputs[0])
    links.new(input_node.outputs[4], map_range_011.inputs[0])
    links.new(color_ramp_003.outputs[0], bump_002.inputs[3])
    links.new(reroute_042.outputs[0], color_ramp_003.inputs[0])
    links.new(reroute_041.outputs[0], bump_002.inputs[4])
    links.new(reroute_009.outputs[0], reroute_039.inputs[0])
    links.new(reroute_002.outputs[0], reroute_040.inputs[0])
    links.new(reroute_039.outputs[0], reroute_041.inputs[0])
    links.new(reroute_011.outputs[0], reroute_042.inputs[0])
    links.new(mix_001.outputs[2], reroute_043.inputs[0])
    links.new(reroute_045.outputs[0], map_range_012.inputs[0])
    links.new(input_node.outputs[6], reroute_044.inputs[0])
    links.new(reroute_044.outputs[0], reroute_045.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(reroute_035.outputs[0], all_edges_014.inputs[1])
    links.new(all_edges_014.outputs[0], reroute_015.inputs[0])
    links.new(math_002.outputs[0], all_edges_014.inputs[0])
    links.new(all_edges_015.outputs[0], reroute_005.inputs[0])
    links.new(map_range_002.outputs[0], all_edges_015.inputs[1])
    links.new(reroute_037.outputs[0], all_edges_015.inputs[0])
    links.new(all_edges_016.outputs[0], mix.inputs[0])
    links.new(map_range_002.outputs[0], all_edges_016.inputs[1])
    links.new(math_001.outputs[0], all_edges_016.inputs[0])
    links.new(reroute_017.outputs[0], all_edges_017.inputs[1])
    links.new(map_range_009.outputs[0], all_edges_017.inputs[0])
    links.new(all_edges_017.outputs[0], reroute_011.inputs[0])
    links.new(reroute_033.outputs[0], cavity_012.inputs[1])
    links.new(cavity_012.outputs[0], mix_003.inputs[0])
    links.new(reroute_032.outputs[0], cavity_012.inputs[0])
    links.new(group_030.outputs[0], map_range.inputs[0])
    links.new(reroute_023.outputs[0], group_030.inputs[0])
    links.new(group_032.outputs[0], map_range_002.inputs[0])
    links.new(map_range_011.outputs[0], group_032.inputs[0])
    links.new(group_034.outputs[0], map_range_003.inputs[0])
    links.new(map_range_012.outputs[0], group_034.inputs[0])
    links.new(map_range_013.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[0], map_range_013.inputs[0])
    links.new(reroute_018.outputs[0], reroute_024.inputs[0])
    links.new(reroute_048.outputs[0], bump_002.inputs[0])
    links.new(reroute_012.outputs[0], reroute_025.inputs[0])
    links.new(reroute_025.outputs[0], bump.inputs[3])
    links.new(reroute_047.outputs[0], reroute_046.inputs[0])
    links.new(reroute_011.outputs[0], reroute_047.inputs[0])
    links.new(reroute_050.outputs[0], reroute_048.inputs[0])
    links.new(reroute_053.outputs[0], bump_001.inputs[0])
    links.new(reroute_050.outputs[0], reroute_051.inputs[0])
    links.new(reroute_043.outputs[0], reroute_052.inputs[0])
    links.new(reroute_051.outputs[0], reroute_053.inputs[0])
    links.new(reroute_055.outputs[0], bump.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_055.inputs[0])
    links.new(reroute_055.outputs[0], reroute_050.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control.inputs[1])
    links.new(bevel.outputs[0], reroute_049.inputs[0])

    return group