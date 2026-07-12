import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_14_r import pf_grunge_14_r
from .pf_grunge_22d_r import pf_grunge_22d_r


def hs_metal_01a():
    """BL_金属01 - 多层锈蚀金属材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损/凹腔脏污"""
    group_name = "BL_金属01"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角半径", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_脏污量", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_脏污纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_脏污扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="粗糙度_脏污缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="BSDF", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "凹凸缩放+开关: 控制凹凸贴图的缩放比例和是否启用凹凸效果")
    frame_001 = create_frame(nodes, "Frame.001", "粗糙度: 表面粗糙度控制")
    frame_002 = create_frame(nodes, "Frame.002", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "脏污: 基于AO的凹腔和表面脏污效果遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (2531.0, 37.4)
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
    colorramp_035.color_ramp.elements[0].position = 0.00906344410032034
    colorramp_035.color_ramp.elements[0].color = (0.0595855675637722, 0.0595855675637722, 0.0595855675637722, 1.0)
    colorramp_035.color_ramp.elements[1].position = 1.0
    colorramp_035.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_035
    colorramp_035.location = (1437.9, -102.1)
    label_node(colorramp_035, "", frame_001)
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (522.1, -141.0)
    label_node(group_036, "", frame_001)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_14_r()
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (928.1, -543.2)
    label_node(bevel, "", frame)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (1524.6, -254.0)
    label_node(mix_003, "", frame_003)
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_003.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[6].default_value = (0.0066, 0.0066, 0.0066, 1.0000)
    mix_003.inputs[7].default_value = (0.0433, 0.0333, 0.0230, 1.0000)
    mix_003.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_037 = nodes.new("ShaderNodeGroup")
    group_037.location = (510.3, -393.9)
    label_node(group_037, "", frame_003)
    group_037.xl_c4d_gradient_type = '0'
    group_037.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_037.node_tree = pf_grunge_22d_r()
    group_037.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    cavity_012 = nodes.new("ShaderNodeGroup")
    cavity_012.location = (1041.2, -255.8)
    label_node(cavity_012, "", frame_003)
    cavity_012.xl_c4d_gradient_type = '0'
    cavity_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_012.node_tree = cavity()
    cavity_012.inputs[2].default_value = 1.0
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (796.7, -350.2)
    label_node(map_range_001, "", frame_003)
    map_range_001.clamp = False
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[4].default_value = -0.8399999141693115
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (1479.7, -283.8)
    label_node(all_edges_014, "", frame_002)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 1.0
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (515.7, -263.9)
    label_node(group_030, "", frame_002)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_14_r()
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (818.3, -349.9)
    label_node(map_range, "", frame_002)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = -0.3899998962879181
    map_range.inputs[4].default_value = 0.7400000095367432
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    colorramp_036 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_036 | ColorRamp.036
    colorramp_036.color_ramp.color_mode = 'RGB'
    colorramp_036.color_ramp.hue_interpolation = 'NEAR'
    colorramp_036.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_036.color_ramp.elements) > 2:
        colorramp_036.color_ramp.elements.remove(colorramp_036.color_ramp.elements[-1])
    while len(colorramp_036.color_ramp.elements) < 2:
        colorramp_036.color_ramp.elements.new(0.5)
    colorramp_036.color_ramp.elements[0].position = 0.4622766375541687
    colorramp_036.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_036.color_ramp.elements[1].position = 0.6136364340782166
    colorramp_036.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_036
    colorramp_036.location = (30.4, -263.6)
    label_node(colorramp_036, "", frame)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1230.7, -333.0)
    label_node(bump, "", frame)
    bump.invert = True
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (1049.3, 774.1)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = True
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[7].default_value = (0.1222, 0.1122, 0.1041, 1.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (326.9, -138.2)
    label_node(map_range_002, "", frame_001)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.10000000149011612
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (314.0, -266.3)
    label_node(map_range_003, "", frame_003)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.05000000074505806
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (324.7, -207.5)
    label_node(map_range_004, "", frame_002)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.1599999964237213
    map_range_004.inputs[4].default_value = 4.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1137.1, -176.2)
    label_node(reroute_001, "", frame_001)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1003.4, -61.9)
    reroute_003.socket_idname = 'NodeSocketColor'
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (315.5, -514.7)
    label_node(map_range_005, "", frame_003)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.48000001907348633
    map_range_005.inputs[4].default_value = 1.0
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (797.1, -102.1)
    label_node(map_range_006, "", frame_003)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.05000000074505806
    map_range_006.inputs[4].default_value = 0.75
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (818.3, -101.8)
    label_node(map_range_007, "", frame_002)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.0020000000949949026
    map_range_007.inputs[4].default_value = 0.32999998331069946
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (701.7, -543.2)
    label_node(map_range_009, "", frame)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[4].default_value = 0.009999999776482582
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (849.1, 1296.8)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (849.1, 618.1)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (849.1, -35.0)
    reroute_004.socket_idname = 'NodeSocketFloat'
    mix = nodes.new("ShaderNodeMix")
    mix.location = (728.1, -101.9)
    label_node(mix, "", frame)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[0].default_value = 0.519336998462677
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (733.8, -382.4)
    label_node(hs_bump_control, "", frame)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1168.0, -35.5)
    reroute_005.socket_idname = 'NodeSocketFloat'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (620.8, -276.9)
    label_node(reroute_006, "", frame)
    reroute_006.socket_idname = 'NodeSocketFloat'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (279.6, -651.9)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (491.4, -602.7)
    label_node(reroute_008, "", frame_003)
    reroute_008.socket_idname = 'NodeSocketFloat'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (748.8, -602.7)
    label_node(reroute_009, "", frame_003)
    reroute_009.socket_idname = 'NodeSocketFloat'
    group_038 = nodes.new("ShaderNodeGroup")
    group_038.location = (522.1, -396.8)
    label_node(group_038, "", frame_001)
    group_038.xl_c4d_gradient_type = '0'
    group_038.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_038.node_tree = pf_grunge_14_r()
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (326.9, -394.0)
    label_node(map_range_008, "", frame_001)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.10000000149011612
    map_range_008.inputs[4].default_value = 1.0
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (1903.9, -16.5)
    reroute_010.socket_idname = 'NodeSocketColor'

    # === 节点连接 ===
    links.new(group_037.outputs[0], map_range_001.inputs[0])
    links.new(reroute_002.outputs[0], mix_006.inputs[0])
    links.new(mix_003.outputs[2], mix_006.inputs[6])
    links.new(reroute_010.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_007.outputs[0], colorramp_036.inputs[0])
    links.new(bump.outputs[0], principled_bsdf.inputs[5])
    links.new(reroute_003.outputs[0], principled_bsdf.inputs[2])
    links.new(bevel.outputs[0], bump.inputs[4])
    links.new(reroute_001.outputs[0], colorramp_035.inputs[0])
    links.new(principled_bsdf.outputs[0], output_node.inputs[0])
    links.new(map_range_003.outputs[0], group_037.inputs[1])
    links.new(reroute_009.outputs[0], map_range_001.inputs[3])
    links.new(input_node.outputs[5], map_range_003.inputs[0])
    links.new(input_node.outputs[9], map_range_002.inputs[0])
    links.new(input_node.outputs[7], map_range_004.inputs[0])
    links.new(colorramp_035.outputs[0], reroute_003.inputs[0])
    links.new(input_node.outputs[4], map_range_005.inputs[0])
    links.new(input_node.outputs[6], map_range_006.inputs[0])
    links.new(input_node.outputs[8], map_range_007.inputs[0])
    links.new(mix.outputs[2], bump.inputs[3])
    links.new(input_node.outputs[0], map_range_009.inputs[0])
    links.new(map_range_009.outputs[0], bevel.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])
    links.new(reroute_005.outputs[0], principled_bsdf.inputs[1])
    links.new(reroute_002.outputs[0], reroute_004.inputs[0])
    links.new(map_range.outputs[0], all_edges_014.inputs[1])
    links.new(map_range_007.outputs[0], all_edges_014.inputs[0])
    links.new(all_edges_014.outputs[0], reroute.inputs[0])
    links.new(map_range_001.outputs[0], cavity_012.inputs[1])
    links.new(cavity_012.outputs[0], mix_003.inputs[0])
    links.new(map_range_006.outputs[0], cavity_012.inputs[0])
    links.new(group_030.outputs[0], map_range.inputs[0])
    links.new(group_036.outputs[0], reroute_001.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control.inputs[1])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(colorramp_036.outputs[0], mix.inputs[7])
    links.new(reroute_004.outputs[0], reroute_005.inputs[0])
    links.new(reroute_006.outputs[0], mix.inputs[6])
    links.new(reroute_005.outputs[0], reroute_006.inputs[0])
    links.new(map_range_005.outputs[0], reroute_008.inputs[0])
    links.new(reroute_008.outputs[0], reroute_009.inputs[0])
    links.new(group_038.outputs[0], reroute_007.inputs[0])
    links.new(input_node.outputs[3], map_range_008.inputs[0])
    links.new(mix_006.outputs[2], reroute_010.inputs[0])
    links.new(map_range_008.outputs[0], group_038.inputs[0])
    links.new(map_range_002.outputs[0], group_036.inputs[0])
    links.new(map_range_004.outputs[0], group_030.inputs[0])

    return group