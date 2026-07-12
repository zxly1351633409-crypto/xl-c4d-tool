import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .nf_grunge_02_r import nf_grunge_02_r
from .pf_grunge_06_r import pf_grunge_06_r
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_19c_r import pf_grunge_19c_r
from .pf_grunge_20b_r import pf_grunge_20b_r
from .pf_grunge_22d_r import pf_grunge_22d_r
from .perlin_noise_main_003 import perlin_noise_main003
from .perlin_noise_001_node_tree_003 import perlin_noise001_node_tree003
from .perlin_noise_002_node_tree_003 import perlin_noise002_node_tree003
from .perlin_noise_003_node_tree_003 import perlin_noise003_node_tree003


def hs_paint_05a():
    """BL_油漆05 - 多层叠加油漆材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/底色混合"""
    group_name = "BL_油漆05"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹腔脏污_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0595, 0.0152, 0.0091, 1.0000)
    group.interface.new_socket(name="油漆细节_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆额外细节_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆额外细节_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆变色_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆变色_偏移", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="条纹_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="条纹_强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="条纹_偏移", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="顶部油漆磨损_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "变色: 表面颜色偏移和褪色效果")
    frame_001 = create_frame(nodes, "Frame.001", "划痕: 表面划痕效果遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "磨损: 表面物理磨损效果")
    frame_004 = create_frame(nodes, "Frame.004", "油漆磨损: 油漆表面的磨损程度控制")
    frame_005 = create_frame(nodes, "Frame.005", "条纹: 竖向条纹状脏污效果")
    frame_006 = create_frame(nodes, "Frame.006", "凹腔脏污: 凹腔区域(缝隙/角落)的脏污遮罩")
    frame_007 = create_frame(nodes, "Frame.007", "粗糙度缩放: 控制粗糙度贴图的缩放比例")
    frame_008 = create_frame(nodes, "Frame.008", "凹凸: 凹凸贴图效果")
    frame_009 = create_frame(nodes, "Frame.009", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (6219.4, -1289.9)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.15909090638160706
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
    group_039 = nodes.new("ShaderNodeGroup")
    group_039.location = (482.2, -191.6)
    label_node(group_039, "", frame_007)
    group_039.xl_c4d_gradient_type = '0'
    group_039.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_039.node_tree = pf_grunge_20b_r()
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.5101754069328308
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (799.7, -129.2)
    label_node(color_ramp, "", frame_007)
    group_040 = nodes.new("ShaderNodeGroup")
    group_040.location = (482.2, -446.5)
    label_node(group_040, "", frame_007)
    group_040.xl_c4d_gradient_type = '0'
    group_040.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_040.node_tree = pf_grunge_19c_r()
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.12386707216501236
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.5093382596969604
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (799.7, -381.8)
    label_node(color_ramp_001, "", frame_007)
    mix = nodes.new("ShaderNodeMix")
    mix.location = (1181.0, -175.0)
    label_node(mix, "", frame_007)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[0].default_value = 0.5
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (881.5, -522.4)
    label_node(bevel, "", frame_008)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    group_041 = nodes.new("ShaderNodeGroup")
    group_041.location = (496.9, -254.3)
    label_node(group_041, "", frame_008)
    group_041.xl_c4d_gradient_type = '0'
    group_041.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_041.node_tree = nf_grunge_02_r()
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.1818181574344635
    color_ramp_002.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.6045454740524292
    color_ramp_002.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (778.6, -254.3)
    label_node(color_ramp_002, "", frame_008)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1317.2, -254.3)
    label_node(bump, "", frame_008)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1002.7, -582.8)
    label_node(all_edges_013, "", frame_009)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 1.0
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (508.0, -575.4)
    label_node(group_029, "", frame_009)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_22d_r()
    group_029.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (6532.7, -2054.6)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[1].default_value = 0.504531741142273
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
    mix_shader.location = (7666.9, -1286.0)
    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.location = (695.4, -1304.0)
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_001.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[7].default_value = (0.0930, 0.0633, 0.0512, 1.0000)
    mix_001.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    cavity_013 = nodes.new("ShaderNodeGroup")
    cavity_013.location = (1501.2, -385.2)
    label_node(cavity_013, "", frame_003)
    cavity_013.xl_c4d_gradient_type = '0'
    cavity_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_013.node_tree = cavity()
    cavity_013.inputs[2].default_value = 0.5
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (550.6, -388.7)
    label_node(group_034, "", frame_003)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_15_r()
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (741.2, -385.2)
    label_node(map_range_003, "", frame_003)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 1.0
    map_range_003.inputs[3].default_value = -0.38999998569488525
    map_range_003.inputs[4].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (2.5, -1302.4)
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
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (438.3, -102.0)
    label_node(group_030, "", frame_001)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_22d_r()
    group_030.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_004 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_004 | Color Ramp.004
    color_ramp_004.color_ramp.color_mode = 'RGB'
    color_ramp_004.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_004.color_ramp.interpolation = 'EASE'
    while len(color_ramp_004.color_ramp.elements) > 2:
        color_ramp_004.color_ramp.elements.remove(color_ramp_004.color_ramp.elements[-1])
    while len(color_ramp_004.color_ramp.elements) < 2:
        color_ramp_004.color_ramp.elements.new(0.5)
    color_ramp_004.color_ramp.elements[0].position = 0.4747188687324524
    color_ramp_004.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp_004.color_ramp.elements[1].position = 0.664665699005127
    color_ramp_004.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    # XL_PF_RAMP_END color_ramp_004
    color_ramp_004.location = (735.9, -102.0)
    label_node(color_ramp_004, "", frame_001)
    color_ramp_005 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_005 | Color Ramp.005
    color_ramp_005.color_ramp.color_mode = 'RGB'
    color_ramp_005.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_005.color_ramp.interpolation = 'EASE'
    while len(color_ramp_005.color_ramp.elements) > 2:
        color_ramp_005.color_ramp.elements.remove(color_ramp_005.color_ramp.elements[-1])
    while len(color_ramp_005.color_ramp.elements) < 2:
        color_ramp_005.color_ramp.elements.new(0.5)
    color_ramp_005.color_ramp.elements[0].position = 0.9090908765792847
    color_ramp_005.color_ramp.elements[0].color = (0.04745437204837799, 0.010326914489269257, 0.00836277101188898, 1.0)
    color_ramp_005.color_ramp.elements[1].position = 1.0
    color_ramp_005.color_ramp.elements[1].color = (0.03636204078793526, 0.03636204078793526, 0.03636204078793526, 1.0)
    # XL_PF_RAMP_END color_ramp_005
    color_ramp_005.location = (1025.6, -193.2)
    label_node(color_ramp_005, "", frame_001)
    separate_xyz = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (410.3, -102.4)
    label_node(separate_xyz, "", frame_004)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (220.3, -102.4)
    label_node(mapping, "", frame_004)
    mapping.vector_type = 'POINT'
    mapping.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate = nodes.new("ShaderNodeTexCoord")
    texture_coordinate.location = (30.3, -102.4)
    label_node(texture_coordinate, "", frame_004)
    texture_coordinate.from_instancer = False
    color_ramp_006 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_006 | Color Ramp.006
    color_ramp_006.color_ramp.color_mode = 'RGB'
    color_ramp_006.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_006.color_ramp.interpolation = 'EASE'
    while len(color_ramp_006.color_ramp.elements) > 2:
        color_ramp_006.color_ramp.elements.remove(color_ramp_006.color_ramp.elements[-1])
    while len(color_ramp_006.color_ramp.elements) < 2:
        color_ramp_006.color_ramp.elements.new(0.5)
    color_ramp_006.color_ramp.elements[0].position = 0.2900303304195404
    color_ramp_006.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp_006.color_ramp.elements[1].position = 0.3987913131713867
    color_ramp_006.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    # XL_PF_RAMP_END color_ramp_006
    color_ramp_006.location = (612.8, -102.4)
    label_node(color_ramp_006, "", frame_004)
    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.location = (2039.7, -1303.6)
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
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (915.3, -102.4)
    label_node(mix_004, "", frame_004)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[7].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_031 = nodes.new("ShaderNodeGroup")
    group_031.location = (413.1, -457.3)
    label_node(group_031, "", frame_004)
    group_031.xl_c4d_gradient_type = '0'
    group_031.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_031.node_tree = pf_grunge_22d_r()
    group_031.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_007 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_007 | Color Ramp.007
    color_ramp_007.color_ramp.color_mode = 'RGB'
    color_ramp_007.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_007.color_ramp.interpolation = 'EASE'
    while len(color_ramp_007.color_ramp.elements) > 2:
        color_ramp_007.color_ramp.elements.remove(color_ramp_007.color_ramp.elements[-1])
    while len(color_ramp_007.color_ramp.elements) < 2:
        color_ramp_007.color_ramp.elements.new(0.5)
    color_ramp_007.color_ramp.elements[0].position = 0.39404019713401794
    color_ramp_007.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp_007.color_ramp.elements[1].position = 0.531626284122467
    color_ramp_007.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    # XL_PF_RAMP_END color_ramp_007
    color_ramp_007.location = (622.5, -311.8)
    label_node(color_ramp_007, "", frame_004)
    cavity_017 = nodes.new("ShaderNodeGroup")
    cavity_017.location = (932.6, -190.3)
    label_node(cavity_017, "", frame_006)
    cavity_017.xl_c4d_gradient_type = '0'
    cavity_017.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_017.node_tree = cavity()
    cavity_017.inputs[2].default_value = 1.1100002527236938
    group_042 = nodes.new("ShaderNodeGroup")
    group_042.location = (406.7, -140.0)
    label_node(group_042, "", frame_006)
    group_042.xl_c4d_gradient_type = '0'
    group_042.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_042.node_tree = pf_grunge_15_r()
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (671.2, -344.9)
    label_node(map_range_007, "", frame_006)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 0.42000001668930054
    map_range_007.inputs[4].default_value = 0.42999839782714844
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.location = (3361.4, -1303.0)
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    mix_005.blend_type = 'MIX'
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    mix_005.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_005.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[7].default_value = (0.0278, 0.0278, 0.0278, 1.0000)
    mix_005.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mix_007 = nodes.new("ShaderNodeMix")
    mix_007.location = (2694.3, -1301.0)
    mix_007.data_type = 'RGBA'
    mix_007.factor_mode = 'UNIFORM'
    mix_007.blend_type = 'MIX'
    mix_007.clamp_factor = True
    mix_007.clamp_result = False
    mix_007.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_007.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (399.8, -124.8)
    label_node(group_032, "", frame_005)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = pf_grunge_06_r()
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (802.5, -124.8)
    label_node(map_range, "", frame_005)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (1007.0, -435.7)
    label_node(all_edges_014, "", frame_009)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 1.0
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (722.6, -575.4)
    label_node(map_range_001, "", frame_009)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[3].default_value = -2.180000066757202
    map_range_001.inputs[4].default_value = 2.4700000286102295
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (1714.0, -710.6)
    label_node(mix_006, "", frame_009)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[7].default_value = (0.0687, 0.0457, 0.0383, 1.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (1720.9, -1147.2)
    label_node(bump_001, "", frame_009)
    bump_001.invert = True
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    mix_008 = nodes.new("ShaderNodeMix")
    mix_008.location = (-636.6, -1302.4)
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
    color_ramp_009 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_009 | Color Ramp.009
    color_ramp_009.color_ramp.color_mode = 'RGB'
    color_ramp_009.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_009.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_009.color_ramp.elements) > 2:
        color_ramp_009.color_ramp.elements.remove(color_ramp_009.color_ramp.elements[-1])
    while len(color_ramp_009.color_ramp.elements) < 2:
        color_ramp_009.color_ramp.elements.new(0.5)
    color_ramp_009.color_ramp.elements[0].position = 0.5772724151611328
    color_ramp_009.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_009.color_ramp.elements[1].position = 0.5954546332359314
    color_ramp_009.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_009
    color_ramp_009.location = (1249.8, -101.9)
    label_node(color_ramp_009, "", frame)
    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.location = (804.1, -191.3)
    label_node(noise_texture, "", frame)
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    noise_texture.inputs[2].default_value = 0.25
    noise_texture.inputs[3].default_value = 15.0
    noise_texture.inputs[4].default_value = 0.6288673877716064
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[7].default_value = 1.0
    mapping_001 = nodes.new("ShaderNodeMapping")
    mapping_001.location = (614.1, -191.3)
    label_node(mapping_001, "", frame)
    mapping_001.vector_type = 'POINT'
    mapping_001.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (138.0, -191.3)
    label_node(texture_coordinate_001, "", frame)
    texture_coordinate_001.from_instancer = False
    vector_transform = nodes.new("ShaderNodeVectorTransform")
    vector_transform.location = (324.2, -191.3)
    label_node(vector_transform, "", frame)
    vector_transform.vector_type = 'VECTOR'
    vector_transform.convert_from = 'OBJECT'
    vector_transform.convert_to = 'WORLD'
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (1370.1, -589.3)
    label_node(hue_saturation_value, "", frame)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 0.7699999809265137
    hue_saturation_value.inputs[2].default_value = 0.5899999737739563
    hue_saturation_value.inputs[3].default_value = 1.0
    mix_009 = nodes.new("ShaderNodeMix")
    mix_009.location = (1324.9, -1303.7)
    mix_009.data_type = 'RGBA'
    mix_009.factor_mode = 'UNIFORM'
    mix_009.blend_type = 'MIX'
    mix_009.clamp_factor = True
    mix_009.clamp_result = False
    mix_009.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_009.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_009.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_009.inputs[7].default_value = (0.0174, 0.0121, 0.0114, 1.0000)
    mix_009.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    all_edges_015 = nodes.new("ShaderNodeGroup")
    all_edges_015.location = (1501.2, -106.5)
    label_node(all_edges_015, "", frame_003)
    all_edges_015.xl_c4d_gradient_type = '0'
    all_edges_015.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_015.node_tree = all_edges()
    all_edges_015.inputs[2].default_value = 5.0
    group_033 = nodes.new("ShaderNodeGroup")
    group_033.location = (550.6, -113.5)
    label_node(group_033, "", frame_003)
    group_033.xl_c4d_gradient_type = '0'
    group_033.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_033.node_tree = pf_grunge_15_r()
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (1025.2, -106.5)
    label_node(map_range_002, "", frame_003)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 1.0
    map_range_002.inputs[3].default_value = -0.25
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.4136362373828888
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.46818190813064575
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (735.2, -106.5)
    label_node(color_ramp_003, "", frame_003)
    color_ramp_010 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_010 | Color Ramp.010
    color_ramp_010.color_ramp.color_mode = 'RGB'
    color_ramp_010.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_010.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_010.color_ramp.elements) > 2:
        color_ramp_010.color_ramp.elements.remove(color_ramp_010.color_ramp.elements[-1])
    while len(color_ramp_010.color_ramp.elements) < 2:
        color_ramp_010.color_ramp.elements.new(0.5)
    color_ramp_010.color_ramp.elements[0].position = 0.1087612733244896
    color_ramp_010.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_010.color_ramp.elements[1].position = 0.19460317492485046
    color_ramp_010.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_010
    color_ramp_010.location = (1025.1, -143.2)
    label_node(color_ramp_010, "", frame_005)
    mix_010 = nodes.new("ShaderNodeMix")
    mix_010.location = (1315.1, -143.2)
    label_node(mix_010, "", frame_005)
    mix_010.data_type = 'RGBA'
    mix_010.factor_mode = 'UNIFORM'
    mix_010.blend_type = 'MIX'
    mix_010.clamp_factor = True
    mix_010.clamp_result = False
    mix_010.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_010.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_010.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_010.inputs[6].default_value = (0.2214, 0.1744, 0.1225, 1.0000)
    mix_010.inputs[7].default_value = (0.0641, 0.0438, 0.0405, 1.0000)
    mix_010.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mix_011 = nodes.new("ShaderNodeMix")
    mix_011.location = (922.2, -360.1)
    label_node(mix_011, "", frame_004)
    mix_011.data_type = 'RGBA'
    mix_011.factor_mode = 'UNIFORM'
    mix_011.blend_type = 'MIX'
    mix_011.clamp_factor = True
    mix_011.clamp_result = False
    mix_011.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_011.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_011.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_011.inputs[7].default_value = (0.0952, 0.0839, 0.0414, 1.0000)
    mix_011.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mix_012 = nodes.new("ShaderNodeMix")
    mix_012.location = (1610.3, -449.7)
    label_node(mix_012, "", frame)
    mix_012.data_type = 'RGBA'
    mix_012.factor_mode = 'UNIFORM'
    mix_012.blend_type = 'MIX'
    mix_012.clamp_factor = True
    mix_012.clamp_result = False
    mix_012.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_012.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_012.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_012.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_012 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_012 | Color Ramp.012
    color_ramp_012.color_ramp.color_mode = 'RGB'
    color_ramp_012.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_012.color_ramp.interpolation = 'CARDINAL'
    while len(color_ramp_012.color_ramp.elements) > 2:
        color_ramp_012.color_ramp.elements.remove(color_ramp_012.color_ramp.elements[-1])
    while len(color_ramp_012.color_ramp.elements) < 2:
        color_ramp_012.color_ramp.elements.new(0.5)
    color_ramp_012.color_ramp.elements[0].position = 0.6025541424751282
    color_ramp_012.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
    color_ramp_012.color_ramp.elements[1].position = 0.6166301965713501
    color_ramp_012.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
    # XL_PF_RAMP_END color_ramp_012
    color_ramp_012.location = (1255.2, -319.1)
    label_node(color_ramp_012, "", frame)
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (6656.4, -1899.6)
    reroute_004.socket_idname = 'NodeSocketFloat'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (6021.8, -2308.3)
    reroute_005.socket_idname = 'NodeSocketVector'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (6030.8, -2108.6)
    reroute_006.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-602.4, -1106.0)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-602.4, -1197.5)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-379.9, -813.5)
    reroute_010.socket_idname = 'NodeSocketFloat'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-189.6, -535.9)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-3673.4, -1497.5)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (-3673.4, -1477.2)
    reroute_013.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (-3673.4, -1456.4)
    reroute_014.socket_idname = 'NodeSocketColor'
    reroute = nodes.new("NodeReroute")
    reroute.location = (4004.1, -1439.0)
    reroute.socket_idname = 'NodeSocketVector'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (3709.4, -1386.2)
    reroute_015.socket_idname = 'NodeSocketColor'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (527.2, -122.5)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (684.9, 115.1)
    reroute_002.socket_idname = 'NodeSocketColor'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (1225.5, 464.6)
    reroute_003.socket_idname = 'NodeSocketColor'
    invert_color = nodes.new("ShaderNodeInvert")
    invert_color.location = (1314.8, -105.6)
    label_node(invert_color, "", frame_005)
    invert_color.inputs[0].default_value = 1.0
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (1264.3, 524.1)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (1679.0, -1578.8)
    label_node(reroute_017, "", frame_009)
    reroute_017.socket_idname = 'NodeSocketVector'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (6774.8, -1364.1)
    reroute_018.socket_idname = 'NodeSocketShader'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (7120.1, -1344.8)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (7255.9, -1384.6)
    reroute_020.socket_idname = 'NodeSocketShader'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (3295.9, -1874.1)
    reroute_021.socket_idname = 'NodeSocketColor'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (3176.5, -2655.8)
    reroute_022.socket_idname = 'NodeSocketVector'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (1026.0, -119.2)
    label_node(reroute_023, "", frame_005)
    reroute_023.socket_idname = 'NodeSocketFloat'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (1154.9, -612.6)
    label_node(reroute_024, "", frame)
    reroute_024.socket_idname = 'NodeSocketColor'
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (355.5, -469.7)
    label_node(map_range_004, "", frame)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.25
    map_range_004.inputs[4].default_value = 3.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (263.4, -213.1)
    label_node(map_range_005, "", frame_001)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.10000000149011612
    map_range_005.inputs[4].default_value = 0.5600000023841858
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (371.2, -112.1)
    label_node(map_range_006, "", frame_003)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.10000000149011612
    map_range_006.inputs[4].default_value = 1.0
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (371.2, -388.9)
    label_node(map_range_008, "", frame_003)
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
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (1281.0, -101.9)
    label_node(map_range_009, "", frame_003)
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
    map_range_010.location = (1279.8, -348.3)
    label_node(map_range_010, "", frame_003)
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
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (973.7, -599.1)
    label_node(reroute_025, "", frame_003)
    reroute_025.socket_idname = 'NodeSocketFloat'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1424.5, -599.1)
    label_node(reroute_026, "", frame_003)
    reroute_026.socket_idname = 'NodeSocketFloat'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (1271.3, -339.4)
    label_node(reroute_027, "", frame_003)
    reroute_027.socket_idname = 'NodeSocketFloat'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (1445.6, -338.9)
    label_node(reroute_028, "", frame_003)
    reroute_028.socket_idname = 'NodeSocketFloat'
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (226.0, -521.1)
    label_node(map_range_011, "", frame_004)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = -0.04999998211860657
    map_range_011.inputs[4].default_value = 1.0
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_012 = nodes.new("ShaderNodeMapRange")
    map_range_012.location = (235.4, -254.7)
    label_node(map_range_012, "", frame_005)
    map_range_012.clamp = True
    map_range_012.interpolation_type = 'LINEAR'
    map_range_012.data_type = 'FLOAT'
    map_range_012.inputs[2].default_value = 100.0
    map_range_012.inputs[3].default_value = 0.15000000596046448
    map_range_012.inputs[4].default_value = 0.3800000250339508
    map_range_012.inputs[5].default_value = 4.0
    map_range_012.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_012.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_012.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_013 = nodes.new("ShaderNodeMapRange")
    map_range_013.location = (621.7, -252.9)
    label_node(map_range_013, "", frame_005)
    map_range_013.clamp = True
    map_range_013.interpolation_type = 'LINEAR'
    map_range_013.data_type = 'FLOAT'
    map_range_013.inputs[2].default_value = 100.0
    map_range_013.inputs[3].default_value = -1.8100000619888306
    map_range_013.inputs[4].default_value = -1.3399999141693115
    map_range_013.inputs[5].default_value = 4.0
    map_range_013.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_013.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_013.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_014 = nodes.new("ShaderNodeMapRange")
    map_range_014.location = (449.2, -344.6)
    label_node(map_range_014, "", frame_006)
    map_range_014.clamp = True
    map_range_014.interpolation_type = 'LINEAR'
    map_range_014.data_type = 'FLOAT'
    map_range_014.inputs[2].default_value = 100.0
    map_range_014.inputs[3].default_value = -0.10000020265579224
    map_range_014.inputs[4].default_value = 2.820000171661377
    map_range_014.inputs[5].default_value = 4.0
    map_range_014.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_014.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_014.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_015 = nodes.new("ShaderNodeMapRange")
    map_range_015.location = (672.4, -101.7)
    label_node(map_range_015, "", frame_006)
    map_range_015.clamp = False
    map_range_015.interpolation_type = 'LINEAR'
    map_range_015.data_type = 'FLOAT'
    map_range_015.inputs[2].default_value = 100.0
    map_range_015.inputs[3].default_value = -0.16999998688697815
    map_range_015.inputs[4].default_value = 0.2199999988079071
    map_range_015.inputs[5].default_value = 4.0
    map_range_015.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_015.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_015.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_016 = nodes.new("ShaderNodeMapRange")
    map_range_016.location = (227.0, -150.2)
    label_node(map_range_016, "", frame_006)
    map_range_016.clamp = True
    map_range_016.interpolation_type = 'LINEAR'
    map_range_016.data_type = 'FLOAT'
    map_range_016.inputs[2].default_value = 100.0
    map_range_016.inputs[3].default_value = 0.10000000149011612
    map_range_016.inputs[4].default_value = 1.0
    map_range_016.inputs[5].default_value = 4.0
    map_range_016.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_016.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_016.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_017 = nodes.new("ShaderNodeMapRange")
    map_range_017.location = (328.4, -253.7)
    label_node(map_range_017, "", frame_008)
    map_range_017.clamp = True
    map_range_017.interpolation_type = 'LINEAR'
    map_range_017.data_type = 'FLOAT'
    map_range_017.inputs[2].default_value = 100.0
    map_range_017.inputs[3].default_value = 0.10000000149011612
    map_range_017.inputs[4].default_value = 1.0
    map_range_017.inputs[5].default_value = 4.0
    map_range_017.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_017.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_017.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_018 = nodes.new("ShaderNodeMapRange")
    map_range_018.location = (252.0, -101.9)
    label_node(map_range_018, "", frame_007)
    map_range_018.clamp = True
    map_range_018.interpolation_type = 'LINEAR'
    map_range_018.data_type = 'FLOAT'
    map_range_018.inputs[2].default_value = 100.0
    map_range_018.inputs[3].default_value = 0.10000000149011612
    map_range_018.inputs[4].default_value = 0.8400000333786011
    map_range_018.inputs[5].default_value = 4.0
    map_range_018.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_018.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_018.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_018.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_019 = nodes.new("ShaderNodeMapRange")
    map_range_019.location = (248.3, -350.3)
    label_node(map_range_019, "", frame_007)
    map_range_019.clamp = True
    map_range_019.interpolation_type = 'LINEAR'
    map_range_019.data_type = 'FLOAT'
    map_range_019.inputs[2].default_value = 100.0
    map_range_019.inputs[3].default_value = 0.20000000298023224
    map_range_019.inputs[4].default_value = 1.8899999856948853
    map_range_019.inputs[5].default_value = 4.0
    map_range_019.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_019.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_019.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_019.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math = nodes.new("ShaderNodeMath")
    math.location = (1099.2, -389.5)
    label_node(math, "", frame_008)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (1187.1, -554.9)
    label_node(reroute_029, "", frame_008)
    reroute_029.socket_idname = 'NodeSocketVector'
    map_range_020 = nodes.new("ShaderNodeMapRange")
    map_range_020.location = (661.9, -565.9)
    label_node(map_range_020, "", frame_008)
    map_range_020.clamp = True
    map_range_020.interpolation_type = 'LINEAR'
    map_range_020.data_type = 'FLOAT'
    map_range_020.inputs[2].default_value = 100.0
    map_range_020.inputs[3].default_value = 9.999999747378752e-05
    map_range_020.inputs[4].default_value = 0.019999999552965164
    map_range_020.inputs[5].default_value = 4.0
    map_range_020.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_020.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_020.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_020.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (1389.2, -1264.6)
    label_node(math_001, "", frame_009)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (1891.3, -744.3)
    label_node(reroute_032, "", frame_009)
    reroute_032.socket_idname = 'NodeSocketColor'
    color_ramp_008 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_008 | Color Ramp.008
    color_ramp_008.color_ramp.color_mode = 'RGB'
    color_ramp_008.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_008.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_008.color_ramp.elements) > 2:
        color_ramp_008.color_ramp.elements.remove(color_ramp_008.color_ramp.elements[-1])
    while len(color_ramp_008.color_ramp.elements) < 2:
        color_ramp_008.color_ramp.elements.new(0.5)
    color_ramp_008.color_ramp.elements[0].position = 0.0
    color_ramp_008.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_008.color_ramp.elements[1].position = 1.0
    color_ramp_008.color_ramp.elements[1].color = (0.0636003315448761, 0.0636003315448761, 0.0636003315448761, 1.0)
    # XL_PF_RAMP_END color_ramp_008
    color_ramp_008.location = (1536.0, -1264.6)
    label_node(color_ramp_008, "", frame_009)
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (6729.2, -2086.8)
    reroute_033.socket_idname = 'NodeSocketShader'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (1354.2, -615.1)
    label_node(reroute_034, "", frame_009)
    reroute_034.socket_idname = 'NodeSocketFloat'
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (1346.0, -437.7)
    label_node(reroute_035, "", frame_009)
    reroute_035.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (5989.2, -1899.1)
    reroute_037.socket_idname = 'NodeSocketFloat'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (1960.5, -616.5)
    label_node(reroute_038, "", frame_009)
    reroute_038.socket_idname = 'NodeSocketFloat'
    invert_color_001 = nodes.new("ShaderNodeInvert")
    invert_color_001.location = (6019.8, -2168.0)
    invert_color_001.inputs[0].default_value = 1.0
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (6224.0, -2151.3)
    math_002.operation = 'ADD'
    math_002.use_clamp = True
    math_002.inputs[1].default_value = 0.6000000238418579
    math_002.inputs[2].default_value = 0.5
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (6394.6, -2308.3)
    reroute_039.socket_idname = 'NodeSocketVector'
    hue_saturation_value_001 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_001.location = (1492.3, -852.0)
    label_node(hue_saturation_value_001, "", frame_009)
    hue_saturation_value_001.inputs[1].default_value = 0.6000000238418579
    hue_saturation_value_001.inputs[3].default_value = 0.6747967600822449
    map_range_022 = nodes.new("ShaderNodeMapRange")
    map_range_022.location = (324.4, -576.9)
    label_node(map_range_022, "", frame_009)
    map_range_022.clamp = True
    map_range_022.interpolation_type = 'LINEAR'
    map_range_022.data_type = 'FLOAT'
    map_range_022.inputs[2].default_value = 100.0
    map_range_022.inputs[3].default_value = 0.20000000298023224
    map_range_022.inputs[4].default_value = 0.6000000238418579
    map_range_022.inputs[5].default_value = 4.0
    map_range_022.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_022.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_022.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_022.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_022.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_022.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_023 = nodes.new("ShaderNodeMapRange")
    map_range_023.location = (718.8, -101.7)
    label_node(map_range_023, "", frame_009)
    map_range_023.clamp = True
    map_range_023.interpolation_type = 'LINEAR'
    map_range_023.data_type = 'FLOAT'
    map_range_023.inputs[2].default_value = 100.0
    map_range_023.inputs[4].default_value = 0.44999998807907104
    map_range_023.inputs[5].default_value = 4.0
    map_range_023.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_023.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_023.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_023.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_023.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_023.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_024 = nodes.new("ShaderNodeMapRange")
    map_range_024.location = (718.8, -336.2)
    label_node(map_range_024, "", frame_009)
    map_range_024.clamp = True
    map_range_024.interpolation_type = 'LINEAR'
    map_range_024.data_type = 'FLOAT'
    map_range_024.inputs[2].default_value = 100.0
    map_range_024.inputs[4].default_value = 0.2200000137090683
    map_range_024.inputs[5].default_value = 4.0
    map_range_024.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_024.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_024.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_024.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_024.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_024.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    hue_saturation_value_002 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_002.location = (1374.8, -773.8)
    label_node(hue_saturation_value_002, "", frame)
    hue_saturation_value_002.inputs[0].default_value = 0.5
    hue_saturation_value_002.inputs[1].default_value = 0.6900001168251038
    hue_saturation_value_002.inputs[2].default_value = 0.5400000214576721
    hue_saturation_value_002.inputs[3].default_value = 1.0
    hue_saturation_value_003 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_003.location = (1374.1, -959.0)
    label_node(hue_saturation_value_003, "", frame)
    hue_saturation_value_003.inputs[0].default_value = 0.5
    hue_saturation_value_003.inputs[1].default_value = 1.0500000715255737
    hue_saturation_value_003.inputs[2].default_value = 0.6399999856948853
    hue_saturation_value_003.inputs[3].default_value = 1.0
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (-1591.5, -2210.6)
    reroute_036.socket_idname = 'NodeSocketColor'
    group_043 = nodes.new("ShaderNodeGroup")
    group_043.location = (0.0, 0.0)
    group_043.xl_c4d_gradient_type = '0'
    group_043.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_001 = nodes.new("ShaderNodeGroup")
    group_001.location = (0.0, 0.0)
    group_001.xl_c4d_gradient_type = '0'
    group_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (1092.6, -101.9)
    label_node(hs_bump_control, "", frame_008)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (35.0, -1228.2)
    label_node(reroute_030, "", frame_009)
    reroute_030.socket_idname = 'NodeSocketFloat'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (3483.1, -2501.8)
    reroute_040.socket_idname = 'NodeSocketFloat'
    reroute_041 = nodes.new("NodeReroute")
    reroute_041.location = (1211.4, -614.9)
    label_node(reroute_041, "", frame_009)
    reroute_041.socket_idname = 'NodeSocketFloat'
    reroute_042 = nodes.new("NodeReroute")
    reroute_042.location = (1229.2, -1366.2)
    label_node(reroute_042, "", frame_009)
    reroute_042.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (1281.8, -676.0)
    label_node(reroute_016, "", frame_008)
    reroute_016.socket_idname = 'NodeSocketVector'
    reroute_043 = nodes.new("NodeReroute")
    reroute_043.location = (1189.6, -1389.3)
    label_node(reroute_043, "", frame_009)
    reroute_043.socket_idname = 'NodeSocketFloat'
    perlin_noise = nodes.new("ShaderNodeGroup")
    perlin_noise.location = (1026.9, -1277.1)
    label_node(perlin_noise, "", frame_009)
    perlin_noise.xl_c4d_gradient_type = '0'
    perlin_noise.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise.node_tree = perlin_noise_main003()
    perlin_noise.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise.inputs[2].default_value = 16.0
    perlin_noise.inputs[3].default_value = 6.0
    perlin_noise.inputs[4].default_value = 0.6899999976158142
    perlin_noise.inputs[5].default_value = 2.5
    perlin_noise.inputs[7].default_value = 60.0
    perlin_noise.inputs[8].default_value = 0.07999999821186066
    perlin_noise.inputs[9].default_value = 0.4000000059604645
    perlin_noise_001 = nodes.new("ShaderNodeGroup")
    perlin_noise_001.location = (0.0, 0.0)
    perlin_noise_001.xl_c4d_gradient_type = '0'
    perlin_noise_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise_001.node_tree = perlin_noise001_node_tree003()
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
    perlin_noise_002.node_tree = perlin_noise002_node_tree003()
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
    perlin_noise_003.node_tree = perlin_noise003_node_tree003()
    perlin_noise_003.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise_003.inputs[2].default_value = 8.0
    perlin_noise_003.inputs[3].default_value = 10.0
    perlin_noise_003.inputs[5].default_value = 2.0
    perlin_noise_003.inputs[7].default_value = 60.0
    perlin_noise_003.inputs[9].default_value = 1.0

    # === 节点连接 ===
    links.new(reroute_011.outputs[0], mix_009.inputs[0])
    links.new(texture_coordinate_001.outputs[3], vector_transform.inputs[0])
    links.new(mix_002.outputs[2], mix_001.inputs[6])
    links.new(mix_001.outputs[2], mix_009.inputs[6])
    links.new(reroute_024.outputs[0], hue_saturation_value.inputs[4])
    links.new(vector_transform.outputs[0], mapping_001.inputs[0])
    links.new(reroute_013.outputs[0], mix_008.inputs[6])
    links.new(reroute_015.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_019.outputs[0], mix_shader.inputs[0])
    links.new(reroute_020.outputs[0], mix_shader.inputs[2])
    links.new(group_030.outputs[0], color_ramp_004.inputs[0])
    links.new(reroute_018.outputs[0], mix_shader.inputs[1])
    links.new(mapping_001.outputs[0], noise_texture.inputs[0])
    links.new(reroute_014.outputs[0], mix_008.inputs[0])
    links.new(color_ramp_001.outputs[0], mix.inputs[7])
    links.new(reroute_017.outputs[0], bump_001.inputs[4])
    links.new(color_ramp_003.outputs[0], map_range_002.inputs[0])
    links.new(math.outputs[0], bump.inputs[3])
    links.new(group_041.outputs[0], color_ramp_002.inputs[0])
    links.new(reroute_006.outputs[0], principled_bsdf_001.inputs[0])
    links.new(group_040.outputs[0], color_ramp_001.inputs[0])
    links.new(group_039.outputs[0], color_ramp.inputs[0])
    links.new(group_029.outputs[0], map_range_001.inputs[0])
    links.new(reroute_002.outputs[0], mix_003.inputs[0])
    links.new(mix_007.outputs[2], mix_005.inputs[6])
    links.new(mix_005.outputs[2], principled_bsdf.inputs[0])
    links.new(group_042.outputs[0], map_range_007.inputs[0])
    links.new(color_ramp_007.outputs[0], mix_004.inputs[0])
    links.new(group_031.outputs[0], color_ramp_007.inputs[0])
    links.new(reroute.outputs[0], principled_bsdf.inputs[5])
    links.new(reroute_007.outputs[0], mix_007.inputs[0])
    links.new(color_ramp_006.outputs[0], mix_004.inputs[6])
    links.new(color_ramp_007.outputs[0], mix_011.inputs[0])
    links.new(texture_coordinate.outputs[1], mapping.inputs[0])
    links.new(color_ramp_008.outputs[0], bump_001.inputs[3])
    links.new(separate_xyz.outputs[2], color_ramp_006.inputs[0])
    links.new(group_032.outputs[0], map_range.inputs[0])
    links.new(mapping.outputs[0], separate_xyz.inputs[0])
    links.new(color_ramp_010.outputs[0], mix_010.inputs[0])
    links.new(color_ramp.outputs[0], mix.inputs[6])
    links.new(reroute_008.outputs[0], mix_002.inputs[0])
    links.new(color_ramp_004.outputs[0], color_ramp_005.inputs[0])
    links.new(map_range.outputs[0], color_ramp_010.inputs[0])
    links.new(group_034.outputs[0], map_range_003.inputs[0])
    links.new(group_033.outputs[0], color_ramp_003.inputs[0])
    links.new(hue_saturation_value.outputs[0], mix_012.inputs[6])
    links.new(reroute_012.outputs[0], mix_008.inputs[7])
    links.new(noise_texture.outputs[0], color_ramp_009.inputs[0])
    links.new(noise_texture.outputs[0], color_ramp_012.inputs[0])
    links.new(color_ramp_012.outputs[0], mix_012.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(reroute_010.outputs[0], mix_001.inputs[0])
    links.new(reroute_029.outputs[0], bump.inputs[4])
    links.new(reroute_037.outputs[0], reroute_004.inputs[0])
    links.new(bump_001.outputs[0], reroute_005.inputs[0])
    links.new(reroute_032.outputs[0], reroute_006.inputs[0])
    links.new(color_ramp_004.outputs[0], reroute_008.inputs[0])
    links.new(color_ramp_005.outputs[0], reroute_009.inputs[0])
    links.new(mix_008.outputs[2], mix_002.inputs[7])
    links.new(reroute_009.outputs[0], mix_002.inputs[6])
    links.new(mix_012.outputs[2], reroute_012.inputs[0])
    links.new(reroute_024.outputs[0], reroute_013.inputs[0])
    links.new(color_ramp_009.outputs[0], reroute_014.inputs[0])
    links.new(mix_009.outputs[2], mix_003.inputs[7])
    links.new(reroute_001.outputs[0], mix_003.inputs[6])
    links.new(reroute_022.outputs[0], reroute.inputs[0])
    links.new(reroute_021.outputs[0], reroute_015.inputs[0])
    links.new(mix_011.outputs[2], reroute_001.inputs[0])
    links.new(mix_004.outputs[2], reroute_002.inputs[0])
    links.new(mix_010.outputs[2], reroute_003.inputs[0])
    links.new(mix_003.outputs[2], mix_007.inputs[7])
    links.new(reroute_003.outputs[0], mix_007.inputs[6])
    links.new(reroute_023.outputs[0], invert_color.inputs[1])
    links.new(invert_color.outputs[0], reroute_007.inputs[0])
    links.new(reroute_016.outputs[0], reroute_017.inputs[0])
    links.new(principled_bsdf.outputs[0], reroute_018.inputs[0])
    links.new(reroute_004.outputs[0], reroute_019.inputs[0])
    links.new(reroute_033.outputs[0], reroute_020.inputs[0])
    links.new(mix.outputs[2], reroute_021.inputs[0])
    links.new(bump.outputs[0], reroute_022.inputs[0])
    links.new(map_range.outputs[0], reroute_023.inputs[0])
    links.new(map_range_004.outputs[0], mapping_001.inputs[3])
    links.new(input_node.outputs[14], mapping_001.inputs[1])
    links.new(input_node.outputs[9], reroute_024.inputs[0])
    links.new(map_range_005.outputs[0], group_030.inputs[1])
    links.new(input_node.outputs[10], map_range_005.inputs[0])
    links.new(map_range_006.outputs[0], group_033.inputs[0])
    links.new(input_node.outputs[11], map_range_006.inputs[0])
    links.new(input_node.outputs[11], map_range_008.inputs[0])
    links.new(map_range_008.outputs[0], group_034.inputs[0])
    links.new(map_range_003.outputs[0], reroute_025.inputs[0])
    links.new(reroute_025.outputs[0], reroute_026.inputs[0])
    links.new(map_range_002.outputs[0], reroute_027.inputs[0])
    links.new(reroute_027.outputs[0], reroute_028.inputs[0])
    links.new(input_node.outputs[12], map_range_009.inputs[0])
    links.new(input_node.outputs[6], map_range_010.inputs[0])
    links.new(map_range_011.outputs[0], group_031.inputs[1])
    links.new(map_range_012.outputs[0], group_032.inputs[1])
    links.new(input_node.outputs[18], group_032.inputs[0])
    links.new(map_range_013.outputs[0], map_range.inputs[3])
    links.new(input_node.outputs[16], map_range_012.inputs[0])
    links.new(input_node.outputs[17], map_range_013.inputs[0])
    links.new(map_range_014.outputs[0], map_range_007.inputs[3])
    links.new(input_node.outputs[5], map_range_014.inputs[0])
    links.new(map_range_016.outputs[0], group_042.inputs[0])
    links.new(input_node.outputs[6], map_range_015.inputs[0])
    links.new(input_node.outputs[4], map_range_016.inputs[0])
    links.new(map_range_017.outputs[0], group_041.inputs[0])
    links.new(input_node.outputs[15], map_range_018.inputs[0])
    links.new(input_node.outputs[15], map_range_019.inputs[0])
    links.new(map_range_018.outputs[0], group_039.inputs[0])
    links.new(map_range_019.outputs[0], group_040.inputs[0])
    links.new(color_ramp_002.outputs[0], math.inputs[0])
    links.new(input_node.outputs[1], math.inputs[1])
    links.new(bevel.outputs[0], reroute_029.inputs[0])
    links.new(map_range_020.outputs[0], bevel.inputs[0])
    links.new(input_node.outputs[0], map_range_020.inputs[0])
    links.new(input_node.outputs[2], map_range_017.inputs[0])
    links.new(mix_006.outputs[2], reroute_032.inputs[0])
    links.new(math_001.outputs[0], color_ramp_008.inputs[0])
    links.new(principled_bsdf_001.outputs[0], reroute_033.inputs[0])
    links.new(reroute_034.outputs[0], mix_006.inputs[0])
    links.new(reroute_035.outputs[0], reroute_037.inputs[0])
    links.new(reroute_034.outputs[0], reroute_038.inputs[0])
    links.new(reroute_038.outputs[0], invert_color_001.inputs[1])
    links.new(reroute_039.outputs[0], principled_bsdf_001.inputs[5])
    links.new(invert_color_001.outputs[0], math_002.inputs[0])
    links.new(math_002.outputs[0], principled_bsdf_001.inputs[2])
    links.new(reroute_005.outputs[0], reroute_039.inputs[0])
    links.new(input_node.outputs[9], hue_saturation_value_001.inputs[4])
    links.new(hue_saturation_value_001.outputs[0], mix_006.inputs[6])
    links.new(input_node.outputs[7], map_range_022.inputs[0])
    links.new(map_range_022.outputs[0], group_029.inputs[1])
    links.new(input_node.outputs[13], map_range_004.inputs[0])
    links.new(input_node.outputs[8], map_range_023.inputs[0])
    links.new(input_node.outputs[8], map_range_024.inputs[0])
    links.new(map_range_001.outputs[0], all_edges_013.inputs[1])
    links.new(reroute_041.outputs[0], reroute_034.inputs[0])
    links.new(map_range_024.outputs[0], all_edges_013.inputs[0])
    links.new(map_range_001.outputs[0], all_edges_014.inputs[1])
    links.new(all_edges_014.outputs[0], reroute_035.inputs[0])
    links.new(map_range_023.outputs[0], all_edges_014.inputs[0])
    links.new(reroute_028.outputs[0], all_edges_015.inputs[1])
    links.new(all_edges_015.outputs[0], reroute_011.inputs[0])
    links.new(map_range_009.outputs[0], all_edges_015.inputs[0])
    links.new(reroute_026.outputs[0], cavity_013.inputs[1])
    links.new(cavity_013.outputs[0], reroute_010.inputs[0])
    links.new(map_range_010.outputs[0], cavity_013.inputs[0])
    links.new(cavity_017.outputs[0], mix_005.inputs[0])
    links.new(map_range_007.outputs[0], cavity_017.inputs[1])
    links.new(map_range_015.outputs[0], cavity_017.inputs[0])
    links.new(reroute_024.outputs[0], hue_saturation_value_002.inputs[4])
    links.new(reroute_036.outputs[0], mix_011.inputs[6])
    links.new(hue_saturation_value_003.outputs[0], mix_012.inputs[7])
    links.new(reroute_024.outputs[0], hue_saturation_value_003.inputs[4])
    links.new(hue_saturation_value_002.outputs[0], reroute_036.inputs[0])
    links.new(reroute_043.outputs[0], math_001.inputs[1])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[1])
    links.new(reroute_030.outputs[0], bump_001.inputs[0])
    links.new(reroute_040.outputs[0], reroute_030.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_040.inputs[0])
    links.new(all_edges_013.outputs[0], reroute_041.inputs[0])
    links.new(reroute_042.outputs[0], math_001.inputs[0])
    links.new(reroute_041.outputs[0], reroute_042.inputs[0])
    links.new(reroute_029.outputs[0], reroute_016.inputs[0])
    links.new(input_node.outputs[19], map_range_011.inputs[0])
    links.new(perlin_noise.outputs[0], reroute_043.inputs[0])

    return group