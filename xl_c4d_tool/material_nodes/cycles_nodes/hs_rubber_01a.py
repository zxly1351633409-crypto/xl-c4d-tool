import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .cavity import cavity
from .edge import edge
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_14_r import pf_grunge_14_r
from .pf_grunge_17c_r import pf_grunge_17c_r
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_20_r import pf_grunge_20_r as _pf_grunge_20_r_fn
from .pf_grunge_21c_r import pf_grunge_21c_r
from .pf_grunge_23_r import pf_grunge_23_r
from .perlin_noise_001_node_tree_004 import perlin_noise001_node_tree004
from .perlin_noise_001_node_tree_005 import perlin_noise001_node_tree005
from .perlin_noise_002_node_tree_004 import perlin_noise002_node_tree004
from .perlin_noise_003_node_tree_004 import perlin_noise003_node_tree004


def hs_rubber_01a():
    """BL_橡胶01 - 基础橡胶材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损"""
    group_name = "BL_橡胶01"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污凹腔", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘损伤", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "凹凸: 凹凸贴图效果")
    frame_001 = create_frame(nodes, "Frame.001", "凹腔: AO采样检测凹面/凸面区域生成遮罩")
    frame_002 = create_frame(nodes, "Frame.002", "粗糙度: 表面粗糙度控制")
    frame_003 = create_frame(nodes, "Frame.003", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_004 = create_frame(nodes, "Frame.004", "脏污: 基于AO的凹腔和表面脏污效果遮罩")
    frame_005 = create_frame(nodes, "Frame.005", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (-393.9, 53.3)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.1909089982509613
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
    group_002 = nodes.new("ShaderNodeGroup")
    group_002.location = (1413.8, -286.4)
    label_node(group_002, "", frame_001)
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
    color_ramp_001.color_ramp.elements[0].position = 0.051359523087739944
    color_ramp_001.color_ramp.elements[0].color = (0.0052530644461512566, 0.0052530644461512566, 0.0052530644461512566, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.46940451860427856
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (505.3, -354.9)
    label_node(color_ramp_001, "", frame_001)
    value_001 = nodes.new("ShaderNodeValue")
    value_001.location = (29.6, -354.9)
    label_node(value_001, "", frame_001)
    group_009 = nodes.new("ShaderNodeGroup")
    group_009.location = (1413.9, -101.9)
    label_node(group_009, "", frame_003)
    group_009.xl_c4d_gradient_type = '0'
    group_009.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_009.node_tree = edge()
    group_009.inputs[2].default_value = 3.0
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.23636361956596375
    color_ramp_002.color_ramp.elements[0].color = (0.00910858903080225, 0.00910858903080225, 0.00910858903080225, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 1.0
    color_ramp_002.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (506.0, -402.9)
    label_node(color_ramp_002, "", frame_003)
    value_002 = nodes.new("ShaderNodeValue")
    value_002.location = (30.3, -402.9)
    label_node(value_002, "", frame_003)
    group_004 = nodes.new("ShaderNodeGroup")
    group_004.location = (242.8, -402.9)
    label_node(group_004, "", frame_003)
    group_004.xl_c4d_gradient_type = '0'
    group_004.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_004.node_tree = pf_grunge_21c_r()
    mix = nodes.new("ShaderNodeMix")
    mix.location = (-1425.4, 33.3)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[7].default_value = (0.0597, 0.0396, 0.0348, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (-1733.4, 33.3)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[7].default_value = (0.0201, 0.0177, 0.0167, 1.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (1226.0, -576.6)
    label_node(bevel, "", frame)
    bevel.samples = 32
    bevel.inputs[0].default_value = 0.004999999888241291
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1415.2, -344.2)
    label_node(bump, "", frame)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    rgb = nodes.new("ShaderNodeRGB")
    rgb.location = (1413.9, -283.9)
    label_node(rgb, "", frame_003)
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.0
    color_ramp_003.color_ramp.elements[0].color = (0.9624618291854858, 0.9624618291854858, 0.9624618291854858, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.6000000834465027
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (801.8, -346.6)
    label_node(color_ramp_003, "", frame)
    group_005 = nodes.new("ShaderNodeGroup")
    group_005.location = (479.9, -346.6)
    label_node(group_005, "", frame)
    group_005.xl_c4d_gradient_type = '0'
    group_005.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_005.node_tree = pf_grunge_23_r()
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (1817.4, 100.4)
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (1144.4, -45.6)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[0].default_value = (0.0192, 0.0192, 0.0192, 1.0000)
    principled_bsdf_001.inputs[2].default_value = 0.6761814951896667
    principled_bsdf_001.inputs[3].default_value = 1.5
    principled_bsdf_001.inputs[4].default_value = 1.0
    principled_bsdf_001.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_001.inputs[11].default_value = 1.399999976158142
    principled_bsdf_001.inputs[13].default_value = 0.16818171739578247
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
    color_ramp_006 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_006 | Color Ramp.006
    color_ramp_006.color_ramp.color_mode = 'RGB'
    color_ramp_006.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_006.color_ramp.interpolation = 'B_SPLINE'
    while len(color_ramp_006.color_ramp.elements) > 2:
        color_ramp_006.color_ramp.elements.remove(color_ramp_006.color_ramp.elements[-1])
    while len(color_ramp_006.color_ramp.elements) < 2:
        color_ramp_006.color_ramp.elements.new(0.5)
    color_ramp_006.color_ramp.elements[0].position = 0.24169179797172546
    color_ramp_006.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_006.color_ramp.elements[1].position = 0.6042298078536987
    color_ramp_006.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_006
    color_ramp_006.location = (782.3, -82.6)
    label_node(color_ramp_006, "", frame_002)
    group_006 = nodes.new("ShaderNodeGroup")
    group_006.location = (484.6, -84.0)
    label_node(group_006, "", frame_002)
    group_006.xl_c4d_gradient_type = '0'
    group_006.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_006.node_tree = pf_grunge_14_r()
    group_010 = nodes.new("ShaderNodeGroup")
    group_010.location = (1022.2, -343.8)
    label_node(group_010, "", frame_005)
    group_010.xl_c4d_gradient_type = '0'
    group_010.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_010.node_tree = edge()
    group_010.inputs[2].default_value = 3.0
    color_ramp_008 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_008 | Color Ramp.008
    color_ramp_008.color_ramp.color_mode = 'RGB'
    color_ramp_008.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_008.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_008.color_ramp.elements) > 2:
        color_ramp_008.color_ramp.elements.remove(color_ramp_008.color_ramp.elements[-1])
    while len(color_ramp_008.color_ramp.elements) < 2:
        color_ramp_008.color_ramp.elements.new(0.5)
    color_ramp_008.color_ramp.elements[0].position = 0.4355122447013855
    color_ramp_008.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_008.color_ramp.elements[1].position = 0.6042298078536987
    color_ramp_008.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_008
    color_ramp_008.location = (581.6, -355.6)
    label_node(color_ramp_008, "", frame_005)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (895.4, -167.8)
    bump_001.invert = True
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 2.0
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (-1117.3, 33.3)
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[7].default_value = (0.0080, 0.0074, 0.0070, 1.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_005 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_005 | Color Ramp.005
    color_ramp_005.color_ramp.color_mode = 'RGB'
    color_ramp_005.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_005.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_005.color_ramp.elements) > 2:
        color_ramp_005.color_ramp.elements.remove(color_ramp_005.color_ramp.elements[-1])
    while len(color_ramp_005.color_ramp.elements) < 2:
        color_ramp_005.color_ramp.elements.new(0.5)
    color_ramp_005.color_ramp.elements[0].position = 0.39220017194747925
    color_ramp_005.color_ramp.elements[0].color = (0.0052530644461512566, 0.0052530644461512566, 0.0052530644461512566, 1.0)
    color_ramp_005.color_ramp.elements[1].position = 0.8363639116287231
    color_ramp_005.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_005
    color_ramp_005.location = (791.1, -102.2)
    label_node(color_ramp_005, "", frame_004)
    group_011 = nodes.new("ShaderNodeGroup")
    group_011.location = (527.9, -102.2)
    label_node(group_011, "", frame_004)
    group_011.xl_c4d_gradient_type = '0'
    group_011.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_011.node_tree = pf_grunge_17c_r()
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (2667.1, 145.3)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (1144.4, -740.8)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[0].default_value = (0.0864, 0.0682, 0.0579, 1.0000)
    principled_bsdf_002.inputs[2].default_value = 0.7033718228340149
    principled_bsdf_002.inputs[3].default_value = 1.5
    principled_bsdf_002.inputs[4].default_value = 1.0
    principled_bsdf_002.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_002.inputs[11].default_value = 1.399999976158142
    principled_bsdf_002.inputs[13].default_value = 0.16818171739578247
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
    group_007 = nodes.new("ShaderNodeGroup")
    group_007.location = (1310.1, 929.0)
    group_007.xl_c4d_gradient_type = '0'
    group_007.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_007.node_tree = cavity()
    group_007.inputs[2].default_value = 1.0
    color_ramp_007 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_007 | Color Ramp.007
    color_ramp_007.color_ramp.color_mode = 'RGB'
    color_ramp_007.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_007.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_007.color_ramp.elements) > 2:
        color_ramp_007.color_ramp.elements.remove(color_ramp_007.color_ramp.elements[-1])
    while len(color_ramp_007.color_ramp.elements) < 2:
        color_ramp_007.color_ramp.elements.new(0.5)
    color_ramp_007.color_ramp.elements[0].position = 0.28398793935775757
    color_ramp_007.color_ramp.elements[0].color = (0.0052530644461512566, 0.0052530644461512566, 0.0052530644461512566, 1.0)
    color_ramp_007.color_ramp.elements[1].position = 0.4935738146305084
    color_ramp_007.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_007
    color_ramp_007.location = (911.5, 929.0)
    pf_grunge_20_r = nodes.new("ShaderNodeGroup")
    pf_grunge_20_r.location = (411.3, -357.3)
    label_node(pf_grunge_20_r, "", frame_005)
    pf_grunge_20_r.xl_c4d_gradient_type = '0'
    pf_grunge_20_r.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    pf_grunge_20_r.node_tree = _pf_grunge_20_r_fn()
    pf_grunge_19_r_003 = nodes.new("ShaderNodeGroup")
    pf_grunge_19_r_003.location = (242.1, -354.9)
    label_node(pf_grunge_19_r_003, "", frame_001)
    pf_grunge_19_r_003.xl_c4d_gradient_type = '0'
    pf_grunge_19_r_003.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    pf_grunge_19_r_003.node_tree = pf_grunge_19_r()
    pf_grunge_19_r_004 = nodes.new("ShaderNodeGroup")
    pf_grunge_19_r_004.location = (709.0, 929.0)
    pf_grunge_19_r_004.xl_c4d_gradient_type = '0'
    pf_grunge_19_r_004.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    pf_grunge_19_r_004.node_tree = pf_grunge_19_r()
    reroute = nodes.new("NodeReroute")
    reroute.location = (-1570.7, 1097.4)
    reroute.socket_idname = 'NodeSocketColor'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (-1742.0, 423.9)
    reroute_001.socket_idname = 'NodeSocketFloat'
    bevel_001 = nodes.new("ShaderNodeBevel")
    bevel_001.location = (616.4, -457.7)
    bevel_001.samples = 32
    bevel_001.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (249.6, 535.8)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (2327.8, 48.1)
    reroute_003.socket_idname = 'NodeSocketShader'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (2326.2, 88.5)
    reroute_004.socket_idname = 'NodeSocketFloat'
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (603.1, -151.7)
    label_node(map_range, "", frame_003)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 100.0
    map_range.inputs[3].default_value = 0.029999999329447746
    map_range.inputs[4].default_value = 0.6800000071525574
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (602.3, -102.3)
    label_node(map_range_001, "", frame_001)
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
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (351.4, -104.7)
    label_node(map_range_002, "", frame_004)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.20000000298023224
    map_range_002.inputs[4].default_value = 1.5
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (-521.7, -106.1)
    reroute_005.socket_idname = 'NodeSocketVector'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-574.8, -41.5)
    reroute_006.socket_idname = 'NodeSocketColor'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (1133.0, 42.4)
    reroute_007.socket_idname = 'NodeSocketFloat'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (734.8, -309.2)
    reroute_008.socket_idname = 'NodeSocketFloat'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (1510.5, 0.8)
    reroute_009.socket_idname = 'NodeSocketShader'
    math = nodes.new("ShaderNodeMath")
    math.location = (1143.2, -369.1)
    label_node(math, "", frame)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (289.9, -346.6)
    label_node(map_range_003, "", frame)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.009999999776482582
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (288.4, -102.2)
    label_node(map_range_004, "", frame)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.0010000000474974513
    map_range_004.inputs[4].default_value = 0.10000000149011612
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-1117.3, -898.3)
    reroute_011.socket_idname = 'NodeSocketVector'
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (301.0, -84.6)
    label_node(map_range_005, "", frame_002)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.07999999821186066
    map_range_005.inputs[4].default_value = 1.190000057220459
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (250.7, -357.1)
    label_node(map_range_006, "", frame_005)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.10000000149011612
    map_range_006.inputs[4].default_value = 0.48000001907348633
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (251.6, -102.4)
    label_node(map_range_007, "", frame_005)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.004999999888241291
    map_range_007.inputs[4].default_value = 0.09000003337860107
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (853.9, -135.7)
    label_node(reroute_012, "", frame_005)
    reroute_012.socket_idname = 'NodeSocketFloat'
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (486.8, -36.3)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (533.0, 930.1)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.10000000149011612
    map_range_008.inputs[4].default_value = 1.7899999618530273
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (545.8, 1177.5)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[3].default_value = 0.009999999776482582
    map_range_009.inputs[4].default_value = 0.5300000309944153
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (1123.2, 1139.2)
    reroute_013.socket_idname = 'NodeSocketFloat'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1136.3, -171.9)
    label_node(hs_bump_control, "", frame)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (33.3, -724.6)
    reroute_010.socket_idname = 'NodeSocketFloat'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (514.0, -248.4)
    reroute_014.socket_idname = 'NodeSocketFloat'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (457.0, -457.7)
    label_node(percentage_to_0_1, "百分比转0-1")
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[4].default_value = 0.019999999552965164
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (857.8, -330.9)
    reroute_015.socket_idname = 'NodeSocketVector'
    perlin_noise = nodes.new("ShaderNodeGroup")
    perlin_noise.location = (159.6, -131.5)
    perlin_noise.xl_c4d_gradient_type = '0'
    perlin_noise.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise.node_tree = perlin_noise001_node_tree004()
    perlin_noise.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise.inputs[2].default_value = 55.119998931884766
    perlin_noise.inputs[3].default_value = 4.190000057220459
    perlin_noise.inputs[5].default_value = 5.630000114440918
    perlin_noise.inputs[7].default_value = 60.0
    perlin_noise.inputs[9].default_value = 1.0
    perlin_noise_001 = nodes.new("ShaderNodeGroup")
    perlin_noise_001.location = (0.0, 0.0)
    perlin_noise_001.xl_c4d_gradient_type = '0'
    perlin_noise_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise_001.node_tree = perlin_noise001_node_tree005()
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
    perlin_noise_002.node_tree = perlin_noise002_node_tree004()
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
    perlin_noise_003.node_tree = perlin_noise003_node_tree004()
    perlin_noise_003.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise_003.inputs[2].default_value = 8.0
    perlin_noise_003.inputs[3].default_value = 10.0
    perlin_noise_003.inputs[5].default_value = 2.0
    perlin_noise_003.inputs[7].default_value = 60.0
    perlin_noise_003.inputs[9].default_value = 1.0

    # === 节点连接 ===
    links.new(group_009.outputs[0], mix_001.inputs[0])
    links.new(reroute_011.outputs[0], principled_bsdf_002.inputs[5])
    links.new(color_ramp_002.outputs[0], group_009.inputs[1])
    links.new(mix_shader.outputs[0], mix_shader_001.inputs[1])
    links.new(value_002.outputs[0], group_004.inputs[0])
    links.new(reroute_007.outputs[0], mix_shader.inputs[0])
    links.new(group_007.outputs[0], reroute_004.inputs[0])
    links.new(group_004.outputs[0], color_ramp_002.inputs[0])
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    links.new(principled_bsdf_002.outputs[0], reroute_003.inputs[0])
    links.new(reroute_009.outputs[0], mix_shader.inputs[2])
    links.new(group_010.outputs[0], reroute_002.inputs[0])
    links.new(reroute_006.outputs[0], principled_bsdf.inputs[2])
    links.new(group_002.outputs[0], reroute_001.inputs[0])
    links.new(mix_001.outputs[2], mix.inputs[6])
    links.new(color_ramp_005.outputs[0], reroute.inputs[0])
    links.new(reroute_015.outputs[0], bump_001.inputs[4])
    links.new(pf_grunge_19_r_004.outputs[0], color_ramp_007.inputs[0])
    links.new(mix_002.outputs[2], principled_bsdf.inputs[0])
    links.new(reroute.outputs[0], mix_002.inputs[0])
    links.new(pf_grunge_19_r_003.outputs[0], color_ramp_001.inputs[0])
    links.new(value_001.outputs[0], pf_grunge_19_r_003.inputs[0])
    links.new(group_011.outputs[0], color_ramp_005.inputs[0])
    links.new(pf_grunge_20_r.outputs[0], color_ramp_008.inputs[0])
    links.new(mix.outputs[2], mix_002.inputs[6])
    links.new(reroute_005.outputs[0], principled_bsdf.inputs[5])
    links.new(group_006.outputs[0], color_ramp_006.inputs[0])
    links.new(color_ramp_008.outputs[0], group_010.inputs[1])
    links.new(reroute_008.outputs[0], bump_001.inputs[3])
    links.new(reroute_004.outputs[0], mix_shader_001.inputs[0])
    links.new(bump_001.outputs[0], principled_bsdf_001.inputs[5])
    links.new(color_ramp_007.outputs[0], group_007.inputs[1])
    links.new(rgb.outputs[0], mix_001.inputs[6])
    links.new(reroute_001.outputs[0], mix.inputs[0])
    links.new(color_ramp_001.outputs[0], group_002.inputs[1])
    links.new(group_005.outputs[0], color_ramp_003.inputs[0])
    links.new(math.outputs[0], bump.inputs[3])
    links.new(bevel.outputs[0], bump.inputs[4])
    links.new(reroute_003.outputs[0], mix_shader_001.inputs[2])
    links.new(mix_shader_001.outputs[0], output_node.inputs[0])
    links.new(map_range.outputs[0], group_009.inputs[0])
    links.new(input_node.outputs[8], map_range.inputs[0])
    links.new(map_range_001.outputs[0], group_002.inputs[0])
    links.new(map_range_002.outputs[0], group_011.inputs[0])
    links.new(reroute_011.outputs[0], reroute_005.inputs[0])
    links.new(color_ramp_006.outputs[0], reroute_006.inputs[0])
    links.new(reroute_002.outputs[0], reroute_007.inputs[0])
    links.new(math_001.outputs[0], reroute_008.inputs[0])
    links.new(principled_bsdf_001.outputs[0], reroute_009.inputs[0])
    links.new(color_ramp_003.outputs[0], math.inputs[0])
    links.new(input_node.outputs[2], math.inputs[1])
    links.new(input_node.outputs[3], map_range_003.inputs[0])
    links.new(map_range_003.outputs[0], group_005.inputs[0])
    links.new(input_node.outputs[3], map_range_004.inputs[0])
    links.new(bump.outputs[0], reroute_011.inputs[0])
    links.new(input_node.outputs[6], map_range_002.inputs[0])
    links.new(map_range_005.outputs[0], group_006.inputs[0])
    links.new(input_node.outputs[0], map_range_005.inputs[0])
    links.new(input_node.outputs[7], map_range_006.inputs[0])
    links.new(map_range_006.outputs[0], pf_grunge_20_r.inputs[0])
    links.new(input_node.outputs[7], map_range_007.inputs[0])
    links.new(reroute_012.outputs[0], group_010.inputs[0])
    links.new(map_range_007.outputs[0], reroute_012.inputs[0])
    links.new(reroute_002.outputs[0], math_001.inputs[0])
    links.new(input_node.outputs[5], map_range_001.inputs[0])
    links.new(input_node.outputs[5], map_range_008.inputs[0])
    links.new(map_range_008.outputs[0], pf_grunge_19_r_004.inputs[0])
    links.new(input_node.outputs[5], map_range_009.inputs[0])
    links.new(reroute_013.outputs[0], group_007.inputs[0])
    links.new(map_range_009.outputs[0], reroute_013.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control.inputs[0])
    links.new(input_node.outputs[4], hs_bump_control.inputs[1])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(reroute_014.outputs[0], bump_001.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_010.inputs[0])
    links.new(reroute_010.outputs[0], reroute_014.inputs[0])
    links.new(percentage_to_0_1.outputs[0], bevel_001.inputs[0])
    links.new(input_node.outputs[1], percentage_to_0_1.inputs[0])
    links.new(bevel_001.outputs[0], reroute_015.inputs[0])
    links.new(perlin_noise.outputs[0], math_001.inputs[1])

    return group