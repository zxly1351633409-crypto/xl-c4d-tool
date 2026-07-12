import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .cavity import cavity
from .dent_noise_001_node_tree_001 import dent_noise001_node_tree001
from .dent_noise_001_node_tree_002 import dent_noise001_node_tree002
from .dent_noise_002_node_tree_001 import dent_noise002_node_tree001
from .dent_noise_003_node_tree_001 import dent_noise003_node_tree001
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_14_r import pf_grunge_14_r
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_19c_r import pf_grunge_19c_r
from .pf_grunge_22e_r import pf_grunge_22e_r


def hs_plastic_01a():
    """BL_塑料 - 指纹磨损塑料材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损"""
    group_name = "BL_塑料"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="颜色: 材质颜色通道", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0040, 0.0040, 0.0040, 1.0000)
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="瑕疵缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹陷缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame_001 = create_frame(nodes, "Frame.001", "清漆粗糙度: 清漆(Coat)表面的粗糙度控制")
    frame_002 = create_frame(nodes, "Frame.002", "倒角: 法线倒角检测产生边缘遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "凹凸: 凹凸贴图效果")
    frame_004 = create_frame(nodes, "Frame.004", "粗糙度: 表面粗糙度控制")
    frame_005 = create_frame(nodes, "Frame.005", "颜色: 材质颜色通道")
    frame_006 = create_frame(nodes, "Frame.006", "脏污: 基于AO的凹腔和表面脏污效果遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (166.6, 8.4)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[8].default_value = 0.5
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 1.0
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.10000000149011612
    principled_bsdf.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf.inputs[19].default_value = 0.3499999940395355
    principled_bsdf.inputs[21].default_value = 1.350000023841858
    principled_bsdf.inputs[22].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf.inputs[25].default_value = 0.5
    principled_bsdf.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[30].default_value = 1.3300000429153442
    color_ramp_004 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_004 | Color Ramp.004
    color_ramp_004.color_ramp.color_mode = 'RGB'
    color_ramp_004.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_004.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp_004.color_ramp.elements) > 2:
        color_ramp_004.color_ramp.elements.remove(color_ramp_004.color_ramp.elements[-1])
    while len(color_ramp_004.color_ramp.elements) < 2:
        color_ramp_004.color_ramp.elements.new(0.5)
    color_ramp_004.color_ramp.elements[0].position = 0.14199401438236237
    color_ramp_004.color_ramp.elements[0].color = (0.013669434934854507, 0.013669434934854507, 0.013669434934854507, 1.0)
    color_ramp_004.color_ramp.elements[1].position = 1.0
    color_ramp_004.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_004
    color_ramp_004.location = (-1091.1, -51.4)
    group_006 = nodes.new("ShaderNodeGroup")
    group_006.location = (247.8, -102.1)
    label_node(group_006, "", frame_004)
    group_006.xl_c4d_gradient_type = '0'
    group_006.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_006.node_tree = pf_grunge_19_r()
    mix = nodes.new("ShaderNodeMix")
    mix.location = (-523.1, 236.7)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[7].default_value = (0.0039, 0.0038, 0.0031, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_005 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_005 | Color Ramp.005
    color_ramp_005.color_ramp.color_mode = 'RGB'
    color_ramp_005.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_005.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_005.color_ramp.elements) > 2:
        color_ramp_005.color_ramp.elements.remove(color_ramp_005.color_ramp.elements[-1])
    while len(color_ramp_005.color_ramp.elements) < 2:
        color_ramp_005.color_ramp.elements.new(0.5)
    color_ramp_005.color_ramp.elements[0].position = 0.27190327644348145
    color_ramp_005.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_005.color_ramp.elements[1].position = 0.38972797989845276
    color_ramp_005.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_005
    color_ramp_005.location = (-1091.1, 292.9)
    group_007 = nodes.new("ShaderNodeGroup")
    group_007.location = (247.8, -102.1)
    label_node(group_007, "", frame_005)
    group_007.xl_c4d_gradient_type = '0'
    group_007.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_007.node_tree = pf_grunge_14_r()
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (154.9, -812.5)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[0].default_value = (0.0399, 0.0299, 0.0208, 1.0000)
    principled_bsdf_001.inputs[2].default_value = 0.7792872786521912
    principled_bsdf_001.inputs[3].default_value = 1.5
    principled_bsdf_001.inputs[4].default_value = 1.0
    principled_bsdf_001.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_001.inputs[11].default_value = 1.399999976158142
    principled_bsdf_001.inputs[13].default_value = 0.11631419509649277
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
    mix_shader.location = (785.9, 46.6)
    group_002 = nodes.new("ShaderNodeGroup")
    group_002.location = (-622.6, 739.5)
    group_002.xl_c4d_gradient_type = '0'
    group_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_002.node_tree = cavity()
    group_002.inputs[2].default_value = 1.0
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.3111782968044281
    color_ramp_001.color_ramp.elements[0].color = (0.056417111307382584, 0.056417111307382584, 0.056417111307382584, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.46940451860427856
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (-1091.1, 738.9)
    group_003 = nodes.new("ShaderNodeGroup")
    group_003.location = (247.8, -351.3)
    label_node(group_003, "", frame_006)
    group_003.xl_c4d_gradient_type = '0'
    group_003.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_003.node_tree = pf_grunge_19c_r()
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (416.2, -66.0)
    label_node(bevel, "", frame_002)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-353.7, -518.5)
    bump.invert = True
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    color_ramp_006 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_006 | Color Ramp.006
    color_ramp_006.color_ramp.color_mode = 'RGB'
    color_ramp_006.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_006.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_006.color_ramp.elements) > 2:
        color_ramp_006.color_ramp.elements.remove(color_ramp_006.color_ramp.elements[-1])
    while len(color_ramp_006.color_ramp.elements) < 2:
        color_ramp_006.color_ramp.elements.new(0.5)
    color_ramp_006.color_ramp.elements[0].position = 0.0
    color_ramp_006.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp_006.color_ramp.elements[1].position = 0.20543815195560455
    color_ramp_006.color_ramp.elements[1].color = (0.004827409982681274, 0.004827409982681274, 0.004827409982681274, 1.0)
    # XL_PF_RAMP_END color_ramp_006
    color_ramp_006.location = (-1091.1, -480.9)
    group_008 = nodes.new("ShaderNodeGroup")
    group_008.location = (538.9, -102.2)
    label_node(group_008, "", frame_003)
    group_008.xl_c4d_gradient_type = '0'
    group_008.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_008.node_tree = pf_grunge_22e_r()
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (29.9, -351.3)
    label_node(map_range_001, "", frame_006)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.10000000149011612
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (29.9, -102.1)
    label_node(map_range_002, "", frame_005)
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
    map_range_003.location = (29.9, -102.1)
    label_node(map_range_003, "", frame_004)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.10000000149011612
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (339.9, -105.3)
    label_node(map_range_004, "", frame_003)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.10000000149011612
    map_range_004.inputs[4].default_value = 1.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (636.3, -10.6)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (636.3, -52.4)
    reroute_005.socket_idname = 'NodeSocketShader'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-19.2, -147.3)
    reroute_001.socket_idname = 'NodeSocketVector'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-19.2, -44.9)
    reroute_006.socket_idname = 'NodeSocketColor'
    math = nodes.new("ShaderNodeMath")
    math.location = (-523.1, -59.8)
    math.operation = 'ADD'
    math.use_clamp = True
    math.inputs[2].default_value = 0.5
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (-230.4, 236.7)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[7].default_value = (0.0363, 0.0338, 0.0243, 1.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (-1389.0, -653.7)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = True
    math_001.inputs[2].default_value = 0.5
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.10271894931793213
    color_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.40483367443084717
    color_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (740.3, -380.1)
    label_node(color_ramp, "", frame_003)
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-561.1, -20.0)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-799.6, -513.8)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-382.3, -20.4)
    reroute_010.socket_idname = 'NodeSocketColor'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-561.1, -185.5)
    reroute_011.socket_idname = 'NodeSocketColor'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-715.7, -165.0)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (-683.0, -513.8)
    reroute_013.socket_idname = 'NodeSocketColor'
    group_009 = nodes.new("ShaderNodeGroup")
    group_009.location = (213.0, -112.6)
    label_node(group_009, "", frame_001)
    group_009.xl_c4d_gradient_type = '0'
    group_009.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_009.node_tree = pf_grunge_22e_r()
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.3323265612125397
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.44108712673187256
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (469.9, -102.0)
    label_node(color_ramp_003, "", frame_001)
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-0.0, -589.2)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (-421.4, -1223.2)
    reroute_014.socket_idname = 'NodeSocketColor'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (-319.8, -969.9)
    reroute_015.socket_idname = 'NodeSocketVector'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (-669.0, -853.2)
    reroute_016.socket_idname = 'NodeSocketVector'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (-671.1, 81.0)
    reroute_018.socket_idname = 'NodeSocketColor'
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (339.9, -379.6)
    label_node(map_range_005, "", frame_003)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 1.0
    map_range_005.inputs[3].default_value = 16.0
    map_range_005.inputs[4].default_value = 64.0
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (226.2, -66.0)
    label_node(map_range_006, "", frame_002)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.0020000000949949026
    map_range_006.inputs[4].default_value = 0.03999999910593033
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (-1365.7, 109.5)
    reroute_017.socket_idname = 'NodeSocketColor'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (-1365.7, 555.4)
    reroute_019.socket_idname = 'NodeSocketColor'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (-1365.7, -233.4)
    reroute_021.socket_idname = 'NodeSocketColor'
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (31.4, -101.7)
    label_node(map_range_008, "", frame_006)
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
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (-872.4, 802.3)
    reroute_028.socket_idname = 'NodeSocketFloat'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (-741.4, 659.8)
    reroute_029.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (-757.1, 637.8)
    reroute_030.socket_idname = 'NodeSocketColor'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (-1370.6, 800.6)
    reroute_031.socket_idname = 'NodeSocketFloat'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (420.3, -137.2)
    label_node(reroute_032, "", frame_006)
    reroute_032.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (-2502.6, 481.7)
    reroute_003.socket_idname = 'NodeSocketFloatPercentage'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (-2502.6, 105.7)
    reroute_004.socket_idname = 'NodeSocketFloatPercentage'
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (30.2, -111.4)
    label_node(map_range_009, "", frame_001)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 1.0
    map_range_009.inputs[3].default_value = 0.25
    map_range_009.inputs[4].default_value = 1.2000000476837158
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (-2502.6, -1329.4)
    reroute_033.socket_idname = 'NodeSocketFloatPercentage'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (-995.9, -318.4)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (-570.5, -351.8)
    reroute_002.socket_idname = 'NodeSocketFloat'
    dent_noise = nodes.new("ShaderNodeGroup")
    dent_noise.location = (526.9, -379.7)
    label_node(dent_noise, "", frame_003)
    dent_noise.xl_c4d_gradient_type = '0'
    dent_noise.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    dent_noise.node_tree = dent_noise001_node_tree001()
    dent_noise.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    dent_noise.inputs[3].default_value = 0.3999999761581421
    dent_noise.inputs[4].default_value = 6.0
    dent_noise_001 = nodes.new("ShaderNodeGroup")
    dent_noise_001.location = (0.0, 0.0)
    dent_noise_001.xl_c4d_gradient_type = '0'
    dent_noise_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    dent_noise_001.node_tree = dent_noise001_node_tree002()
    dent_noise_001.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    dent_noise_001.inputs[2].default_value = 5.0
    dent_noise_002 = nodes.new("ShaderNodeGroup")
    dent_noise_002.location = (0.0, 0.0)
    dent_noise_002.xl_c4d_gradient_type = '0'
    dent_noise_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    dent_noise_002.node_tree = dent_noise002_node_tree001()
    dent_noise_002.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    dent_noise_002.inputs[2].default_value = 5.0
    dent_noise_003 = nodes.new("ShaderNodeGroup")
    dent_noise_003.location = (0.0, 0.0)
    dent_noise_003.xl_c4d_gradient_type = '0'
    dent_noise_003.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    dent_noise_003.node_tree = dent_noise003_node_tree001()
    dent_noise_003.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    dent_noise_003.inputs[2].default_value = 5.0

    # === 节点连接 ===
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    links.new(reroute_030.outputs[0], group_002.inputs[1])
    links.new(reroute_006.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_018.outputs[0], mix.inputs[0])
    links.new(reroute_013.outputs[0], bump.inputs[3])
    links.new(math.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_016.outputs[0], bump.inputs[4])
    links.new(reroute_021.outputs[0], color_ramp_004.inputs[0])
    links.new(reroute_001.outputs[0], principled_bsdf.inputs[5])
    links.new(map_range_003.outputs[0], group_006.inputs[0])
    links.new(reroute_017.outputs[0], color_ramp_005.inputs[0])
    links.new(map_range_002.outputs[0], group_007.inputs[0])
    links.new(reroute_019.outputs[0], color_ramp_001.inputs[0])
    links.new(reroute_015.outputs[0], principled_bsdf_001.inputs[5])
    links.new(map_range_001.outputs[0], group_003.inputs[0])
    links.new(reroute_005.outputs[0], mix_shader.inputs[2])
    links.new(reroute.outputs[0], mix_shader.inputs[0])
    links.new(group_002.outputs[0], reroute.inputs[0])
    links.new(principled_bsdf_001.outputs[0], reroute_005.inputs[0])
    links.new(bump.outputs[0], reroute_001.inputs[0])
    links.new(mix_001.outputs[2], reroute_006.inputs[0])
    links.new(map_range_004.outputs[0], group_008.inputs[0])
    links.new(reroute_012.outputs[0], math.inputs[0])
    links.new(reroute_011.outputs[0], math.inputs[1])
    links.new(input_node.outputs[0], mix.inputs[6])
    links.new(mix.outputs[2], mix_001.inputs[6])
    links.new(reroute_010.outputs[0], mix_001.inputs[0])
    links.new(group_008.outputs[0], math_001.inputs[0])
    links.new(color_ramp.outputs[0], math_001.inputs[1])
    links.new(math_001.outputs[0], color_ramp_006.inputs[0])
    links.new(reroute_009.outputs[0], reroute_008.inputs[0])
    links.new(color_ramp_006.outputs[0], reroute_009.inputs[0])
    links.new(reroute_008.outputs[0], reroute_010.inputs[0])
    links.new(reroute_013.outputs[0], reroute_011.inputs[0])
    links.new(color_ramp_004.outputs[0], reroute_012.inputs[0])
    links.new(reroute_009.outputs[0], reroute_013.inputs[0])
    links.new(reroute_007.outputs[0], principled_bsdf.inputs[20])
    links.new(group_009.outputs[0], color_ramp_003.inputs[0])
    links.new(reroute_014.outputs[0], reroute_007.inputs[0])
    links.new(color_ramp_003.outputs[0], reroute_014.inputs[0])
    links.new(reroute_016.outputs[0], reroute_015.inputs[0])
    links.new(bevel.outputs[0], reroute_016.inputs[0])
    links.new(color_ramp_005.outputs[0], reroute_018.inputs[0])
    links.new(map_range_006.outputs[0], bevel.inputs[0])
    links.new(group_007.outputs[0], reroute_017.inputs[0])
    links.new(group_003.outputs[0], reroute_019.inputs[0])
    links.new(group_006.outputs[0], reroute_021.inputs[0])
    links.new(reroute_004.outputs[0], map_range_003.inputs[0])
    links.new(input_node.outputs[7], map_range_001.inputs[0])
    links.new(reroute_003.outputs[0], map_range_002.inputs[0])
    links.new(input_node.outputs[6], map_range_005.inputs[0])
    links.new(input_node.outputs[2], map_range_004.inputs[0])
    links.new(input_node.outputs[8], map_range_008.inputs[0])
    links.new(reroute_029.outputs[0], group_002.inputs[0])
    links.new(reroute_031.outputs[0], reroute_028.inputs[0])
    links.new(reroute_028.outputs[0], reroute_029.inputs[0])
    links.new(color_ramp_001.outputs[0], reroute_030.inputs[0])
    links.new(reroute_032.outputs[0], reroute_031.inputs[0])
    links.new(map_range_008.outputs[0], reroute_032.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(input_node.outputs[1], reroute_004.inputs[0])
    links.new(reroute_033.outputs[0], map_range_009.inputs[0])
    links.new(map_range_009.outputs[0], group_009.inputs[0])
    links.new(reroute_004.outputs[0], reroute_033.inputs[0])
    links.new(reroute_004.outputs[0], reroute_003.inputs[0])
    links.new(input_node.outputs[3], map_range_006.inputs[0])
    links.new(reroute_002.outputs[0], bump.inputs[0])
    links.new(input_node.outputs[4], hs_bump_control.inputs[0])
    links.new(input_node.outputs[5], hs_bump_control.inputs[1])
    links.new(hs_bump_control.outputs[0], reroute_002.inputs[0])
    links.new(map_range_005.outputs[0], dent_noise.inputs[2])
    links.new(dent_noise.outputs[0], color_ramp.inputs[0])

    return group