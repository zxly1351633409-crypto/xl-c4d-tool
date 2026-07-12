import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .hs_chipping import hs_chipping
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_22e_r import pf_grunge_22e_r


def hs_paint_01a():
    """BL_油漆01 - 基础剥落油漆材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/底色混合"""
    group_name = "BL_油漆01"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="凹腔脏污_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="凹腔脏污_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="边缘磨损_位置", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_主扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 10.0
    group.interface.new_socket(name="边缘磨损_次扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 10.0
    group.interface.new_socket(name="底部污渍_位置", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="底部污渍_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="底部污渍_条纹", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="底部污渍_偏移", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="渗漏_量", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="渗漏_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="渗漏_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="油漆颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.1022, 0.0976, 0.0685, 1.0000)
    group.interface.new_socket(name="油漆变色_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="油漆细节_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 25.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩", (0.09, 0.09, 0.09))
    frame_001 = create_frame(nodes, "Frame.001", "油漆颜色: 油漆材质的基础颜色层")
    frame_002 = create_frame(nodes, "Frame.002", "铁锈渗漏: 模拟铁锈从缝隙渗漏的流淌效果")
    frame_003 = create_frame(nodes, "Frame.003", "凹腔脏污: 凹腔区域(缝隙/角落)的脏污遮罩")
    frame_005 = create_frame(nodes, "Frame.005", "底部污垢: 模型底部的污垢堆积效果")
    frame_009 = create_frame(nodes, "Frame.009", "最大值控制器: 控制效果的峰值限制")
    frame_010 = create_frame(nodes, "Frame.010", "比例缩放: 按比例缩放纹理坐标")
    frame_011 = create_frame(nodes, "Frame.011", "缩放: 控制纹理/效果的缩放比例")
    frame_012 = create_frame(nodes, "Frame.012", "保持原样: 不做额外处理")
    frame_013 = create_frame(nodes, "Frame.013", "渐变保持: 保持颜色渐变不做调整")
    frame_017 = create_frame(nodes, "Frame.017", "粗糙度+凹凸: 粗糙度贴图与凹凸贴图综合控制")
    frame_004 = create_frame(nodes, "Frame.004", "碎裂剥落: 基于噪声纹理的碎片/剥落遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (-677.8, -531.0)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.2954545319080353
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
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1487.6, -101.8)
    label_node(all_edges_013, "", frame)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 2.0
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (763.3, -165.8)
    label_node(group_029, "", frame)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_22b_r()
    mix = nodes.new("ShaderNodeMix")
    mix.location = (1137.3, -218.8)
    label_node(mix, "", frame_001)
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
    colorramp_040 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_040 | ColorRamp.040
    colorramp_040.color_ramp.color_mode = 'RGB'
    colorramp_040.color_ramp.hue_interpolation = 'NEAR'
    colorramp_040.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_040.color_ramp.elements) > 2:
        colorramp_040.color_ramp.elements.remove(colorramp_040.color_ramp.elements[-1])
    while len(colorramp_040.color_ramp.elements) < 2:
        colorramp_040.color_ramp.elements.new(0.5)
    colorramp_040.color_ramp.elements[0].position = 0.14803658425807953
    colorramp_040.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_040.color_ramp.elements[1].position = 0.7039275169372559
    colorramp_040.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_040
    colorramp_040.location = (29.9, -36.1)
    label_node(colorramp_040, "", frame_013)
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (569.3, -148.9)
    label_node(group_030, "", frame_001)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_15_r()
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (921.3, -406.2)
    label_node(hue_saturation_value, "", frame_001)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 0.8100000023841858
    hue_saturation_value.inputs[2].default_value = 0.6299999952316284
    hue_saturation_value.inputs[3].default_value = 1.0
    colorramp_041 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_041 | ColorRamp.041
    colorramp_041.color_ramp.color_mode = 'RGB'
    colorramp_041.color_ramp.hue_interpolation = 'NEAR'
    colorramp_041.color_ramp.interpolation = 'B_SPLINE'
    while len(colorramp_041.color_ramp.elements) > 2:
        colorramp_041.color_ramp.elements.remove(colorramp_041.color_ramp.elements[-1])
    while len(colorramp_041.color_ramp.elements) < 2:
        colorramp_041.color_ramp.elements.new(0.5)
    colorramp_041.color_ramp.elements[0].position = 0.27794548869132996
    colorramp_041.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_041.color_ramp.elements[1].position = 0.6999998688697815
    colorramp_041.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_041
    colorramp_041.location = (918.5, -317.8)
    label_node(colorramp_041, "", frame_017)
    group_031 = nodes.new("ShaderNodeGroup")
    group_031.location = (581.2, -465.5)
    label_node(group_031, "", frame_017)
    group_031.xl_c4d_gradient_type = '0'
    group_031.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_031.node_tree = pf_grunge_22e_r()
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (-2280.2, -551.1)
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
    cavity_012 = nodes.new("ShaderNodeGroup")
    cavity_012.location = (1022.2, -102.3)
    label_node(cavity_012, "", frame_003)
    cavity_012.xl_c4d_gradient_type = '0'
    cavity_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_012.node_tree = cavity()
    cavity_012.inputs[2].default_value = 1.399999976158142
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (453.0, -181.5)
    label_node(group_032, "", frame_003)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = pf_grunge_15_r()
    colorramp_043 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_043 | ColorRamp.043
    colorramp_043.color_ramp.color_mode = 'RGB'
    colorramp_043.color_ramp.hue_interpolation = 'NEAR'
    colorramp_043.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_043.color_ramp.elements) > 2:
        colorramp_043.color_ramp.elements.remove(colorramp_043.color_ramp.elements[-1])
    while len(colorramp_043.color_ramp.elements) < 2:
        colorramp_043.color_ramp.elements.new(0.5)
    colorramp_043.color_ramp.elements[0].position = 0.19980771839618683
    colorramp_043.color_ramp.elements[0].color = (0.11143158376216888, 0.06909624487161636, 0.027629852294921875, 1.0)
    colorramp_043.color_ramp.elements[1].position = 0.6888214349746704
    colorramp_043.color_ramp.elements[1].color = (0.05187201499938965, 0.04273592680692673, 0.0356258898973465, 1.0)
    # XL_PF_RAMP_END colorramp_043
    colorramp_043.location = (1332.8, -194.9)
    label_node(colorramp_043, "", frame_003)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1950.4, -324.3)
    label_node(bump, "", frame_017)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (-2743.3, -554.4)
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_044 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_044 | ColorRamp.044
    colorramp_044.color_ramp.color_mode = 'RGB'
    colorramp_044.color_ramp.hue_interpolation = 'NEAR'
    colorramp_044.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_044.color_ramp.elements) > 2:
        colorramp_044.color_ramp.elements.remove(colorramp_044.color_ramp.elements[-1])
    while len(colorramp_044.color_ramp.elements) < 2:
        colorramp_044.color_ramp.elements.new(0.5)
    colorramp_044.color_ramp.elements[0].position = 0.17031028866767883
    colorramp_044.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_044.color_ramp.elements[1].position = 0.28378188610076904
    colorramp_044.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_044
    colorramp_044.location = (29.7, -36.3)
    label_node(colorramp_044, "", frame_012)
    group_033 = nodes.new("ShaderNodeGroup")
    group_033.location = (216.4, -35.7)
    label_node(group_033, "", frame_010)
    group_033.xl_c4d_gradient_type = '0'
    group_033.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_033.node_tree = pf_grunge_15_r()
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (1846.6, -377.0)
    label_node(mix_003, "", frame_002)
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_003.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000, 1.0000)
    mix_003.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.location = (29.7, -36.1)
    label_node(noise_texture, "", frame_011)
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    noise_texture.inputs[3].default_value = 3.9099998474121094
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 6.099999904632568
    noise_texture.inputs[7].default_value = 1.0
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (754.4, -368.1)
    label_node(mapping, "", frame_002)
    mapping.vector_type = 'POINT'
    mapping.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping.inputs[3].default_value = (0.1000, 2.2900, 0.1600)
    texture_coordinate = nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (753.8, -219.5)
    label_node(texture_coordinate, "", frame_002)
    texture_coordinate.from_instancer = False
    vector_transform_001 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_001.location = (755.3, -327.4)
    label_node(vector_transform_001, "", frame_002)
    vector_transform_001.vector_type = 'VECTOR'
    vector_transform_001.convert_from = 'OBJECT'
    vector_transform_001.convert_to = 'WORLD'
    colorramp_046 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_046 | ColorRamp.046
    colorramp_046.color_ramp.color_mode = 'RGB'
    colorramp_046.color_ramp.hue_interpolation = 'NEAR'
    colorramp_046.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_046.color_ramp.elements) > 2:
        colorramp_046.color_ramp.elements.remove(colorramp_046.color_ramp.elements[-1])
    while len(colorramp_046.color_ramp.elements) < 2:
        colorramp_046.color_ramp.elements.new(0.5)
    colorramp_046.color_ramp.elements[0].position = 0.13636362552642822
    colorramp_046.color_ramp.elements[0].color = (0.11241188645362854, 0.06681473553180695, 0.015552390366792679, 1.0)
    colorramp_046.color_ramp.elements[1].position = 0.5272727608680725
    colorramp_046.color_ramp.elements[1].color = (0.0633276030421257, 0.05257216840982437, 0.03321413695812225, 1.0)
    # XL_PF_RAMP_END colorramp_046
    colorramp_046.location = (1749.1, -601.5)
    label_node(colorramp_046, "", frame_002)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (931.9, -737.4)
    label_node(bevel, "", frame_017)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (2130.6, -966.2)
    label_node(principled_bsdf_001, "", frame)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[1].default_value = 0.1818181872367859
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
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (2486.2, -460.5)
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (1015.5, -167.4)
    label_node(map_range, "", frame)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[1].default_value = 0.08999999612569809
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = -0.8499999046325684
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (1486.3, -274.2)
    label_node(all_edges_014, "", frame)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 2.0
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (1833.4, -152.1)
    label_node(mix_004, "", frame)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[6].default_value = (0.2217, 0.1121, 0.0154, 1.0000)
    mix_004.inputs[7].default_value = (0.0500, 0.0257, 0.0144, 1.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (1944.6, -1088.7)
    label_node(bump_001, "", frame)
    bump_001.invert = False
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    bump_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
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
    colorramp_047.location = (1057.2, -1025.4)
    label_node(colorramp_047, "", frame)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (780.7, -1127.1)
    label_node(group_034, "", frame)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_22e_r()
    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.location = (749.4, -941.2)
    label_node(gradient_texture, "", frame_005)
    gradient_texture.gradient_type = 'LINEAR'
    mapping_001 = nodes.new("ShaderNodeMapping")
    mapping_001.location = (-4308.1, 804.2)
    mapping_001.vector_type = 'POINT'
    mapping_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_001.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (350.8, -903.0)
    label_node(texture_coordinate_001, "", frame_005)
    texture_coordinate_001.from_instancer = False
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.13181819021701813
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.22272750735282898
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (907.8, -865.9)
    label_node(color_ramp, "", frame_005)
    vector_transform_002 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_002.location = (351.2, -935.2)
    label_node(vector_transform_002, "", frame_005)
    vector_transform_002.vector_type = 'VECTOR'
    vector_transform_002.convert_from = 'OBJECT'
    vector_transform_002.convert_to = 'OBJECT'
    separate_xyz_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_002.location = (748.1, -865.8)
    label_node(separate_xyz_002, "", frame_005)
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (2112.4, -721.1)
    label_node(mix_005, "", frame_005)
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    mix_005.blend_type = 'MIX'
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    mix_005.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_005.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[6].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    mix_005.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.location = (887.1, -106.5)
    label_node(noise_texture_001, "", frame_005)
    noise_texture_001.noise_dimensions = '3D'
    noise_texture_001.noise_type = 'FBM'
    noise_texture_001.normalize = True
    noise_texture_001.inputs[3].default_value = 3.9100000858306885
    noise_texture_001.inputs[4].default_value = 0.5
    noise_texture_001.inputs[5].default_value = 6.099999904632568
    noise_texture_001.inputs[7].default_value = 1.0
    mapping_002 = nodes.new("ShaderNodeMapping")
    mapping_002.location = (685.8, -105.4)
    label_node(mapping_002, "", frame_005)
    mapping_002.vector_type = 'POINT'
    mapping_002.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    texture_coordinate_002 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_002.location = (351.7, -106.7)
    label_node(texture_coordinate_002, "", frame_005)
    texture_coordinate_002.from_instancer = False
    vector_transform_003 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_003.location = (520.6, -106.4)
    label_node(vector_transform_003, "", frame_005)
    vector_transform_003.vector_type = 'VECTOR'
    vector_transform_003.convert_from = 'OBJECT'
    vector_transform_003.convert_to = 'WORLD'
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (-1254.0, -551.8)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[6].default_value = (0.0565, 0.0395, 0.0286, 1.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mix_007 = nodes.new("ShaderNodeMix")
    mix_007.location = (1289.1, -726.4)
    label_node(mix_007, "", frame_005)
    mix_007.data_type = 'RGBA'
    mix_007.factor_mode = 'UNIFORM'
    mix_007.blend_type = 'MIX'
    mix_007.clamp_factor = True
    mix_007.clamp_result = False
    mix_007.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_007.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[7].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    mix_007.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_049 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_049 | ColorRamp.049
    colorramp_049.color_ramp.color_mode = 'RGB'
    colorramp_049.color_ramp.hue_interpolation = 'NEAR'
    colorramp_049.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_049.color_ramp.elements) > 2:
        colorramp_049.color_ramp.elements.remove(colorramp_049.color_ramp.elements[-1])
    while len(colorramp_049.color_ramp.elements) < 2:
        colorramp_049.color_ramp.elements.new(0.5)
    colorramp_049.color_ramp.elements[0].position = 0.12272726744413376
    colorramp_049.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_049.color_ramp.elements[1].position = 0.24090911448001862
    colorramp_049.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_049
    colorramp_049.location = (907.0, -653.3)
    label_node(colorramp_049, "", frame_005)
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (573.9, -664.9)
    label_node(group_036, "", frame_005)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_15_r()
    mix_008 = nodes.new("ShaderNodeMix")
    mix_008.location = (-1689.7, -551.3)
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
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (770.0, -105.5)
    label_node(map_range_002, "", frame_003)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 1.0
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    colorramp_050 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_050 | ColorRamp.050
    colorramp_050.color_ramp.color_mode = 'RGB'
    colorramp_050.color_ramp.hue_interpolation = 'NEAR'
    colorramp_050.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_050.color_ramp.elements) > 2:
        colorramp_050.color_ramp.elements.remove(colorramp_050.color_ramp.elements[-1])
    while len(colorramp_050.color_ramp.elements) < 2:
        colorramp_050.color_ramp.elements.new(0.5)
    colorramp_050.color_ramp.elements[0].position = 0.4500000774860382
    colorramp_050.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_050.color_ramp.elements[1].position = 0.5000001192092896
    colorramp_050.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_050
    colorramp_050.location = (1228.7, -106.6)
    label_node(colorramp_050, "", frame_005)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (30.4, -35.9)
    label_node(map_range_003, "", frame_009)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[3].default_value = -5.0
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (29.9, -44.8)
    label_node(vector_math, "", frame_010)
    vector_math.operation = 'MULTIPLY'
    vector_math.inputs[0].default_value = (0.0100, 0.0200, 0.0200)
    vector_math.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[3].default_value = 1.0
    reroute = nodes.new("NodeReroute")
    reroute.location = (1710.7, -134.0)
    label_node(reroute, "", frame)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (2061.0, -134.0)
    label_node(reroute_001, "", frame)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1710.7, -1229.3)
    label_node(reroute_002, "", frame)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1212.9, -201.0)
    label_node(reroute_004, "", frame)
    reroute_004.socket_idname = 'NodeSocketFloat'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (2169.1, -566.0)
    reroute_005.socket_idname = 'NodeSocketShader'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (2169.1, -518.5)
    reroute_006.socket_idname = 'NodeSocketFloat'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-3639.1, -1720.9)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-3659.7, -1495.3)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-3283.8, -709.7)
    reroute_010.socket_idname = 'NodeSocketColor'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-3152.0, -750.1)
    reroute_011.socket_idname = 'NodeSocketColor'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-2506.3, -723.6)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (-2412.5, -747.0)
    reroute_013.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (-2805.3, 257.4)
    reroute_014.socket_idname = 'NodeSocketFloat'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1254.3, -135.8)
    label_node(reroute_015, "", frame_003)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (1254.3, -377.8)
    label_node(reroute_016, "", frame_003)
    reroute_016.socket_idname = 'NodeSocketFloat'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (-2077.8, -584.3)
    reroute_017.socket_idname = 'NodeSocketColor'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (-2016.0, 915.4)
    reroute_018.socket_idname = 'NodeSocketColor'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (-1929.5, -746.4)
    reroute_021.socket_idname = 'NodeSocketColor'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (-1488.6, -585.8)
    reroute_022.socket_idname = 'NodeSocketColor'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (-1363.1, -746.7)
    reroute_023.socket_idname = 'NodeSocketColor'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (1662.1, -760.8)
    label_node(reroute_024, "", frame_005)
    reroute_024.socket_idname = 'NodeSocketColor'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (1817.1, -919.1)
    label_node(reroute_025, "", frame_005)
    reroute_025.socket_idname = 'NodeSocketColor'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1995.2, -875.5)
    label_node(reroute_026, "", frame_005)
    reroute_026.socket_idname = 'NodeSocketColor'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (-775.5, -625.2)
    reroute_027.socket_idname = 'NodeSocketColor'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (1228.6, -351.4)
    label_node(reroute_028, "", frame_017)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (1358.6, -468.5)
    label_node(reroute_029, "", frame_017)
    reroute_029.socket_idname = 'NodeSocketColor'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (1350.3, -492.1)
    label_node(reroute_030, "", frame_017)
    reroute_030.socket_idname = 'NodeSocketVector'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1563.5, -351.4)
    label_node(reroute_031, "", frame_017)
    reroute_031.socket_idname = 'NodeSocketColor'
    colorramp_042 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_042 | ColorRamp.042
    colorramp_042.color_ramp.color_mode = 'RGB'
    colorramp_042.color_ramp.hue_interpolation = 'NEAR'
    colorramp_042.color_ramp.interpolation = 'EASE'
    while len(colorramp_042.color_ramp.elements) > 2:
        colorramp_042.color_ramp.elements.remove(colorramp_042.color_ramp.elements[-1])
    while len(colorramp_042.color_ramp.elements) < 2:
        colorramp_042.color_ramp.elements.new(0.5)
    colorramp_042.color_ramp.elements[0].position = 0.18198297917842865
    colorramp_042.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_042.color_ramp.elements[1].position = 0.6999998688697815
    colorramp_042.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_042
    colorramp_042.location = (923.2, -525.3)
    label_node(colorramp_042, "", frame_017)
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (-760.1, -687.2)
    reroute_032.socket_idname = 'NodeSocketVector'
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (592.0, -154.4)
    label_node(math_001, "", frame)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 0.38999998569488525
    math_001.inputs[2].default_value = 0.5
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (579.4, -1171.7)
    label_node(math_002, "", frame)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 1.100000023841858
    math_002.inputs[2].default_value = 0.5
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (468.6, -258.1)
    label_node(reroute_033, "", frame)
    reroute_033.socket_idname = 'NodeSocketFloat'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (468.6, -1276.9)
    label_node(reroute_034, "", frame)
    reroute_034.socket_idname = 'NodeSocketFloat'
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (1266.6, -213.3)
    label_node(math_003, "", frame)
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    math_003.inputs[2].default_value = 0.5
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (1267.3, -390.0)
    label_node(math_004, "", frame)
    math_004.operation = 'MULTIPLY'
    math_004.use_clamp = False
    math_004.inputs[1].default_value = 0.5
    math_004.inputs[2].default_value = 0.5
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (1078.1, -441.1)
    label_node(reroute_035, "", frame)
    reroute_035.socket_idname = 'NodeSocketFloat'
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (283.7, -234.4)
    label_node(map_range_006, "", frame)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.10000000149011612
    map_range_006.inputs[4].default_value = 4.0
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (820.2, -408.8)
    label_node(map_range_007, "", frame)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.10000000149011612
    map_range_007.inputs[4].default_value = 10.0
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (821.0, -650.8)
    label_node(map_range_008, "", frame)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.27000001072883606
    map_range_008.inputs[4].default_value = 1.820000171661377
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1162.8, -686.5)
    label_node(reroute_036, "", frame)
    reroute_036.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (1446.1, -202.1)
    label_node(reroute_037, "", frame)
    reroute_037.socket_idname = 'NodeSocketFloat'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (1446.1, -374.4)
    label_node(reroute_038, "", frame)
    reroute_038.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1446.1, -180.3)
    label_node(reroute_003, "", frame)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (1427.6, -354.7)
    label_node(reroute_039, "", frame)
    reroute_039.socket_idname = 'NodeSocketFloat'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (1143.9, -494.6)
    label_node(reroute_040, "", frame)
    reroute_040.socket_idname = 'NodeSocketFloat'
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (1166.2, -440.1)
    label_node(reroute_041, "", frame)
    reroute_041.socket_idname = 'NodeSocketFloat'
    math_005 = nodes.new("ShaderNodeMath")
    math_005.location = (413.7, -465.2)
    label_node(math_005, "", frame_017)
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False
    math_005.inputs[1].default_value = 4.690000057220459
    math_005.inputs[2].default_value = 0.5
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (233.8, -442.5)
    label_node(map_range_009, "", frame_017)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[3].default_value = 0.11999999731779099
    map_range_009.inputs[4].default_value = 1.0
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (1415.9, -619.4)
    label_node(reroute_042, "", frame_002)
    reroute_042.socket_idname = 'NodeSocketColor'
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (312.8, -374.4)
    label_node(map_range_010, "", frame_002)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[3].default_value = 0.20000000298023224
    map_range_010.inputs[4].default_value = 2.819999933242798
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (312.8, -690.6)
    label_node(map_range_011, "", frame_002)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = 1.0
    map_range_011.inputs[4].default_value = 100.0
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (313.3, -119.4)
    label_node(map_range_012, "", frame_002)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.30000001192092896
    map_range_012.inputs[4].default_value = 0.5
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_043 = nodes.new("NodeReroute")
    reroute_043.location = (1585.9, -171.9)
    label_node(reroute_043, "", frame_002)
    reroute_043.socket_idname = 'NodeSocketFloat'
    reroute_044 = nodes.new("NodeReroute")
    reroute_044.location = (1585.9, -531.2)
    label_node(reroute_044, "", frame_002)
    reroute_044.socket_idname = 'NodeSocketFloat'
    reroute_045 = nodes.new("NodeReroute")
    reroute_045.location = (1215.7, -152.4)
    label_node(reroute_045, "", frame_002)
    reroute_045.socket_idname = 'NodeSocketFloat'
    reroute_046 = nodes.new("NodeReroute")
    reroute_046.location = (1585.3, -551.4)
    label_node(reroute_046, "", frame_002)
    reroute_046.socket_idname = 'NodeSocketColor'
    map_range_014 = nodes.new("ShaderNodeMapRange")
    map_range_014.location = (273.1, -109.1)
    label_node(map_range_014, "", frame_003)
    map_range_014.clamp = True
    map_range_014.interpolation_type = 'LINEAR'
    map_range_014.data_type = 'FLOAT'
    map_range_014.inputs[2].default_value = 100.0
    map_range_014.inputs[3].default_value = 0.10000000149011612
    map_range_014.inputs[4].default_value = 1.0
    map_range_014.inputs[5].default_value = 4.0
    map_range_014.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_015 = nodes.new("ShaderNodeMapRange")
    map_range_015.location = (274.9, -351.7)
    label_node(map_range_015, "", frame_003)
    map_range_015.clamp = True
    map_range_015.interpolation_type = 'LINEAR'
    map_range_015.data_type = 'FLOAT'
    map_range_015.inputs[2].default_value = 100.0
    map_range_015.inputs[3].default_value = -0.16999998688697815
    map_range_015.inputs[4].default_value = 0.1899999976158142
    map_range_015.inputs[5].default_value = 4.0
    map_range_015.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_016 = nodes.new("ShaderNodeMapRange")
    map_range_016.location = (273.3, -594.1)
    label_node(map_range_016, "", frame_003)
    map_range_016.clamp = True
    map_range_016.interpolation_type = 'LINEAR'
    map_range_016.data_type = 'FLOAT'
    map_range_016.inputs[2].default_value = 100.0
    map_range_016.inputs[3].default_value = 0.020000025629997253
    map_range_016.inputs[4].default_value = 2.549999952316284
    map_range_016.inputs[5].default_value = 4.0
    map_range_016.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_047 = nodes.new("NodeReroute")
    reroute_047.location = (881.3, -627.5)
    label_node(reroute_047, "", frame_003)
    reroute_047.socket_idname = 'NodeSocketFloat'
    reroute_048 = nodes.new("NodeReroute")
    reroute_048.location = (638.9, -384.4)
    label_node(reroute_048, "", frame_003)
    reroute_048.socket_idname = 'NodeSocketFloat'
    reroute_049 = nodes.new("NodeReroute")
    reroute_049.location = (247.5, -724.0)
    label_node(reroute_049, "", frame_003)
    reroute_049.socket_idname = 'NodeSocketFloatPercentage'
    reroute_050 = nodes.new("NodeReroute")
    reroute_050.location = (247.5, -482.6)
    label_node(reroute_050, "", frame_003)
    reroute_050.socket_idname = 'NodeSocketFloatPercentage'
    reroute_051 = nodes.new("NodeReroute")
    reroute_051.location = (-2918.3, 165.2)
    reroute_051.socket_idname = 'NodeSocketColor'
    group_048 = nodes.new("ShaderNodeGroup")
    group_048.location = (29.7, -137.2)
    label_node(group_048, "", frame_004)
    group_048.xl_c4d_gradient_type = '0'
    group_048.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_048.node_tree = hs_chipping()
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (336.0, -125.0)
    label_node(map_range_001, "", frame_001)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.09000000357627869
    map_range_001.inputs[4].default_value = 0.5600000023841858
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_052 = nodes.new("NodeReroute")
    reroute_052.location = (-1760.3, -725.0)
    reroute_052.socket_idname = 'NodeSocketColor'
    reroute_053 = nodes.new("NodeReroute")
    reroute_053.location = (-1741.6, -703.9)
    reroute_053.socket_idname = 'NodeSocketFloat'
    reroute_054 = nodes.new("NodeReroute")
    reroute_054.location = (1662.1, -142.9)
    label_node(reroute_054, "", frame_005)
    reroute_054.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-1919.4, -427.9)
    reroute_009.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (-1936.9, -448.4)
    reroute_019.socket_idname = 'NodeSocketColor'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (-1313.4, -706.6)
    reroute_020.socket_idname = 'NodeSocketColor'
    combine_xyz = nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.location = (351.2, -964.3)
    label_node(combine_xyz, "", frame_005)
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (353.1, -652.8)
    label_node(map_range_013, "", frame_005)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = 0.5
    map_range_013.inputs[4].default_value = 1.0
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_017 = nodes.new("ShaderNodeMapRange")
    map_range_017.location = (351.9, -265.8)
    label_node(map_range_017, "", frame_005)
    map_range_017.clamp = True
    map_range_017.interpolation_type = 'LINEAR'
    map_range_017.data_type = 'FLOAT'
    map_range_017.inputs[2].default_value = 100.0
    map_range_017.inputs[3].default_value = 0.009999999776482582
    map_range_017.inputs[4].default_value = 1.0
    map_range_017.inputs[5].default_value = 4.0
    map_range_017.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.location = (520.6, -267.1)
    label_node(vector_math_001, "", frame_005)
    vector_math_001.operation = 'MULTIPLY'
    vector_math_001.inputs[0].default_value = (0.1000, 2.2900, 0.1600)
    vector_math_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math_001.inputs[3].default_value = 1.0
    reroute_055 = nodes.new("NodeReroute")
    reroute_055.location = (491.9, -1101.1)
    label_node(reroute_055, "", frame_005)
    reroute_055.socket_idname = 'NodeSocketVectorEuler'
    map_range_018 = nodes.new("ShaderNodeMapRange")
    map_range_018.location = (685.8, -395.5)
    label_node(map_range_018, "", frame_005)
    map_range_018.clamp = True
    map_range_018.interpolation_type = 'LINEAR'
    map_range_018.data_type = 'FLOAT'
    map_range_018.inputs[2].default_value = 100.0
    map_range_018.inputs[3].default_value = 0.5
    map_range_018.inputs[4].default_value = 1.0
    map_range_018.inputs[5].default_value = 4.0
    map_range_018.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_018.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_018.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_056 = nodes.new("NodeReroute")
    reroute_056.location = (580.1, -395.1)
    label_node(reroute_056, "", frame_001)
    reroute_056.socket_idname = 'NodeSocketColor'
    group_001 = nodes.new("ShaderNodeGroup")
    group_001.location = (0.0, 0.0)
    group_001.xl_c4d_gradient_type = '0'
    group_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1543.3, -1139.7)
    label_node(hs_bump_control, "", frame)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    hs_bump_control_001 = nodes.new("ShaderNodeGroup")
    hs_bump_control_001.location = (1580.5, -544.9)
    label_node(hs_bump_control_001, "", frame_017)
    hs_bump_control_001.xl_c4d_gradient_type = '0'
    hs_bump_control_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control_001.node_tree = _hs_bump_control_fn()
    hs_bump_control_001.inputs[2].default_value = 0.4000000059604645
    reroute_057 = nodes.new("NodeReroute")
    reroute_057.location = (1187.4, -771.7)
    label_node(reroute_057, "", frame_017)
    reroute_057.socket_idname = 'NodeSocketVector'
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (582.8, -143.3)
    label_node(group_035, "", frame_017)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = pf_grunge_22e_r()
    map_range_019 = nodes.new("ShaderNodeMapRange")
    map_range_019.location = (235.4, -120.3)
    label_node(map_range_019, "", frame_017)
    map_range_019.clamp = True
    map_range_019.interpolation_type = 'LINEAR'
    map_range_019.data_type = 'FLOAT'
    map_range_019.inputs[2].default_value = 100.0
    map_range_019.inputs[3].default_value = 0.25
    map_range_019.inputs[4].default_value = 1.5
    map_range_019.inputs[5].default_value = 4.0
    map_range_019.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_019.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_019.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    colorramp_045 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_045 | ColorRamp.045
    colorramp_045.color_ramp.color_mode = 'RGB'
    colorramp_045.color_ramp.hue_interpolation = 'NEAR'
    colorramp_045.color_ramp.interpolation = 'B_SPLINE'
    while len(colorramp_045.color_ramp.elements) > 2:
        colorramp_045.color_ramp.elements.remove(colorramp_045.color_ramp.elements[-1])
    while len(colorramp_045.color_ramp.elements) < 2:
        colorramp_045.color_ramp.elements.new(0.5)
    colorramp_045.color_ramp.elements[0].position = 0.27794548869132996
    colorramp_045.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_045.color_ramp.elements[1].position = 0.6999998688697815
    colorramp_045.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_045
    colorramp_045.location = (921.3, -101.8)
    label_node(colorramp_045, "", frame_017)
    map_range_020 = nodes.new("ShaderNodeMapRange")
    map_range_020.location = (754.5, -731.5)
    label_node(map_range_020, "", frame_017)
    map_range_020.clamp = True
    map_range_020.interpolation_type = 'LINEAR'
    map_range_020.data_type = 'FLOAT'
    map_range_020.inputs[2].default_value = 100.0
    map_range_020.inputs[4].default_value = 0.004999999888241291
    map_range_020.inputs[5].default_value = 4.0
    map_range_020.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_020.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_020.inputs[11].default_value = (4.0000, 4.0000, 4.0000)

    # === 节点连接 ===
    links.new(mix_006.outputs[2], principled_bsdf.inputs[0])
    links.new(colorramp_040.outputs[0], mix.inputs[0])
    links.new(hue_saturation_value.outputs[0], mix.inputs[7])
    links.new(math_005.outputs[0], group_031.inputs[0])
    links.new(group_031.outputs[0], colorramp_041.inputs[0])
    links.new(reroute_027.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_012.outputs[0], mix_001.inputs[6])
    links.new(reroute_014.outputs[0], mix_001.inputs[0])
    links.new(reroute_013.outputs[0], mix_001.inputs[7])
    links.new(reroute_016.outputs[0], colorramp_043.inputs[0])
    links.new(reroute_032.outputs[0], principled_bsdf.inputs[5])
    links.new(reroute_056.outputs[0], mix.inputs[6])
    links.new(reroute_056.outputs[0], hue_saturation_value.inputs[4])
    links.new(mix.outputs[2], mix_002.inputs[6])
    links.new(group_033.outputs[0], colorramp_044.inputs[0])
    links.new(reroute_010.outputs[0], mix_002.inputs[0])
    links.new(reroute_046.outputs[0], mix_003.inputs[6])
    links.new(mapping.outputs[0], noise_texture.inputs[0])
    links.new(vector_transform_001.outputs[0], mapping.inputs[0])
    links.new(texture_coordinate.outputs[3], vector_transform_001.inputs[0])
    links.new(reroute_011.outputs[0], mix_002.inputs[7])
    links.new(reroute_030.outputs[0], bump.inputs[4])
    links.new(reroute_006.outputs[0], mix_shader.inputs[0])
    links.new(reroute_005.outputs[0], mix_shader.inputs[2])
    links.new(mix_004.outputs[2], principled_bsdf_001.inputs[0])
    links.new(bump_001.outputs[0], principled_bsdf_001.inputs[5])
    links.new(reroute_002.outputs[0], bump_001.inputs[3])
    links.new(group_034.outputs[0], colorramp_047.inputs[0])
    links.new(colorramp_047.outputs[0], principled_bsdf_001.inputs[2])
    links.new(texture_coordinate_001.outputs[3], vector_transform_002.inputs[0])
    links.new(mapping_001.outputs[0], separate_xyz_002.inputs[0])
    links.new(gradient_texture.outputs[0], color_ramp.inputs[0])
    links.new(separate_xyz_002.outputs[2], gradient_texture.inputs[0])
    links.new(mapping_002.outputs[0], noise_texture_001.inputs[0])
    links.new(vector_transform_003.outputs[0], mapping_002.inputs[0])
    links.new(texture_coordinate_002.outputs[3], vector_transform_003.inputs[0])
    links.new(reroute_025.outputs[0], mix_005.inputs[7])
    links.new(reroute_020.outputs[0], mix_006.inputs[0])
    links.new(reroute_023.outputs[0], mix_006.inputs[7])
    links.new(color_ramp.outputs[0], mix_007.inputs[6])
    links.new(group_036.outputs[0], colorramp_049.inputs[0])
    links.new(colorramp_049.outputs[0], mix_007.inputs[0])
    links.new(reroute_052.outputs[0], mix_008.inputs[6])
    links.new(reroute_021.outputs[0], mix_008.inputs[7])
    links.new(reroute_053.outputs[0], mix_008.inputs[0])
    links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    links.new(group_032.outputs[0], map_range_002.inputs[0])
    links.new(vector_transform_002.outputs[0], mapping_001.inputs[0])
    links.new(noise_texture_001.outputs[0], colorramp_050.inputs[0])
    links.new(reroute_026.outputs[0], mix_005.inputs[0])
    links.new(noise_texture.outputs[0], map_range_003.inputs[0])
    links.new(reroute_044.outputs[0], mix_003.inputs[0])
    links.new(vector_math.outputs[0], group_033.inputs[0])
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])
    links.new(map_range.outputs[0], reroute_004.inputs[0])
    links.new(principled_bsdf_001.outputs[0], reroute_005.inputs[0])
    links.new(reroute_001.outputs[0], reroute_006.inputs[0])
    links.new(colorramp_046.outputs[0], reroute_007.inputs[0])
    links.new(mix_003.outputs[2], reroute_008.inputs[0])
    links.new(reroute_008.outputs[0], reroute_010.inputs[0])
    links.new(reroute_007.outputs[0], reroute_011.inputs[0])
    links.new(mix_002.outputs[2], reroute_012.inputs[0])
    links.new(reroute_051.outputs[0], reroute_013.inputs[0])
    links.new(reroute_015.outputs[0], reroute_014.inputs[0])
    links.new(reroute_015.outputs[0], reroute_016.inputs[0])
    links.new(mix_001.outputs[2], reroute_017.inputs[0])
    links.new(mix_005.outputs[2], reroute_018.inputs[0])
    links.new(reroute_017.outputs[0], reroute_021.inputs[0])
    links.new(mix_008.outputs[2], reroute_022.inputs[0])
    links.new(reroute_022.outputs[0], reroute_023.inputs[0])
    links.new(mix_007.outputs[2], reroute_024.inputs[0])
    links.new(reroute_024.outputs[0], reroute_025.inputs[0])
    links.new(reroute_054.outputs[0], reroute_026.inputs[0])
    links.new(reroute_031.outputs[0], reroute_027.inputs[0])
    links.new(colorramp_041.outputs[0], reroute_028.inputs[0])
    links.new(reroute_029.outputs[0], bump.inputs[3])
    links.new(reroute_057.outputs[0], reroute_030.inputs[0])
    links.new(reroute_028.outputs[0], reroute_031.inputs[0])
    links.new(group_031.outputs[0], colorramp_042.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(bump.outputs[0], reroute_032.inputs[0])
    links.new(reroute_033.outputs[0], math_001.inputs[0])
    links.new(reroute_034.outputs[0], math_002.inputs[0])
    links.new(reroute_033.outputs[0], reroute_034.inputs[0])
    links.new(reroute_041.outputs[0], math_003.inputs[0])
    links.new(reroute_040.outputs[0], math_004.inputs[0])
    links.new(map_range_006.outputs[0], reroute_033.inputs[0])
    links.new(map_range_007.outputs[0], reroute_035.inputs[0])
    links.new(input_node.outputs[6], map_range_006.inputs[0])
    links.new(input_node.outputs[7], map_range_007.inputs[0])
    links.new(reroute_036.outputs[0], math_003.inputs[1])
    links.new(input_node.outputs[8], map_range_008.inputs[0])
    links.new(map_range_008.outputs[0], reroute_036.inputs[0])
    links.new(reroute_004.outputs[0], reroute_037.inputs[0])
    links.new(reroute_037.outputs[0], reroute_038.inputs[0])
    links.new(math_003.outputs[0], reroute_003.inputs[0])
    links.new(math_004.outputs[0], reroute_039.inputs[0])
    links.new(reroute_035.outputs[0], reroute_040.inputs[0])
    links.new(reroute_035.outputs[0], reroute_041.inputs[0])
    links.new(math_002.outputs[0], group_034.inputs[0])
    links.new(map_range_009.outputs[0], math_005.inputs[0])
    links.new(input_node.outputs[19], map_range_009.inputs[0])
    links.new(colorramp_044.outputs[0], reroute_042.inputs[0])
    links.new(map_range_010.outputs[0], noise_texture.inputs[2])
    links.new(map_range_011.outputs[0], vector_math.inputs[1])
    links.new(reroute_045.outputs[0], map_range_003.inputs[2])
    links.new(map_range_003.outputs[0], reroute_043.inputs[0])
    links.new(reroute_043.outputs[0], reroute_044.inputs[0])
    links.new(input_node.outputs[13], map_range_012.inputs[0])
    links.new(input_node.outputs[14], map_range_010.inputs[0])
    links.new(input_node.outputs[15], map_range_011.inputs[0])
    links.new(map_range_012.outputs[0], reroute_045.inputs[0])
    links.new(reroute_042.outputs[0], reroute_046.inputs[0])
    links.new(reroute_042.outputs[0], colorramp_046.inputs[0])
    links.new(map_range_014.outputs[0], group_032.inputs[0])
    links.new(input_node.outputs[5], map_range_014.inputs[0])
    links.new(reroute_050.outputs[0], map_range_015.inputs[0])
    links.new(reroute_048.outputs[0], map_range_002.inputs[3])
    links.new(reroute_049.outputs[0], map_range_016.inputs[0])
    links.new(map_range_016.outputs[0], reroute_047.inputs[0])
    links.new(map_range_015.outputs[0], reroute_048.inputs[0])
    links.new(input_node.outputs[4], reroute_050.inputs[0])
    links.new(reroute_050.outputs[0], reroute_049.inputs[0])
    links.new(colorramp_043.outputs[0], reroute_051.inputs[0])
    links.new(input_node.outputs[18], group_048.inputs[0])
    links.new(map_range_001.outputs[0], group_030.inputs[0])
    links.new(reroute_019.outputs[0], reroute_052.inputs[0])
    links.new(reroute_009.outputs[0], reroute_053.inputs[0])
    links.new(colorramp_050.outputs[0], reroute_054.inputs[0])
    links.new(group_048.outputs[0], reroute_009.inputs[0])
    links.new(group_048.outputs[1], reroute_019.inputs[0])
    links.new(reroute_018.outputs[0], reroute_020.inputs[0])
    links.new(combine_xyz.outputs[0], mapping_001.inputs[1])
    links.new(map_range_013.outputs[0], group_036.inputs[0])
    links.new(map_range_017.outputs[0], vector_math_001.inputs[1])
    links.new(vector_math_001.outputs[0], mapping_002.inputs[3])
    links.new(input_node.outputs[10], map_range_013.inputs[0])
    links.new(input_node.outputs[11], map_range_017.inputs[0])
    links.new(input_node.outputs[9], combine_xyz.inputs[2])
    links.new(input_node.outputs[11], map_range_018.inputs[0])
    links.new(map_range_018.outputs[0], noise_texture_001.inputs[2])
    links.new(input_node.outputs[12], mapping_002.inputs[1])
    links.new(reroute_037.outputs[0], all_edges_013.inputs[1])
    links.new(all_edges_013.outputs[0], reroute.inputs[0])
    links.new(reroute_003.outputs[0], all_edges_013.inputs[0])
    links.new(reroute_038.outputs[0], all_edges_014.inputs[1])
    links.new(all_edges_014.outputs[0], mix_004.inputs[0])
    links.new(reroute_039.outputs[0], all_edges_014.inputs[0])
    links.new(map_range_002.outputs[0], cavity_012.inputs[1])
    links.new(cavity_012.outputs[0], reroute_015.inputs[0])
    links.new(reroute_047.outputs[0], cavity_012.inputs[0])
    links.new(group_029.outputs[0], map_range.inputs[0])
    links.new(math_001.outputs[0], group_029.inputs[0])
    links.new(group_030.outputs[0], colorramp_040.inputs[0])
    links.new(hs_bump_control.outputs[0], bump_001.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control.inputs[1])
    links.new(bevel.outputs[0], reroute_057.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control_001.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control_001.inputs[1])
    links.new(group_035.outputs[0], colorramp_045.inputs[0])
    links.new(map_range_019.outputs[0], group_035.inputs[0])
    links.new(colorramp_045.outputs[0], reroute_029.inputs[0])
    links.new(input_node.outputs[3], map_range_019.inputs[0])
    links.new(hs_bump_control_001.outputs[0], bump.inputs[0])
    links.new(map_range_020.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[0], map_range_020.inputs[0])
    links.new(input_node.outputs[16], reroute_056.inputs[0])
    links.new(input_node.outputs[17], map_range_001.inputs[0])

    return group