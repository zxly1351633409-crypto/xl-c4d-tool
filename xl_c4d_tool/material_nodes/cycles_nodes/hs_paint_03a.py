import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity as _cavity_fn
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_14_r import pf_grunge_14_r
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_22c_r import pf_grunge_22c_r
from .pf_grunge_22d_r import pf_grunge_22d_r
from .perlin_noise_main_001 import perlin_noise_main001
from .perlin_noise_001_node_tree_001 import perlin_noise001_node_tree001
from .perlin_noise_002_node_tree_001 import perlin_noise002_node_tree001
from .perlin_noise_003_node_tree_001 import perlin_noise003_node_tree001


def hs_paint_03a():
    """BL_油漆03 - 深度划痕油漆材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/底色混合"""
    group_name = "BL_油漆03"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹腔脏污_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="基础颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0529, 0.0648, 0.0595, 1.0000)
    group.interface.new_socket(name="细节颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.3372, 0.3372, 0.3372, 1.0000)
    group.interface.new_socket(name="油漆细节_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="变色_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="变色_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_次扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_主颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0931, 0.0529, 0.0704, 1.0000)
    group.interface.new_socket(name="边缘磨损_次颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.2346, 0.2346, 0.2346, 1.0000)
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame_010 = create_frame(nodes, "Frame.010", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "基础颜色+铁锈: 底层颜色与铁锈效果")
    frame_002 = create_frame(nodes, "Frame.002", "凹腔脏污: 凹腔区域(缝隙/角落)的脏污遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")
    frame_004 = create_frame(nodes, "Frame.004", "油漆细节: 油漆材质的磨损/剥落细节层")
    frame_006 = create_frame(nodes, "Frame.006", "粗糙度: 表面粗糙度控制")
    frame_007 = create_frame(nodes, "Frame.007", "凹凸: 凹凸贴图效果")

    # === 节点创建 ===
    colorramp_030 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_030 | ColorRamp.030
    colorramp_030.color_ramp.color_mode = 'RGB'
    colorramp_030.color_ramp.hue_interpolation = 'NEAR'
    colorramp_030.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_030.color_ramp.elements) > 2:
        colorramp_030.color_ramp.elements.remove(colorramp_030.color_ramp.elements[-1])
    while len(colorramp_030.color_ramp.elements) < 2:
        colorramp_030.color_ramp.elements.new(0.5)
    colorramp_030.color_ramp.elements[0].position = 0.4045453667640686
    colorramp_030.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_030.color_ramp.elements[1].position = 0.6363636255264282
    colorramp_030.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_030
    colorramp_030.location = (855.4, -367.6)
    label_node(colorramp_030, "", frame_010)
    all_edges_010 = nodes.new("ShaderNodeGroup")
    all_edges_010.location = (1417.8, -303.9)
    label_node(all_edges_010, "", frame_010)
    all_edges_010.xl_c4d_gradient_type = '0'
    all_edges_010.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_010.node_tree = all_edges()
    all_edges_010.inputs[2].default_value = 2.0
    group_027 = nodes.new("ShaderNodeGroup")
    group_027.location = (540.4, -367.6)
    label_node(group_027, "", frame_010)
    group_027.xl_c4d_gradient_type = '0'
    group_027.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_027.node_tree = pf_grunge_22d_r()
    group_027.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (648.3, -912.2)
    label_node(group_034, "", frame_002)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_15_r()
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (960.6, -911.3)
    label_node(map_range_003, "", frame_002)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 1.0
    map_range_003.inputs[3].default_value = -0.11999999731779099
    map_range_003.inputs[4].default_value = 1.2999999523162842
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (970.2, -1064.0)
    label_node(principled_bsdf, "", frame_003)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[1].default_value = 0.3409999907016754
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.5
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
    mix = nodes.new("ShaderNodeMix")
    mix.location = (-2895.2, 494.1)
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
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (514.2, -159.8)
    label_node(group_035, "", frame)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = pf_grunge_15_r()
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (523.7, -216.5)
    label_node(group_036, "", frame_006)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_15_r()
    colorramp_032 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_032 | ColorRamp.032
    colorramp_032.color_ramp.color_mode = 'RGB'
    colorramp_032.color_ramp.hue_interpolation = 'NEAR'
    colorramp_032.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_032.color_ramp.elements) > 2:
        colorramp_032.color_ramp.elements.remove(colorramp_032.color_ramp.elements[-1])
    while len(colorramp_032.color_ramp.elements) < 2:
        colorramp_032.color_ramp.elements.new(0.5)
    colorramp_032.color_ramp.elements[0].position = 0.00906345248222351
    colorramp_032.color_ramp.elements[0].color = (0.22854101657867432, 0.22854101657867432, 0.22854101657867432, 1.0)
    colorramp_032.color_ramp.elements[1].position = 0.7531579732894897
    colorramp_032.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_032
    colorramp_032.location = (853.8, -101.7)
    label_node(colorramp_032, "", frame_006)
    colorramp_033 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_033 | ColorRamp.033
    colorramp_033.color_ramp.color_mode = 'RGB'
    colorramp_033.color_ramp.hue_interpolation = 'NEAR'
    colorramp_033.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_033.color_ramp.elements) > 2:
        colorramp_033.color_ramp.elements.remove(colorramp_033.color_ramp.elements[-1])
    while len(colorramp_033.color_ramp.elements) < 2:
        colorramp_033.color_ramp.elements.new(0.5)
    colorramp_033.color_ramp.elements[0].position = 0.0181818176060915
    colorramp_033.color_ramp.elements[0].color = (0.318574458360672, 0.24022454023361206, 0.1869504749774933, 1.0)
    colorramp_033.color_ramp.elements[1].position = 1.0
    colorramp_033.color_ramp.elements[1].color = (0.06673276424407959, 0.0446690171957016, 0.04189262166619301, 1.0)
    # XL_PF_RAMP_END colorramp_033
    colorramp_033.location = (-3318.4, 329.3)
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (-2367.9, 1167.1)
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_003.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[7].default_value = (0.0801, 0.0422, 0.0233, 1.0000)
    mix_003.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_039 = nodes.new("ShaderNodeGroup")
    group_039.location = (647.2, -366.6)
    label_node(group_039, "", frame_002)
    group_039.xl_c4d_gradient_type = '0'
    group_039.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_039.node_tree = pf_grunge_15_r()
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (959.5, -366.6)
    label_node(map_range_005, "", frame_002)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 1.0
    map_range_005.inputs[3].default_value = -0.2499999701976776
    map_range_005.inputs[4].default_value = 1.059999942779541
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (-2662.8, 820.5)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[7].default_value = (0.0250, 0.0288, 0.0305, 1.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_040 = nodes.new("ShaderNodeGroup")
    group_040.location = (647.2, -649.3)
    label_node(group_040, "", frame_002)
    group_040.xl_c4d_gradient_type = '0'
    group_040.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_040.node_tree = pf_grunge_15_r()
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (959.5, -649.3)
    label_node(map_range_006, "", frame_002)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 1.0
    map_range_006.inputs[3].default_value = 0.009999990463256836
    map_range_006.inputs[4].default_value = 0.940000057220459
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (-1646.5, 1684.2)
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
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (1537.7, -102.0)
    label_node(mix_006, "", frame)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    all_edges_011 = nodes.new("ShaderNodeGroup")
    all_edges_011.location = (1417.8, -489.9)
    label_node(all_edges_011, "", frame_010)
    all_edges_011.xl_c4d_gradient_type = '0'
    all_edges_011.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_011.node_tree = all_edges()
    all_edges_011.inputs[2].default_value = 3.0
    mix_007 = nodes.new("ShaderNodeMix")
    mix_007.location = (-2379.3, 1684.3)
    mix_007.data_type = 'RGBA'
    mix_007.factor_mode = 'UNIFORM'
    mix_007.blend_type = 'MIX'
    mix_007.clamp_factor = True
    mix_007.clamp_result = False
    mix_007.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_007.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[6].default_value = (0.0847, 0.0638, 0.0434, 1.0000)
    mix_007.inputs[7].default_value = (0.0910, 0.0953, 0.0845, 1.0000)
    mix_007.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (895.5, -427.4)
    label_node(bevel, "", frame_007)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1431.9, -102.4)
    label_node(bump, "", frame_007)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.47999998927116394
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (529.4, -102.4)
    label_node(group_037, "", frame_007)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_22c_r()
    colorramp_036 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_036 | ColorRamp.036
    colorramp_036.color_ramp.color_mode = 'RGB'
    colorramp_036.color_ramp.hue_interpolation = 'NEAR'
    colorramp_036.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_036.color_ramp.elements) > 2:
        colorramp_036.color_ramp.elements.remove(colorramp_036.color_ramp.elements[-1])
    while len(colorramp_036.color_ramp.elements) < 2:
        colorramp_036.color_ramp.elements.new(0.5)
    colorramp_036.color_ramp.elements[0].position = 0.19902484118938446
    colorramp_036.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_036.color_ramp.elements[1].position = 0.5816808938980103
    colorramp_036.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_036
    colorramp_036.location = (845.5, -102.4)
    label_node(colorramp_036, "", frame_007)
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (1260.2, -262.4)
    label_node(mix_001, "", frame)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[6].default_value = (0.0648, 0.0440, 0.0239, 1.0000)
    mix_001.inputs[7].default_value = (0.0437, 0.0276, 0.0228, 1.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (2137.2, -1149.3)
    label_node(principled_bsdf_001, "", frame_003)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[1].default_value = 1.0
    principled_bsdf_001.inputs[2].default_value = 0.6987915635108948
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
    all_edges_012 = nodes.new("ShaderNodeGroup")
    all_edges_012.location = (1082.9, -277.8)
    label_node(all_edges_012, "", frame_003)
    all_edges_012.xl_c4d_gradient_type = '0'
    all_edges_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_012.node_tree = all_edges()
    all_edges_012.inputs[2].default_value = 2.0
    group_028 = nodes.new("ShaderNodeGroup")
    group_028.location = (500.1, -338.9)
    label_node(group_028, "", frame_003)
    group_028.xl_c4d_gradient_type = '0'
    group_028.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_028.node_tree = pf_grunge_14_r()
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (2436.6, -1012.2)
    label_node(mix_shader, "", frame_003)
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (749.9, -338.7)
    label_node(map_range, "", frame_003)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = -0.6399999856948853
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (4428.5, 880.4)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (3122.2, 686.1)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[2].default_value = 0.20000000298023224
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
    cavity_017 = nodes.new("ShaderNodeGroup")
    cavity_017.location = (1092.1, -101.7)
    label_node(cavity_017, "", frame_004)
    cavity_017.xl_c4d_gradient_type = '0'
    cavity_017.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_017.node_tree = _cavity_fn()
    cavity_017.inputs[0].default_value = 0.5
    cavity_017.inputs[2].default_value = 0.5
    group_041 = nodes.new("ShaderNodeGroup")
    group_041.location = (536.4, -103.3)
    label_node(group_041, "", frame_004)
    group_041.xl_c4d_gradient_type = '0'
    group_041.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_041.node_tree = pf_grunge_15_r()
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (811.2, -102.3)
    label_node(map_range_007, "", frame_004)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 1.0
    map_range_007.inputs[3].default_value = -0.7899999618530273
    map_range_007.inputs[4].default_value = 1.0
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    group_042 = nodes.new("ShaderNodeGroup")
    group_042.location = (536.4, -354.8)
    label_node(group_042, "", frame_004)
    group_042.xl_c4d_gradient_type = '0'
    group_042.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_042.node_tree = pf_grunge_15_r()
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (1350.1, -102.0)
    label_node(mix_002, "", frame_004)
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.inputs[0].default_value = 0.5
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.7468960881233215
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.8090910911560059
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (811.2, -353.2)
    label_node(color_ramp, "", frame_004)
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1082.9, -436.4)
    label_node(all_edges_013, "", frame_003)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 2.0
    mix_008 = nodes.new("ShaderNodeMix")
    mix_008.location = (1660.1, -1169.5)
    label_node(mix_008, "", frame_003)
    mix_008.data_type = 'RGBA'
    mix_008.factor_mode = 'UNIFORM'
    mix_008.blend_type = 'MIX'
    mix_008.clamp_factor = True
    mix_008.clamp_result = False
    mix_008.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_008.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    cavity = nodes.new("ShaderNodeGroup")
    cavity.location = (1421.5, -309.3)
    label_node(cavity, "", frame_002)
    cavity.xl_c4d_gradient_type = '0'
    cavity.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity.node_tree = _cavity_fn()
    cavity.inputs[2].default_value = 1.0
    cavity_001 = nodes.new("ShaderNodeGroup")
    cavity_001.location = (1421.5, -649.3)
    label_node(cavity_001, "", frame_002)
    cavity_001.xl_c4d_gradient_type = '0'
    cavity_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_001.node_tree = _cavity_fn()
    cavity_001.inputs[2].default_value = 1.0
    cavity_002 = nodes.new("ShaderNodeGroup")
    cavity_002.location = (1421.5, -904.6)
    label_node(cavity_002, "", frame_002)
    cavity_002.xl_c4d_gradient_type = '0'
    cavity_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_002.node_tree = _cavity_fn()
    cavity_002.inputs[2].default_value = 1.0
    reroute = nodes.new("NodeReroute")
    reroute.location = (-3196.9, -29.6)
    reroute.socket_idname = 'NodeSocketColor'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1398.7, -175.6)
    label_node(reroute_001, "", frame)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (-1903.2, 1711.2)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1687.0, 65.3)
    reroute_004.socket_idname = 'NodeSocketVector'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (152.2, -1117.7)
    label_node(reroute_005, "", frame_003)
    reroute_005.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (685.6, -1223.0)
    label_node(reroute_006, "", frame_003)
    reroute_006.socket_idname = 'NodeSocketVector'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-80.4, 688.2)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (3503.4, 781.6)
    reroute_008.socket_idname = 'NodeSocketShader'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (4238.5, 825.5)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (1031.4, -538.0)
    label_node(reroute_010, "", frame_003)
    reroute_010.socket_idname = 'NodeSocketFloat'
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (874.2, -381.8)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[3].default_value = -1.5
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (874.6, -142.9)
    label_node(map_range_002, "", frame)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[3].default_value = -1.0
    map_range_002.inputs[4].default_value = 2.5
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (294.0, -262.1)
    label_node(map_range_004, "", frame)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.10000000149011612
    map_range_004.inputs[4].default_value = 0.6700000166893005
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (514.2, -371.6)
    label_node(map_range_008, "", frame)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 2.0
    map_range_008.inputs[4].default_value = 1.0
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (392.9, -368.3)
    label_node(map_range_009, "", frame_002)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[3].default_value = 0.10000000149011612
    map_range_009.inputs[4].default_value = 1.0
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (392.9, -649.7)
    label_node(map_range_010, "", frame_002)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[3].default_value = 0.10000000149011612
    map_range_010.inputs[4].default_value = 1.0
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (392.9, -910.8)
    label_node(map_range_011, "", frame_002)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = 0.10000000149011612
    map_range_011.inputs[4].default_value = 1.0
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (355.1, -779.4)
    label_node(reroute_002, "", frame_002)
    reroute_002.socket_idname = 'NodeSocketFloatPercentage'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (355.1, -497.9)
    label_node(reroute_012, "", frame_002)
    reroute_012.socket_idname = 'NodeSocketFloatPercentage'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (355.1, -1041.0)
    label_node(reroute_013, "", frame_002)
    reroute_013.socket_idname = 'NodeSocketFloatPercentage'
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (960.9, -102.1)
    label_node(map_range_012, "", frame_002)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.10000000149011612
    map_range_012.inputs[4].default_value = 2.0
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math = nodes.new("ShaderNodeMath")
    math.location = (1420.1, -150.6)
    label_node(math, "", frame_002)
    math.operation = 'DIVIDE'
    math.use_clamp = False
    math.inputs[1].default_value = 9.489999771118164
    math.inputs[2].default_value = 0.5
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (1419.2, -501.6)
    label_node(math_001, "", frame_002)
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 2.5
    math_001.inputs[2].default_value = 0.5
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (1876.4, -816.0)
    label_node(bump_001, "", frame_003)
    bump_001.invert = True
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (451.6, -982.1)
    label_node(reroute_014, "", frame_003)
    reroute_014.socket_idname = 'NodeSocketVector'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1135.5, -460.5)
    label_node(reroute_015, "", frame_007)
    reroute_015.socket_idname = 'NodeSocketVector'
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (310.3, -341.7)
    label_node(map_range_013, "", frame_003)
    map_range_013.clamp = False
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = 0.20000000298023224
    map_range_013.inputs[4].default_value = 1.5
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (871.7, -129.6)
    label_node(math_002, "", frame_003)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 0.5
    math_002.inputs[2].default_value = 0.5
    map_range_014 = nodes.new("ShaderNodeMapRange")
    map_range_014.location = (308.6, -101.8)
    label_node(map_range_014, "", frame_003)
    map_range_014.clamp = False
    map_range_014.interpolation_type = 'LINEAR'
    map_range_014.data_type = 'FLOAT'
    map_range_014.inputs[2].default_value = 100.0
    map_range_014.inputs[3].default_value = 0.009999999776482582
    map_range_014.inputs[4].default_value = 0.5
    map_range_014.inputs[5].default_value = 4.0
    map_range_014.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (748.0, -133.4)
    label_node(reroute_017, "", frame_003)
    reroute_017.socket_idname = 'NodeSocketFloat'
    texture_coordinate = nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (421.9, -719.0)
    label_node(texture_coordinate, "", frame_003)
    texture_coordinate.from_instancer = False
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (1566.5, -814.9)
    label_node(math_003, "", frame_003)
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    math_003.inputs[2].default_value = 0.5
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (956.1, -941.8)
    label_node(reroute_011, "", frame_003)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (1520.7, -919.4)
    label_node(reroute_019, "", frame_003)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (1520.7, -1326.3)
    label_node(reroute_020, "", frame_003)
    reroute_020.socket_idname = 'NodeSocketFloat'
    map_range_015 = nodes.new("ShaderNodeMapRange")
    map_range_015.location = (302.8, -167.6)
    label_node(map_range_015, "", frame_004)
    map_range_015.clamp = False
    map_range_015.interpolation_type = 'LINEAR'
    map_range_015.data_type = 'FLOAT'
    map_range_015.inputs[2].default_value = 100.0
    map_range_015.inputs[3].default_value = 0.10000000149011612
    map_range_015.inputs[4].default_value = 1.090000033378601
    map_range_015.inputs[5].default_value = 4.0
    map_range_015.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (471.5, -201.8)
    label_node(reroute_023, "", frame_004)
    reroute_023.socket_idname = 'NodeSocketFloat'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (471.5, -455.1)
    label_node(reroute_024, "", frame_004)
    reroute_024.socket_idname = 'NodeSocketFloat'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (1955.9, -481.0)
    label_node(reroute_025, "", frame_003)
    reroute_025.socket_idname = 'NodeSocketFloat'
    map_range_016 = nodes.new("ShaderNodeMapRange")
    map_range_016.location = (316.9, -135.7)
    label_node(map_range_016, "", frame_006)
    map_range_016.clamp = True
    map_range_016.interpolation_type = 'LINEAR'
    map_range_016.data_type = 'FLOAT'
    map_range_016.inputs[2].default_value = 100.0
    map_range_016.inputs[3].default_value = 0.10000000149011612
    map_range_016.inputs[4].default_value = 1.5399999618530273
    map_range_016.inputs[5].default_value = 4.0
    map_range_016.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_017 = nodes.new("ShaderNodeMapRange")
    map_range_017.location = (324.5, -102.4)
    label_node(map_range_017, "", frame_007)
    map_range_017.clamp = True
    map_range_017.interpolation_type = 'LINEAR'
    map_range_017.data_type = 'FLOAT'
    map_range_017.inputs[2].default_value = 1.0
    map_range_017.inputs[3].default_value = 0.10000000149011612
    map_range_017.inputs[4].default_value = 1.5
    map_range_017.inputs[5].default_value = 4.0
    map_range_017.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (1275.5, -460.5)
    label_node(reroute_016, "", frame_007)
    reroute_016.socket_idname = 'NodeSocketVector'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (-3026.0, 418.0)
    reroute_027.socket_idname = 'NodeSocketFloat'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (-685.0, 1651.7)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (-2105.5, 1486.4)
    reroute_029.socket_idname = 'NodeSocketColor'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (-1979.8, 1508.3)
    reroute_030.socket_idname = 'NodeSocketColor'
    map_range_019 = nodes.new("ShaderNodeMapRange")
    map_range_019.location = (309.7, -370.0)
    label_node(map_range_019, "", frame_010)
    map_range_019.clamp = True
    map_range_019.interpolation_type = 'LINEAR'
    map_range_019.data_type = 'FLOAT'
    map_range_019.inputs[2].default_value = 100.0
    map_range_019.inputs[3].default_value = 0.10000000149011612
    map_range_019.inputs[4].default_value = 2.0
    map_range_019.inputs[5].default_value = 4.0
    map_range_019.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_019.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_019.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_020 = nodes.new("ShaderNodeMapRange")
    map_range_020.location = (309.7, -102.2)
    label_node(map_range_020, "", frame_010)
    map_range_020.clamp = True
    map_range_020.interpolation_type = 'LINEAR'
    map_range_020.data_type = 'FLOAT'
    map_range_020.inputs[2].default_value = 100.0
    map_range_020.inputs[3].default_value = 0.019999999552965164
    map_range_020.inputs[4].default_value = 1.0
    map_range_020.inputs[5].default_value = 4.0
    map_range_020.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_020.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_020.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_006 = nodes.new("ShaderNodeMath")
    math_006.location = (540.2, -197.7)
    label_node(math_006, "", frame_010)
    math_006.operation = 'DIVIDE'
    math_006.use_clamp = False
    math_006.inputs[1].default_value = 2.0
    math_006.inputs[2].default_value = 0.5
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1141.8, -135.1)
    label_node(reroute_031, "", frame_010)
    reroute_031.socket_idname = 'NodeSocketFloat'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (1063.3, -230.6)
    label_node(reroute_032, "", frame_010)
    reroute_032.socket_idname = 'NodeSocketFloat'
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (1383.6, -403.4)
    label_node(reroute_033, "", frame_010)
    reroute_033.socket_idname = 'NodeSocketColor'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (1383.6, -590.2)
    label_node(reroute_034, "", frame_010)
    reroute_034.socket_idname = 'NodeSocketColor'
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (1323.5, -569.7)
    label_node(reroute_035, "", frame_010)
    reroute_035.socket_idname = 'NodeSocketFloat'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1323.5, -381.0)
    label_node(reroute_036, "", frame_010)
    reroute_036.socket_idname = 'NodeSocketFloat'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (897.9, -564.7)
    label_node(hs_bump_control, "", frame_007)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.30000001192092896
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (1138.9, -596.1)
    label_node(reroute_018, "", frame_007)
    reroute_018.socket_idname = 'NodeSocketFloat'
    map_range_018 = nodes.new("ShaderNodeMapRange")
    map_range_018.location = (650.7, -344.4)
    label_node(map_range_018, "", frame_007)
    map_range_018.clamp = True
    map_range_018.interpolation_type = 'LINEAR'
    map_range_018.data_type = 'FLOAT'
    map_range_018.inputs[2].default_value = 100.0
    map_range_018.inputs[4].default_value = 0.009999999776482582
    map_range_018.inputs[5].default_value = 4.0
    map_range_018.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_018.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_018.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1000.1, -400.0)
    reroute_026.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (1831.3, -895.0)
    label_node(reroute_037, "", frame_003)
    reroute_037.socket_idname = 'NodeSocketFloat'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (1253.2, -1131.9)
    label_node(reroute_038, "", frame_003)
    reroute_038.socket_idname = 'NodeSocketFloat'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (1693.2, -1131.9)
    label_node(reroute_039, "", frame_003)
    reroute_039.socket_idname = 'NodeSocketFloat'
    perlin_noise = nodes.new("ShaderNodeGroup")
    perlin_noise.location = (605.2, -673.6)
    label_node(perlin_noise, "", frame_003)
    perlin_noise.xl_c4d_gradient_type = '0'
    perlin_noise.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise.node_tree = perlin_noise_main001()
    perlin_noise.inputs[2].default_value = 41.0
    perlin_noise.inputs[3].default_value = 10.0
    perlin_noise.inputs[5].default_value = 2.0
    perlin_noise.inputs[7].default_value = 60.0
    perlin_noise.inputs[9].default_value = 1.0
    perlin_noise_001 = nodes.new("ShaderNodeGroup")
    perlin_noise_001.location = (0.0, 0.0)
    perlin_noise_001.xl_c4d_gradient_type = '0'
    perlin_noise_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise_001.node_tree = perlin_noise001_node_tree001()
    perlin_noise_001.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise_001.inputs[2].default_value = 8.0
    perlin_noise_001.inputs[3].default_value = 10.0
    perlin_noise_001.inputs[5].default_value = 2.0
    perlin_noise_001.inputs[7].default_value = 60.0
    perlin_noise_001.inputs[9].default_value = 1.0
    perlin_noise_002 = nodes.new("ShaderNodeGroup")
    perlin_noise_002.location = (0.0, 0.0)
    perlin_noise_002.xl_c4d_gradient_type = '0'
    perlin_noise_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise_002.node_tree = perlin_noise002_node_tree001()
    perlin_noise_002.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise_002.inputs[2].default_value = 8.0
    perlin_noise_002.inputs[3].default_value = 10.0
    perlin_noise_002.inputs[5].default_value = 2.0
    perlin_noise_002.inputs[7].default_value = 60.0
    perlin_noise_002.inputs[9].default_value = 1.0
    perlin_noise_003 = nodes.new("ShaderNodeGroup")
    perlin_noise_003.location = (0.0, 0.0)
    perlin_noise_003.xl_c4d_gradient_type = '0'
    perlin_noise_003.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise_003.node_tree = perlin_noise003_node_tree001()
    perlin_noise_003.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise_003.inputs[2].default_value = 8.0
    perlin_noise_003.inputs[3].default_value = 10.0
    perlin_noise_003.inputs[5].default_value = 2.0
    perlin_noise_003.inputs[7].default_value = 60.0
    perlin_noise_003.inputs[9].default_value = 1.0

    # === 节点连接 ===
    links.new(group_027.outputs[0], colorramp_030.inputs[0])
    links.new(map_range_011.outputs[0], group_034.inputs[0])
    links.new(group_034.outputs[0], map_range_003.inputs[0])
    links.new(group_036.outputs[0], colorramp_032.inputs[0])
    links.new(colorramp_033.outputs[0], mix.inputs[7])
    links.new(map_range_009.outputs[0], group_039.inputs[0])
    links.new(group_039.outputs[0], map_range_005.inputs[0])
    links.new(mix_004.outputs[2], mix_003.inputs[6])
    links.new(mix.outputs[2], mix_004.inputs[6])
    links.new(map_range_010.outputs[0], group_040.inputs[0])
    links.new(group_040.outputs[0], map_range_006.inputs[0])
    links.new(reroute_030.outputs[0], mix_005.inputs[6])
    links.new(reroute_003.outputs[0], mix_005.inputs[0])
    links.new(reroute.outputs[0], mix.inputs[6])
    links.new(reroute_001.outputs[0], mix_006.inputs[0])
    links.new(reroute_029.outputs[0], mix_005.inputs[7])
    links.new(map_range_017.outputs[0], group_037.inputs[0])
    links.new(group_037.outputs[0], colorramp_036.inputs[0])
    links.new(mix_001.outputs[2], mix_006.inputs[7])
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[2])
    links.new(mix_shader.outputs[0], mix_shader_001.inputs[1])
    links.new(reroute_008.outputs[0], mix_shader_001.inputs[2])
    links.new(group_041.outputs[0], map_range_007.inputs[0])
    links.new(reroute_009.outputs[0], mix_shader_001.inputs[0])
    links.new(color_ramp.outputs[0], mix_002.inputs[7])
    links.new(group_042.outputs[0], color_ramp.inputs[0])
    links.new(mix_shader_001.outputs[0], output_node.inputs[0])
    links.new(reroute_004.outputs[0], principled_bsdf_002.inputs[5])
    links.new(mix_008.outputs[2], principled_bsdf_001.inputs[0])
    links.new(reroute_027.outputs[0], mix.inputs[0])
    links.new(mix_006.outputs[2], reroute.inputs[0])
    links.new(map_range_002.outputs[0], reroute_001.inputs[0])
    links.new(bump.outputs[0], reroute_004.inputs[0])
    links.new(reroute_028.outputs[0], reroute_005.inputs[0])
    links.new(bump.outputs[0], reroute_006.inputs[0])
    links.new(colorramp_032.outputs[0], reroute_007.inputs[0])
    links.new(reroute_005.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_006.outputs[0], principled_bsdf.inputs[5])
    links.new(reroute_007.outputs[0], principled_bsdf.inputs[2])
    links.new(principled_bsdf_002.outputs[0], reroute_008.inputs[0])
    links.new(mix_002.outputs[2], reroute_009.inputs[0])
    links.new(reroute_025.outputs[0], mix_shader.inputs[0])
    links.new(reroute_020.outputs[0], mix_008.inputs[0])
    links.new(map_range.outputs[0], reroute_010.inputs[0])
    links.new(map_range_001.outputs[0], mix_001.inputs[0])
    links.new(group_035.outputs[0], map_range_001.inputs[0])
    links.new(group_035.outputs[0], map_range_002.inputs[0])
    links.new(input_node.outputs[6], mix_006.inputs[6])
    links.new(map_range_004.outputs[0], group_035.inputs[0])
    links.new(input_node.outputs[9], map_range_004.inputs[0])
    links.new(input_node.outputs[10], map_range_008.inputs[0])
    links.new(map_range_008.outputs[0], map_range_002.inputs[2])
    links.new(reroute_012.outputs[0], map_range_009.inputs[0])
    links.new(reroute_002.outputs[0], map_range_010.inputs[0])
    links.new(reroute_013.outputs[0], map_range_011.inputs[0])
    links.new(input_node.outputs[5], reroute_002.inputs[0])
    links.new(reroute_002.outputs[0], reroute_012.inputs[0])
    links.new(reroute_002.outputs[0], reroute_013.inputs[0])
    links.new(input_node.outputs[4], map_range_012.inputs[0])
    links.new(map_range_012.outputs[0], math.inputs[0])
    links.new(map_range_012.outputs[0], math_001.inputs[0])
    links.new(math_003.outputs[0], bump_001.inputs[3])
    links.new(bump_001.outputs[0], principled_bsdf_001.inputs[5])
    links.new(reroute_014.outputs[0], bump_001.inputs[4])
    links.new(reroute_015.outputs[0], reroute_014.inputs[0])
    links.new(reroute_017.outputs[0], math_002.inputs[0])
    links.new(map_range_014.outputs[0], reroute_017.inputs[0])
    links.new(input_node.outputs[13], map_range_013.inputs[0])
    links.new(input_node.outputs[11], map_range_014.inputs[0])
    links.new(reroute_019.outputs[0], math_003.inputs[0])
    links.new(reroute_011.outputs[0], math_003.inputs[1])
    links.new(reroute_019.outputs[0], reroute_020.inputs[0])
    links.new(reroute_023.outputs[0], group_041.inputs[0])
    links.new(reroute_024.outputs[0], group_042.inputs[0])
    links.new(input_node.outputs[8], map_range_015.inputs[0])
    links.new(map_range_015.outputs[0], reroute_023.inputs[0])
    links.new(reroute_023.outputs[0], reroute_024.inputs[0])
    links.new(input_node.outputs[7], principled_bsdf_002.inputs[0])
    links.new(input_node.outputs[14], mix_008.inputs[6])
    links.new(input_node.outputs[15], mix_008.inputs[7])
    links.new(map_range_016.outputs[0], group_036.inputs[0])
    links.new(input_node.outputs[16], map_range_016.inputs[0])
    links.new(input_node.outputs[2], map_range_017.inputs[0])
    links.new(bevel.outputs[0], reroute_015.inputs[0])
    links.new(reroute_015.outputs[0], reroute_016.inputs[0])
    links.new(reroute_016.outputs[0], bump.inputs[4])
    links.new(mix_005.outputs[2], reroute_028.inputs[0])
    links.new(mix_007.outputs[2], reroute_029.inputs[0])
    links.new(mix_003.outputs[2], reroute_030.inputs[0])
    links.new(all_edges_010.outputs[0], reroute_003.inputs[0])
    links.new(reroute_033.outputs[0], all_edges_010.inputs[1])
    links.new(all_edges_011.outputs[0], mix_007.inputs[0])
    links.new(reroute_034.outputs[0], all_edges_011.inputs[1])
    links.new(map_range.outputs[0], all_edges_012.inputs[1])
    links.new(math_002.outputs[0], all_edges_012.inputs[0])
    links.new(all_edges_012.outputs[0], reroute_019.inputs[0])
    links.new(reroute_010.outputs[0], all_edges_013.inputs[1])
    links.new(reroute_017.outputs[0], all_edges_013.inputs[0])
    links.new(all_edges_013.outputs[0], reroute_025.inputs[0])
    links.new(map_range_007.outputs[0], cavity_017.inputs[1])
    links.new(cavity_017.outputs[0], mix_002.inputs[6])
    links.new(map_range_005.outputs[0], cavity.inputs[1])
    links.new(cavity.outputs[0], mix_003.inputs[0])
    links.new(math.outputs[0], cavity.inputs[0])
    links.new(map_range_006.outputs[0], cavity_001.inputs[1])
    links.new(cavity_001.outputs[0], mix_004.inputs[0])
    links.new(math_001.outputs[0], cavity_001.inputs[0])
    links.new(cavity_002.outputs[0], colorramp_033.inputs[0])
    links.new(map_range_003.outputs[0], cavity_002.inputs[1])
    links.new(map_range_012.outputs[0], cavity_002.inputs[0])
    links.new(cavity_002.outputs[0], reroute_027.inputs[0])
    links.new(group_028.outputs[0], map_range.inputs[0])
    links.new(input_node.outputs[12], map_range_019.inputs[0])
    links.new(map_range_019.outputs[0], group_027.inputs[1])
    links.new(input_node.outputs[12], map_range_020.inputs[0])
    links.new(map_range_020.outputs[0], math_006.inputs[0])
    links.new(reroute_036.outputs[0], all_edges_010.inputs[0])
    links.new(reroute_035.outputs[0], all_edges_011.inputs[0])
    links.new(map_range_020.outputs[0], reroute_031.inputs[0])
    links.new(math_006.outputs[0], reroute_032.inputs[0])
    links.new(colorramp_030.outputs[0], reroute_033.inputs[0])
    links.new(reroute_033.outputs[0], reroute_034.inputs[0])
    links.new(reroute_032.outputs[0], reroute_035.inputs[0])
    links.new(reroute_031.outputs[0], reroute_036.inputs[0])
    links.new(reroute_018.outputs[0], bump.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_018.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[1])
    links.new(map_range_018.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[0], map_range_018.inputs[0])
    links.new(colorramp_036.outputs[0], bump.inputs[3])
    links.new(reroute_018.outputs[0], reroute_026.inputs[0])
    links.new(reroute_037.outputs[0], bump_001.inputs[0])
    links.new(reroute_039.outputs[0], reroute_037.inputs[0])
    links.new(reroute_026.outputs[0], reroute_038.inputs[0])
    links.new(reroute_038.outputs[0], reroute_039.inputs[0])
    links.new(map_range_013.outputs[0], group_028.inputs[0])
    links.new(texture_coordinate.outputs[3], perlin_noise.inputs[0])
    links.new(perlin_noise.outputs[0], reroute_011.inputs[0])

    return group