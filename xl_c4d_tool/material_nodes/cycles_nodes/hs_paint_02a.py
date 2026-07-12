import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_09_r import pf_grunge_09_r
from .pf_grunge_14_r import pf_grunge_14_r as _pf_grunge_14_r_fn
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_22e_r import pf_grunge_22e_r


def hs_paint_02a():
    """BL_油漆02 - 中度磨损油漆材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/底色混合"""
    group_name = "BL_油漆02"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_次扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_额外细节", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_额外扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.1878, 0.1500, 0.1046, 1.0000)
    group.interface.new_socket(name="油漆细节_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆细节2_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="顶部落尘_开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="顶部落尘_反转", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="顶部落尘_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="顶部落尘_颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0908, 0.0844, 0.0595, 1.0000)
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "污垢: 表面污垢和脏旧效果")
    frame_002 = create_frame(nodes, "Frame.002", "粗糙度: 表面粗糙度控制")
    frame_003 = create_frame(nodes, "Frame.003", "油漆凹凸: 油漆表层的凹凸纹理")
    frame_004 = create_frame(nodes, "Frame.004", "自上而下灰尘: 模拟从上方积累的灰尘效果")
    frame_001 = create_frame(nodes, "Frame.001", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_005 = create_frame(nodes, "Frame.005", "脏污: 基于AO的凹腔和表面脏污效果遮罩")
    frame_006 = create_frame(nodes, "Frame.006", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (1445.3, -263.0)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 1.0
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
    colorramp_029 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_029 | ColorRamp.029
    colorramp_029.color_ramp.color_mode = 'RGB'
    colorramp_029.color_ramp.hue_interpolation = 'NEAR'
    colorramp_029.color_ramp.interpolation = 'B_SPLINE'
    while len(colorramp_029.color_ramp.elements) > 2:
        colorramp_029.color_ramp.elements.remove(colorramp_029.color_ramp.elements[-1])
    while len(colorramp_029.color_ramp.elements) < 2:
        colorramp_029.color_ramp.elements.new(0.5)
    colorramp_029.color_ramp.elements[0].position = 0.19836576282978058
    colorramp_029.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_029.color_ramp.elements[1].position = 0.45015063881874084
    colorramp_029.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_029
    colorramp_029.location = (850.6, -135.7)
    label_node(colorramp_029, "", frame_002)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (574.2, -191.4)
    label_node(group_034, "", frame_002)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = _pf_grunge_14_r_fn()
    mix = nodes.new("ShaderNodeMix")
    mix.location = (-956.3, -940.9)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[7].default_value = (0.0292, 0.0154, 0.0076, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_030 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_030 | ColorRamp.030
    colorramp_030.color_ramp.color_mode = 'RGB'
    colorramp_030.color_ramp.hue_interpolation = 'NEAR'
    colorramp_030.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_030.color_ramp.elements) > 2:
        colorramp_030.color_ramp.elements.remove(colorramp_030.color_ramp.elements[-1])
    while len(colorramp_030.color_ramp.elements) < 2:
        colorramp_030.color_ramp.elements.new(0.5)
    colorramp_030.color_ramp.elements[0].position = 0.41970592737197876
    colorramp_030.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_030.color_ramp.elements[1].position = 0.5927630662918091
    colorramp_030.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_030
    colorramp_030.location = (1400.4, -362.0)
    label_node(colorramp_030, "", frame_005)
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (596.8, -510.8)
    label_node(group_035, "", frame_005)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = _pf_grunge_14_r_fn()
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1435.1, -161.3)
    label_node(bump, "", frame_003)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    colorramp_031 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_031 | ColorRamp.031
    colorramp_031.color_ramp.color_mode = 'RGB'
    colorramp_031.color_ramp.hue_interpolation = 'NEAR'
    colorramp_031.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_031.color_ramp.elements) > 2:
        colorramp_031.color_ramp.elements.remove(colorramp_031.color_ramp.elements[-1])
    while len(colorramp_031.color_ramp.elements) < 2:
        colorramp_031.color_ramp.elements.new(0.5)
    colorramp_031.color_ramp.elements[0].position = 0.16709673404693604
    colorramp_031.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_031.color_ramp.elements[1].position = 0.5272730588912964
    colorramp_031.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_031
    colorramp_031.location = (755.5, -276.0)
    label_node(colorramp_031, "", frame_003)
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (469.3, -276.0)
    label_node(group_036, "", frame_003)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = _pf_grunge_14_r_fn()
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (2070.0, -630.2)
    label_node(mix_001, "", frame_001)
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
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1356.6, -658.5)
    label_node(all_edges_013, "", frame_001)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 1.0
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (664.9, -928.4)
    label_node(group_029, "", frame_001)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = _pf_grunge_14_r_fn()
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.305795282125473
    color_ramp_001.color_ramp.elements[0].color = (0.006021315231919289, 0.006021315231919289, 0.006021315231919289, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 1.0
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (906.9, -928.4)
    label_node(color_ramp_001, "", frame_001)
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (1433.2, -1008.0)
    label_node(hue_saturation_value, "", frame_001)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 1.190000057220459
    hue_saturation_value.inputs[2].default_value = 0.7400000095367432
    hue_saturation_value.inputs[3].default_value = 1.0
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (1436.2, -186.0)
    label_node(mix_002, "", frame)
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[7].default_value = (0.0235, 0.0250, 0.0324, 1.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (848.8, -249.5)
    label_node(group_037, "", frame)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_09_r()
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (1122.1, -250.4)
    label_node(map_range, "", frame)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[4].default_value = 0.75
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (-422.2, -684.5)
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_003.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    cavity_018 = nodes.new("ShaderNodeGroup")
    cavity_018.location = (1111.2, -101.7)
    label_node(cavity_018, "", frame_005)
    cavity_018.xl_c4d_gradient_type = '0'
    cavity_018.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_018.node_tree = cavity()
    cavity_018.inputs[0].default_value = 0.75
    cavity_018.inputs[2].default_value = 1.0
    group_042 = nodes.new("ShaderNodeGroup")
    group_042.location = (595.0, -263.5)
    label_node(group_042, "", frame_005)
    group_042.xl_c4d_gradient_type = '0'
    group_042.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_042.node_tree = pf_grunge_15_r()
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (878.1, -166.8)
    label_node(map_range_008, "", frame_005)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 1.0
    map_range_008.inputs[3].default_value = -0.1599997729063034
    map_range_008.inputs[4].default_value = 1.0
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    cavity_019 = nodes.new("ShaderNodeGroup")
    cavity_019.location = (1109.5, -293.7)
    label_node(cavity_019, "", frame_005)
    cavity_019.xl_c4d_gradient_type = '0'
    cavity_019.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_019.node_tree = cavity()
    cavity_019.inputs[0].default_value = 0.9300001263618469
    cavity_019.inputs[2].default_value = 2.1100001335144043
    colorramp_032 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_032 | ColorRamp.032
    colorramp_032.color_ramp.color_mode = 'RGB'
    colorramp_032.color_ramp.hue_interpolation = 'NEAR'
    colorramp_032.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_032.color_ramp.elements) > 2:
        colorramp_032.color_ramp.elements.remove(colorramp_032.color_ramp.elements[-1])
    while len(colorramp_032.color_ramp.elements) < 2:
        colorramp_032.color_ramp.elements.new(0.5)
    colorramp_032.color_ramp.elements[0].position = 0.1304452121257782
    colorramp_032.color_ramp.elements[0].color = (0.18268588185310364, 0.16374391317367554, 0.13297931849956512, 1.0)
    colorramp_032.color_ramp.elements[1].position = 0.525680422782898
    colorramp_032.color_ramp.elements[1].color = (0.030013352632522583, 0.014034532010555267, 0.008308978751301765, 1.0)
    # XL_PF_RAMP_END colorramp_032
    colorramp_032.location = (1400.4, -142.2)
    label_node(colorramp_032, "", frame_005)
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (2534.5, -462.5)
    label_node(mix_004, "", frame_001)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (1356.6, -507.1)
    label_node(all_edges_014, "", frame_001)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 1.0
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (667.8, -419.6)
    label_node(group_030, "", frame_001)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = _pf_grunge_14_r_fn()
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.3545455038547516
    color_ramp_002.color_ramp.elements[0].color = (7.25172576494515e-05, 7.25172576494515e-05, 7.25172576494515e-05, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.5500001907348633
    color_ramp_002.color_ramp.elements[1].color = (0.606155276298523, 0.606155276298523, 0.606155276298523, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (909.8, -419.6)
    label_node(color_ramp_002, "", frame_001)
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (2259.6, -232.7)
    label_node(mix_005, "", frame_001)
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    mix_005.blend_type = 'MIX'
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    mix_005.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_005.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[7].default_value = (0.1546, 0.0520, 0.0185, 1.0000)
    mix_005.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    all_edges_015 = nodes.new("ShaderNodeGroup")
    all_edges_015.location = (1358.1, -354.5)
    label_node(all_edges_015, "", frame_001)
    all_edges_015.xl_c4d_gradient_type = '0'
    all_edges_015.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_015.node_tree = all_edges()
    all_edges_015.inputs[2].default_value = 1.0
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (82.4, -2630.7)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (2391.4, -318.4)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[0].default_value = (0.0630, 0.0212, 0.0065, 1.0000)
    principled_bsdf_002.inputs[2].default_value = 0.800000011920929
    principled_bsdf_002.inputs[3].default_value = 1.5
    principled_bsdf_002.inputs[4].default_value = 1.0
    principled_bsdf_002.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_002.inputs[11].default_value = 1.399999976158142
    principled_bsdf_002.inputs[13].default_value = 1.0
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
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (3079.6, -205.4)
    all_edges_018 = nodes.new("ShaderNodeGroup")
    all_edges_018.location = (1009.4, -104.2)
    label_node(all_edges_018, "", frame_006)
    all_edges_018.xl_c4d_gradient_type = '0'
    all_edges_018.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_018.node_tree = all_edges()
    all_edges_018.inputs[2].default_value = 1.0
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (502.5, -349.0)
    label_node(group_032, "", frame_006)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = pf_grunge_22e_r()
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (810.0, -345.5)
    label_node(map_range_002, "", frame_006)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 1.0
    map_range_002.inputs[3].default_value = -0.550000011920929
    map_range_002.inputs[4].default_value = 1.0700000524520874
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    separate_xyz = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (435.5, -291.8)
    label_node(separate_xyz, "", frame_004)
    mapping_001 = nodes.new("ShaderNodeMapping")
    mapping_001.location = (218.4, -144.8)
    label_node(mapping_001, "", frame_004)
    mapping_001.vector_type = 'POINT'
    mapping_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (29.8, -144.8)
    label_node(texture_coordinate_001, "", frame_004)
    texture_coordinate_001.from_instancer = False
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 3:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.10574017465114594
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.23262839019298553
    color_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[2].position = 0.5196374654769897
    color_ramp.color_ramp.elements[2].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (612.9, -184.5)
    label_node(color_ramp, "", frame_004)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (2119.2, -441.6)
    bump_001.invert = False
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    reroute = nodes.new("NodeReroute")
    reroute.location = (1206.8, -1149.7)
    label_node(reroute, "", frame_001)
    reroute.socket_idname = 'NodeSocketColor'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1579.9, -811.5)
    label_node(reroute_001, "", frame_001)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1939.2, -615.5)
    label_node(reroute_002, "", frame_001)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1318.0, -605.6)
    label_node(reroute_004, "", frame_001)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1674.9, -1041.3)
    label_node(reroute_005, "", frame_001)
    reroute_005.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (1649.4, -690.2)
    label_node(reroute_006, "", frame_001)
    reroute_006.socket_idname = 'NodeSocketFloat'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (1318.0, -452.7)
    label_node(reroute_007, "", frame_001)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1283.8, -755.9)
    label_node(reroute_003, "", frame_001)
    reroute_003.socket_idname = 'NodeSocketColor'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (1784.7, -45.5)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1298.1, -2664.8)
    reroute_013.socket_idname = 'NodeSocketVector'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (2715.0, -302.6)
    reroute_014.socket_idname = 'NodeSocketShader'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (2359.6, -45.5)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (2711.5, -264.5)
    reroute_016.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (2070.0, -636.6)
    label_node(reroute_017, "", frame_001)
    reroute_017.socket_idname = 'NodeSocketColor'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (2454.1, -658.4)
    label_node(reroute_018, "", frame_001)
    reroute_018.socket_idname = 'NodeSocketColor'
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (-136.9, -2678.1)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[4].default_value = 0.009999999776482582
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (317.9, -176.5)
    label_node(map_range_003, "", frame_005)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.10000000149011612
    map_range_003.inputs[4].default_value = 0.5600000023841858
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (315.4, -419.9)
    label_node(map_range_004, "", frame_005)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.10000000149011612
    map_range_004.inputs[4].default_value = 0.550000011920929
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (402.6, -415.4)
    label_node(map_range_005, "", frame_001)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.02500000037252903
    map_range_005.inputs[4].default_value = 0.8700000047683716
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (402.6, -927.2)
    label_node(map_range_006, "", frame_001)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.029999999329447746
    map_range_006.inputs[4].default_value = 1.25
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (909.8, -160.8)
    label_node(map_range_007, "", frame_001)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.009999999776482582
    map_range_007.inputs[4].default_value = 1.0
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (1356.6, -204.3)
    label_node(math_001, "", frame_001)
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 2.0
    math_001.inputs[2].default_value = 0.5
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (1283.8, -307.8)
    label_node(reroute_008, "", frame_001)
    reroute_008.socket_idname = 'NodeSocketFloat'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (1283.8, -584.3)
    label_node(reroute_009, "", frame_001)
    reroute_009.socket_idname = 'NodeSocketFloat'
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (910.6, -662.9)
    label_node(map_range_009, "", frame_001)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[3].default_value = 0.009999999776482582
    map_range_009.inputs[4].default_value = 1.3600000143051147
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (1283.8, -736.1)
    label_node(reroute_010, "", frame_001)
    reroute_010.socket_idname = 'NodeSocketFloat'
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (462.6, -1396.9)
    math_002.operation = 'MAXIMUM'
    math_002.use_clamp = False
    math_002.inputs[2].default_value = 0.5
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (-23.0, -1396.9)
    math_003.operation = 'MAXIMUM'
    math_003.use_clamp = False
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (-397.9, -1396.9)
    math_004.operation = 'MAXIMUM'
    math_004.use_clamp = False
    math_004.inputs[2].default_value = 0.5
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (1649.4, -389.6)
    label_node(reroute_019, "", frame_001)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (1928.8, -107.0)
    label_node(reroute_020, "", frame_001)
    reroute_020.socket_idname = 'NodeSocketFloat'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (2052.0, -126.1)
    label_node(reroute_021, "", frame_001)
    reroute_021.socket_idname = 'NodeSocketFloat'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (2228.4, -149.9)
    label_node(reroute_022, "", frame_001)
    reroute_022.socket_idname = 'NodeSocketFloat'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (-83.0, -1546.4)
    reroute_023.socket_idname = 'NodeSocketFloat'
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (379.9, -102.2)
    label_node(map_range_010, "", frame)
    map_range_010.clamp = False
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[3].default_value = 0.03999999910593033
    map_range_010.inputs[4].default_value = 0.3199999928474426
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (846.7, -415.9)
    label_node(map_range_011, "", frame)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = -0.699999988079071
    map_range_011.inputs[4].default_value = -0.5099999308586121
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (329.7, -551.1)
    label_node(reroute_024, "", frame)
    reroute_024.socket_idname = 'NodeSocketFloatPercentage'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (329.7, -207.4)
    label_node(reroute_025, "", frame)
    reroute_025.socket_idname = 'NodeSocketFloatPercentage'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (-138.3, -718.2)
    reroute_026.socket_idname = 'NodeSocketColor'
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (670.2, -363.8)
    label_node(vector_math, "", frame)
    vector_math.operation = 'SCALE'
    vector_math.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[3].default_value = 0.009999999776482582
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (321.2, -348.5)
    label_node(map_range_012, "", frame_006)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.10000000149011612
    map_range_012.inputs[4].default_value = 0.3400000333786011
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (810.0, -101.7)
    label_node(map_range_013, "", frame_006)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = 0.10000000149011612
    map_range_013.inputs[4].default_value = 0.75
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-585.8, -858.9)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (1057.5, -45.5)
    reroute_027.socket_idname = 'NodeSocketFloat'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (444.1, -315.8)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (1117.4, -357.0)
    reroute_029.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (1303.4, -418.0)
    reroute_030.socket_idname = 'NodeSocketVector'
    mix_shader_002 = nodes.new("ShaderNodeMixShader")
    mix_shader_002.location = (3928.2, -203.1)
    principled_bsdf_003 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_003.location = (2986.5, -337.6)
    principled_bsdf_003.distribution = 'MULTI_GGX'
    principled_bsdf_003.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_003.inputs[2].default_value = 0.8999999761581421
    principled_bsdf_003.inputs[3].default_value = 1.5
    principled_bsdf_003.inputs[4].default_value = 1.0
    principled_bsdf_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_003.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_003.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_003.inputs[11].default_value = 1.399999976158142
    principled_bsdf_003.inputs[13].default_value = 1.0
    principled_bsdf_003.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_003.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_003.inputs[20].default_value = 0.029999999329447746
    principled_bsdf_003.inputs[21].default_value = 1.5
    principled_bsdf_003.inputs[22].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_003.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_003.inputs[25].default_value = 0.5
    principled_bsdf_003.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_003.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf_003.inputs[30].default_value = 1.3300000429153442
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (3347.3, -302.3)
    reroute_031.socket_idname = 'NodeSocketShader'
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (3347.3, -281.0)
    reroute_033.socket_idname = 'NodeSocketShader'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (3794.9, -261.7)
    reroute_034.socket_idname = 'NodeSocketFloat'
    math = nodes.new("ShaderNodeMath")
    math.location = (1331.9, -107.2)
    label_node(math, "", frame_004)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[1].default_value = 2.0
    math.inputs[2].default_value = 0.5
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (1792.3, -106.6)
    label_node(math_005, "", frame_004)
    math_005.operation = 'SUBTRACT'
    math_005.use_clamp = True
    math_005.inputs[2].default_value = 0.5
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.11782477796077728
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.4592146575450897
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (1982.1, -102.2)
    label_node(color_ramp_003, "", frame_004)
    pf_grunge_14_r = nodes.new("ShaderNodeGroup")
    pf_grunge_14_r.location = (1331.7, -271.5)
    label_node(pf_grunge_14_r, "", frame_004)
    pf_grunge_14_r.xl_c4d_gradient_type = '0'
    pf_grunge_14_r.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    pf_grunge_14_r.node_tree = _pf_grunge_14_r_fn()
    map_range_014 = nodes.new("ShaderNodeMapRange")
    map_range_014.location = (1508.5, -265.3)
    label_node(map_range_014, "", frame_004)
    map_range_014.clamp = True
    map_range_014.interpolation_type = 'LINEAR'
    map_range_014.data_type = 'FLOAT'
    map_range_014.inputs[2].default_value = 1.0
    map_range_014.inputs[3].default_value = 2.259999990463257
    map_range_014.inputs[4].default_value = 0.7200000286102295
    map_range_014.inputs[5].default_value = 4.0
    map_range_014.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_015 = nodes.new("ShaderNodeMapRange")
    map_range_015.location = (1160.3, -266.8)
    label_node(map_range_015, "", frame_004)
    map_range_015.clamp = True
    map_range_015.interpolation_type = 'LINEAR'
    map_range_015.data_type = 'FLOAT'
    map_range_015.inputs[2].default_value = 100.0
    map_range_015.inputs[3].default_value = 0.07400000095367432
    map_range_015.inputs[4].default_value = 0.30000001192092896
    map_range_015.inputs[5].default_value = 4.0
    map_range_015.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (1724.9, -140.4)
    label_node(reroute_032, "", frame_004)
    reroute_032.socket_idname = 'NodeSocketFloat'
    math_006 = nodes.new("ShaderNodeMath")
    math_006.location = (2283.9, -197.0)
    label_node(math_006, "", frame_004)
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False
    math_006.inputs[2].default_value = 0.5
    math_007 = nodes.new("ShaderNodeMath")
    math_007.location = (1162.9, -106.7)
    label_node(math_007, "", frame_004)
    math_007.operation = 'SUBTRACT'
    math_007.use_clamp = True
    math_007.inputs[0].default_value = 1.0
    math_007.inputs[2].default_value = 0.5
    invert_color = nodes.new("ShaderNodeInvert")
    invert_color.location = (889.3, -139.2)
    label_node(invert_color, "", frame_004)
    map_range_016 = nodes.new("ShaderNodeMapRange")
    map_range_016.location = (374.2, -102.3)
    label_node(map_range_016, "", frame_002)
    map_range_016.clamp = True
    map_range_016.interpolation_type = 'LINEAR'
    map_range_016.data_type = 'FLOAT'
    map_range_016.inputs[2].default_value = 100.0
    map_range_016.inputs[3].default_value = 0.10000000149011612
    map_range_016.inputs[4].default_value = 0.7400000095367432
    map_range_016.inputs[5].default_value = 4.0
    map_range_016.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_017 = nodes.new("ShaderNodeMapRange")
    map_range_017.location = (261.6, -276.0)
    label_node(map_range_017, "", frame_003)
    map_range_017.clamp = True
    map_range_017.interpolation_type = 'LINEAR'
    map_range_017.data_type = 'FLOAT'
    map_range_017.inputs[2].default_value = 100.0
    map_range_017.inputs[3].default_value = 0.10000000149011612
    map_range_017.inputs[4].default_value = 1.0
    map_range_017.inputs[5].default_value = 4.0
    map_range_017.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (495.9, -2664.6)
    reroute_035.socket_idname = 'NodeSocketVector'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1683.5, -809.1)
    label_node(reroute_036, "", frame_001)
    reroute_036.socket_idname = 'NodeSocketColor'
    hue_saturation_value_001 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_001.location = (2070.0, -417.5)
    label_node(hue_saturation_value_001, "", frame_001)
    hue_saturation_value_001.inputs[0].default_value = 0.5
    hue_saturation_value_001.inputs[1].default_value = 0.8400000333786011
    hue_saturation_value_001.inputs[2].default_value = 1.7899999618530273
    hue_saturation_value_001.inputs[3].default_value = 1.0
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (1935.6, -825.9)
    label_node(reroute_037, "", frame_001)
    reroute_037.socket_idname = 'NodeSocketColor'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1067.6, -101.9)
    label_node(hs_bump_control, "", frame_003)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (1326.7, -132.6)
    label_node(reroute_038, "", frame_003)
    reroute_038.socket_idname = 'NodeSocketFloat'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (1281.2, -2219.9)
    reroute_039.socket_idname = 'NodeSocketFloat'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (1920.8, -522.0)
    reroute_040.socket_idname = 'NodeSocketFloat'
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (2044.2, -584.7)
    reroute_041.socket_idname = 'NodeSocketFloat'
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (2042.6, -605.0)
    reroute_042.socket_idname = 'NodeSocketVector'

    # === 节点连接 ===
    links.new(group_037.outputs[0], map_range.inputs[0])
    links.new(reroute_012.outputs[0], mix_003.inputs[6])
    links.new(reroute_036.outputs[0], mix_001.inputs[6])
    links.new(group_032.outputs[0], map_range_002.inputs[0])
    links.new(reroute_035.outputs[0], bump.inputs[4])
    links.new(colorramp_030.outputs[0], mix.inputs[0])
    links.new(reroute_026.outputs[0], mix_002.inputs[6])
    links.new(separate_xyz.outputs[2], color_ramp.inputs[0])
    links.new(reroute_014.outputs[0], mix_shader_001.inputs[2])
    links.new(colorramp_032.outputs[0], mix_003.inputs[7])
    links.new(reroute_016.outputs[0], mix_shader_001.inputs[0])
    links.new(group_042.outputs[0], map_range_008.inputs[0])
    links.new(reroute.outputs[0], hue_saturation_value.inputs[4])
    links.new(mix_004.outputs[2], mix.inputs[6])
    links.new(reroute_019.outputs[0], mix_005.inputs[0])
    links.new(bump_001.outputs[0], principled_bsdf_002.inputs[5])
    links.new(reroute_028.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_041.outputs[0], bump_001.inputs[3])
    links.new(reroute_037.outputs[0], mix_001.inputs[7])
    links.new(reroute_042.outputs[0], bump_001.inputs[4])
    links.new(reroute_017.outputs[0], mix_004.inputs[6])
    links.new(reroute_006.outputs[0], mix_001.inputs[0])
    links.new(map_range.outputs[0], mix_002.inputs[0])
    links.new(reroute_002.outputs[0], mix_004.inputs[0])
    links.new(reroute_018.outputs[0], mix_004.inputs[7])
    links.new(texture_coordinate_001.outputs[1], mapping_001.inputs[0])
    links.new(mapping_001.outputs[0], separate_xyz.inputs[0])
    links.new(reroute_030.outputs[0], principled_bsdf.inputs[5])
    links.new(mix_shader_002.outputs[0], output_node.inputs[0])
    links.new(principled_bsdf.outputs[0], mix_shader_001.inputs[1])
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute_007.outputs[0], reroute_004.inputs[0])
    links.new(hue_saturation_value.outputs[0], reroute_005.inputs[0])
    links.new(color_ramp_002.outputs[0], reroute_007.inputs[0])
    links.new(color_ramp_001.outputs[0], reroute_003.inputs[0])
    links.new(reroute_027.outputs[0], reroute_011.inputs[0])
    links.new(reroute_035.outputs[0], reroute_013.inputs[0])
    links.new(principled_bsdf_002.outputs[0], reroute_014.inputs[0])
    links.new(reroute_011.outputs[0], reroute_015.inputs[0])
    links.new(reroute_015.outputs[0], reroute_016.inputs[0])
    links.new(mix_001.outputs[2], reroute_017.inputs[0])
    links.new(mix_005.outputs[2], reroute_018.inputs[0])
    links.new(input_node.outputs[10], reroute.inputs[0])
    links.new(map_range_003.outputs[0], group_042.inputs[0])
    links.new(input_node.outputs[4], map_range_003.inputs[0])
    links.new(input_node.outputs[12], map_range_004.inputs[0])
    links.new(input_node.outputs[5], map_range_006.inputs[0])
    links.new(input_node.outputs[5], map_range_005.inputs[0])
    links.new(reroute_008.outputs[0], math_001.inputs[0])
    links.new(map_range_007.outputs[0], reroute_008.inputs[0])
    links.new(reroute_008.outputs[0], reroute_009.inputs[0])
    links.new(input_node.outputs[6], map_range_007.inputs[0])
    links.new(input_node.outputs[7], map_range_009.inputs[0])
    links.new(map_range_009.outputs[0], reroute_010.inputs[0])
    links.new(colorramp_029.outputs[0], math_002.inputs[1])
    links.new(math_003.outputs[0], math_002.inputs[0])
    links.new(reroute_020.outputs[0], math_004.inputs[0])
    links.new(reroute_021.outputs[0], math_004.inputs[1])
    links.new(math_004.outputs[0], math_003.inputs[0])
    links.new(reroute_023.outputs[0], math_003.inputs[1])
    links.new(reroute_019.outputs[0], reroute_020.inputs[0])
    links.new(reroute_006.outputs[0], reroute_022.inputs[0])
    links.new(reroute_022.outputs[0], reroute_023.inputs[0])
    links.new(reroute_029.outputs[0], principled_bsdf.inputs[2])
    links.new(map_range_010.outputs[0], group_037.inputs[0])
    links.new(reroute_025.outputs[0], map_range_010.inputs[0])
    links.new(reroute_024.outputs[0], map_range_011.inputs[0])
    links.new(map_range_011.outputs[0], map_range.inputs[3])
    links.new(reroute_025.outputs[0], reroute_024.inputs[0])
    links.new(input_node.outputs[11], reroute_025.inputs[0])
    links.new(mix_003.outputs[2], reroute_026.inputs[0])
    links.new(vector_math.outputs[0], group_037.inputs[1])
    links.new(map_range_012.outputs[0], group_032.inputs[0])
    links.new(input_node.outputs[8], map_range_012.inputs[0])
    links.new(input_node.outputs[9], map_range_013.inputs[0])
    links.new(mix.outputs[2], reroute_012.inputs[0])
    links.new(mix_002.outputs[2], reroute_028.inputs[0])
    links.new(math_002.outputs[0], reroute_029.inputs[0])
    links.new(bump.outputs[0], reroute_030.inputs[0])
    links.new(reroute_033.outputs[0], mix_shader_002.inputs[1])
    links.new(reroute_031.outputs[0], mix_shader_002.inputs[2])
    links.new(reroute_034.outputs[0], mix_shader_002.inputs[0])
    links.new(principled_bsdf_003.outputs[0], reroute_031.inputs[0])
    links.new(mix_shader_001.outputs[0], reroute_033.inputs[0])
    links.new(math_006.outputs[0], reroute_034.inputs[0])
    links.new(reroute_032.outputs[0], math_005.inputs[0])
    links.new(math_005.outputs[0], color_ramp_003.inputs[0])
    links.new(map_range_014.outputs[0], math_005.inputs[1])
    links.new(input_node.outputs[16], map_range_015.inputs[0])
    links.new(input_node.outputs[17], principled_bsdf_003.inputs[0])
    links.new(math.outputs[0], reroute_032.inputs[0])
    links.new(color_ramp_003.outputs[0], math_006.inputs[0])
    links.new(input_node.outputs[14], math_006.inputs[1])
    links.new(math_007.outputs[0], math.inputs[0])
    links.new(input_node.outputs[15], invert_color.inputs[0])
    links.new(color_ramp.outputs[0], invert_color.inputs[1])
    links.new(invert_color.outputs[0], math_007.inputs[1])
    links.new(input_node.outputs[13], map_range_016.inputs[0])
    links.new(bevel.outputs[0], reroute_035.inputs[0])
    links.new(reroute_001.outputs[0], reroute_036.inputs[0])
    links.new(hue_saturation_value_001.outputs[0], mix_005.inputs[6])
    links.new(reroute_036.outputs[0], hue_saturation_value_001.inputs[4])
    links.new(reroute_005.outputs[0], reroute_037.inputs[0])
    links.new(reroute_003.outputs[0], all_edges_013.inputs[1])
    links.new(all_edges_013.outputs[0], reroute_006.inputs[0])
    links.new(reroute_010.outputs[0], all_edges_013.inputs[0])
    links.new(reroute_004.outputs[0], all_edges_014.inputs[1])
    links.new(all_edges_014.outputs[0], reroute_002.inputs[0])
    links.new(reroute_009.outputs[0], all_edges_014.inputs[0])
    links.new(all_edges_014.outputs[0], reroute_021.inputs[0])
    links.new(reroute_007.outputs[0], all_edges_015.inputs[1])
    links.new(math_001.outputs[0], all_edges_015.inputs[0])
    links.new(all_edges_015.outputs[0], reroute_019.inputs[0])
    links.new(map_range_002.outputs[0], all_edges_018.inputs[1])
    links.new(map_range_013.outputs[0], all_edges_018.inputs[0])
    links.new(all_edges_018.outputs[0], reroute_027.inputs[0])
    links.new(map_range_008.outputs[0], cavity_018.inputs[1])
    links.new(cavity_018.outputs[0], mix_003.inputs[0])
    links.new(map_range_008.outputs[0], cavity_019.inputs[1])
    links.new(cavity_019.outputs[0], colorramp_032.inputs[0])
    links.new(group_034.outputs[0], colorramp_029.inputs[0])
    links.new(group_035.outputs[0], colorramp_030.inputs[0])
    links.new(group_036.outputs[0], colorramp_031.inputs[0])
    links.new(group_029.outputs[0], color_ramp_001.inputs[0])
    links.new(group_030.outputs[0], color_ramp_002.inputs[0])
    links.new(pf_grunge_14_r.outputs[0], map_range_014.inputs[0])
    links.new(input_node.outputs[0], map_range_001.inputs[0])
    links.new(map_range_001.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[1])
    links.new(colorramp_031.outputs[0], bump.inputs[3])
    links.new(input_node.outputs[2], map_range_017.inputs[0])
    links.new(reroute_038.outputs[0], bump.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_038.inputs[0])
    links.new(reroute_040.outputs[0], bump_001.inputs[0])
    links.new(reroute_038.outputs[0], reroute_039.inputs[0])
    links.new(reroute_039.outputs[0], reroute_040.inputs[0])
    links.new(reroute_011.outputs[0], reroute_041.inputs[0])
    links.new(reroute_013.outputs[0], reroute_042.inputs[0])
    links.new(map_range_006.outputs[0], group_029.inputs[0])
    links.new(map_range_005.outputs[0], group_030.inputs[0])
    links.new(map_range_017.outputs[0], group_036.inputs[0])
    links.new(map_range_016.outputs[0], group_034.inputs[0])
    links.new(map_range_004.outputs[0], group_035.inputs[0])
    links.new(map_range_015.outputs[0], pf_grunge_14_r.inputs[0])

    return group