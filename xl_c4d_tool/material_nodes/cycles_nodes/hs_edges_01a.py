import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_19b_r import pf_grunge_19b_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_22e_r import pf_grunge_22e_r


def hs_edges_01a():
    """BL_边缘磨损 - 多层边缘磨损材质
    基于Principled BSDF，含凹凸开关/粗糙度/多层边缘检测"""
    group_name = "BL_边缘磨损"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="输入着色器: 底层材质着色器输入", in_out="INPUT", socket_type="NodeSocketShader")
    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第1层_颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.4735, 0.2270, 0.1070, 1.0000)
    group.interface.new_socket(name="第1层_变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第1层_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第1层_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第2层_颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0418, 0.0245, 0.0146, 1.0000)
    group.interface.new_socket(name="第2层_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第2层_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第2层_变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第3层_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第3层_变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第3层_颜色A", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0418, 0.0245, 0.0146, 1.0000)
    group.interface.new_socket(name="第3层_颜色A扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="第3层_颜色B", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0423, 0.0262, 0.0168, 1.0000)
    group.interface.new_socket(name="第3层_颜色B扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "第3层: 第三层材质叠加", (0.09, 0.09, 0.09))
    frame_001 = create_frame(nodes, "Frame.001", "第1层: 第一层材质叠加")
    frame_009 = create_frame(nodes, "Frame.009", "第2层: 第二层材质叠加")
    frame_005 = create_frame(nodes, "Frame.005", "输入着色器: 底层材质着色器输入")

    # === 节点创建 ===
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1799.4, -1231.0)
    label_node(all_edges_013, "", frame)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 5.0
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (773.2, -331.8)
    label_node(group_029, "", frame)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_15_r()
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (2716.8, -559.8)
    label_node(principled_bsdf_001, "", frame)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[3].default_value = 1.5
    principled_bsdf_001.inputs[4].default_value = 1.0
    principled_bsdf_001.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_001.inputs[11].default_value = 1.399999976158142
    principled_bsdf_001.inputs[13].default_value = 0.19090907275676727
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
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (1074.2, -539.3)
    label_node(map_range, "", frame)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[1].default_value = 0.09999999403953552
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[4].default_value = 20.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (1799.4, -377.8)
    label_node(all_edges_014, "", frame)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 5.0
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (2346.9, -581.4)
    label_node(mix_004, "", frame)
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
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (2391.7, -920.9)
    label_node(bump_001, "", frame)
    bump_001.invert = True
    bump_001.inputs[1].default_value = 0.6800000071525574
    bump_001.inputs[2].default_value = 1.0
    colorramp_047 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_047 | ColorRamp.047
    colorramp_047.color_ramp.color_mode = 'RGB'
    colorramp_047.color_ramp.hue_interpolation = 'NEAR'
    colorramp_047.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_047.color_ramp.elements) > 2:
        colorramp_047.color_ramp.elements.remove(colorramp_047.color_ramp.elements[-1])
    while len(colorramp_047.color_ramp.elements) < 2:
        colorramp_047.color_ramp.elements.new(0.5)
    colorramp_047.color_ramp.elements[0].position = 0.29003027081489563
    colorramp_047.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_047.color_ramp.elements[1].position = 1.0
    colorramp_047.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_047
    colorramp_047.location = (2155.6, -102.1)
    label_node(colorramp_047, "", frame)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (1799.4, -207.9)
    label_node(group_034, "", frame)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_22e_r()
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (564.3, -331.8)
    label_node(math_001, "", frame)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 1.0
    math_001.inputs[2].default_value = 0.5
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (1308.0, -989.9)
    label_node(math_003, "", frame)
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (1308.0, -733.6)
    label_node(math_004, "", frame)
    math_004.operation = 'MULTIPLY'
    math_004.use_clamp = False
    math_004.inputs[1].default_value = 0.5
    math_004.inputs[2].default_value = 0.5
    principled_bsdf_004 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_004.location = (2790.5, -484.0)
    label_node(principled_bsdf_004, "", frame_001)
    principled_bsdf_004.distribution = 'MULTI_GGX'
    principled_bsdf_004.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_004.inputs[1].default_value = 1.0
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
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (349.7, -253.0)
    label_node(map_range_006, "", frame)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.5
    map_range_006.inputs[4].default_value = 4.0
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (1078.7, -804.1)
    label_node(map_range_007, "", frame)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.0010000000474974513
    map_range_007.inputs[4].default_value = 0.007000000216066837
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (1079.9, -1082.0)
    label_node(map_range_008, "", frame)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.009999999776482582
    map_range_008.inputs[4].default_value = 9.0
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    bevel_001 = nodes.new("ShaderNodeBevel")
    bevel_001.location = (1915.4, -1384.6)
    label_node(bevel_001, "", frame)
    bevel_001.samples = 32
    bevel_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (2737.4, -488.9)
    label_node(principled_bsdf_002, "", frame_009)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[3].default_value = 1.100000023841858
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
    all_edges_015 = nodes.new("ShaderNodeGroup")
    all_edges_015.location = (1855.8, -207.5)
    label_node(all_edges_015, "", frame_009)
    all_edges_015.xl_c4d_gradient_type = '0'
    all_edges_015.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_015.node_tree = all_edges()
    all_edges_015.inputs[2].default_value = 2.0
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (1940.9, -2151.6)
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (1273.5, -552.8)
    label_node(group_030, "", frame_009)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_22b_r()
    mix_shader_004 = nodes.new("ShaderNodeMixShader")
    mix_shader_004.location = (2883.1, -2151.6)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (1664.9, -302.9)
    label_node(map_range_001, "", frame_009)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[1].default_value = 0.09999999403953552
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_shader_002 = nodes.new("ShaderNodeMixShader")
    mix_shader_002.location = (1312.0, -2151.6)
    all_edges_018 = nodes.new("ShaderNodeGroup")
    all_edges_018.location = (1993.5, -217.5)
    label_node(all_edges_018, "", frame_001)
    all_edges_018.xl_c4d_gradient_type = '0'
    all_edges_018.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_018.node_tree = all_edges()
    all_edges_018.inputs[2].default_value = 4.0
    group_033 = nodes.new("ShaderNodeGroup")
    group_033.location = (1255.3, -429.5)
    label_node(group_033, "", frame_001)
    group_033.xl_c4d_gradient_type = '0'
    group_033.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_033.node_tree = pf_grunge_19b_r()
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (1541.1, -421.5)
    label_node(map_range_002, "", frame_001)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[1].default_value = 0.09999999403953552
    map_range_002.inputs[2].default_value = 1.0
    map_range_002.inputs[4].default_value = -1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (2472.4, -674.2)
    label_node(bump, "", frame_001)
    bump.invert = True
    bump.inputs[1].default_value = 0.0010000000474974513
    bump.inputs[3].default_value = 1.0
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (2055.4, -780.6)
    label_node(bevel, "", frame_001)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    bump_002 = nodes.new("ShaderNodeBump")
    bump_002.location = (2437.4, -611.2)
    label_node(bump_002, "", frame_009)
    bump_002.invert = True
    bump_002.inputs[1].default_value = 0.0010000000474974513
    bump_002.inputs[2].default_value = 0.10000000149011612
    bump_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (1928.4, -315.4)
    label_node(reroute, "", frame_001)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (821.9, -2639.9)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1788.7, -2230.4)
    reroute_003.socket_idname = 'NodeSocketShader'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1877.2, -2250.0)
    reroute_004.socket_idname = 'NodeSocketShader'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (2258.0, -2250.5)
    reroute_005.socket_idname = 'NodeSocketShader'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (2358.4, -2230.1)
    reroute_006.socket_idname = 'NodeSocketShader'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (2667.2, -2208.6)
    reroute_007.socket_idname = 'NodeSocketFloat'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (659.7, -2920.7)
    reroute_008.socket_idname = 'NodeSocketShader'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (656.8, -1631.8)
    reroute_009.socket_idname = 'NodeSocketShader'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (2194.3, -2186.5)
    reroute_012.socket_idname = 'NodeSocketShader'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1639.6, -2184.9)
    reroute_013.socket_idname = 'NodeSocketShader'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (1121.8, -2250.7)
    reroute_014.socket_idname = 'NodeSocketShader'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (689.5, -1362.9)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (1072.4, -2229.4)
    reroute_016.socket_idname = 'NodeSocketShader'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (722.3, -4564.5)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (1519.3, -1329.2)
    label_node(reroute_017, "", frame)
    reroute_017.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (2251.5, -1064.0)
    label_node(reroute_019, "", frame)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (2296.4, -1083.4)
    label_node(reroute_020, "", frame)
    reroute_020.socket_idname = 'NodeSocketVector'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (2105.1, -1262.8)
    label_node(reroute_021, "", frame)
    reroute_021.socket_idname = 'NodeSocketFloat'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (2248.5, -756.9)
    label_node(reroute_022, "", frame)
    reroute_022.socket_idname = 'NodeSocketColor'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (2248.5, -735.4)
    label_node(reroute_023, "", frame)
    reroute_023.socket_idname = 'NodeSocketFloat'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (2248.5, -777.3)
    label_node(reroute_024, "", frame)
    reroute_024.socket_idname = 'NodeSocketColor'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (1519.3, -573.8)
    label_node(reroute_025, "", frame)
    reroute_025.socket_idname = 'NodeSocketFloat'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1765.2, -454.7)
    label_node(reroute_026, "", frame)
    reroute_026.socket_idname = 'NodeSocketFloat'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (1564.2, -765.3)
    label_node(reroute_028, "", frame)
    reroute_028.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (2307.5, -752.5)
    label_node(reroute_030, "", frame_009)
    reroute_030.socket_idname = 'NodeSocketFloat'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1582.9, -433.6)
    label_node(reroute_031, "", frame_009)
    reroute_031.socket_idname = 'NodeSocketColor'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (1065.5, -338.4)
    label_node(percentage_to_0_1, "百分比转0-1", frame_001)
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1.inputs[4].default_value = 2.5
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_1.location = (1065.5, -102.0)
    label_node(percentage_to_0_1_1, "百分比转0-1", frame_001)
    percentage_to_0_1_1.clamp = True
    percentage_to_0_1_1.interpolation_type = 'LINEAR'
    percentage_to_0_1_1.data_type = 'FLOAT'
    percentage_to_0_1_1.inputs[2].default_value = 100.0
    percentage_to_0_1_1.inputs[3].default_value = 0.05000000074505806
    percentage_to_0_1_1.inputs[4].default_value = 0.12999999523162842
    percentage_to_0_1_1.inputs[5].default_value = 4.0
    percentage_to_0_1_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_2 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_2.location = (1065.5, -583.2)
    label_node(percentage_to_0_1_2, "百分比转0-1", frame_001)
    percentage_to_0_1_2.clamp = True
    percentage_to_0_1_2.interpolation_type = 'LINEAR'
    percentage_to_0_1_2.data_type = 'FLOAT'
    percentage_to_0_1_2.inputs[2].default_value = 100.0
    percentage_to_0_1_2.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1_2.inputs[4].default_value = 0.6499999761581421
    percentage_to_0_1_2.inputs[5].default_value = 4.0
    percentage_to_0_1_2.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (1928.4, -296.2)
    label_node(reroute_032, "", frame_001)
    reroute_032.socket_idname = 'NodeSocketFloat'
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (1753.6, -135.3)
    label_node(reroute_033, "", frame_001)
    reroute_033.socket_idname = 'NodeSocketFloat'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (2249.9, -836.8)
    label_node(reroute_034, "", frame_001)
    reroute_034.socket_idname = 'NodeSocketVector'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1768.3, -455.5)
    label_node(reroute_036, "", frame_001)
    reroute_036.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (2645.3, -716.6)
    label_node(reroute_037, "", frame)
    reroute_037.socket_idname = 'NodeSocketVector'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (2642.4, -654.1)
    label_node(reroute_038, "", frame)
    reroute_038.socket_idname = 'NodeSocketColor'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (1473.7, -1308.1)
    label_node(reroute_039, "", frame)
    reroute_039.socket_idname = 'NodeSocketFloat'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (1617.7, -476.4)
    label_node(reroute_040, "", frame)
    reroute_040.socket_idname = 'NodeSocketFloat'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (722.3, -3897.3)
    reroute_027.socket_idname = 'NodeSocketShader'
    percentage_to_0_1_3 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_3.location = (1730.6, -1431.7)
    label_node(percentage_to_0_1_3, "百分比转0-1", frame)
    percentage_to_0_1_3.clamp = True
    percentage_to_0_1_3.interpolation_type = 'LINEAR'
    percentage_to_0_1_3.data_type = 'FLOAT'
    percentage_to_0_1_3.inputs[2].default_value = 100.0
    percentage_to_0_1_3.inputs[4].default_value = 0.019999999552965164
    percentage_to_0_1_3.inputs[5].default_value = 4.0
    percentage_to_0_1_3.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_4 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_4.location = (1065.5, -827.8)
    label_node(percentage_to_0_1_4, "百分比转0-1", frame_001)
    percentage_to_0_1_4.clamp = True
    percentage_to_0_1_4.interpolation_type = 'LINEAR'
    percentage_to_0_1_4.data_type = 'FLOAT'
    percentage_to_0_1_4.inputs[2].default_value = 100.0
    percentage_to_0_1_4.inputs[4].default_value = 0.009999999776482582
    percentage_to_0_1_4.inputs[5].default_value = 4.0
    percentage_to_0_1_4.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_4.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_4.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (350.6, -507.6)
    label_node(map_range_011, "", frame)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = -4.670000076293945
    map_range_011.inputs[4].default_value = -0.10000000149011612
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (782.8, -731.8)
    label_node(reroute_010, "", frame)
    reroute_010.socket_idname = 'NodeSocketFloat'
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (1065.5, -102.1)
    label_node(map_range_012, "", frame_009)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.10000000149011612
    map_range_012.inputs[4].default_value = 0.5
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (1062.6, -349.1)
    label_node(map_range_013, "", frame_009)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = -1.5
    map_range_013.inputs[4].default_value = -0.25
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_014 = nodes.new("ShaderNodeMapRange")
    map_range_014.location = (1061.0, -592.0)
    label_node(map_range_014, "", frame_009)
    map_range_014.clamp = True
    map_range_014.interpolation_type = 'LINEAR'
    map_range_014.data_type = 'FLOAT'
    map_range_014.inputs[2].default_value = 100.0
    map_range_014.inputs[3].default_value = 0.20000000298023224
    map_range_014.inputs[4].default_value = 1.600000023841858
    map_range_014.inputs[5].default_value = 4.0
    map_range_014.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (351.3, -935.1)
    label_node(reroute_041, "", frame)
    reroute_041.socket_idname = 'NodeSocketFloatPercentage'
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (1396.8, -494.7)
    label_node(reroute_042, "", frame_009)
    reroute_042.socket_idname = 'NodeSocketFloat'
    reroute_043 = nodes.new("NodeReroute")
    reroute_043.location = (1447.4, -285.4)
    label_node(reroute_043, "", frame_009)
    reroute_043.socket_idname = 'NodeSocketFloat'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1956.7, -629.0)
    label_node(hs_bump_control, "", frame_001)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (2264.6, -755.1)
    label_node(reroute_035, "", frame_001)
    reroute_035.socket_idname = 'NodeSocketFloat'
    hs_bump_control_001 = nodes.new("ShaderNodeGroup")
    hs_bump_control_001.location = (1940.5, -659.8)
    label_node(hs_bump_control_001, "", frame_009)
    hs_bump_control_001.xl_c4d_gradient_type = '0'
    hs_bump_control_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control_001.node_tree = _hs_bump_control_fn()
    hs_bump_control_001.inputs[2].default_value = 0.4000000059604645
    hs_bump_control_002 = nodes.new("ShaderNodeGroup")
    hs_bump_control_002.location = (1827.1, -1047.5)
    label_node(hs_bump_control_002, "", frame)
    hs_bump_control_002.xl_c4d_gradient_type = '0'
    hs_bump_control_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control_002.node_tree = _hs_bump_control_fn()
    hs_bump_control_002.inputs[2].default_value = 0.4000000059604645
    reroute_044 = nodes.new("NodeReroute")
    reroute_044.location = (2128.6, -1079.8)
    label_node(reroute_044, "", frame)
    reroute_044.socket_idname = 'NodeSocketFloat'
    reroute_045 = nodes.new("NodeReroute")
    reroute_045.location = (2352.7, -1001.3)
    label_node(reroute_045, "", frame)
    reroute_045.socket_idname = 'NodeSocketFloat'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (1473.7, -1023.6)
    label_node(reroute_029, "", frame)
    reroute_029.socket_idname = 'NodeSocketFloat'
    math = nodes.new("ShaderNodeMath")
    math.location = (1316.0, -2277.3)
    math.operation = 'SUBTRACT'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    reroute_046 = nodes.new("NodeReroute")
    reroute_046.location = (1128.8, -2208.2)
    reroute_046.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1641.6, -2209.6)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (1112.4, -2381.4)
    reroute_018.socket_idname = 'NodeSocketFloat'
    reroute_047 = nodes.new("NodeReroute")
    reroute_047.location = (1201.1, -2403.9)
    reroute_047.socket_idname = 'NodeSocketFloat'
    reroute_048 = nodes.new("NodeReroute")
    reroute_048.location = (2521.7, -137.7)
    label_node(reroute_048, "", frame)
    reroute_048.socket_idname = 'NodeSocketColor'
    colorramp_048 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_048 | ColorRamp.048
    colorramp_048.color_ramp.color_mode = 'RGB'
    colorramp_048.color_ramp.hue_interpolation = 'NEAR'
    colorramp_048.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_048.color_ramp.elements) > 2:
        colorramp_048.color_ramp.elements.remove(colorramp_048.color_ramp.elements[-1])
    while len(colorramp_048.color_ramp.elements) < 2:
        colorramp_048.color_ramp.elements.new(0.5)
    colorramp_048.color_ramp.elements[0].position = 0.3746221959590912
    colorramp_048.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_048.color_ramp.elements[1].position = 0.9879153966903687
    colorramp_048.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_048
    colorramp_048.location = (2496.8, -884.0)
    label_node(colorramp_048, "", frame_001)
    reroute_049 = nodes.new("NodeReroute")
    reroute_049.location = (1503.0, -1051.9)
    label_node(reroute_049, "", frame_001)
    reroute_049.socket_idname = 'NodeSocketColor'
    reroute_050 = nodes.new("NodeReroute")
    reroute_050.location = (1503.0, -462.1)
    label_node(reroute_050, "", frame_001)
    reroute_050.socket_idname = 'NodeSocketColor'
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (2334.4, -939.0)
    label_node(math_002, "", frame_001)
    math_002.operation = 'SUBTRACT'
    math_002.use_clamp = False
    math_002.inputs[2].default_value = 0.5
    reroute_053 = nodes.new("NodeReroute")
    reroute_053.location = (2288.0, -249.1)
    label_node(reroute_053, "", frame_001)
    reroute_053.socket_idname = 'NodeSocketFloat'
    reroute_054 = nodes.new("NodeReroute")
    reroute_054.location = (2288.0, -1065.7)
    label_node(reroute_054, "", frame_001)
    reroute_054.socket_idname = 'NodeSocketFloat'
    reroute_055 = nodes.new("NodeReroute")
    reroute_055.location = (2288.0, -793.7)
    label_node(reroute_055, "", frame_001)
    reroute_055.socket_idname = 'NodeSocketFloat'

    # === 节点连接 ===
    links.new(reroute_046.outputs[0], mix_shader_002.inputs[0])
    links.new(reroute_006.outputs[0], mix_shader_004.inputs[1])
    links.new(reroute_004.outputs[0], mix_shader_001.inputs[2])
    links.new(reroute_030.outputs[0], bump_002.inputs[3])
    links.new(bump_002.outputs[0], principled_bsdf_002.inputs[5])
    links.new(reroute_014.outputs[0], mix_shader_002.inputs[2])
    links.new(reroute_034.outputs[0], bump.inputs[4])
    links.new(reroute_050.outputs[0], map_range_002.inputs[0])
    links.new(bump.outputs[0], principled_bsdf_004.inputs[5])
    links.new(reroute_020.outputs[0], bump_001.inputs[4])
    links.new(reroute_037.outputs[0], principled_bsdf_001.inputs[5])
    links.new(reroute_023.outputs[0], mix_004.inputs[0])
    links.new(reroute_005.outputs[0], mix_shader_004.inputs[2])
    links.new(reroute_038.outputs[0], principled_bsdf_001.inputs[2])
    links.new(reroute_003.outputs[0], mix_shader_001.inputs[1])
    links.new(reroute_031.outputs[0], map_range_001.inputs[0])
    links.new(mix_004.outputs[2], principled_bsdf_001.inputs[0])
    links.new(map_range_001.outputs[0], all_edges_015.inputs[1])
    links.new(mix_shader_004.outputs[0], output_node.inputs[0])
    links.new(map_range_006.outputs[0], math_001.inputs[0])
    links.new(map_range_008.outputs[0], math_003.inputs[1])
    links.new(map_range_007.outputs[0], math_004.inputs[0])
    links.new(map_range_007.outputs[0], math_003.inputs[0])
    links.new(reroute_026.outputs[0], all_edges_014.inputs[0])
    links.new(reroute_039.outputs[0], all_edges_013.inputs[0])
    links.new(reroute_007.outputs[0], mix_shader_004.inputs[0])
    links.new(reroute_019.outputs[0], bump_001.inputs[3])
    links.new(reroute_017.outputs[0], all_edges_013.inputs[1])
    links.new(reroute_040.outputs[0], all_edges_014.inputs[1])
    links.new(all_edges_015.outputs[0], reroute_001.inputs[0])
    links.new(reroute_036.outputs[0], reroute.inputs[0])
    links.new(reroute.outputs[0], all_edges_018.inputs[1])
    links.new(reroute_016.outputs[0], mix_shader_002.inputs[1])
    links.new(reroute_013.outputs[0], reroute_003.inputs[0])
    links.new(reroute_008.outputs[0], reroute_004.inputs[0])
    links.new(reroute_027.outputs[0], reroute_005.inputs[0])
    links.new(reroute_012.outputs[0], reroute_006.inputs[0])
    links.new(principled_bsdf_002.outputs[0], reroute_008.inputs[0])
    links.new(principled_bsdf_004.outputs[0], reroute_009.inputs[0])
    links.new(mix_shader_001.outputs[0], reroute_012.inputs[0])
    links.new(mix_shader_002.outputs[0], reroute_013.inputs[0])
    links.new(reroute_009.outputs[0], reroute_014.inputs[0])
    links.new(reroute_053.outputs[0], reroute_015.inputs[0])
    links.new(input_node.outputs[0], reroute_016.inputs[0])
    links.new(reroute_021.outputs[0], reroute_011.inputs[0])
    links.new(reroute_011.outputs[0], reroute_007.inputs[0])
    links.new(reroute_025.outputs[0], reroute_017.inputs[0])
    links.new(bevel_001.outputs[0], reroute_020.inputs[0])
    links.new(all_edges_013.outputs[0], reroute_021.inputs[0])
    links.new(reroute_021.outputs[0], reroute_019.inputs[0])
    links.new(reroute_022.outputs[0], mix_004.inputs[6])
    links.new(reroute_024.outputs[0], mix_004.inputs[7])
    links.new(all_edges_014.outputs[0], reroute_023.inputs[0])
    links.new(map_range.outputs[0], reroute_025.inputs[0])
    links.new(reroute_028.outputs[0], reroute_026.inputs[0])
    links.new(math_004.outputs[0], reroute_028.inputs[0])
    links.new(all_edges_015.outputs[0], reroute_030.inputs[0])
    links.new(input_node.outputs[5], percentage_to_0_1.inputs[0])
    links.new(input_node.outputs[6], percentage_to_0_1_1.inputs[0])
    links.new(input_node.outputs[7], percentage_to_0_1_2.inputs[0])
    links.new(percentage_to_0_1_2.outputs[0], map_range_002.inputs[3])
    links.new(reroute_032.outputs[0], all_edges_018.inputs[0])
    links.new(reroute_033.outputs[0], reroute_032.inputs[0])
    links.new(percentage_to_0_1_1.outputs[0], reroute_033.inputs[0])
    links.new(bevel.outputs[0], reroute_034.inputs[0])
    links.new(map_range_002.outputs[0], reroute_036.inputs[0])
    links.new(bump_001.outputs[0], reroute_037.inputs[0])
    links.new(reroute_048.outputs[0], reroute_038.inputs[0])
    links.new(reroute_029.outputs[0], reroute_039.inputs[0])
    links.new(reroute_025.outputs[0], reroute_040.inputs[0])
    links.new(principled_bsdf_001.outputs[0], reroute_027.inputs[0])
    links.new(input_node.outputs[1], percentage_to_0_1_3.inputs[0])
    links.new(percentage_to_0_1_3.outputs[0], bevel_001.inputs[0])
    links.new(input_node.outputs[1], percentage_to_0_1_4.inputs[0])
    links.new(percentage_to_0_1_4.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[14], reroute_022.inputs[0])
    links.new(input_node.outputs[16], reroute_024.inputs[0])
    links.new(reroute_010.outputs[0], map_range.inputs[3])
    links.new(input_node.outputs[13], map_range_006.inputs[0])
    links.new(input_node.outputs[12], map_range_011.inputs[0])
    links.new(reroute_041.outputs[0], map_range_007.inputs[0])
    links.new(input_node.outputs[17], map_range_008.inputs[0])
    links.new(map_range_011.outputs[0], reroute_010.inputs[0])
    links.new(input_node.outputs[8], principled_bsdf_002.inputs[0])
    links.new(input_node.outputs[9], map_range_012.inputs[0])
    links.new(reroute_043.outputs[0], all_edges_015.inputs[0])
    links.new(reroute_042.outputs[0], map_range_001.inputs[3])
    links.new(input_node.outputs[10], map_range_013.inputs[0])
    links.new(input_node.outputs[11], map_range_014.inputs[0])
    links.new(input_node.outputs[4], principled_bsdf_004.inputs[0])
    links.new(input_node.outputs[15], reroute_041.inputs[0])
    links.new(map_range_013.outputs[0], reroute_042.inputs[0])
    links.new(map_range_012.outputs[0], reroute_043.inputs[0])
    links.new(reroute_035.outputs[0], bump.inputs[0])
    links.new(reroute_045.outputs[0], bump_001.inputs[0])
    links.new(reroute_044.outputs[0], reroute_045.inputs[0])
    links.new(math_003.outputs[0], reroute_029.inputs[0])
    links.new(reroute_018.outputs[0], math.inputs[0])
    links.new(reroute_015.outputs[0], reroute_046.inputs[0])
    links.new(reroute_047.outputs[0], math.inputs[1])
    links.new(reroute_002.outputs[0], mix_shader_001.inputs[0])
    links.new(math.outputs[0], reroute_002.inputs[0])
    links.new(reroute_001.outputs[0], reroute_018.inputs[0])
    links.new(reroute_046.outputs[0], reroute_047.inputs[0])
    links.new(colorramp_047.outputs[0], reroute_048.inputs[0])
    links.new(reroute_050.outputs[0], reroute_049.inputs[0])
    links.new(colorramp_048.outputs[0], principled_bsdf_004.inputs[2])
    links.new(reroute_049.outputs[0], math_002.inputs[0])
    links.new(all_edges_018.outputs[0], reroute_053.inputs[0])
    links.new(reroute_055.outputs[0], reroute_054.inputs[0])
    links.new(reroute_054.outputs[0], math_002.inputs[1])
    links.new(reroute_053.outputs[0], reroute_055.inputs[0])
    links.new(reroute_055.outputs[0], bump.inputs[2])
    links.new(math_002.outputs[0], colorramp_048.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[1])
    links.new(input_node.outputs[2], hs_bump_control.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_035.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control_001.inputs[1])
    links.new(input_node.outputs[2], hs_bump_control_001.inputs[0])
    links.new(hs_bump_control_001.outputs[0], bump_002.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control_002.inputs[1])
    links.new(input_node.outputs[2], hs_bump_control_002.inputs[0])
    links.new(hs_bump_control_002.outputs[0], reroute_044.inputs[0])
    links.new(percentage_to_0_1.outputs[0], group_033.inputs[0])
    links.new(group_033.outputs[0], reroute_050.inputs[0])
    links.new(group_030.outputs[0], principled_bsdf_002.inputs[2])
    links.new(group_030.outputs[0], reroute_031.inputs[0])
    links.new(map_range_014.outputs[0], group_030.inputs[0])
    links.new(map_range_006.outputs[0], group_034.inputs[0])
    links.new(group_034.outputs[0], colorramp_047.inputs[0])
    links.new(group_029.outputs[0], map_range.inputs[0])
    links.new(math_001.outputs[0], group_029.inputs[0])

    return group