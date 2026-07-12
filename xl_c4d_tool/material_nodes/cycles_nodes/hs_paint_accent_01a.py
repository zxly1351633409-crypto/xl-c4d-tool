import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .edge import edge
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_21c_r import pf_grunge_21c_r
from .pf_grunge_25_r import pf_grunge_25_r


def hs_paint_accent_01a():
    """BL_强调色 - 强调色油漆材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/底色混合"""
    group_name = "BL_强调色"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="污渍缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="污渍颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0000, 0.0000, 0.0000, 1.0000)
    group.interface.new_socket(name="油漆颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.2307, 0.2086, 0.1590, 1.0000)
    group.interface.new_socket(name="油漆粗糙度_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="BSDF", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "粗糙度: 表面粗糙度控制")
    frame_001 = create_frame(nodes, "Frame.001", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_002 = create_frame(nodes, "Frame.002", "污垢: 表面污垢和脏旧效果")

    # === 节点创建 ===
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (802.0, -114.7)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
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
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.12084585428237915
    color_ramp_002.color_ramp.elements[0].color = (0.03848109766840935, 0.03848109766840935, 0.03848109766840935, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.8217513561248779
    color_ramp_002.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (730.0, -102.3)
    label_node(color_ramp_002, "", frame)
    group_004 = nodes.new("ShaderNodeGroup")
    group_004.location = (409.9, -102.3)
    label_node(group_004, "", frame)
    group_004.xl_c4d_gradient_type = '0'
    group_004.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_004.node_tree = pf_grunge_25_r()
    group_009 = nodes.new("ShaderNodeGroup")
    group_009.location = (1400.6, -387.7)
    label_node(group_009, "", frame_001)
    group_009.xl_c4d_gradient_type = '0'
    group_009.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_009.node_tree = edge()
    group_009.inputs[2].default_value = 4.0
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.2118377536535263
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.6284008026123047
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (864.9, -386.8)
    label_node(color_ramp_003, "", frame_001)
    group_005 = nodes.new("ShaderNodeGroup")
    group_005.location = (549.6, -387.7)
    label_node(group_005, "", frame_001)
    group_005.xl_c4d_gradient_type = '0'
    group_005.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_005.node_tree = pf_grunge_21c_r()
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (23.7, -681.8)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mix = nodes.new("ShaderNodeMix")
    mix.location = (1424.6, -101.9)
    label_node(mix, "", frame_002)
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
    color_ramp_004 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_004 | Color Ramp.004
    color_ramp_004.color_ramp.color_mode = 'RGB'
    color_ramp_004.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_004.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_004.color_ramp.elements) > 2:
        color_ramp_004.color_ramp.elements.remove(color_ramp_004.color_ramp.elements[-1])
    while len(color_ramp_004.color_ramp.elements) < 2:
        color_ramp_004.color_ramp.elements.new(0.5)
    color_ramp_004.color_ramp.elements[0].position = 0.43806663155555725
    color_ramp_004.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_004.color_ramp.elements[1].position = 0.601210355758667
    color_ramp_004.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_004
    color_ramp_004.location = (906.2, -101.9)
    label_node(color_ramp_004, "", frame_002)
    group_006 = nodes.new("ShaderNodeGroup")
    group_006.location = (573.6, -101.9)
    label_node(group_006, "", frame_002)
    group_006.xl_c4d_gradient_type = '0'
    group_006.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_006.node_tree = pf_grunge_19_r()
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (375.5, 232.1)
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
    reroute = nodes.new("NodeReroute")
    reroute.location = (287.5, -715.6)
    reroute.socket_idname = 'NodeSocketVector'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1137.8, -349.3)
    label_node(reroute_001, "", frame_002)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1233.9, -278.3)
    label_node(reroute_002, "", frame_002)
    reroute_002.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1233.9, -299.3)
    label_node(reroute_003, "", frame_002)
    reroute_003.socket_idname = 'NodeSocketColor'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1233.9, -256.2)
    label_node(reroute_004, "", frame_002)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1209.9, -487.1)
    label_node(reroute_005, "", frame_001)
    reroute_005.socket_idname = 'NodeSocketColor'
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (335.9, -106.6)
    label_node(map_range, "", frame_002)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 100.0
    map_range.inputs[3].default_value = 0.05000000074505806
    map_range.inputs[4].default_value = 0.27000001072883606
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (219.9, -102.3)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.30000001192092896
    map_range_001.inputs[4].default_value = 1.2000000476837158
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (473.8, -207.8)
    reroute_007.socket_idname = 'NodeSocketFloat'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (653.6, -167.3)
    reroute_008.socket_idname = 'NodeSocketColor'
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (-159.7, -688.9)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.0010000000474974513
    map_range_002.inputs[4].default_value = 0.019999999552965164
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-64.5, -187.2)
    reroute_009.socket_idname = 'NodeSocketFloat'
    bump = nodes.new("ShaderNodeBump")
    bump.location = (426.2, -332.9)
    bump.invert = True
    bump.inputs[1].default_value = 0.0010000000474974513
    bump.inputs[2].default_value = 0.10000000149011612
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-64.5, 664.1)
    reroute_006.socket_idname = 'NodeSocketFloat'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-64.5, 77.6)
    reroute_010.socket_idname = 'NodeSocketFloat'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-115.7, 56.3)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (44.9, -512.0)
    reroute_013.socket_idname = 'NodeSocketColor'
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 4:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.2507549226284027
    color_ramp.color_ramp.elements[1].color = (0.041433341801166534, 0.041433341801166534, 0.041433341801166534, 1.0)
    color_ramp.color_ramp.elements[2].position = 0.5438054800033569
    color_ramp.color_ramp.elements[2].color = (0.10808304697275162, 0.10808304697275162, 0.10808304697275162, 1.0)
    color_ramp.color_ramp.elements[3].position = 0.7341384887695312
    color_ramp.color_ramp.elements[3].color = (0.44374537467956543, 0.44374537467956543, 0.44374537467956543, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (-1.3, 375.4)
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (-64.5, 192.3)
    reroute_014.socket_idname = 'NodeSocketFloat'
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (165.3, -282.3)
    mix_002.data_type = 'FLOAT'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'DIFFERENCE'
    mix_002.clamp_factor = True
    mix_002.clamp_result = True
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[3].default_value = 0.20000000298023224
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[6].default_value = (0.1556, 0.1556, 0.1556, 1.0000)
    mix_002.inputs[7].default_value = (0.5327, 0.4258, 0.4150, 1.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (-64.5, -389.8)
    reroute_016.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (668.4, -269.5)
    reroute_017.socket_idname = 'NodeSocketVector'
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (348.9, -357.2)
    label_node(map_range_003, "", frame_001)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.10000000149011612
    map_range_003.inputs[4].default_value = 0.27000001072883606
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (348.9, -102.1)
    label_node(map_range_004, "", frame_001)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.009999999776482582
    map_range_004.inputs[4].default_value = 0.05000000074505806
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1300.4, -466.2)
    label_node(reroute_015, "", frame_001)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (1017.0, -134.7)
    label_node(reroute_019, "", frame_001)
    reroute_019.socket_idname = 'NodeSocketFloat'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (-161.3, -938.8)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (408.2, -971.6)
    reroute_020.socket_idname = 'NodeSocketFloat'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (408.2, -413.3)
    reroute_021.socket_idname = 'NodeSocketFloat'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (-64.5, -476.5)
    reroute_022.socket_idname = 'NodeSocketFloat'

    # === 节点连接 ===
    links.new(bevel.outputs[0], reroute.inputs[0])
    links.new(reroute_007.outputs[0], principled_bsdf_001.inputs[2])
    links.new(reroute_008.outputs[0], principled_bsdf_001.inputs[0])
    links.new(group_006.outputs[0], color_ramp_004.inputs[0])
    links.new(reroute_004.outputs[0], mix.inputs[0])
    links.new(group_004.outputs[0], color_ramp_002.inputs[0])
    links.new(reroute_005.outputs[0], group_009.inputs[1])
    links.new(group_005.outputs[0], color_ramp_003.inputs[0])
    links.new(reroute_012.outputs[0], mix_001.inputs[6])
    links.new(principled_bsdf_001.outputs[0], output_node.inputs[0])
    links.new(reroute_002.outputs[0], mix.inputs[6])
    links.new(reroute_003.outputs[0], mix.inputs[7])
    links.new(reroute_001.outputs[0], reroute_002.inputs[0])
    links.new(color_ramp_004.outputs[0], reroute_004.inputs[0])
    links.new(color_ramp_003.outputs[0], reroute_005.inputs[0])
    links.new(map_range.outputs[0], group_006.inputs[0])
    links.new(input_node.outputs[7], reroute_001.inputs[0])
    links.new(input_node.outputs[6], reroute_003.inputs[0])
    links.new(input_node.outputs[5], map_range.inputs[0])
    links.new(input_node.outputs[8], map_range_001.inputs[0])
    links.new(map_range_001.outputs[0], group_004.inputs[0])
    links.new(mix_001.outputs[2], reroute_008.inputs[0])
    links.new(map_range_002.outputs[0], bevel.inputs[0])
    links.new(reroute_010.outputs[0], reroute_009.inputs[0])
    links.new(reroute_009.outputs[0], principled_bsdf_001.inputs[1])
    links.new(reroute.outputs[0], bump.inputs[4])
    links.new(reroute_022.outputs[0], bump.inputs[3])
    links.new(reroute_017.outputs[0], principled_bsdf_001.inputs[5])
    links.new(group_009.outputs[0], reroute_006.inputs[0])
    links.new(reroute_014.outputs[0], reroute_010.inputs[0])
    links.new(reroute_010.outputs[0], mix_001.inputs[0])
    links.new(mix.outputs[2], reroute_012.inputs[0])
    links.new(color_ramp_002.outputs[0], reroute_013.inputs[0])
    links.new(color_ramp.outputs[0], mix_001.inputs[7])
    links.new(reroute_006.outputs[0], reroute_014.inputs[0])
    links.new(reroute_014.outputs[0], color_ramp.inputs[0])
    links.new(reroute_009.outputs[0], reroute_016.inputs[0])
    links.new(reroute_016.outputs[0], mix_002.inputs[0])
    links.new(mix_002.outputs[0], reroute_007.inputs[0])
    links.new(reroute_013.outputs[0], mix_002.inputs[2])
    links.new(bump.outputs[0], reroute_017.inputs[0])
    links.new(input_node.outputs[0], map_range_002.inputs[0])
    links.new(map_range_003.outputs[0], group_005.inputs[0])
    links.new(input_node.outputs[3], map_range_003.inputs[0])
    links.new(input_node.outputs[4], map_range_004.inputs[0])
    links.new(reroute_015.outputs[0], group_009.inputs[0])
    links.new(reroute_019.outputs[0], reroute_015.inputs[0])
    links.new(map_range_004.outputs[0], reroute_019.inputs[0])
    links.new(reroute_021.outputs[0], bump.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_020.inputs[0])
    links.new(reroute_020.outputs[0], reroute_021.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control.inputs[1])
    links.new(reroute_016.outputs[0], reroute_022.inputs[0])

    return group