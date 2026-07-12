import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .nf_grunge_04_r import nf_grunge_04_r
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_19b_r import pf_grunge_19b_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_22d_r import pf_grunge_22d_r
from .white_splashes import white_splashes


def hs_metal_05a():
    """BL_金属05 - 白色锈蚀金属材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损/凹腔脏污"""
    group_name = "BL_金属05"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="油漆颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.2258, 0.2258, 0.2258, 1.0000)
    group.interface.new_socket(name="油漆细节", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    edges = create_frame(nodes, "边缘磨损: 基于倒角检测的边缘磨损效果遮罩", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩", (0.14, 0.14, 0.14))
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "油漆缩放滑块: 油漆纹理的缩放比例滑块")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (3271.4, -867.2)
    label_node(principled_bsdf, "", frame)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[1].default_value = 1.0
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.0  # 镜面IOR级别：与源资产一致(0.0)，不可留默认0.5
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
    colorramp_029.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_029.color_ramp.elements) > 2:
        colorramp_029.color_ramp.elements.remove(colorramp_029.color_ramp.elements[-1])
    while len(colorramp_029.color_ramp.elements) < 2:
        colorramp_029.color_ramp.elements.new(0.5)
    colorramp_029.color_ramp.elements[0].position = 0.0
    colorramp_029.color_ramp.elements[0].color = (0.4309120178222656, 0.4309120178222656, 0.4309120178222656, 1.0)
    colorramp_029.color_ramp.elements[1].position = 1.0
    colorramp_029.color_ramp.elements[1].color = (0.7627803683280945, 0.7627803683280945, 0.7627803683280945, 1.0)
    # XL_PF_RAMP_END colorramp_029
    colorramp_029.location = (1060.4, -1494.7)
    label_node(colorramp_029, "", frame)
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (780.5, -1645.4)
    label_node(group_032, "", frame)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = nf_grunge_04_r()
    colorramp_031 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_031 | ColorRamp.031
    colorramp_031.color_ramp.color_mode = 'RGB'
    colorramp_031.color_ramp.hue_interpolation = 'NEAR'
    colorramp_031.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_031.color_ramp.elements) > 2:
        colorramp_031.color_ramp.elements.remove(colorramp_031.color_ramp.elements[-1])
    while len(colorramp_031.color_ramp.elements) < 2:
        colorramp_031.color_ramp.elements.new(0.5)
    colorramp_031.color_ramp.elements[0].position = 0.15000002086162567
    colorramp_031.color_ramp.elements[0].color = (0.004154332913458347, 0.004154332913458347, 0.004154332913458347, 1.0)
    colorramp_031.color_ramp.elements[1].position = 0.34545445442199707
    colorramp_031.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_031
    colorramp_031.location = (1055.1, -1903.2)
    label_node(colorramp_031, "", frame)
    group_033 = nodes.new("ShaderNodeGroup")
    group_033.location = (780.5, -2052.4)
    label_node(group_033, "", frame)
    group_033.xl_c4d_gradient_type = '0'
    group_033.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_033.node_tree = pf_grunge_19_r()
    bump = nodes.new("ShaderNodeBump")
    bump.location = (2165.3, -1594.8)
    label_node(bump, "", frame)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 1.0
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (2458.9, -153.4)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[3].default_value = 1.5
    principled_bsdf_001.inputs[4].default_value = 1.0
    principled_bsdf_001.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_001.inputs[11].default_value = 1.399999976158142
    principled_bsdf_001.inputs[13].default_value = 0.2545454502105713
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
    all_edges_011 = nodes.new("ShaderNodeGroup")
    all_edges_011.location = (1527.1, -102.0)
    label_node(all_edges_011, "", edges)
    all_edges_011.xl_c4d_gradient_type = '0'
    all_edges_011.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_011.node_tree = all_edges()
    all_edges_011.inputs[2].default_value = 2.0
    group_028 = nodes.new("ShaderNodeGroup")
    group_028.location = (955.4, -321.6)
    label_node(group_028, "", edges)
    group_028.xl_c4d_gradient_type = '0'
    group_028.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_028.node_tree = pf_grunge_19b_r()
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (3204.2, 300.8)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (1913.7, -546.6)
    bump_001.invert = True
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 1.0
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (1654.2, -2177.9)
    label_node(bevel, "", frame)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_040 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_040 | ColorRamp.040
    colorramp_040.color_ramp.color_mode = 'RGB'
    colorramp_040.color_ramp.hue_interpolation = 'NEAR'
    colorramp_040.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_040.color_ramp.elements) > 2:
        colorramp_040.color_ramp.elements.remove(colorramp_040.color_ramp.elements[-1])
    while len(colorramp_040.color_ramp.elements) < 2:
        colorramp_040.color_ramp.elements.new(0.5)
    colorramp_040.color_ramp.elements[0].position = 0.1727272868156433
    colorramp_040.color_ramp.elements[0].color = (0.010729137808084488, 0.010729137808084488, 0.010729137808084488, 1.0)
    colorramp_040.color_ramp.elements[1].position = 0.25909096002578735
    colorramp_040.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_040
    colorramp_040.location = (1052.1, -2140.4)
    label_node(colorramp_040, "", frame)
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (780.5, -2291.7)
    label_node(group_036, "", frame)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_22b_r()
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (1347.9, -1900.7)
    label_node(mix_006, "", frame)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[0].default_value = 0.36666661500930786
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    value_039 = nodes.new("ShaderNodeValue")
    value_039.location = (682.8, -524.7)
    label_node(value_039, "", frame)
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (1048.9, -423.0)
    label_node(group_037, "", frame)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_22d_r()
    group_037.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (2404.8, -566.6)
    label_node(mix_003, "", frame)
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
    mix = nodes.new("ShaderNodeMix")
    mix.location = (2053.0, -285.4)
    label_node(mix, "", edges)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[6].default_value = (0.0999, 0.0527, 0.0296, 1.0000)
    mix.inputs[7].default_value = (0.1263, 0.1263, 0.1263, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (1270.0, -384.3)
    label_node(map_range, "", edges)
    map_range.clamp = False
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[1].default_value = 0.34999996423721313
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (-502.5, -188.0)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[0].default_value = (0.0378, 0.0318, 0.0229, 1.0000)
    principled_bsdf_002.inputs[3].default_value = 1.5
    principled_bsdf_002.inputs[4].default_value = 1.0
    principled_bsdf_002.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_002.inputs[11].default_value = 1.399999976158142
    principled_bsdf_002.inputs[13].default_value = 0.2545454502105713
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
    mix_shader_001.location = (485.3, 254.9)
    colorramp_030 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_030 | ColorRamp.030
    colorramp_030.color_ramp.color_mode = 'RGB'
    colorramp_030.color_ramp.hue_interpolation = 'NEAR'
    colorramp_030.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_030.color_ramp.elements) > 2:
        colorramp_030.color_ramp.elements.remove(colorramp_030.color_ramp.elements[-1])
    while len(colorramp_030.color_ramp.elements) < 2:
        colorramp_030.color_ramp.elements.new(0.5)
    colorramp_030.color_ramp.elements[0].position = 0.08636362850666046
    colorramp_030.color_ramp.elements[0].color = (0.06470122188329697, 0.06470122188329697, 0.06470122188329697, 1.0)
    colorramp_030.color_ramp.elements[1].position = 0.41363638639450073
    colorramp_030.color_ramp.elements[1].color = (0.7627803683280945, 0.7627803683280945, 0.7627803683280945, 1.0)
    # XL_PF_RAMP_END colorramp_030
    colorramp_030.location = (-878.3, -186.0)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (3556.6, -1266.8)
    label_node(group_034, "", frame)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_15_r()
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (2956.1, -418.9)
    label_node(mix_004, "", frame)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[7].default_value = (0.0878, 0.0878, 0.0878, 1.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    value_002 = nodes.new("ShaderNodeValue")
    value_002.location = (476.0, -402.6)
    label_node(value_002, "", edges)
    value_003 = nodes.new("ShaderNodeValue")
    value_003.location = (476.0, -244.5)
    label_node(value_003, "", edges)
    value_004 = nodes.new("ShaderNodeValue")
    value_004.location = (478.4, -564.9)
    label_node(value_004, "", edges)
    colorramp_032 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_032 | ColorRamp.032
    colorramp_032.color_ramp.color_mode = 'RGB'
    colorramp_032.color_ramp.hue_interpolation = 'NEAR'
    colorramp_032.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_032.color_ramp.elements) > 2:
        colorramp_032.color_ramp.elements.remove(colorramp_032.color_ramp.elements[-1])
    while len(colorramp_032.color_ramp.elements) < 2:
        colorramp_032.color_ramp.elements.new(0.5)
    colorramp_032.color_ramp.elements[0].position = 0.1993958055973053
    colorramp_032.color_ramp.elements[0].color = (0.24929755926132202, 0.3109142780303955, 0.28840649127960205, 1.0)
    colorramp_032.color_ramp.elements[1].position = 0.39879146218299866
    colorramp_032.color_ramp.elements[1].color = (0.05663662403821945, 0.04468653351068497, 0.0281886737793684, 1.0)
    # XL_PF_RAMP_END colorramp_032
    colorramp_032.location = (1855.4, -352.0)
    label_node(colorramp_032, "", frame)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (1260.4, -408.6)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = False
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[3].default_value = -0.35999998450279236
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (1623.0, -939.8)
    label_node(mix_005, "", frame)
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    mix_005.blend_type = 'MIX'
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    mix_005.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_005.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_033 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_033 | ColorRamp.033
    colorramp_033.color_ramp.color_mode = 'RGB'
    colorramp_033.color_ramp.hue_interpolation = 'NEAR'
    colorramp_033.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_033.color_ramp.elements) > 2:
        colorramp_033.color_ramp.elements.remove(colorramp_033.color_ramp.elements[-1])
    while len(colorramp_033.color_ramp.elements) < 2:
        colorramp_033.color_ramp.elements.new(0.5)
    colorramp_033.color_ramp.elements[0].position = 0.1818181872367859
    colorramp_033.color_ramp.elements[0].color = (0.004154332913458347, 0.004154332913458347, 0.004154332913458347, 1.0)
    colorramp_033.color_ramp.elements[1].position = 0.5727271437644958
    colorramp_033.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_033
    colorramp_033.location = (1260.8, -942.1)
    label_node(colorramp_033, "", frame)
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (997.6, -952.8)
    label_node(group_035, "", frame)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = pf_grunge_19_r()
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (1105.8, -1325.8)
    label_node(hue_saturation_value, "", frame)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 1.0
    hue_saturation_value.inputs[2].default_value = 0.75
    hue_saturation_value.inputs[3].default_value = 1.0
    all_edges_012 = nodes.new("ShaderNodeGroup")
    all_edges_012.location = (1527.1, -284.1)
    label_node(all_edges_012, "", edges)
    all_edges_012.xl_c4d_gradient_type = '0'
    all_edges_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_012.node_tree = all_edges()
    all_edges_012.inputs[2].default_value = 2.0
    math = nodes.new("ShaderNodeMath")
    math.location = (1278.2, -193.2)
    label_node(math, "", edges)
    math.operation = 'DIVIDE'
    math.use_clamp = False
    math.inputs[1].default_value = 1.399999976158142
    math.inputs[2].default_value = 0.5
    group_038 = nodes.new("ShaderNodeGroup")
    group_038.location = (2222.9, -101.7)
    label_node(group_038, "", frame)
    group_038.xl_c4d_gradient_type = '0'
    group_038.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_038.node_tree = white_splashes()
    cavity_014 = nodes.new("ShaderNodeGroup")
    cavity_014.location = (1439.8, -407.3)
    label_node(cavity_014, "", frame)
    cavity_014.xl_c4d_gradient_type = '0'
    cavity_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_014.node_tree = cavity()
    cavity_014.inputs[0].default_value = 0.11000001430511475
    cavity_014.inputs[2].default_value = 3.0
    reroute = nodes.new("NodeReroute")
    reroute.location = (1803.8, -534.4)
    label_node(reroute, "", frame)
    reroute.socket_idname = 'NodeSocketFloat'
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (781.6, -942.4)
    label_node(math_001, "", frame)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 0.5
    math_001.inputs[2].default_value = 0.5
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (685.1, -1048.4)
    label_node(reroute_001, "", frame)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (685.1, -1723.6)
    label_node(reroute_005, "", frame)
    reroute_005.socket_idname = 'NodeSocketFloat'
    hue_saturation_value_001 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_001.location = (1105.9, -1159.7)
    label_node(hue_saturation_value_001, "", frame)
    hue_saturation_value_001.inputs[0].default_value = 0.5
    hue_saturation_value_001.inputs[1].default_value = 1.0
    hue_saturation_value_001.inputs[2].default_value = 0.40000003576278687
    hue_saturation_value_001.inputs[3].default_value = 1.0
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1477.3, -1191.6)
    label_node(reroute_002, "", frame)
    reroute_002.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (1467.2, -1357.3)
    label_node(reroute_006, "", frame)
    reroute_006.socket_idname = 'NodeSocketColor'
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (502.7, -1035.4)
    label_node(math_003, "", frame)
    math_003.operation = 'DIVIDE'
    math_003.use_clamp = False
    math_003.inputs[1].default_value = 25.0
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (3298.9, -1266.8)
    label_node(math_004, "", frame)
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False
    math_004.inputs[1].default_value = 30.0
    math_004.inputs[2].default_value = 0.5
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (769.3, -149.3)
    label_node(math_005, "", edges)
    math_005.operation = 'DIVIDE'
    math_005.use_clamp = False
    math_005.inputs[2].default_value = 0.5
    math_006 = nodes.new("ShaderNodeMath")
    math_006.location = (770.3, -309.6)
    label_node(math_006, "", edges)
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False
    math_006.inputs[2].default_value = 0.5
    math_007 = nodes.new("ShaderNodeMath")
    math_007.location = (769.2, -471.5)
    label_node(math_007, "", edges)
    math_007.operation = 'MULTIPLY'
    math_007.use_clamp = False
    math_007.inputs[2].default_value = 0.5
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (688.9, -254.1)
    label_node(reroute_007, "", edges)
    reroute_007.socket_idname = 'NodeSocketFloat'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (688.9, -415.2)
    label_node(reroute_008, "", edges)
    reroute_008.socket_idname = 'NodeSocketFloat'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (688.9, -576.2)
    label_node(reroute_009, "", edges)
    reroute_009.socket_idname = 'NodeSocketFloat'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (688.9, -336.8)
    label_node(reroute_010, "", edges)
    reroute_010.socket_idname = 'NodeSocketFloat'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (1483.3, 945.7)
    reroute_012.socket_idname = 'NodeSocketFloat'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (1483.3, -690.5)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1245.8, -354.9)
    label_node(reroute_013, "", edges)
    reroute_013.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (1245.8, -514.8)
    label_node(reroute_014, "", edges)
    reroute_014.socket_idname = 'NodeSocketColor'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1246.9, -632.2)
    label_node(reroute_015, "", edges)
    reroute_015.socket_idname = 'NodeSocketColor'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (1483.3, 242.3)
    reroute_017.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (1249.6, 768.6)
    reroute_019.socket_idname = 'NodeSocketColor'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (1249.6, -209.1)
    reroute_020.socket_idname = 'NodeSocketColor'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (1493.7, -1130.3)
    reroute_021.socket_idname = 'NodeSocketVector'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (-823.9, -546.1)
    reroute_022.socket_idname = 'NodeSocketVector'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (2425.2, -1628.1)
    label_node(reroute_023, "", frame)
    reroute_023.socket_idname = 'NodeSocketVector'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (2384.3, -1524.2)
    label_node(reroute_024, "", frame)
    reroute_024.socket_idname = 'NodeSocketColor'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (2088.1, -971.3)
    label_node(reroute_025, "", frame)
    reroute_025.socket_idname = 'NodeSocketColor'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1803.8, -720.8)
    label_node(reroute_026, "", frame)
    reroute_026.socket_idname = 'NodeSocketFloat'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (659.7, -1046.3)
    label_node(reroute_027, "", frame)
    reroute_027.socket_idname = 'NodeSocketFloat'
    math_008 = nodes.new("ShaderNodeMath")
    math_008.location = (868.7, -465.5)
    label_node(math_008, "", frame)
    math_008.operation = 'MULTIPLY'
    math_008.use_clamp = False
    math_008.inputs[2].default_value = 0.5
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (690.6, -592.7)
    label_node(reroute_028, "", frame)
    reroute_028.socket_idname = 'NodeSocketFloat'
    math_009 = nodes.new("ShaderNodeMath")
    math_009.location = (479.3, -320.0)
    label_node(math_009, "", edges)
    math_009.operation = 'DIVIDE'
    math_009.use_clamp = False
    math_009.inputs[1].default_value = 10.0
    math_009.inputs[2].default_value = 0.5
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (1107.7, -184.0)
    label_node(reroute_029, "", edges)
    reroute_029.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (971.6, -1388.2)
    label_node(reroute_030, "", frame)
    reroute_030.socket_idname = 'NodeSocketColor'
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (316.4, -290.5)
    label_node(map_range_003, "", edges)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.5
    map_range_003.inputs[4].default_value = 7.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (310.5, -1035.3)
    label_node(map_range_004, "", frame)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 1.0
    map_range_004.inputs[4].default_value = 10.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (252.4, -1165.7)
    label_node(reroute_033, "", frame)
    reroute_033.socket_idname = 'NodeSocketFloatPercentage'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1876.5, -2211.0)
    label_node(reroute_031, "", frame)
    reroute_031.socket_idname = 'NodeSocketVector'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (1786.3, -1934.6)
    label_node(reroute_034, "", frame)
    reroute_034.socket_idname = 'NodeSocketColor'
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.1752265989780426
    color_ramp.color_ramp.elements[0].color = (0.05384170264005661, 0.05384170264005661, 0.05384170264005661, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.9848942756652832
    color_ramp.color_ramp.elements[1].color = (4.953776836395264, 4.953776836395264, 4.953776836395264, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (1509.4, -536.0)
    label_node(color_ramp, "", edges)
    math_011 = nodes.new("ShaderNodeMath")
    math_011.location = (2043.5, -515.2)
    label_node(math_011, "", edges)
    math_011.operation = 'SUBTRACT'
    math_011.use_clamp = True
    math_011.inputs[2].default_value = 0.5
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'CONSTANT'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.0
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.7190333008766174
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (1543.5, 39.3)
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (1983.1, -440.3)
    label_node(reroute_035, "", edges)
    reroute_035.socket_idname = 'NodeSocketFloat'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1983.1, -641.3)
    label_node(reroute_036, "", edges)
    reroute_036.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (1847.4, -620.1)
    label_node(reroute_037, "", edges)
    reroute_037.socket_idname = 'NodeSocketColor'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (960.3, -143.8)
    reroute_038.socket_idname = 'NodeSocketFloat'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (-844.3, 196.9)
    reroute_039.socket_idname = 'NodeSocketColor'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (1915.2, 537.4)
    reroute_040.socket_idname = 'NodeSocketFloat'
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (2412.5, -247.0)
    reroute_041.socket_idname = 'NodeSocketColor'
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (1955.1, -225.9)
    reroute_042.socket_idname = 'NodeSocketColor'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1749.9, -1647.4)
    label_node(hs_bump_control, "", frame)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.30000001192092896
    hs_bump_control_001 = nodes.new("ShaderNodeGroup")
    hs_bump_control_001.location = (1272.0, -594.1)
    hs_bump_control_001.xl_c4d_gradient_type = '0'
    hs_bump_control_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control_001.node_tree = _hs_bump_control_fn()
    hs_bump_control_001.inputs[2].default_value = 0.4000000059604645
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (497.5, -2095.4)
    label_node(map_range_005, "", frame)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.20000000298023224
    map_range_005.inputs[4].default_value = 1.2000000476837158
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (1496.4, -2142.8)
    label_node(map_range_006, "", frame)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[4].default_value = 0.004999999888241291
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (2093.4, 549.2)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MULTIPLY'
    mix_001.clamp_factor = True
    mix_001.clamp_result = True
    mix_001.inputs[0].default_value = 0.75
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (863.7, 381.3)
    reroute_003.socket_idname = 'NodeSocketColor'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (1932.5, 352.4)
    reroute_016.socket_idname = 'NodeSocketFloat'

    # === 节点连接 ===
    links.new(reroute_026.outputs[0], mix_003.inputs[0])
    links.new(bump_001.outputs[0], principled_bsdf_001.inputs[5])
    links.new(math_008.outputs[0], group_037.inputs[1])
    links.new(group_033.outputs[0], colorramp_031.inputs[0])
    links.new(reroute_023.outputs[0], principled_bsdf.inputs[5])
    links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[2])
    links.new(colorramp_031.outputs[0], mix_006.inputs[6])
    links.new(reroute_024.outputs[0], principled_bsdf.inputs[2])
    links.new(group_032.outputs[0], colorramp_029.inputs[0])
    links.new(reroute_021.outputs[0], bump_001.inputs[4])
    links.new(reroute_031.outputs[0], bump.inputs[4])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(mix_004.outputs[2], principled_bsdf.inputs[0])
    links.new(reroute_034.outputs[0], bump.inputs[3])
    links.new(colorramp_040.outputs[0], mix_006.inputs[7])
    links.new(reroute_020.outputs[0], principled_bsdf_001.inputs[0])
    links.new(reroute_011.outputs[0], bump_001.inputs[3])
    links.new(principled_bsdf.outputs[0], mix_shader_001.inputs[1])
    links.new(principled_bsdf_002.outputs[0], mix_shader_001.inputs[2])
    links.new(reroute_022.outputs[0], principled_bsdf_002.inputs[5])
    links.new(group_034.outputs[0], colorramp_030.inputs[0])
    links.new(colorramp_030.outputs[0], principled_bsdf_002.inputs[2])
    links.new(mix_003.outputs[2], mix_004.inputs[6])
    links.new(group_038.outputs[0], mix_004.inputs[0])
    links.new(math_006.outputs[0], group_028.inputs[0])
    links.new(math_007.outputs[0], map_range.inputs[3])
    links.new(reroute_014.outputs[0], map_range.inputs[0])
    links.new(mix_shader_001.outputs[0], mix_shader.inputs[1])
    links.new(reroute.outputs[0], colorramp_032.inputs[0])
    links.new(group_037.outputs[0], map_range_001.inputs[0])
    links.new(reroute_025.outputs[0], mix_003.inputs[6])
    links.new(colorramp_032.outputs[0], mix_003.inputs[7])
    links.new(group_035.outputs[0], colorramp_033.inputs[0])
    links.new(colorramp_033.outputs[0], mix_005.inputs[0])
    links.new(reroute_006.outputs[0], mix_005.inputs[7])
    links.new(reroute_002.outputs[0], mix_005.inputs[6])
    links.new(reroute_030.outputs[0], hue_saturation_value.inputs[4])
    links.new(reroute_001.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], group_035.inputs[0])
    links.new(reroute_027.outputs[0], reroute_001.inputs[0])
    links.new(reroute_005.outputs[0], group_032.inputs[0])
    links.new(reroute_001.outputs[0], reroute_005.inputs[0])
    links.new(reroute_030.outputs[0], hue_saturation_value_001.inputs[4])
    links.new(input_node.outputs[6], group_038.inputs[0])
    links.new(hue_saturation_value_001.outputs[0], reroute_002.inputs[0])
    links.new(hue_saturation_value.outputs[0], reroute_006.inputs[0])
    links.new(map_range_004.outputs[0], math_003.inputs[0])
    links.new(input_node.outputs[7], math_004.inputs[0])
    links.new(math_004.outputs[0], group_034.inputs[0])
    links.new(value_004.outputs[0], math_007.inputs[1])
    links.new(reroute_029.outputs[0], math.inputs[0])
    links.new(value_003.outputs[0], math_005.inputs[1])
    links.new(value_002.outputs[0], math_006.inputs[1])
    links.new(reroute_007.outputs[0], math_005.inputs[0])
    links.new(reroute_009.outputs[0], math_007.inputs[0])
    links.new(reroute_010.outputs[0], reroute_008.inputs[0])
    links.new(reroute_008.outputs[0], reroute_009.inputs[0])
    links.new(reroute_008.outputs[0], math_006.inputs[0])
    links.new(math_009.outputs[0], reroute_010.inputs[0])
    links.new(reroute_010.outputs[0], reroute_007.inputs[0])
    links.new(reroute_017.outputs[0], reroute_011.inputs[0])
    links.new(group_028.outputs[0], reroute_013.inputs[0])
    links.new(reroute_013.outputs[0], reroute_014.inputs[0])
    links.new(reroute_014.outputs[0], reroute_015.inputs[0])
    links.new(reroute_012.outputs[0], reroute_017.inputs[0])
    links.new(reroute_017.outputs[0], mix_shader.inputs[0])
    links.new(mix.outputs[2], reroute_019.inputs[0])
    links.new(reroute_019.outputs[0], reroute_020.inputs[0])
    links.new(reroute_023.outputs[0], reroute_022.inputs[0])
    links.new(colorramp_029.outputs[0], reroute_024.inputs[0])
    links.new(mix_005.outputs[2], reroute_025.inputs[0])
    links.new(reroute.outputs[0], reroute_026.inputs[0])
    links.new(math_003.outputs[0], reroute_027.inputs[0])
    links.new(value_039.outputs[0], math_008.inputs[0])
    links.new(reroute_028.outputs[0], math_008.inputs[1])
    links.new(reroute_001.outputs[0], reroute_028.inputs[0])
    links.new(math_005.outputs[0], reroute_029.inputs[0])
    links.new(input_node.outputs[5], reroute_030.inputs[0])
    links.new(map_range_003.outputs[0], math_009.inputs[0])
    links.new(reroute_033.outputs[0], map_range_004.inputs[0])
    links.new(input_node.outputs[7], reroute_033.inputs[0])
    links.new(bump.outputs[0], reroute_023.inputs[0])
    links.new(reroute_031.outputs[0], reroute_021.inputs[0])
    links.new(bevel.outputs[0], reroute_031.inputs[0])
    links.new(mix_006.outputs[2], reroute_034.inputs[0])
    links.new(map_range.outputs[0], all_edges_011.inputs[1])
    links.new(all_edges_011.outputs[0], reroute_012.inputs[0])
    links.new(reroute_029.outputs[0], all_edges_011.inputs[0])
    links.new(reroute_035.outputs[0], mix.inputs[0])
    links.new(map_range.outputs[0], all_edges_012.inputs[1])
    links.new(math.outputs[0], all_edges_012.inputs[0])
    links.new(map_range_001.outputs[0], cavity_014.inputs[1])
    links.new(cavity_014.outputs[0], reroute.inputs[0])
    links.new(group_036.outputs[0], colorramp_040.inputs[0])
    links.new(input_node.outputs[4], map_range_003.inputs[0])
    links.new(reroute_015.outputs[0], color_ramp.inputs[0])
    links.new(reroute_037.outputs[0], math_011.inputs[0])
    links.new(reroute_036.outputs[0], math_011.inputs[1])
    links.new(reroute_042.outputs[0], principled_bsdf_001.inputs[1])
    links.new(all_edges_012.outputs[0], reroute_035.inputs[0])
    links.new(reroute_035.outputs[0], reroute_036.inputs[0])
    links.new(color_ramp.outputs[0], reroute_037.inputs[0])
    links.new(reroute_038.outputs[0], color_ramp_001.inputs[0])
    links.new(reroute_036.outputs[0], reroute_038.inputs[0])
    links.new(reroute_039.outputs[0], mix_shader_001.inputs[0])
    links.new(group_034.outputs[0], reroute_039.inputs[0])
    links.new(reroute_041.outputs[0], principled_bsdf_001.inputs[2])
    links.new(mix_001.outputs[2], reroute_041.inputs[0])
    links.new(color_ramp_001.outputs[0], reroute_042.inputs[0])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(hs_bump_control_001.outputs[0], bump_001.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control_001.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control_001.inputs[1])
    links.new(map_range_005.outputs[0], group_033.inputs[0])
    links.new(map_range_005.outputs[0], group_036.inputs[0])
    links.new(input_node.outputs[2], map_range_005.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[1])
    links.new(input_node.outputs[0], map_range_006.inputs[0])
    links.new(map_range_006.outputs[0], bevel.inputs[0])
    links.new(reroute_037.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], mix_001.inputs[6])
    links.new(reroute_016.outputs[0], mix_001.inputs[7])
    links.new(reroute_040.outputs[0], reroute_016.inputs[0])
    links.new(math_011.outputs[0], reroute_040.inputs[0])

    return group