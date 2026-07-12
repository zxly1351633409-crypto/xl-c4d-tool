import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_03_r import pf_grunge_03_r
from .pf_grunge_14_r import pf_grunge_14_r
from .pf_grunge_20_r import pf_grunge_20_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_22e_r import pf_grunge_22e_r


def hs_metal_04a():
    """BL_金属04 - 重度腐蚀金属材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损/凹腔脏污"""
    group_name = "BL_金属04"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹腔脏污_随机", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹腔脏污_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="边缘磨损_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="油漆细节_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆细节_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "脏污: 基于AO的凹腔和表面脏污效果遮罩")
    frame_002 = create_frame(nodes, "Frame.002", "粗糙度: 表面粗糙度控制")
    frame_003 = create_frame(nodes, "Frame.003", "凹凸: 凹凸贴图效果")
    frame_004 = create_frame(nodes, "Frame.004", "油漆细节: 油漆材质的磨损/剥落细节层")
    frame_008 = create_frame(nodes, "Frame.008", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩", (0.09, 0.09, 0.09))

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (398.0, 12.4)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
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
    colorramp_035 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_035 | ColorRamp.035
    colorramp_035.color_ramp.color_mode = 'RGB'
    colorramp_035.color_ramp.hue_interpolation = 'NEAR'
    colorramp_035.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_035.color_ramp.elements) > 2:
        colorramp_035.color_ramp.elements.remove(colorramp_035.color_ramp.elements[-1])
    while len(colorramp_035.color_ramp.elements) < 2:
        colorramp_035.color_ramp.elements.new(0.5)
    colorramp_035.color_ramp.elements[0].position = 0.23448239266872406
    colorramp_035.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_035.color_ramp.elements[1].position = 0.6788244843482971
    colorramp_035.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_035
    colorramp_035.location = (936.9, -126.3)
    label_node(colorramp_035, "", frame_002)
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (616.2, -197.7)
    label_node(group_036, "", frame_002)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_14_r()
    cavity_017 = nodes.new("ShaderNodeGroup")
    cavity_017.location = (1706.2, -102.0)
    label_node(cavity_017, "", frame)
    cavity_017.xl_c4d_gradient_type = '0'
    cavity_017.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_017.node_tree = cavity()
    cavity_017.inputs[2].default_value = 1.0
    group_041 = nodes.new("ShaderNodeGroup")
    group_041.location = (990.2, -199.7)
    label_node(group_041, "", frame)
    group_041.xl_c4d_gradient_type = '0'
    group_041.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_041.node_tree = pf_grunge_03_r()
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (1257.2, -104.0)
    label_node(map_range_007, "", frame)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 1.5
    map_range_007.inputs[3].default_value = -0.009999901056289673
    map_range_007.inputs[4].default_value = 1.0
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    colorramp_036 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_036 | ColorRamp.036
    colorramp_036.color_ramp.color_mode = 'RGB'
    colorramp_036.color_ramp.hue_interpolation = 'NEAR'
    colorramp_036.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_036.color_ramp.elements) > 2:
        colorramp_036.color_ramp.elements.remove(colorramp_036.color_ramp.elements[-1])
    while len(colorramp_036.color_ramp.elements) < 2:
        colorramp_036.color_ramp.elements.new(0.5)
    colorramp_036.color_ramp.elements[0].position = 0.4955917000770569
    colorramp_036.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_036.color_ramp.elements[1].position = 0.5370230078697205
    colorramp_036.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_036
    colorramp_036.location = (939.0, -108.4)
    label_node(colorramp_036, "", frame_003)
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (617.6, -171.8)
    label_node(group_037, "", frame_003)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_22b_r()
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-539.2, -226.1)
    bump.invert = True
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (399.7, -451.8)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[2].default_value = 0.8772727251052856
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
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (1170.1, 52.2)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (-1331.2, -903.5)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (61.2, -770.0)
    bump_001.invert = False
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    colorramp_037 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_037 | ColorRamp.037
    colorramp_037.color_ramp.color_mode = 'RGB'
    colorramp_037.color_ramp.hue_interpolation = 'NEAR'
    colorramp_037.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_037.color_ramp.elements) > 2:
        colorramp_037.color_ramp.elements.remove(colorramp_037.color_ramp.elements[-1])
    while len(colorramp_037.color_ramp.elements) < 3:
        colorramp_037.color_ramp.elements.new(0.5)
    colorramp_037.color_ramp.elements[0].position = 0.4750001132488251
    colorramp_037.color_ramp.elements[0].color = (0.06804414838552475, 0.056222155690193176, 0.043334051966667175, 1.0)
    colorramp_037.color_ramp.elements[1].position = 0.7590909004211426
    colorramp_037.color_ramp.elements[1].color = (0.10410013794898987, 0.02928939461708069, 0.003638840513303876, 1.0)
    colorramp_037.color_ramp.elements[2].position = 0.9636363387107849
    colorramp_037.color_ramp.elements[2].color = (0.050959035754203796, 0.02931380830705166, 0.015891682356595993, 1.0)
    # XL_PF_RAMP_END colorramp_037
    colorramp_037.location = (-43.1, -471.9)
    cavity_018 = nodes.new("ShaderNodeGroup")
    cavity_018.location = (1510.4, -607.7)
    label_node(cavity_018, "", frame)
    cavity_018.xl_c4d_gradient_type = '0'
    cavity_018.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_018.node_tree = cavity()
    cavity_018.inputs[2].default_value = 2.0
    group_042 = nodes.new("ShaderNodeGroup")
    group_042.location = (767.4, -675.6)
    label_node(group_042, "", frame)
    group_042.xl_c4d_gradient_type = '0'
    group_042.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_042.node_tree = pf_grunge_20_r()
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (1056.8, -569.1)
    label_node(map_range_008, "", frame)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 1.0
    map_range_008.inputs[3].default_value = -0.5999999642372131
    map_range_008.inputs[4].default_value = 1.0
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (1778.6, -535.2)
    label_node(mix_003, "", frame)
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_003.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[6].default_value = (0.0140, 0.0140, 0.0140, 1.0000)
    mix_003.inputs[7].default_value = (0.4985, 0.1163, 0.0280, 1.0000)
    mix_003.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (3995.7, 96.5)
    bump_002 = nodes.new("ShaderNodeBump")
    bump_002.location = (2199.4, -178.8)
    bump_002.invert = True
    bump_002.inputs[1].default_value = 1.0
    bump_002.inputs[2].default_value = 0.10000000149011612
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-275.6, -657.0)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (-627.7, -935.6)
    reroute_003.socket_idname = 'NodeSocketVector'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (-13.0, -935.6)
    reroute_004.socket_idname = 'NodeSocketVector'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (-13.0, -1007.8)
    reroute_005.socket_idname = 'NodeSocketVector'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-7.2, -144.8)
    reroute_006.socket_idname = 'NodeSocketVector'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (666.5, -1007.8)
    reroute_007.socket_idname = 'NodeSocketVector'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (176.3, -41.4)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (959.3, 35.5)
    reroute_010.socket_idname = 'NodeSocketFloat'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (2085.6, -319.1)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1366.3, -341.5)
    reroute_013.socket_idname = 'NodeSocketVector'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (-275.6, 35.0)
    reroute_018.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (2085.6, 38.3)
    reroute_016.socket_idname = 'NodeSocketFloat'
    math = nodes.new("ShaderNodeMath")
    math.location = (810.3, -199.8)
    label_node(math, "", frame)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[1].default_value = 0.5
    math.inputs[2].default_value = 0.5
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (767.4, -777.7)
    label_node(math_001, "", frame)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 0.5
    math_001.inputs[2].default_value = 0.5
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (1393.2, -677.3)
    label_node(math_002, "", frame)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 2.0
    math_002.inputs[2].default_value = 0.5
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1241.3, -706.1)
    label_node(reroute_015, "", frame)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (1440.3, -199.7)
    label_node(reroute_017, "", frame)
    reroute_017.socket_idname = 'NodeSocketFloat'
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (1062.1, -329.8)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.009999999776482582
    map_range_001.inputs[4].default_value = 0.38999998569488525
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (1508.5, -364.3)
    label_node(reroute_019, "", frame)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (1334.9, -364.6)
    label_node(reroute_020, "", frame)
    reroute_020.socket_idname = 'NodeSocketFloat'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (1334.9, -681.9)
    label_node(reroute_021, "", frame)
    reroute_021.socket_idname = 'NodeSocketFloat'
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (410.8, -436.8)
    label_node(map_range_002, "", frame)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.05000000074505806
    map_range_002.inputs[4].default_value = 4.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (289.2, -101.6)
    label_node(map_range_003, "", frame_003)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.30000001192092896
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (305.0, -102.3)
    label_node(map_range_004, "", frame_002)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.05000000074505806
    map_range_004.inputs[4].default_value = 1.0799999237060547
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (-275.6, -916.7)
    reroute_022.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (2085.6, -112.5)
    reroute_030.socket_idname = 'NodeSocketFloat'
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (-498.7, 540.5)
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
    group_043 = nodes.new("ShaderNodeGroup")
    group_043.location = (508.4, -107.1)
    label_node(group_043, "", frame_004)
    group_043.xl_c4d_gradient_type = '0'
    group_043.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_043.node_tree = pf_grunge_03_r()
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (1263.2, -205.4)
    label_node(mix_005, "", frame_004)
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    mix_005.blend_type = 'MIX'
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    mix_005.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_005.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[6].default_value = (0.2040, 0.1229, 0.0261, 1.0000)
    mix_005.inputs[7].default_value = (0.0043, 0.0043, 0.0043, 1.0000)
    mix_005.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (800.4, -103.4)
    label_node(map_range_009, "", frame_004)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 1.190000057220459
    map_range_009.inputs[4].default_value = 5.529999732971191
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_007 = nodes.new("ShaderNodeMath")
    math_007.location = (1073.2, -205.4)
    label_node(math_007, "", frame_004)
    math_007.operation = 'DIVIDE'
    math_007.use_clamp = False
    math_007.inputs[1].default_value = 0.8199999928474426
    math_007.inputs[2].default_value = 0.5
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1530.1, -101.7)
    label_node(all_edges_013, "", frame_008)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 4.0
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (805.8, -165.7)
    label_node(group_029, "", frame_008)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_22b_r()
    principled_bsdf_003 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_003.location = (3386.9, -55.9)
    principled_bsdf_003.distribution = 'MULTI_GGX'
    principled_bsdf_003.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_003.inputs[3].default_value = 1.5
    principled_bsdf_003.inputs[4].default_value = 1.0
    principled_bsdf_003.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_003.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_003.inputs[11].default_value = 1.399999976158142
    principled_bsdf_003.inputs[13].default_value = 0.19090907275676727
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
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (1057.9, -167.3)
    label_node(map_range_010, "", frame_008)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[1].default_value = 0.08999999612569809
    map_range_010.inputs[2].default_value = 1.0
    map_range_010.inputs[3].default_value = -0.8499999046325684
    map_range_010.inputs[4].default_value = 1.0
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_016 = nodes.new("ShaderNodeGroup")
    all_edges_016.location = (1528.7, -274.0)
    label_node(all_edges_016, "", frame_008)
    all_edges_016.xl_c4d_gradient_type = '0'
    all_edges_016.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_016.node_tree = all_edges()
    all_edges_016.inputs[2].default_value = 1.0
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (1875.8, -152.0)
    label_node(mix_006, "", frame_008)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[6].default_value = (0.1273, 0.0575, 0.0342, 1.0000)
    mix_006.inputs[7].default_value = (0.0500, 0.0176, 0.0090, 1.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_047 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_047 | ColorRamp.047
    colorramp_047.color_ramp.color_mode = 'RGB'
    colorramp_047.color_ramp.hue_interpolation = 'NEAR'
    colorramp_047.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_047.color_ramp.elements) > 2:
        colorramp_047.color_ramp.elements.remove(colorramp_047.color_ramp.elements[-1])
    while len(colorramp_047.color_ramp.elements) < 2:
        colorramp_047.color_ramp.elements.new(0.5)
    colorramp_047.color_ramp.elements[0].position = 0.0
    colorramp_047.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_047.color_ramp.elements[1].position = 0.64090895652771
    colorramp_047.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_047
    colorramp_047.location = (1053.0, -821.8)
    label_node(colorramp_047, "", frame_008)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (764.1, -923.4)
    label_node(group_034, "", frame_008)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_22e_r()
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1800.6, -133.9)
    label_node(reroute_031, "", frame_008)
    reroute_031.socket_idname = 'NodeSocketFloat'
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (1410.6, 37.1)
    reroute_033.socket_idname = 'NodeSocketFloat'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (1255.4, -200.9)
    label_node(reroute_034, "", frame_008)
    reroute_034.socket_idname = 'NodeSocketFloat'
    math_009 = nodes.new("ShaderNodeMath")
    math_009.location = (562.9, -968.0)
    label_node(math_009, "", frame_008)
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False
    math_009.inputs[1].default_value = 1.100000023841858
    math_009.inputs[2].default_value = 0.5
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (511.0, -258.0)
    label_node(reroute_035, "", frame_008)
    reroute_035.socket_idname = 'NodeSocketFloat'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (511.0, -1073.2)
    label_node(reroute_036, "", frame_008)
    reroute_036.socket_idname = 'NodeSocketFloat'
    math_010 = nodes.new("ShaderNodeMath")
    math_010.location = (1309.0, -213.1)
    label_node(math_010, "", frame_008)
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = False
    math_010.inputs[2].default_value = 0.5
    math_011 = nodes.new("ShaderNodeMath")
    math_011.location = (1309.8, -389.9)
    label_node(math_011, "", frame_008)
    math_011.operation = 'MULTIPLY'
    math_011.use_clamp = False
    math_011.inputs[1].default_value = 0.5
    math_011.inputs[2].default_value = 0.5
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (1120.6, -441.0)
    label_node(reroute_037, "", frame_008)
    reroute_037.socket_idname = 'NodeSocketFloat'
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (326.2, -234.3)
    label_node(map_range_011, "", frame_008)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = 0.25
    map_range_011.inputs[4].default_value = 1.5
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (862.7, -408.6)
    label_node(map_range_012, "", frame_008)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.10000000149011612
    map_range_012.inputs[4].default_value = 1.600000023841858
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (863.5, -650.7)
    label_node(map_range_013, "", frame_008)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = 0.27000001072883606
    map_range_013.inputs[4].default_value = 1.820000171661377
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (1205.2, -686.4)
    label_node(reroute_038, "", frame_008)
    reroute_038.socket_idname = 'NodeSocketFloat'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (1488.5, -201.9)
    label_node(reroute_039, "", frame_008)
    reroute_039.socket_idname = 'NodeSocketFloat'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (1488.5, -374.3)
    label_node(reroute_040, "", frame_008)
    reroute_040.socket_idname = 'NodeSocketFloat'
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (1488.5, -180.1)
    label_node(reroute_041, "", frame_008)
    reroute_041.socket_idname = 'NodeSocketFloat'
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (1470.1, -354.6)
    label_node(reroute_042, "", frame_008)
    reroute_042.socket_idname = 'NodeSocketFloat'
    reroute_043 = nodes.new("NodeReroute")
    reroute_043.location = (1186.3, -494.4)
    label_node(reroute_043, "", frame_008)
    reroute_043.socket_idname = 'NodeSocketFloat'
    reroute_044 = nodes.new("NodeReroute")
    reroute_044.location = (1208.7, -440.0)
    label_node(reroute_044, "", frame_008)
    reroute_044.socket_idname = 'NodeSocketFloat'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1706.3, -150.8)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (1919.7, -133.0)
    label_node(reroute_032, "", frame_004)
    reroute_032.socket_idname = 'NodeSocketFloat'
    reroute_045 = nodes.new("NodeReroute")
    reroute_045.location = (1897.2, -242.2)
    label_node(reroute_045, "", frame_004)
    reroute_045.socket_idname = 'NodeSocketColor'
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (1072.9, -116.0)
    label_node(math_003, "", frame_004)
    math_003.operation = 'SUBTRACT'
    math_003.use_clamp = False
    math_003.inputs[0].default_value = 1.0
    math_003.inputs[2].default_value = 0.5
    reroute_046 = nodes.new("NodeReroute")
    reroute_046.location = (-690.0, 33.9)
    reroute_046.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (2073.3, 1273.3)
    reroute_002.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (2073.3, 1942.3)
    reroute_009.socket_idname = 'NodeSocketColor'
    math_008 = nodes.new("ShaderNodeMath")
    math_008.location = (634.5, -154.3)
    label_node(math_008, "", frame_008)
    math_008.operation = 'ADD'
    math_008.use_clamp = False
    math_008.inputs[1].default_value = 0.5
    math_008.inputs[2].default_value = 0.5
    reroute = nodes.new("NodeReroute")
    reroute.location = (3740.8, -2.0)
    reroute.socket_idname = 'NodeSocketShader'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (2910.3, -109.1)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (2805.1, -150.4)
    reroute_014.socket_idname = 'NodeSocketColor'
    hs_bump_control_001 = nodes.new("ShaderNodeGroup")
    hs_bump_control_001.location = (-1704.3, -905.2)
    hs_bump_control_001.xl_c4d_gradient_type = '0'
    hs_bump_control_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control_001.node_tree = _hs_bump_control_fn()
    hs_bump_control_001.inputs[2].default_value = 0.30000001192092896
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (-1321.2, -851.5)
    reroute_024.socket_idname = 'NodeSocketFloat'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (-987.1, -369.3)
    reroute_025.socket_idname = 'NodeSocketColor'
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (-1643.8, -1110.8)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[4].default_value = 0.009999999776482582
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix = nodes.new("ShaderNodeMix")
    mix.location = (-727.0, -55.1)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'ADD'
    mix.clamp_factor = True
    mix.clamp_result = True
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (-751.8, -210.0)
    reroute_026.socket_idname = 'NodeSocketFloat'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (-751.8, -306.6)
    reroute_027.socket_idname = 'NodeSocketFloat'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (-987.1, -250.5)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (-984.1, -230.6)
    reroute_029.socket_idname = 'NodeSocketColor'
    reroute_047 = nodes.new("NodeReroute")
    reroute_047.location = (-627.7, -390.3)
    reroute_047.socket_idname = 'NodeSocketVector'
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (-984.9, -590.4)
    math_004.operation = 'ADD'
    math_004.use_clamp = False
    math_004.inputs[1].default_value = 0.10000000149011612
    math_004.inputs[2].default_value = 0.5
    reroute_048 = nodes.new("NodeReroute")
    reroute_048.location = (-751.8, -624.8)
    reroute_048.socket_idname = 'NodeSocketFloat'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (-720.2, -851.1)
    reroute_023.socket_idname = 'NodeSocketFloat'
    reroute_049 = nodes.new("NodeReroute")
    reroute_049.location = (-720.2, -306.6)
    reroute_049.socket_idname = 'NodeSocketFloat'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (320.5, -101.9)
    label_node(percentage_to_0_1, "百分比转0-1", frame_004)
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1.inputs[4].default_value = 1.0
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_1.location = (322.4, -347.8)
    label_node(percentage_to_0_1_1, "百分比转0-1", frame_004)
    percentage_to_0_1_1.clamp = True
    percentage_to_0_1_1.interpolation_type = 'LINEAR'
    percentage_to_0_1_1.data_type = 'FLOAT'
    percentage_to_0_1_1.inputs[2].default_value = 100.0
    percentage_to_0_1_1.inputs[3].default_value = 1.0
    percentage_to_0_1_1.inputs[5].default_value = 4.0
    percentage_to_0_1_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)

    # === 节点连接 ===
    links.new(reroute_004.outputs[0], bump_001.inputs[4])
    links.new(reroute_047.outputs[0], bump.inputs[4])
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[2])
    links.new(bump_001.outputs[0], principled_bsdf_001.inputs[5])
    links.new(colorramp_037.outputs[0], principled_bsdf_001.inputs[0])
    links.new(mix_shader.outputs[0], mix_shader_001.inputs[1])
    links.new(group_042.outputs[0], map_range_008.inputs[0])
    links.new(reroute_006.outputs[0], principled_bsdf.inputs[5])
    links.new(group_037.outputs[0], colorramp_036.inputs[0])
    links.new(reroute_008.outputs[0], principled_bsdf.inputs[0])
    links.new(group_041.outputs[0], map_range_007.inputs[0])
    links.new(reroute_001.outputs[0], colorramp_037.inputs[0])
    links.new(group_036.outputs[0], colorramp_035.inputs[0])
    links.new(reroute_011.outputs[0], bump_002.inputs[3])
    links.new(reroute_013.outputs[0], bump_002.inputs[4])
    links.new(reroute_018.outputs[0], reroute_001.inputs[0])
    links.new(bevel.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], reroute_004.inputs[0])
    links.new(reroute_004.outputs[0], reroute_005.inputs[0])
    links.new(bump.outputs[0], reroute_006.inputs[0])
    links.new(reroute_005.outputs[0], reroute_007.inputs[0])
    links.new(mix_004.outputs[2], reroute_008.inputs[0])
    links.new(reroute_010.outputs[0], mix_shader.inputs[0])
    links.new(reroute_018.outputs[0], reroute_010.inputs[0])
    links.new(reroute_030.outputs[0], reroute_011.inputs[0])
    links.new(reroute_007.outputs[0], reroute_013.inputs[0])
    links.new(reroute_016.outputs[0], mix_shader_001.inputs[0])
    links.new(math_001.outputs[0], group_042.inputs[0])
    links.new(math.outputs[0], group_041.inputs[0])
    links.new(map_range_002.outputs[0], math.inputs[0])
    links.new(map_range_008.outputs[0], reroute_015.inputs[0])
    links.new(map_range_007.outputs[0], reroute_017.inputs[0])
    links.new(reroute_021.outputs[0], math_002.inputs[0])
    links.new(map_range_001.outputs[0], reroute_020.inputs[0])
    links.new(reroute_020.outputs[0], reroute_019.inputs[0])
    links.new(reroute_020.outputs[0], reroute_021.inputs[0])
    links.new(input_node.outputs[4], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], math_001.inputs[0])
    links.new(input_node.outputs[10], map_range_004.inputs[0])
    links.new(input_node.outputs[2], map_range_003.inputs[0])
    links.new(input_node.outputs[5], map_range_001.inputs[0])
    links.new(reroute_001.outputs[0], reroute_022.inputs[0])
    links.new(mix_shader_001.outputs[0], output_node.inputs[0])
    links.new(reroute_016.outputs[0], reroute_030.inputs[0])
    links.new(reroute_046.outputs[0], reroute_018.inputs[0])
    links.new(reroute_017.outputs[0], cavity_017.inputs[1])
    links.new(reroute_019.outputs[0], cavity_017.inputs[0])
    links.new(reroute_015.outputs[0], cavity_018.inputs[1])
    links.new(cavity_018.outputs[0], mix_003.inputs[0])
    links.new(math_002.outputs[0], cavity_018.inputs[0])
    links.new(group_043.outputs[0], map_range_009.inputs[0])
    links.new(reroute_032.outputs[0], mix_004.inputs[0])
    links.new(map_range_009.outputs[0], math_007.inputs[0])
    links.new(math_007.outputs[0], mix_005.inputs[0])
    links.new(reroute_012.outputs[0], principled_bsdf_003.inputs[0])
    links.new(group_034.outputs[0], colorramp_047.inputs[0])
    links.new(reroute_014.outputs[0], principled_bsdf_003.inputs[2])
    links.new(reroute_031.outputs[0], reroute_033.inputs[0])
    links.new(map_range_010.outputs[0], reroute_034.inputs[0])
    links.new(reroute_036.outputs[0], math_009.inputs[0])
    links.new(reroute_035.outputs[0], reroute_036.inputs[0])
    links.new(reroute_044.outputs[0], math_010.inputs[0])
    links.new(reroute_043.outputs[0], math_011.inputs[0])
    links.new(map_range_011.outputs[0], reroute_035.inputs[0])
    links.new(map_range_012.outputs[0], reroute_037.inputs[0])
    links.new(reroute_038.outputs[0], math_010.inputs[1])
    links.new(map_range_013.outputs[0], reroute_038.inputs[0])
    links.new(reroute_034.outputs[0], reroute_039.inputs[0])
    links.new(reroute_039.outputs[0], reroute_040.inputs[0])
    links.new(math_010.outputs[0], reroute_041.inputs[0])
    links.new(math_011.outputs[0], reroute_042.inputs[0])
    links.new(reroute_037.outputs[0], reroute_043.inputs[0])
    links.new(reroute_037.outputs[0], reroute_044.inputs[0])
    links.new(math_009.outputs[0], group_034.inputs[0])
    links.new(reroute_039.outputs[0], all_edges_013.inputs[1])
    links.new(all_edges_013.outputs[0], reroute_031.inputs[0])
    links.new(reroute_041.outputs[0], all_edges_013.inputs[0])
    links.new(reroute_040.outputs[0], all_edges_016.inputs[1])
    links.new(all_edges_016.outputs[0], mix_006.inputs[0])
    links.new(reroute_042.outputs[0], all_edges_016.inputs[0])
    links.new(group_029.outputs[0], map_range_010.inputs[0])
    links.new(map_range_003.outputs[0], group_037.inputs[0])
    links.new(reroute_025.outputs[0], bump.inputs[3])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[1])
    links.new(mix_005.outputs[2], reroute_045.inputs[0])
    links.new(mix_003.outputs[2], mix_004.inputs[7])
    links.new(reroute_045.outputs[0], mix_004.inputs[6])
    links.new(map_range_009.outputs[0], math_003.inputs[1])
    links.new(math_003.outputs[0], reroute_032.inputs[0])
    links.new(cavity_017.outputs[0], reroute_046.inputs[0])
    links.new(colorramp_047.outputs[0], reroute_002.inputs[0])
    links.new(mix_006.outputs[2], reroute_009.inputs[0])
    links.new(reroute.outputs[0], mix_shader_001.inputs[2])
    links.new(reroute_033.outputs[0], reroute_016.inputs[0])
    links.new(reroute_035.outputs[0], math_008.inputs[0])
    links.new(math_008.outputs[0], group_029.inputs[0])
    links.new(bump_002.outputs[0], principled_bsdf_003.inputs[5])
    links.new(hs_bump_control.outputs[0], bump_002.inputs[0])
    links.new(principled_bsdf_003.outputs[0], reroute.inputs[0])
    links.new(reroute_009.outputs[0], reroute_012.inputs[0])
    links.new(reroute_002.outputs[0], reroute_014.inputs[0])
    links.new(input_node.outputs[6], map_range_011.inputs[0])
    links.new(input_node.outputs[7], map_range_012.inputs[0])
    links.new(input_node.outputs[7], map_range_013.inputs[0])
    links.new(reroute_022.outputs[0], bump_001.inputs[3])
    links.new(input_node.outputs[1], hs_bump_control_001.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control_001.inputs[1])
    links.new(reroute_023.outputs[0], bump_001.inputs[0])
    links.new(hs_bump_control_001.outputs[0], reroute_024.inputs[0])
    links.new(colorramp_036.outputs[0], reroute_025.inputs[0])
    links.new(input_node.outputs[0], map_range_005.inputs[0])
    links.new(map_range_005.outputs[0], bevel.inputs[0])
    links.new(reroute_026.outputs[0], mix.inputs[0])
    links.new(reroute_028.outputs[0], mix.inputs[7])
    links.new(reroute_029.outputs[0], mix.inputs[6])
    links.new(mix.outputs[2], principled_bsdf.inputs[2])
    links.new(reroute_027.outputs[0], reroute_026.inputs[0])
    links.new(reroute_048.outputs[0], reroute_027.inputs[0])
    links.new(reroute_049.outputs[0], bump.inputs[0])
    links.new(reroute_025.outputs[0], reroute_028.inputs[0])
    links.new(colorramp_035.outputs[0], reroute_029.inputs[0])
    links.new(reroute_003.outputs[0], reroute_047.inputs[0])
    links.new(reroute_024.outputs[0], math_004.inputs[0])
    links.new(math_004.outputs[0], reroute_048.inputs[0])
    links.new(reroute_024.outputs[0], reroute_023.inputs[0])
    links.new(reroute_023.outputs[0], reroute_049.inputs[0])
    links.new(map_range_004.outputs[0], group_036.inputs[0])
    links.new(input_node.outputs[8], percentage_to_0_1.inputs[0])
    links.new(input_node.outputs[9], percentage_to_0_1_1.inputs[0])
    links.new(percentage_to_0_1.outputs[0], group_043.inputs[0])
    links.new(percentage_to_0_1_1.outputs[0], map_range_009.inputs[3])

    return group