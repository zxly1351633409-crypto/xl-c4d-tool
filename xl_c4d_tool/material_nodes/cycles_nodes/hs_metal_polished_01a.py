import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .edge import edge
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_21c_r import pf_grunge_21c_r
from .pf_grunge_25_r import pf_grunge_25_r


def hs_metal_polished_01a():
    """BL_抛光金属 - 光滑抛光金属材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污"""
    group_name = "BL_抛光金属"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="污渍缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘损伤_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘损伤_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "粗糙度: 表面粗糙度控制")
    frame_001 = create_frame(nodes, "Frame.001", "颜色: 材质颜色通道")
    frame_002 = create_frame(nodes, "Frame.002", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "倒角: 法线倒角检测产生边缘遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (664.9, -46.9)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.2000000476837158
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
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.0
    color_ramp_002.color_ramp.elements[0].color = (0.3489055633544922, 0.3489055633544922, 0.3489055633544922, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 1.0
    color_ramp_002.color_ramp.elements[1].color = (0.1699446439743042, 0.1699446439743042, 0.1699446439743042, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (926.3, -102.1)
    label_node(color_ramp_002, "", frame)
    group_004 = nodes.new("ShaderNodeGroup")
    group_004.location = (520.1, -102.1)
    label_node(group_004, "", frame)
    group_004.xl_c4d_gradient_type = '0'
    group_004.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_004.node_tree = pf_grunge_25_r()
    group_009 = nodes.new("ShaderNodeGroup")
    group_009.location = (1334.7, -394.0)
    label_node(group_009, "", frame_002)
    group_009.xl_c4d_gradient_type = '0'
    group_009.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_009.node_tree = edge()
    group_009.inputs[2].default_value = 1.0
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.3481457829475403
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.9123867154121399
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (926.3, -397.7)
    label_node(color_ramp_003, "", frame_002)
    group_005 = nodes.new("ShaderNodeGroup")
    group_005.location = (568.1, -397.7)
    label_node(group_005, "", frame_002)
    group_005.xl_c4d_gradient_type = '0'
    group_005.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_005.node_tree = pf_grunge_21c_r()
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (664.9, -415.6)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[0].default_value = (0.0214, 0.0214, 0.0214, 1.0000)
    principled_bsdf_001.inputs[2].default_value = 0.5835440754890442
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
    mix_shader.location = (1232.8, -1.9)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (556.4, -101.9)
    label_node(bevel, "", frame_003)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mix = nodes.new("ShaderNodeMix")
    mix.location = (1336.2, -102.1)
    label_node(mix, "", frame_001)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[6].default_value = (0.1325, 0.1325, 0.1325, 1.0000)
    mix.inputs[7].default_value = (0.0354, 0.0141, 0.0043, 1.0000)
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
    color_ramp_004.color_ramp.elements[0].position = 0.4773400127887726
    color_ramp_004.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_004.color_ramp.elements[1].position = 0.555891215801239
    color_ramp_004.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_004
    color_ramp_004.location = (926.5, -102.1)
    label_node(color_ramp_004, "", frame_001)
    group_006 = nodes.new("ShaderNodeGroup")
    group_006.location = (542.9, -102.1)
    label_node(group_006, "", frame_001)
    group_006.xl_c4d_gradient_type = '0'
    group_006.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_006.node_tree = pf_grunge_19_r()
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (353.2, -104.2)
    label_node(map_range, "", frame_003)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 100.0
    map_range.inputs[3].default_value = 0.0010000000474974513
    map_range.inputs[4].default_value = 0.019999999552965164
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (409.0, 701.4)
    reroute.socket_idname = 'NodeSocketFloat'
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (352.9, -102.1)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.10000000149011612
    map_range_001.inputs[4].default_value = 1.9800000190734863
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (353.1, -102.1)
    label_node(map_range_002, "", frame_001)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.05000000074505806
    map_range_002.inputs[4].default_value = 0.75
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (352.9, -373.9)
    label_node(map_range_003, "", frame_002)
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
    map_range_004.location = (352.9, -102.3)
    label_node(map_range_004, "", frame_002)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.009999999776482582
    map_range_004.inputs[4].default_value = 0.30000001192092896
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1098.4, -135.1)
    label_node(reroute_002, "", frame_002)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1471.8, -135.7)
    label_node(reroute_003, "", frame)
    reroute_003.socket_idname = 'NodeSocketColor'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (10.8, 332.3)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1462.6, -135.7)
    label_node(reroute_001, "", frame_003)
    reroute_001.socket_idname = 'NodeSocketVector'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (58.0, -569.3)
    reroute_005.socket_idname = 'NodeSocketVector'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (58.0, -202.0)
    reroute_006.socket_idname = 'NodeSocketVector'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-34.2, -160.8)
    reroute_007.socket_idname = 'NodeSocketColor'
    invert_color = nodes.new("ShaderNodeInvert")
    invert_color.location = (134.8, 70.6)
    invert_color.inputs[0].default_value = 1.0
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (1200.1, -331.4)
    label_node(reroute_008, "", frame_001)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (1200.1, -136.5)
    label_node(reroute_009, "", frame_001)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-75.6, 132.9)
    reroute_010.socket_idname = 'NodeSocketColor'
    math = nodes.new("ShaderNodeMath")
    math.location = (133.3, -35.3)
    math.operation = 'MAXIMUM'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (87.4, -140.3)
    reroute_011.socket_idname = 'NodeSocketColor'

    # === 节点连接 ===
    links.new(reroute.outputs[0], mix_shader.inputs[0])
    links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[2])
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    links.new(color_ramp_003.outputs[0], group_009.inputs[1])
    links.new(group_006.outputs[0], color_ramp_004.inputs[0])
    links.new(group_005.outputs[0], color_ramp_003.inputs[0])
    links.new(math.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_004.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_009.outputs[0], mix.inputs[0])
    links.new(group_004.outputs[0], color_ramp_002.inputs[0])
    links.new(reroute_005.outputs[0], principled_bsdf_001.inputs[5])
    links.new(reroute_006.outputs[0], principled_bsdf.inputs[5])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(group_009.outputs[0], reroute.inputs[0])
    links.new(map_range_002.outputs[0], group_006.inputs[0])
    links.new(map_range_001.outputs[0], group_004.inputs[0])
    links.new(map_range.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[2], map_range.inputs[0])
    links.new(input_node.outputs[0], map_range_001.inputs[0])
    links.new(input_node.outputs[1], map_range_002.inputs[0])
    links.new(input_node.outputs[3], map_range_003.inputs[0])
    links.new(input_node.outputs[4], map_range_004.inputs[0])
    links.new(map_range_003.outputs[0], group_005.inputs[0])
    links.new(reroute_002.outputs[0], group_009.inputs[0])
    links.new(map_range_004.outputs[0], reroute_002.inputs[0])
    links.new(color_ramp_002.outputs[0], reroute_003.inputs[0])
    links.new(mix.outputs[2], reroute_004.inputs[0])
    links.new(bevel.outputs[0], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], reroute_005.inputs[0])
    links.new(reroute_001.outputs[0], reroute_006.inputs[0])
    links.new(reroute_003.outputs[0], reroute_007.inputs[0])
    links.new(reroute_009.outputs[0], reroute_008.inputs[0])
    links.new(color_ramp_004.outputs[0], reroute_009.inputs[0])
    links.new(reroute_008.outputs[0], reroute_010.inputs[0])
    links.new(reroute_010.outputs[0], invert_color.inputs[1])
    links.new(invert_color.outputs[0], principled_bsdf.inputs[1])
    links.new(reroute_007.outputs[0], math.inputs[1])
    links.new(reroute_011.outputs[0], math.inputs[0])
    links.new(reroute_010.outputs[0], reroute_011.inputs[0])

    return group