import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .cavity import cavity
from .hs_bump_control import hs_bump_control
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_22d_r import pf_grunge_22d_r
from .perlin_noise_main_002 import perlin_noise_main002
from .perlin_noise_001_node_tree_002 import perlin_noise001_node_tree002
from .perlin_noise_002_node_tree_002 import perlin_noise002_node_tree002
from .perlin_noise_003_node_tree_002 import perlin_noise003_node_tree002


def hs_paint_04a():
    """BL_油漆04 - 清漆层油漆材质
    基于Principled BSDF，含凹凸开关/粗糙度/边缘磨损/底色混合"""
    group_name = "BL_油漆04"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_纹理", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_随机", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_凹腔扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_偏移", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "油漆图案: 油漆纹理图案层")
    frame_001 = create_frame(nodes, "Frame.001", "凹腔脏污: 凹腔区域(缝隙/角落)的脏污遮罩")
    frame_002 = create_frame(nodes, "Frame.002", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "粗糙度: 表面粗糙度控制")
    frame_004 = create_frame(nodes, "Frame.004", "凹凸: 凹凸贴图效果")

    # === 节点创建 ===
    all_edges_013 = nodes.new("ShaderNodeGroup")
    all_edges_013.location = (1113.8, -347.6)
    label_node(all_edges_013, "", frame_002)
    all_edges_013.xl_c4d_gradient_type = '0'
    all_edges_013.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_013.node_tree = all_edges()
    all_edges_013.inputs[2].default_value = 1.0
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (443.5, -409.1)
    label_node(group_029, "", frame_002)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_22d_r()
    group_029.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 3:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.48036321997642517
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.5438059568405151
    color_ramp_001.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0)
    color_ramp_001.color_ramp.elements[2].position = 0.9909365773200989
    color_ramp_001.color_ramp.elements[2].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (663.4, -409.1)
    label_node(color_ramp_001, "", frame_002)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (-708.3, -54.4)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[3].default_value = 1.5
    principled_bsdf_002.inputs[4].default_value = 1.0
    principled_bsdf_002.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_002.inputs[11].default_value = 1.399999976158142
    principled_bsdf_002.inputs[13].default_value = 0.45000001788139343
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
    colorramp_029 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_029 | ColorRamp.029
    colorramp_029.color_ramp.color_mode = 'RGB'
    colorramp_029.color_ramp.hue_interpolation = 'NEAR'
    colorramp_029.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_029.color_ramp.elements) > 2:
        colorramp_029.color_ramp.elements.remove(colorramp_029.color_ramp.elements[-1])
    while len(colorramp_029.color_ramp.elements) < 2:
        colorramp_029.color_ramp.elements.new(0.5)
    colorramp_029.color_ramp.elements[0].position = 0.012084580957889557
    colorramp_029.color_ramp.elements[0].color = (0.018040833994746208, 0.018040833994746208, 0.018040833994746208, 1.0)
    colorramp_029.color_ramp.elements[1].position = 0.5074294805526733
    colorramp_029.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_029
    colorramp_029.location = (832.4, -127.2)
    label_node(colorramp_029, "", frame_003)
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (540.9, -148.3)
    label_node(group_034, "", frame_003)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_15_r()
    bump_002 = nodes.new("ShaderNodeBump")
    bump_002.location = (1371.9, -229.9)
    label_node(bump_002, "", frame_004)
    bump_002.invert = False
    bump_002.inputs[1].default_value = 1.0
    bump_002.inputs[2].default_value = 0.10000000149011612
    bevel_002 = nodes.new("ShaderNodeBevel")
    bevel_002.location = (929.6, -489.2)
    label_node(bevel_002, "", frame_004)
    bevel_002.samples = 32
    bevel_002.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.location = (931.9, -255.8)
    label_node(noise_texture_002, "", frame)
    noise_texture_002.noise_dimensions = '3D'
    noise_texture_002.noise_type = 'FBM'
    noise_texture_002.normalize = True
    noise_texture_002.inputs[3].default_value = 3.3899993896484375
    noise_texture_002.inputs[4].default_value = 0.5574125051498413
    noise_texture_002.inputs[5].default_value = 2.0
    noise_texture_002.inputs[7].default_value = 1.0
    mapping_002 = nodes.new("ShaderNodeMapping")
    mapping_002.location = (462.2, -255.8)
    label_node(mapping_002, "", frame)
    mapping_002.vector_type = 'TEXTURE'
    mapping_002.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_002.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_002 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_002.location = (33.5, -255.8)
    label_node(texture_coordinate_002, "", frame)
    texture_coordinate_002.from_instancer = False
    vector_transform_002 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_002.location = (223.5, -255.8)
    label_node(vector_transform_002, "", frame)
    vector_transform_002.vector_type = 'VECTOR'
    vector_transform_002.convert_from = 'WORLD'
    vector_transform_002.convert_to = 'WORLD'
    color_ramp_007 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_007 | Color Ramp.007
    color_ramp_007.color_ramp.color_mode = 'RGB'
    color_ramp_007.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_007.color_ramp.interpolation = 'EASE'
    while len(color_ramp_007.color_ramp.elements) > 2:
        color_ramp_007.color_ramp.elements.remove(color_ramp_007.color_ramp.elements[-1])
    while len(color_ramp_007.color_ramp.elements) < 2:
        color_ramp_007.color_ramp.elements.new(0.5)
    color_ramp_007.color_ramp.elements[0].position = 0.4965943992137909
    color_ramp_007.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_007.color_ramp.elements[1].position = 0.587860643863678
    color_ramp_007.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_007
    color_ramp_007.location = (1664.4, -107.3)
    label_node(color_ramp_007, "", frame)
    mix_007 = nodes.new("ShaderNodeMix")
    mix_007.location = (2166.2, -102.3)
    label_node(mix_007, "", frame)
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
    mix_010 = nodes.new("ShaderNodeMix")
    mix_010.location = (2290.7, -525.0)
    label_node(mix_010, "", frame_001)
    mix_010.data_type = 'RGBA'
    mix_010.factor_mode = 'UNIFORM'
    mix_010.blend_type = 'MIX'
    mix_010.clamp_factor = True
    mix_010.clamp_result = False
    mix_010.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_010.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_010.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_010.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_039 = nodes.new("ShaderNodeGroup")
    group_039.location = (1346.8, -166.4)
    label_node(group_039, "", frame_001)
    group_039.xl_c4d_gradient_type = '0'
    group_039.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_039.node_tree = pf_grunge_22d_r()
    group_039.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_010 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_010 | Color Ramp.010
    color_ramp_010.color_ramp.color_mode = 'RGB'
    color_ramp_010.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_010.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_010.color_ramp.elements) > 2:
        color_ramp_010.color_ramp.elements.remove(color_ramp_010.color_ramp.elements[-1])
    while len(color_ramp_010.color_ramp.elements) < 2:
        color_ramp_010.color_ramp.elements.new(0.5)
    color_ramp_010.color_ramp.elements[0].position = 0.43181800842285156
    color_ramp_010.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_010.color_ramp.elements[1].position = 0.6772727966308594
    color_ramp_010.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_010
    color_ramp_010.location = (1642.7, -143.5)
    label_node(color_ramp_010, "", frame_001)
    mix_011 = nodes.new("ShaderNodeMix")
    mix_011.location = (1664.4, -625.0)
    label_node(mix_011, "", frame)
    mix_011.data_type = 'RGBA'
    mix_011.factor_mode = 'UNIFORM'
    mix_011.blend_type = 'MIX'
    mix_011.clamp_factor = True
    mix_011.clamp_result = False
    mix_011.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_011.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_011.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_011.inputs[6].default_value = (0.0233, 0.0301, 0.0350, 1.0000)
    mix_011.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    mapping_004 = nodes.new("ShaderNodeMapping")
    mapping_004.location = (462.2, -857.2)
    label_node(mapping_004, "", frame)
    mapping_004.vector_type = 'TEXTURE'
    mapping_004.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_004.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_004 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_004.location = (33.5, -857.2)
    label_node(texture_coordinate_004, "", frame)
    texture_coordinate_004.from_instancer = False
    vector_transform_004 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_004.location = (223.5, -857.2)
    label_node(vector_transform_004, "", frame)
    vector_transform_004.vector_type = 'VECTOR'
    vector_transform_004.convert_from = 'WORLD'
    vector_transform_004.convert_to = 'WORLD'
    color_ramp_011 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_011 | Color Ramp.011
    color_ramp_011.color_ramp.color_mode = 'RGB'
    color_ramp_011.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_011.color_ramp.interpolation = 'EASE'
    while len(color_ramp_011.color_ramp.elements) > 2:
        color_ramp_011.color_ramp.elements.remove(color_ramp_011.color_ramp.elements[-1])
    while len(color_ramp_011.color_ramp.elements) < 2:
        color_ramp_011.color_ramp.elements.new(0.5)
    color_ramp_011.color_ramp.elements[0].position = 0.4184562861919403
    color_ramp_011.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_011.color_ramp.elements[1].position = 0.44578447937965393
    color_ramp_011.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_011
    color_ramp_011.location = (1121.9, -745.5)
    label_node(color_ramp_011, "", frame)
    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.location = (931.9, -745.5)
    label_node(noise_texture, "", frame)
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    noise_texture.inputs[3].default_value = 8.309999465942383
    noise_texture.inputs[4].default_value = 0.6956908106803894
    noise_texture.inputs[5].default_value = 1.809999942779541
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.22999998927116394
    mix_012 = nodes.new("ShaderNodeMix")
    mix_012.location = (1409.7, -788.1)
    label_node(mix_012, "", frame)
    mix_012.data_type = 'RGBA'
    mix_012.factor_mode = 'UNIFORM'
    mix_012.blend_type = 'MIX'
    mix_012.clamp_factor = True
    mix_012.clamp_result = False
    mix_012.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_012.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_012.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_012.inputs[6].default_value = (0.3203, 0.2249, 0.0699, 1.0000)
    mix_012.inputs[7].default_value = (0.0110, 0.0127, 0.0129, 1.0000)
    mix_012.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_012.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    colorramp_030 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN colorramp_030 | ColorRamp.030
    colorramp_030.color_ramp.color_mode = 'RGB'
    colorramp_030.color_ramp.hue_interpolation = 'NEAR'
    colorramp_030.color_ramp.interpolation = 'LINEAR'
    while len(colorramp_030.color_ramp.elements) > 2:
        colorramp_030.color_ramp.elements.remove(colorramp_030.color_ramp.elements[-1])
    while len(colorramp_030.color_ramp.elements) < 2:
        colorramp_030.color_ramp.elements.new(0.5)
    colorramp_030.color_ramp.elements[0].position = 0.1727272868156433
    colorramp_030.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_030.color_ramp.elements[1].position = 0.4590909779071808
    colorramp_030.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END colorramp_030
    colorramp_030.location = (832.1, -221.0)
    label_node(colorramp_030, "", frame_004)
    color_ramp_012 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_012 | Color Ramp.012
    color_ramp_012.color_ramp.color_mode = 'RGB'
    color_ramp_012.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_012.color_ramp.interpolation = 'EASE'
    while len(color_ramp_012.color_ramp.elements) > 2:
        color_ramp_012.color_ramp.elements.remove(color_ramp_012.color_ramp.elements[-1])
    while len(color_ramp_012.color_ramp.elements) < 2:
        color_ramp_012.color_ramp.elements.new(0.5)
    color_ramp_012.color_ramp.elements[0].position = 0.4212852418422699
    color_ramp_012.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_012.color_ramp.elements[1].position = 0.5316535830497742
    color_ramp_012.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_012
    color_ramp_012.location = (1121.9, -330.2)
    label_node(color_ramp_012, "", frame)
    mix_013 = nodes.new("ShaderNodeMix")
    mix_013.location = (1664.4, -334.0)
    label_node(mix_013, "", frame)
    mix_013.data_type = 'RGBA'
    mix_013.factor_mode = 'UNIFORM'
    mix_013.blend_type = 'MIX'
    mix_013.clamp_factor = True
    mix_013.clamp_result = False
    mix_013.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_013.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_013.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_013.inputs[6].default_value = (0.2219, 0.0977, 0.0553, 1.0000)
    mix_013.inputs[7].default_value = (0.0303, 0.0452, 0.0441, 1.0000)
    mix_013.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_013.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_003 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_003.location = (545.3, -163.9)
    principled_bsdf_003.distribution = 'MULTI_GGX'
    principled_bsdf_003.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_003.inputs[3].default_value = 1.5
    principled_bsdf_003.inputs[4].default_value = 1.0
    principled_bsdf_003.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_003.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_003.inputs[11].default_value = 1.399999976158142
    principled_bsdf_003.inputs[13].default_value = 0.5
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
    mix_shader_002 = nodes.new("ShaderNodeMixShader")
    mix_shader_002.location = (1240.9, -1.7)
    bump_003 = nodes.new("ShaderNodeBump")
    bump_003.location = (255.7, -471.6)
    bump_003.invert = True
    bump_003.inputs[1].default_value = 1.0
    bump_003.inputs[2].default_value = 4.0
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (540.0, -247.0)
    label_node(group_035, "", frame_004)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = pf_grunge_15_r()
    all_edges_017 = nodes.new("ShaderNodeGroup")
    all_edges_017.location = (1113.8, -506.4)
    label_node(all_edges_017, "", frame_002)
    all_edges_017.xl_c4d_gradient_type = '0'
    all_edges_017.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_017.node_tree = all_edges()
    all_edges_017.inputs[2].default_value = 1.0
    color_ramp_013 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_013 | Color Ramp.013
    color_ramp_013.color_ramp.color_mode = 'RGB'
    color_ramp_013.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_013.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_013.color_ramp.elements) > 2:
        color_ramp_013.color_ramp.elements.remove(color_ramp_013.color_ramp.elements[-1])
    while len(color_ramp_013.color_ramp.elements) < 6:
        color_ramp_013.color_ramp.elements.new(0.5)
    color_ramp_013.color_ramp.elements[0].position = 0.004854368977248669
    color_ramp_013.color_ramp.elements[0].color = (0.04373428598046303, 0.048171669244766235, 0.05286135897040367, 0.9999999403953552)
    color_ramp_013.color_ramp.elements[1].position = 0.10194161534309387
    color_ramp_013.color_ramp.elements[1].color = (0.04373428598046303, 0.048171669244766235, 0.05286135897040367, 1.0)
    color_ramp_013.color_ramp.elements[2].position = 0.4563106894493103
    color_ramp_013.color_ramp.elements[2].color = (0.08710958063602448, 0.04285421222448349, 0.024744141846895218, 1.0)
    color_ramp_013.color_ramp.elements[3].position = 0.5315538048744202
    color_ramp_013.color_ramp.elements[3].color = (0.039791591465473175, 0.04230130836367607, 0.06736983358860016, 1.0)
    color_ramp_013.color_ramp.elements[4].position = 0.7742719650268555
    color_ramp_013.color_ramp.elements[4].color = (0.07951472699642181, 0.013072257861495018, 0.0650915876030922, 1.0)
    color_ramp_013.color_ramp.elements[5].position = 0.8689320087432861
    color_ramp_013.color_ramp.elements[5].color = (0.03794214129447937, 0.02796923741698265, 0.023228462785482407, 1.0)
    # XL_PF_RAMP_END color_ramp_013
    color_ramp_013.location = (2027.2, -445.4)
    label_node(color_ramp_013, "", frame_002)
    cavity_012 = nodes.new("ShaderNodeGroup")
    cavity_012.location = (1207.2, -483.8)
    label_node(cavity_012, "", frame_001)
    cavity_012.xl_c4d_gradient_type = '0'
    cavity_012.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_012.node_tree = cavity()
    cavity_012.inputs[2].default_value = 1.779999852180481
    group_041 = nodes.new("ShaderNodeGroup")
    group_041.location = (607.8, -386.0)
    label_node(group_041, "", frame_001)
    group_041.xl_c4d_gradient_type = '0'
    group_041.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_041.node_tree = pf_grunge_22d_r()
    group_041.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    mix_015 = nodes.new("ShaderNodeMix")
    mix_015.location = (1862.4, -524.2)
    label_node(mix_015, "", frame_001)
    mix_015.data_type = 'RGBA'
    mix_015.factor_mode = 'UNIFORM'
    mix_015.blend_type = 'MIX'
    mix_015.clamp_factor = True
    mix_015.clamp_result = False
    mix_015.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_015.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_015.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_015.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_015.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_018 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_018 | Color Ramp.018
    color_ramp_018.color_ramp.color_mode = 'RGB'
    color_ramp_018.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_018.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_018.color_ramp.elements) > 2:
        color_ramp_018.color_ramp.elements.remove(color_ramp_018.color_ramp.elements[-1])
    while len(color_ramp_018.color_ramp.elements) < 4:
        color_ramp_018.color_ramp.elements.new(0.5)
    color_ramp_018.color_ramp.elements[0].position = 0.24244724214076996
    color_ramp_018.color_ramp.elements[0].color = (0.02351474016904831, 0.034531015902757645, 0.0744682177901268, 1.0)
    color_ramp_018.color_ramp.elements[1].position = 0.4335349500179291
    color_ramp_018.color_ramp.elements[1].color = (0.02537793666124344, 0.027505073696374893, 0.03680817782878876, 1.0)
    color_ramp_018.color_ramp.elements[2].position = 0.47734150290489197
    color_ramp_018.color_ramp.elements[2].color = (0.2871597707271576, 0.2834875285625458, 0.20178751647472382, 1.0)
    color_ramp_018.color_ramp.elements[3].position = 0.5135953426361084
    color_ramp_018.color_ramp.elements[3].color = (0.022052355110645294, 0.011479256674647331, 0.010309570468962193, 1.0)
    # XL_PF_RAMP_END color_ramp_018
    color_ramp_018.location = (1570.5, -731.0)
    label_node(color_ramp_018, "", frame_001)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (848.5, -386.0)
    label_node(map_range_003, "", frame_001)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[1].default_value = -0.04999999701976776
    map_range_003.inputs[2].default_value = 1.0
    map_range_003.inputs[3].default_value = -0.5199999809265137
    map_range_003.inputs[4].default_value = 0.809999942779541
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    noise_texture_004 = nodes.new("ShaderNodeTexNoise")
    noise_texture_004.location = (600.1, -668.2)
    label_node(noise_texture_004, "", frame_001)
    noise_texture_004.noise_dimensions = '3D'
    noise_texture_004.noise_type = 'FBM'
    noise_texture_004.normalize = True
    noise_texture_004.inputs[2].default_value = 3.0799999237060547
    noise_texture_004.inputs[3].default_value = 1.8199999332427979
    noise_texture_004.inputs[4].default_value = 1.0
    noise_texture_004.inputs[5].default_value = 2.9000000953674316
    noise_texture_004.inputs[7].default_value = 1.0
    mapping_005 = nodes.new("ShaderNodeMapping")
    mapping_005.location = (410.1, -668.2)
    label_node(mapping_005, "", frame_001)
    mapping_005.vector_type = 'TEXTURE'
    mapping_005.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping_005.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    mapping_005.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    texture_coordinate_005 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_005.location = (30.1, -668.2)
    label_node(texture_coordinate_005, "", frame_001)
    texture_coordinate_005.from_instancer = False
    vector_transform_005 = nodes.new("ShaderNodeVectorTransform")
    vector_transform_005.location = (220.1, -668.2)
    label_node(vector_transform_005, "", frame_001)
    vector_transform_005.vector_type = 'VECTOR'
    vector_transform_005.convert_from = 'WORLD'
    vector_transform_005.convert_to = 'WORLD'
    mix_016 = nodes.new("ShaderNodeMix")
    mix_016.location = (1158.5, -668.2)
    label_node(mix_016, "", frame_001)
    mix_016.data_type = 'RGBA'
    mix_016.factor_mode = 'UNIFORM'
    mix_016.blend_type = 'MIX'
    mix_016.clamp_factor = True
    mix_016.clamp_result = False
    mix_016.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_016.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_016.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_016.inputs[6].default_value = (0.0000, 0.0000, 0.0000, 1.0000)
    mix_016.inputs[7].default_value = (0.0058, 0.0057, 0.0064, 1.0000)
    mix_016.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_016.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_017 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_017 | Color Ramp.017
    color_ramp_017.color_ramp.color_mode = 'RGB'
    color_ramp_017.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_017.color_ramp.interpolation = 'EASE'
    while len(color_ramp_017.color_ramp.elements) > 2:
        color_ramp_017.color_ramp.elements.remove(color_ramp_017.color_ramp.elements[-1])
    while len(color_ramp_017.color_ramp.elements) < 2:
        color_ramp_017.color_ramp.elements.new(0.5)
    color_ramp_017.color_ramp.elements[0].position = 0.5484477281570435
    color_ramp_017.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_017.color_ramp.elements[1].position = 0.5863639712333679
    color_ramp_017.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_017
    color_ramp_017.location = (802.6, -668.2)
    label_node(color_ramp_017, "", frame_001)
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (291.0, 580.2)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (914.7, -101.0)
    reroute_002.socket_idname = 'NodeSocketShader'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (676.4, -59.4)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (-2120.4, 55.9)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (-942.2, 56.2)
    reroute_005.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (2040.0, -277.9)
    label_node(reroute_006, "", frame)
    reroute_006.socket_idname = 'NodeSocketColor'
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (680.2, -390.4)
    label_node(map_range, "", frame)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 100.0
    map_range.inputs[3].default_value = 1.0
    map_range.inputs[4].default_value = 1.8100001811981201
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (679.4, -636.6)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 3.169999837875366
    map_range_001.inputs[4].default_value = 0.43000003695487976
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (1885.3, -658.0)
    label_node(reroute_007, "", frame)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (2040.0, -298.2)
    label_node(reroute_008, "", frame)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (2040.0, -256.7)
    label_node(reroute_009, "", frame)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (899.4, -403.6)
    label_node(reroute_010, "", frame)
    reroute_010.socket_idname = 'NodeSocketVector'
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (410.1, -387.5)
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
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (1159.4, -104.7)
    label_node(map_range_004, "", frame_001)
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
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (265.1, -518.0)
    label_node(reroute_011, "", frame_001)
    reroute_011.socket_idname = 'NodeSocketFloatPercentage'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (1081.0, -107.0)
    label_node(reroute_012, "", frame_001)
    reroute_012.socket_idname = 'NodeSocketFloatPercentage'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (413.2, -107.0)
    label_node(reroute_013, "", frame_001)
    reroute_013.socket_idname = 'NodeSocketFloatPercentage'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1508.5, -680.2)
    label_node(reroute_015, "", frame_001)
    reroute_015.socket_idname = 'NodeSocketFloat'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (1508.5, -914.4)
    label_node(reroute_014, "", frame_001)
    reroute_014.socket_idname = 'NodeSocketFloat'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (2037.8, -680.3)
    label_node(reroute_016, "", frame_001)
    reroute_016.socket_idname = 'NodeSocketColor'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (2037.8, -722.5)
    label_node(reroute_017, "", frame_001)
    reroute_017.socket_idname = 'NodeSocketColor'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (2151.7, -701.2)
    label_node(reroute_018, "", frame_001)
    reroute_018.socket_idname = 'NodeSocketColor'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (-3155.7, -184.7)
    reroute_019.socket_idname = 'NodeSocketColor'
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (848.6, -142.7)
    label_node(map_range_005, "", frame_001)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.07000000029802322
    map_range_005.inputs[4].default_value = 24.670000076293945
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (1103.3, -583.7)
    label_node(reroute_020, "", frame_001)
    reroute_020.socket_idname = 'NodeSocketFloat'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (1105.7, -563.3)
    label_node(reroute_021, "", frame_001)
    reroute_021.socket_idname = 'NodeSocketFloat'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (202.5, 481.5)
    reroute_022.socket_idname = 'NodeSocketColor'
    math = nodes.new("ShaderNodeMath")
    math.location = (1755.3, -486.6)
    label_node(math, "", frame_002)
    math.operation = 'ADD'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (1477.4, -394.6)
    label_node(math_001, "", frame_002)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 0.5
    math_001.inputs[2].default_value = 0.5
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (1425.5, -612.2)
    label_node(reroute_023, "", frame_002)
    reroute_023.socket_idname = 'NodeSocketFloat'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (1624.2, -612.6)
    label_node(reroute_024, "", frame_002)
    reroute_024.socket_idname = 'NodeSocketFloat'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (-306.1, -249.0)
    reroute_026.socket_idname = 'NodeSocketFloat'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (-25.0, -614.2)
    reroute_028.socket_idname = 'NodeSocketFloat'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (2038.2, -379.8)
    label_node(reroute_029, "", frame_002)
    reroute_029.socket_idname = 'NodeSocketFloat'
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (-209.9, -435.1)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = True
    math_002.inputs[2].default_value = 0.5
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (-377.3, -673.5)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 1.0
    map_range_006.inputs[3].default_value = 0.3700000047683716
    map_range_006.inputs[4].default_value = 1.0
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (287.4, -410.4)
    label_node(map_range_007, "", frame_002)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 7.450580596923828e-09
    map_range_007.inputs[4].default_value = 0.2799999713897705
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (501.4, -102.2)
    label_node(map_range_008, "", frame_002)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = -0.019999999552965164
    map_range_008.inputs[4].default_value = 0.1300000101327896
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_003 = nodes.new("ShaderNodeMath")
    math_003.location = (831.4, -101.6)
    label_node(math_003, "", frame_002)
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    math_003.inputs[1].default_value = 3.620000123977661
    math_003.inputs[2].default_value = 0.5
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (804.1, -205.3)
    label_node(reroute_030, "", frame_002)
    reroute_030.socket_idname = 'NodeSocketFloat'
    reroute = nodes.new("NodeReroute")
    reroute.location = (889.0, -374.8)
    label_node(reroute, "", frame_002)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (811.2, -374.8)
    label_node(reroute_025, "", frame_002)
    reroute_025.socket_idname = 'NodeSocketFloat'
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (324.2, -102.1)
    label_node(map_range_010, "", frame_003)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[3].default_value = 0.05000000074505806
    map_range_010.inputs[4].default_value = 0.5
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (-724.2, -635.2)
    reroute_027.socket_idname = 'NodeSocketVector'
    map_range_011 = nodes.new("ShaderNodeMapRange")
    map_range_011.location = (363.4, -197.3)
    label_node(map_range_011, "", frame_004)
    map_range_011.clamp = True
    map_range_011.interpolation_type = 'LINEAR'
    map_range_011.data_type = 'FLOAT'
    map_range_011.inputs[2].default_value = 100.0
    map_range_011.inputs[3].default_value = 0.10000000149011612
    map_range_011.inputs[4].default_value = 0.75
    map_range_011.inputs[5].default_value = 4.0
    map_range_011.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_011.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_011.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_004 = nodes.new("ShaderNodeMath")
    math_004.location = (1112.2, -302.8)
    label_node(math_004, "", frame_004)
    math_004.operation = 'MULTIPLY'
    math_004.use_clamp = False
    math_004.inputs[2].default_value = 0.5
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (1241.1, -522.6)
    label_node(reroute_031, "", frame_004)
    reroute_031.socket_idname = 'NodeSocketVector'
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (359.8, -116.9)
    label_node(reroute_033, "", frame_004)
    reroute_033.socket_idname = 'NodeSocketFloatPercentage'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (-1088.6, -999.0)
    reroute_034.socket_idname = 'NodeSocketVector'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (-907.5, -211.1)
    reroute_032.socket_idname = 'NodeSocketVector'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (741.5, -490.3)
    label_node(percentage_to_0_1, "百分比转0-1", frame_004)
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
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (-769.3, -523.8)
    reroute_035.socket_idname = 'NodeSocketColor'
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (-451.7, -523.8)
    reroute_036.socket_idname = 'NodeSocketColor'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (-306.1, -274.8)
    reroute_037.socket_idname = 'NodeSocketColor'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (-1133.8, -148.7)
    reroute_038.socket_idname = 'NodeSocketColor'
    hs_bump_control_001 = nodes.new("ShaderNodeGroup")
    hs_bump_control_001.location = (1109.3, -118.7)
    label_node(hs_bump_control_001, "", frame_004)
    hs_bump_control_001.xl_c4d_gradient_type = '0'
    hs_bump_control_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control_001.node_tree = hs_bump_control()
    hs_bump_control_001.inputs[2].default_value = 0.4000000059604645
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (-1447.6, -589.9)
    reroute_039.socket_idname = 'NodeSocketFloat'
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (210.3, -589.9)
    reroute_040.socket_idname = 'NodeSocketFloat'
    perlin_noise = nodes.new("ShaderNodeGroup")
    perlin_noise.location = (-558.8, -677.2)
    perlin_noise.xl_c4d_gradient_type = '0'
    perlin_noise.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise.node_tree = perlin_noise_main002()
    perlin_noise.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise.inputs[2].default_value = 10.0
    perlin_noise.inputs[3].default_value = 10.0
    perlin_noise.inputs[5].default_value = 2.0
    perlin_noise.inputs[7].default_value = 60.0
    perlin_noise.inputs[9].default_value = 1.0
    perlin_noise_001 = nodes.new("ShaderNodeGroup")
    perlin_noise_001.location = (0.0, 0.0)
    perlin_noise_001.xl_c4d_gradient_type = '0'
    perlin_noise_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    perlin_noise_001.node_tree = perlin_noise001_node_tree002()
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
    perlin_noise_002.node_tree = perlin_noise002_node_tree002()
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
    perlin_noise_003.node_tree = perlin_noise003_node_tree002()
    perlin_noise_003.inputs[0].default_value = (0.0000, 0.0000, 0.0000)
    perlin_noise_003.inputs[2].default_value = 8.0
    perlin_noise_003.inputs[3].default_value = 10.0
    perlin_noise_003.inputs[5].default_value = 2.0
    perlin_noise_003.inputs[7].default_value = 60.0
    perlin_noise_003.inputs[9].default_value = 1.0

    # === 节点连接 ===
    links.new(group_029.outputs[0], color_ramp_001.inputs[0])
    links.new(texture_coordinate_002.outputs[3], vector_transform_002.inputs[0])
    links.new(map_range_010.outputs[0], group_034.inputs[0])
    links.new(reroute_009.outputs[0], mix_007.inputs[0])
    links.new(reroute_032.outputs[0], principled_bsdf_002.inputs[5])
    links.new(reroute_010.outputs[0], noise_texture_002.inputs[0])
    links.new(vector_transform_002.outputs[0], mapping_002.inputs[0])
    links.new(reroute_031.outputs[0], bump_002.inputs[4])
    links.new(reroute_038.outputs[0], principled_bsdf_002.inputs[2])
    links.new(group_034.outputs[0], colorramp_029.inputs[0])
    links.new(noise_texture_002.outputs[0], color_ramp_007.inputs[0])
    links.new(reroute_005.outputs[0], principled_bsdf_002.inputs[0])
    links.new(group_039.outputs[0], color_ramp_010.inputs[0])
    links.new(reroute_016.outputs[0], mix_010.inputs[0])
    links.new(texture_coordinate_004.outputs[3], vector_transform_004.inputs[0])
    links.new(vector_transform_004.outputs[0], mapping_004.inputs[0])
    links.new(color_ramp_011.outputs[0], mix_011.inputs[0])
    links.new(mapping_004.outputs[0], noise_texture.inputs[0])
    links.new(noise_texture.outputs[0], color_ramp_011.inputs[0])
    links.new(color_ramp_011.outputs[0], mix_012.inputs[0])
    links.new(mix_012.outputs[2], mix_011.inputs[7])
    links.new(math_004.outputs[0], bump_002.inputs[3])
    links.new(noise_texture_002.outputs[0], color_ramp_012.inputs[0])
    links.new(color_ramp_012.outputs[0], mix_013.inputs[0])
    links.new(reroute_008.outputs[0], mix_007.inputs[7])
    links.new(reroute_002.outputs[0], mix_shader_002.inputs[2])
    links.new(principled_bsdf_002.outputs[0], mix_shader_002.inputs[1])
    links.new(reroute_003.outputs[0], mix_shader_002.inputs[0])
    links.new(reroute_027.outputs[0], bump_003.inputs[4])
    links.new(group_035.outputs[0], colorramp_030.inputs[0])
    links.new(reroute_022.outputs[0], principled_bsdf_003.inputs[0])
    links.new(math.outputs[0], color_ramp_013.inputs[0])
    links.new(reroute_017.outputs[0], mix_010.inputs[7])
    links.new(reroute_018.outputs[0], mix_010.inputs[6])
    links.new(color_ramp_018.outputs[0], mix_015.inputs[7])
    links.new(group_041.outputs[0], map_range_003.inputs[0])
    links.new(texture_coordinate_005.outputs[3], vector_transform_005.inputs[0])
    links.new(mapping_005.outputs[0], noise_texture_004.inputs[0])
    links.new(vector_transform_005.outputs[0], mapping_005.inputs[0])
    links.new(color_ramp_017.outputs[0], mix_016.inputs[0])
    links.new(mix_016.outputs[2], mix_015.inputs[6])
    links.new(noise_texture_004.outputs[0], color_ramp_017.inputs[0])
    links.new(mix_shader_002.outputs[0], output_node.inputs[0])
    links.new(reroute_029.outputs[0], reroute_001.inputs[0])
    links.new(reroute_015.outputs[0], mix_015.inputs[0])
    links.new(reroute_014.outputs[0], color_ramp_018.inputs[0])
    links.new(principled_bsdf_003.outputs[0], reroute_002.inputs[0])
    links.new(reroute_001.outputs[0], reroute_003.inputs[0])
    links.new(mix_010.outputs[2], reroute_004.inputs[0])
    links.new(reroute_004.outputs[0], reroute_005.inputs[0])
    links.new(reroute_007.outputs[0], reroute_006.inputs[0])
    links.new(reroute_006.outputs[0], mix_007.inputs[6])
    links.new(map_range.outputs[0], noise_texture_002.inputs[2])
    links.new(map_range_001.outputs[0], noise_texture.inputs[2])
    links.new(input_node.outputs[6], map_range.inputs[0])
    links.new(input_node.outputs[6], map_range_001.inputs[0])
    links.new(input_node.outputs[9], mapping_002.inputs[1])
    links.new(input_node.outputs[9], mapping_004.inputs[1])
    links.new(mix_011.outputs[2], reroute_007.inputs[0])
    links.new(mix_013.outputs[2], reroute_008.inputs[0])
    links.new(color_ramp_007.outputs[0], reroute_009.inputs[0])
    links.new(mapping_002.outputs[0], reroute_010.inputs[0])
    links.new(reroute_011.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], group_041.inputs[1])
    links.new(map_range_004.outputs[0], group_039.inputs[1])
    links.new(input_node.outputs[7], reroute_011.inputs[0])
    links.new(reroute_012.outputs[0], map_range_004.inputs[0])
    links.new(reroute_013.outputs[0], reroute_012.inputs[0])
    links.new(reroute_011.outputs[0], reroute_013.inputs[0])
    links.new(reroute_015.outputs[0], reroute_014.inputs[0])
    links.new(color_ramp_010.outputs[0], reroute_016.inputs[0])
    links.new(reroute_019.outputs[0], reroute_017.inputs[0])
    links.new(mix_015.outputs[2], reroute_018.inputs[0])
    links.new(mix_007.outputs[2], reroute_019.inputs[0])
    links.new(map_range_003.outputs[0], reroute_020.inputs[0])
    links.new(map_range_005.outputs[0], reroute_021.inputs[0])
    links.new(input_node.outputs[8], map_range_005.inputs[0])
    links.new(color_ramp_013.outputs[0], reroute_022.inputs[0])
    links.new(reroute_024.outputs[0], math.inputs[1])
    links.new(math_001.outputs[0], math.inputs[0])
    links.new(reroute_023.outputs[0], reroute_024.inputs[0])
    links.new(reroute_026.outputs[0], principled_bsdf_003.inputs[1])
    links.new(reroute_024.outputs[0], reroute_026.inputs[0])
    links.new(reroute_028.outputs[0], bump_003.inputs[3])
    links.new(math_002.outputs[0], reroute_028.inputs[0])
    links.new(math.outputs[0], reroute_029.inputs[0])
    links.new(reroute_026.outputs[0], math_002.inputs[0])
    links.new(map_range_006.outputs[0], math_002.inputs[1])
    links.new(bump_003.outputs[0], principled_bsdf_003.inputs[5])
    links.new(map_range_007.outputs[0], group_029.inputs[1])
    links.new(input_node.outputs[4], map_range_007.inputs[0])
    links.new(reroute_030.outputs[0], math_003.inputs[0])
    links.new(map_range_008.outputs[0], reroute_030.inputs[0])
    links.new(input_node.outputs[5], map_range_008.inputs[0])
    links.new(reroute_025.outputs[0], reroute.inputs[0])
    links.new(reroute_030.outputs[0], reroute_025.inputs[0])
    links.new(input_node.outputs[10], map_range_010.inputs[0])
    links.new(reroute_034.outputs[0], reroute_027.inputs[0])
    links.new(map_range_011.outputs[0], group_035.inputs[0])
    links.new(input_node.outputs[3], map_range_011.inputs[0])
    links.new(colorramp_030.outputs[0], math_004.inputs[0])
    links.new(input_node.outputs[1], math_004.inputs[1])
    links.new(bevel_002.outputs[0], reroute_031.inputs[0])
    links.new(input_node.outputs[3], reroute_033.inputs[0])
    links.new(reroute_031.outputs[0], reroute_034.inputs[0])
    links.new(bump_002.outputs[0], reroute_032.inputs[0])
    links.new(color_ramp_001.outputs[0], all_edges_013.inputs[1])
    links.new(all_edges_013.outputs[0], math_001.inputs[0])
    links.new(math_003.outputs[0], all_edges_013.inputs[0])
    links.new(color_ramp_001.outputs[0], all_edges_017.inputs[1])
    links.new(all_edges_017.outputs[0], reroute_023.inputs[0])
    links.new(reroute.outputs[0], all_edges_017.inputs[0])
    links.new(reroute_020.outputs[0], cavity_012.inputs[1])
    links.new(reroute_021.outputs[0], cavity_012.inputs[0])
    links.new(cavity_012.outputs[0], reroute_015.inputs[0])
    links.new(reroute_037.outputs[0], principled_bsdf_003.inputs[2])
    links.new(input_node.outputs[0], percentage_to_0_1.inputs[0])
    links.new(percentage_to_0_1.outputs[0], bevel_002.inputs[0])
    links.new(reroute_035.outputs[0], reroute_036.inputs[0])
    links.new(reroute_036.outputs[0], reroute_037.inputs[0])
    links.new(colorramp_029.outputs[0], reroute_038.inputs[0])
    links.new(reroute_038.outputs[0], reroute_035.inputs[0])
    links.new(input_node.outputs[1], hs_bump_control_001.inputs[0])
    links.new(input_node.outputs[2], hs_bump_control_001.inputs[1])
    links.new(hs_bump_control_001.outputs[0], bump_002.inputs[0])
    links.new(reroute_040.outputs[0], bump_003.inputs[0])
    links.new(hs_bump_control_001.outputs[0], reroute_039.inputs[0])
    links.new(reroute_039.outputs[0], reroute_040.inputs[0])
    links.new(perlin_noise.outputs[0], map_range_006.inputs[0])

    return group