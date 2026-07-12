import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .all_edges import all_edges
from .hs_bump_control import hs_bump_control
from .pf_grunge_15_r import pf_grunge_15_r
from .pf_grunge_20_r import pf_grunge_20_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_22c_r import pf_grunge_22c_r


def hs_metal_02a():
    """BL_金属02 - 工业磨损金属材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损/凹腔脏污"""
    group_name = "BL_金属02"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    group.interface.new_socket(name="边缘磨损_基础扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_基础随机", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_彩色颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0352, 0.0352, 0.0352, 1.0000)
    group.interface.new_socket(name="边缘磨损_彩色扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损_彩色随机", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆_细节随机", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")
    frame_001 = create_frame(nodes, "Frame.001", "粗糙度: 表面粗糙度控制")
    frame_002 = create_frame(nodes, "Frame.002", "凹凸+开关: 控制凹凸贴图是否启用及其强度")
    frame_003 = create_frame(nodes, "Frame.003", "油漆飞溅: 油漆飞溅/泼洒效果")
    frame_004 = create_frame(nodes, "Frame.004", "比例缩放: 按比例缩放纹理坐标")
    frame_005 = create_frame(nodes, "Frame.005", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (-1136.6, 236.0)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[1].default_value = 1.0
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
    group_039 = nodes.new("ShaderNodeGroup")
    group_039.location = (630.2, -62.5)
    label_node(group_039, "", frame_001)
    group_039.xl_c4d_gradient_type = '0'
    group_039.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_039.node_tree = pf_grunge_20_r()
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.1601208597421646
    color_ramp_001.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.4864049255847931
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (924.7, -35.8)
    label_node(color_ramp_001, "", frame_001)
    group_040 = nodes.new("ShaderNodeGroup")
    group_040.location = (630.2, -350.5)
    label_node(group_040, "", frame_001)
    group_040.xl_c4d_gradient_type = '0'
    group_040.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_040.node_tree = pf_grunge_22b_r()
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.23262856900691986
    color_ramp_002.color_ramp.elements[0].color = (0.001200072467327118, 0.001200072467327118, 0.001200072467327118, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.5585553050041199
    color_ramp_002.color_ramp.elements[1].color = (0.6197326183319092, 0.6197326183319092, 0.6197326183319092, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (924.7, -249.2)
    label_node(color_ramp_002, "", frame_001)
    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.location = (1411.6, -114.3)
    label_node(mix_002, "", frame_001)
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'MULTIPLY'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.inputs[0].default_value = 0.6077347993850708
    mix_002.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_002.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (-1135.1, 719.5)
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
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (-223.9, 258.1)
    group_041 = nodes.new("ShaderNodeGroup")
    group_041.location = (445.6, -354.7)
    label_node(group_041, "", frame_005)
    group_041.xl_c4d_gradient_type = '0'
    group_041.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_041.node_tree = pf_grunge_20_r()
    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.location = (1408.9, -113.6)
    label_node(mix_004, "", frame_004)
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_004.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[7].default_value = (0.0394, 0.0383, 0.0353, 1.0000)
    mix_004.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_043 = nodes.new("ShaderNodeGroup")
    group_043.location = (628.6, -250.2)
    label_node(group_043, "", frame_004)
    group_043.xl_c4d_gradient_type = '0'
    group_043.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_043.node_tree = pf_grunge_22b_r()
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
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.8459215760231018
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (923.1, -102.3)
    label_node(color_ramp_003, "", frame_004)
    color_ramp_007 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_007 | Color Ramp.007
    color_ramp_007.color_ramp.color_mode = 'RGB'
    color_ramp_007.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_007.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_007.color_ramp.elements) > 2:
        color_ramp_007.color_ramp.elements.remove(color_ramp_007.color_ramp.elements[-1])
    while len(color_ramp_007.color_ramp.elements) < 7:
        color_ramp_007.color_ramp.elements.new(0.5)
    color_ramp_007.color_ramp.elements[0].position = 0.021590877324342728
    color_ramp_007.color_ramp.elements[0].color = (0.05569557473063469, 0.06987615674734116, 0.09988588094711304, 1.0)
    color_ramp_007.color_ramp.elements[1].position = 0.0676136240363121
    color_ramp_007.color_ramp.elements[1].color = (0.1347331553697586, 0.1112581118941307, 0.01676870509982109, 1.0)
    color_ramp_007.color_ramp.elements[2].position = 0.11363636702299118
    color_ramp_007.color_ramp.elements[2].color = (0.12796925008296967, 0.13284410536289215, 0.1695721298456192, 1.0)
    color_ramp_007.color_ramp.elements[3].position = 0.2613636255264282
    color_ramp_007.color_ramp.elements[3].color = (0.039691172540187836, 0.02472284436225891, 0.02267036959528923, 1.0)
    color_ramp_007.color_ramp.elements[4].position = 0.37727245688438416
    color_ramp_007.color_ramp.elements[4].color = (0.057931408286094666, 0.05507471412420273, 0.04206816479563713, 1.0)
    color_ramp_007.color_ramp.elements[5].position = 0.45454561710357666
    color_ramp_007.color_ramp.elements[5].color = (0.09121139347553253, 0.09023121744394302, 0.0901566594839096, 1.0)
    color_ramp_007.color_ramp.elements[6].position = 0.5795453786849976
    color_ramp_007.color_ramp.elements[6].color = (0.10069325566291809, 0.0836835503578186, 0.06498248130083084, 1.0)
    # XL_PF_RAMP_END color_ramp_007
    color_ramp_007.location = (923.1, -312.1)
    label_node(color_ramp_007, "", frame_004)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1413.9, -36.1)
    label_node(bump, "", frame_002)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.009999999776482582
    group_044 = nodes.new("ShaderNodeGroup")
    group_044.location = (388.0, -186.9)
    label_node(group_044, "", frame_002)
    group_044.xl_c4d_gradient_type = '0'
    group_044.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_044.node_tree = pf_grunge_22b_r()
    color_ramp_008 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_008 | Color Ramp.008
    color_ramp_008.color_ramp.color_mode = 'RGB'
    color_ramp_008.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_008.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_008.color_ramp.elements) > 2:
        color_ramp_008.color_ramp.elements.remove(color_ramp_008.color_ramp.elements[-1])
    while len(color_ramp_008.color_ramp.elements) < 2:
        color_ramp_008.color_ramp.elements.new(0.5)
    color_ramp_008.color_ramp.elements[0].position = 0.47253498435020447
    color_ramp_008.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_008.color_ramp.elements[1].position = 0.782120406627655
    color_ramp_008.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_008
    color_ramp_008.location = (682.5, -38.5)
    label_node(color_ramp_008, "", frame_002)
    all_edges_014 = nodes.new("ShaderNodeGroup")
    all_edges_014.location = (886.8, -289.8)
    label_node(all_edges_014, "", frame_005)
    all_edges_014.xl_c4d_gradient_type = '0'
    all_edges_014.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_014.node_tree = all_edges()
    all_edges_014.inputs[2].default_value = 1.0
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (708.2, -355.2)
    label_node(map_range, "", frame_005)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = -0.14999999105930328
    map_range.inputs[4].default_value = 0.18000000715255737
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (964.0, -571.8)
    label_node(bevel, "", frame_002)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mix_shader_001 = nodes.new("ShaderNodeMixShader")
    mix_shader_001.location = (2586.6, 258.1)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (1250.1, -123.6)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[1].default_value = 0.36363640427589417
    principled_bsdf_002.inputs[3].default_value = 1.5
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
    group_045 = nodes.new("ShaderNodeGroup")
    group_045.location = (514.3, -199.2)
    label_node(group_045, "", frame_003)
    group_045.xl_c4d_gradient_type = '0'
    group_045.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_045.node_tree = pf_grunge_15_r()
    color_ramp_004 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_004 | Color Ramp.004
    color_ramp_004.color_ramp.color_mode = 'RGB'
    color_ramp_004.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_004.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_004.color_ramp.elements) > 2:
        color_ramp_004.color_ramp.elements.remove(color_ramp_004.color_ramp.elements[-1])
    while len(color_ramp_004.color_ramp.elements) < 2:
        color_ramp_004.color_ramp.elements.new(0.5)
    color_ramp_004.color_ramp.elements[0].position = 0.6957840323448181
    color_ramp_004.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_004.color_ramp.elements[1].position = 0.8519640564918518
    color_ramp_004.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_004
    color_ramp_004.location = (819.8, -101.9)
    label_node(color_ramp_004, "", frame_003)
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (1086.7, -263.8)
    bump_001.invert = False
    bump_001.inputs[1].default_value = 1.0
    bump_001.inputs[2].default_value = 0.10000000149011612
    color_ramp_005 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_005 | Color Ramp.005
    color_ramp_005.color_ramp.color_mode = 'RGB'
    color_ramp_005.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_005.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_005.color_ramp.elements) > 2:
        color_ramp_005.color_ramp.elements.remove(color_ramp_005.color_ramp.elements[-1])
    while len(color_ramp_005.color_ramp.elements) < 2:
        color_ramp_005.color_ramp.elements.new(0.5)
    color_ramp_005.color_ramp.elements[0].position = 0.5136362910270691
    color_ramp_005.color_ramp.elements[0].color = (0.048747673630714417, 0.04656212776899338, 0.05853872746229172, 1.0)
    color_ramp_005.color_ramp.elements[1].position = 0.6409091353416443
    color_ramp_005.color_ramp.elements[1].color = (0.1091780960559845, 0.1091780960559845, 0.1091780960559845, 1.0)
    # XL_PF_RAMP_END color_ramp_005
    color_ramp_005.location = (1228.3, -103.5)
    label_node(color_ramp_005, "", frame_003)
    mix_shader_002 = nodes.new("ShaderNodeMixShader")
    mix_shader_002.location = (3373.2, 297.3)
    group_042 = nodes.new("ShaderNodeGroup")
    group_042.location = (507.8, -389.0)
    label_node(group_042, "", frame)
    group_042.xl_c4d_gradient_type = '0'
    group_042.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_042.node_tree = pf_grunge_22c_r()
    all_edges_015 = nodes.new("ShaderNodeGroup")
    all_edges_015.location = (1023.2, -316.8)
    label_node(all_edges_015, "", frame)
    all_edges_015.xl_c4d_gradient_type = '0'
    all_edges_015.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_015.node_tree = all_edges()
    all_edges_015.inputs[2].default_value = 1.0
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (709.9, -343.9)
    label_node(map_range_001, "", frame)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[4].default_value = 0.47999995946884155
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    principled_bsdf_003 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_003.location = (2567.2, 130.2)
    principled_bsdf_003.distribution = 'MULTI_GGX'
    principled_bsdf_003.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_003.inputs[1].default_value = 1.0
    principled_bsdf_003.inputs[2].default_value = 0.27009063959121704
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
    bump_002 = nodes.new("ShaderNodeBump")
    bump_002.location = (2408.2, -13.5)
    bump_002.invert = True
    bump_002.inputs[1].default_value = 1.0
    bump_002.inputs[2].default_value = 1.0
    all_edges_016 = nodes.new("ShaderNodeGroup")
    all_edges_016.location = (1026.0, -479.3)
    label_node(all_edges_016, "", frame)
    all_edges_016.xl_c4d_gradient_type = '0'
    all_edges_016.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    all_edges_016.node_tree = all_edges()
    all_edges_016.inputs[2].default_value = 1.0
    mix = nodes.new("ShaderNodeMix")
    mix.location = (1344.2, -411.6)
    label_node(mix, "", frame)
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[6].default_value = (0.0825, 0.0579, 0.0486, 1.0000)
    mix.inputs[7].default_value = (0.1120, 0.1120, 0.1120, 1.0000)
    mix.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (2249.4, 1183.9)
    reroute.socket_idname = 'NodeSocketFloat'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (2249.4, -155.5)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (2249.4, 243.5)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (2292.2, 1089.5)
    reroute_003.socket_idname = 'NodeSocketColor'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (2292.2, 78.2)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1141.8, -285.5)
    label_node(reroute_005, "", frame_003)
    reroute_005.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (775.5, 200.9)
    reroute_006.socket_idname = 'NodeSocketColor'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-3.3, 179.0)
    reroute_007.socket_idname = 'NodeSocketShader'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (775.5, -404.7)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-1807.2, -1037.9)
    reroute_009.socket_idname = 'NodeSocketVector'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-2278.0, -217.8)
    reroute_010.socket_idname = 'NodeSocketColor'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-2188.3, -217.8)
    reroute_011.socket_idname = 'NodeSocketColor'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-1522.7, 75.2)
    reroute_012.socket_idname = 'NodeSocketVector'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (-1601.1, -218.3)
    reroute_013.socket_idname = 'NodeSocketColor'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (-1592.3, 623.5)
    reroute_014.socket_idname = 'NodeSocketColor'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (-2269.4, -789.6)
    reroute_015.socket_idname = 'NodeSocketVector'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (-571.3, 161.1)
    reroute_016.socket_idname = 'NodeSocketShader'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (-854.3, 184.1)
    reroute_017.socket_idname = 'NodeSocketShader'
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (-846.5, 686.6)
    reroute_018.socket_idname = 'NodeSocketShader'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (-581.3, 200.5)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (-1225.8, 1198.8)
    reroute_020.socket_idname = 'NodeSocketFloat'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (-1232.9, 557.8)
    reroute_021.socket_idname = 'NodeSocketVector'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (93.4, 201.2)
    reroute_022.socket_idname = 'NodeSocketColor'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (517.2, -175.7)
    reroute_023.socket_idname = 'NodeSocketColor'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (517.2, 1394.6)
    reroute_024.socket_idname = 'NodeSocketColor'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (-1129.2, -873.6)
    reroute_025.socket_idname = 'NodeSocketVector'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (1884.4, 158.1)
    reroute_026.socket_idname = 'NodeSocketShader'
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (226.8, -189.5)
    label_node(map_range_002, "", frame_002)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.10000000149011612
    map_range_002.inputs[4].default_value = 2.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (1289.7, -320.9)
    label_node(reroute_027, "", frame_002)
    reroute_027.socket_idname = 'NodeSocketVector'
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (350.2, -105.3)
    label_node(map_range_003, "", frame_001)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.18000000715255737
    map_range_003.inputs[4].default_value = 1.25
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (280.0, -165.1)
    label_node(map_range_004, "", frame_004)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.10999999940395355
    map_range_004.inputs[4].default_value = 0.4700000286102295
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (278.0, -354.5)
    label_node(map_range_005, "", frame_005)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.019999999552965164
    map_range_005.inputs[4].default_value = 1.2200000286102295
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (705.1, -102.4)
    label_node(map_range_006, "", frame_005)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[4].default_value = 0.6200000643730164
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (319.7, -240.9)
    label_node(map_range_007, "", frame_003)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.059999994933605194
    map_range_007.inputs[4].default_value = 0.4400000274181366
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (328.9, -337.6)
    label_node(map_range_008, "", frame)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.04000000283122063
    map_range_008.inputs[4].default_value = 0.5
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (1021.7, -289.9)
    label_node(math_002, "", frame)
    math_002.operation = 'DIVIDE'
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 5.0
    math_002.inputs[2].default_value = 0.5
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (961.0, -293.8)
    label_node(reroute_028, "", frame)
    reroute_028.socket_idname = 'NodeSocketFloat'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (961.0, -555.2)
    label_node(reroute_029, "", frame)
    reroute_029.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (986.9, -416.4)
    label_node(reroute_030, "", frame)
    reroute_030.socket_idname = 'NodeSocketFloat'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (986.9, -580.2)
    label_node(reroute_031, "", frame)
    reroute_031.socket_idname = 'NodeSocketFloat'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (918.3, -413.4)
    label_node(reroute_032, "", frame)
    reroute_032.socket_idname = 'NodeSocketFloat'
    map_range_009 = nodes.new("ShaderNodeMapRange")
    map_range_009.location = (709.1, -101.7)
    label_node(map_range_009, "", frame)
    map_range_009.clamp = True
    map_range_009.interpolation_type = 'LINEAR'
    map_range_009.data_type = 'FLOAT'
    map_range_009.inputs[2].default_value = 100.0
    map_range_009.inputs[3].default_value = 0.009999999776482582
    map_range_009.inputs[4].default_value = 1.5
    map_range_009.inputs[5].default_value = 4.0
    map_range_009.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_009.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_009.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (328.9, -586.1)
    label_node(map_range_010, "", frame)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[3].default_value = -0.6700000166893005
    map_range_010.inputs[4].default_value = -0.11999999731779099
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (652.7, -619.9)
    label_node(reroute_033, "", frame)
    reroute_033.socket_idname = 'NodeSocketFloat'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (1093.1, -1022.8)
    reroute_034.socket_idname = 'NodeSocketVector'
    reroute_035 = nodes.new("NodeReroute")
    reroute_035.location = (699.4, -344.7)
    reroute_035.socket_idname = 'NodeSocketFloat'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (774.0, -571.8)
    label_node(percentage_to_0_1, "百分比转0-1", frame_002)
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[4].default_value = 0.009999999776482582
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_036 = nodes.new("NodeReroute")
    reroute_036.location = (1287.3, -117.1)
    label_node(reroute_036, "", frame_002)
    reroute_036.socket_idname = 'NodeSocketFloat'
    reroute_037 = nodes.new("NodeReroute")
    reroute_037.location = (1287.3, -179.1)
    label_node(reroute_037, "", frame_002)
    reroute_037.socket_idname = 'NodeSocketColor'
    reroute_038 = nodes.new("NodeReroute")
    reroute_038.location = (1139.4, -71.5)
    label_node(reroute_038, "", frame_002)
    reroute_038.socket_idname = 'NodeSocketColor'
    reroute_039 = nodes.new("NodeReroute")
    reroute_039.location = (429.0, -873.6)
    reroute_039.socket_idname = 'NodeSocketVector'
    group_003 = nodes.new("ShaderNodeGroup")
    group_003.location = (363.7, -378.7)
    group_003.xl_c4d_gradient_type = '0'
    group_003.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_003.node_tree = hs_bump_control()
    group_003.inputs[2].default_value = 0.4000000059604645
    group_001 = nodes.new("ShaderNodeGroup")
    group_001.location = (790.7, -331.6)
    label_node(group_001, "", frame_002)
    group_001.xl_c4d_gradient_type = '0'
    group_001.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_001.node_tree = hs_bump_control()
    group_001.inputs[2].default_value = 0.4000000059604645
    group_002 = nodes.new("ShaderNodeGroup")
    group_002.location = (1898.7, -63.2)
    group_002.xl_c4d_gradient_type = '0'
    group_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_002.node_tree = hs_bump_control()
    group_002.inputs[2].default_value = 0.4000000059604645
    reroute_040 = nodes.new("NodeReroute")
    reroute_040.location = (2249.8, -176.1)
    reroute_040.socket_idname = 'NodeSocketVector'

    # === 节点连接 ===
    links.new(reroute_016.outputs[0], mix_shader.inputs[2])
    links.new(group_045.outputs[0], color_ramp_004.inputs[0])
    links.new(reroute_017.outputs[0], mix_shader.inputs[1])
    links.new(color_ramp_002.outputs[0], mix_002.inputs[7])
    links.new(reroute_007.outputs[0], mix_shader_001.inputs[1])
    links.new(color_ramp_001.outputs[0], mix_002.inputs[6])
    links.new(reroute_026.outputs[0], mix_shader_001.inputs[2])
    links.new(reroute_013.outputs[0], principled_bsdf_002.inputs[2])
    links.new(reroute_027.outputs[0], bump.inputs[4])
    links.new(reroute_004.outputs[0], principled_bsdf_003.inputs[0])
    links.new(reroute_021.outputs[0], principled_bsdf_001.inputs[5])
    links.new(reroute_019.outputs[0], mix_shader.inputs[0])
    links.new(principled_bsdf_003.outputs[0], mix_shader_002.inputs[2])
    links.new(reroute_037.outputs[0], bump.inputs[3])
    links.new(group_042.outputs[0], map_range_001.inputs[0])
    links.new(reroute_012.outputs[0], principled_bsdf.inputs[5])
    links.new(map_range_008.outputs[0], group_042.inputs[0])
    links.new(color_ramp_007.outputs[0], mix_004.inputs[6])
    links.new(mix_shader_001.outputs[0], mix_shader_002.inputs[1])
    links.new(mix_004.outputs[2], principled_bsdf.inputs[0])
    links.new(reroute_023.outputs[0], principled_bsdf_002.inputs[0])
    links.new(reroute_005.outputs[0], color_ramp_005.inputs[0])
    links.new(reroute_039.outputs[0], bump_001.inputs[4])
    links.new(color_ramp_003.outputs[0], mix_004.inputs[0])
    links.new(reroute_008.outputs[0], bump_001.inputs[3])
    links.new(bump_001.outputs[0], principled_bsdf_002.inputs[5])
    links.new(reroute_006.outputs[0], mix_shader_001.inputs[0])
    links.new(mix_shader_002.outputs[0], output_node.inputs[0])
    links.new(reroute_001.outputs[0], bump_002.inputs[3])
    links.new(bump_002.outputs[0], principled_bsdf_003.inputs[5])
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])
    links.new(reroute_002.outputs[0], mix_shader_002.inputs[0])
    links.new(mix.outputs[2], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], reroute_004.inputs[0])
    links.new(color_ramp_004.outputs[0], reroute_005.inputs[0])
    links.new(reroute_022.outputs[0], reroute_006.inputs[0])
    links.new(mix_shader.outputs[0], reroute_007.inputs[0])
    links.new(reroute_006.outputs[0], reroute_008.inputs[0])
    links.new(reroute_027.outputs[0], reroute_009.inputs[0])
    links.new(mix_002.outputs[2], reroute_010.inputs[0])
    links.new(reroute_010.outputs[0], reroute_011.inputs[0])
    links.new(reroute_013.outputs[0], principled_bsdf.inputs[2])
    links.new(reroute_014.outputs[0], principled_bsdf_001.inputs[2])
    links.new(reroute_015.outputs[0], reroute_012.inputs[0])
    links.new(reroute_011.outputs[0], reroute_013.inputs[0])
    links.new(reroute_011.outputs[0], reroute_014.inputs[0])
    links.new(bump.outputs[0], reroute_015.inputs[0])
    links.new(reroute_018.outputs[0], reroute_016.inputs[0])
    links.new(principled_bsdf.outputs[0], reroute_017.inputs[0])
    links.new(principled_bsdf_001.outputs[0], reroute_018.inputs[0])
    links.new(reroute_020.outputs[0], reroute_019.inputs[0])
    links.new(reroute_012.outputs[0], reroute_021.inputs[0])
    links.new(input_node.outputs[6], principled_bsdf_001.inputs[0])
    links.new(reroute_005.outputs[0], reroute_022.inputs[0])
    links.new(reroute_024.outputs[0], reroute_023.inputs[0])
    links.new(color_ramp_005.outputs[0], reroute_024.inputs[0])
    links.new(reroute_009.outputs[0], reroute_025.inputs[0])
    links.new(principled_bsdf_002.outputs[0], reroute_026.inputs[0])
    links.new(input_node.outputs[3], map_range_002.inputs[0])
    links.new(bevel.outputs[0], reroute_027.inputs[0])
    links.new(input_node.outputs[11], map_range_003.inputs[0])
    links.new(input_node.outputs[9], map_range_004.inputs[0])
    links.new(map_range_007.outputs[0], group_045.inputs[0])
    links.new(input_node.outputs[10], map_range_007.inputs[0])
    links.new(reroute_028.outputs[0], math_002.inputs[0])
    links.new(reroute_028.outputs[0], reroute_029.inputs[0])
    links.new(reroute_032.outputs[0], reroute_030.inputs[0])
    links.new(reroute_030.outputs[0], reroute_031.inputs[0])
    links.new(map_range_001.outputs[0], reroute_032.inputs[0])
    links.new(input_node.outputs[5], map_range_008.inputs[0])
    links.new(map_range_009.outputs[0], reroute_028.inputs[0])
    links.new(input_node.outputs[4], map_range_009.inputs[0])
    links.new(input_node.outputs[5], map_range_010.inputs[0])
    links.new(reroute_033.outputs[0], map_range_001.inputs[3])
    links.new(map_range_010.outputs[0], reroute_033.inputs[0])
    links.new(reroute_040.outputs[0], bump_002.inputs[4])
    links.new(reroute_009.outputs[0], reroute_034.inputs[0])
    links.new(input_node.outputs[7], map_range_006.inputs[0])
    links.new(input_node.outputs[8], map_range_005.inputs[0])
    links.new(map_range.outputs[0], all_edges_014.inputs[1])
    links.new(all_edges_014.outputs[0], reroute_020.inputs[0])
    links.new(map_range_006.outputs[0], all_edges_014.inputs[0])
    links.new(reroute_030.outputs[0], all_edges_015.inputs[1])
    links.new(all_edges_015.outputs[0], reroute.inputs[0])
    links.new(math_002.outputs[0], all_edges_015.inputs[0])
    links.new(all_edges_016.outputs[0], mix.inputs[0])
    links.new(reroute_031.outputs[0], all_edges_016.inputs[1])
    links.new(reroute_029.outputs[0], all_edges_016.inputs[0])
    links.new(group_039.outputs[0], color_ramp_001.inputs[0])
    links.new(map_range_003.outputs[0], group_039.inputs[0])
    links.new(group_041.outputs[0], map_range.inputs[0])
    links.new(map_range_005.outputs[0], group_041.inputs[0])
    links.new(group_040.outputs[0], color_ramp_002.inputs[0])
    links.new(map_range_003.outputs[0], group_040.inputs[0])
    links.new(group_043.outputs[0], color_ramp_007.inputs[0])
    links.new(group_043.outputs[0], color_ramp_003.inputs[0])
    links.new(map_range_004.outputs[0], group_043.inputs[0])
    links.new(group_044.outputs[0], color_ramp_008.inputs[0])
    links.new(map_range_002.outputs[0], group_044.inputs[0])
    links.new(reroute_035.outputs[0], bump_001.inputs[0])
    links.new(group_003.outputs[0], reroute_035.inputs[0])
    links.new(input_node.outputs[0], percentage_to_0_1.inputs[0])
    links.new(percentage_to_0_1.outputs[0], bevel.inputs[0])
    links.new(reroute_036.outputs[0], bump.inputs[0])
    links.new(reroute_038.outputs[0], reroute_037.inputs[0])
    links.new(color_ramp_008.outputs[0], reroute_038.inputs[0])
    links.new(reroute_025.outputs[0], reroute_039.inputs[0])
    links.new(input_node.outputs[2], group_003.inputs[1])
    links.new(input_node.outputs[1], group_003.inputs[0])
    links.new(input_node.outputs[1], group_001.inputs[0])
    links.new(input_node.outputs[2], group_001.inputs[1])
    links.new(group_001.outputs[0], reroute_036.inputs[0])
    links.new(input_node.outputs[2], group_002.inputs[1])
    links.new(input_node.outputs[1], group_002.inputs[0])
    links.new(group_002.outputs[0], bump_002.inputs[0])
    links.new(reroute_034.outputs[0], reroute_040.inputs[0])

    return group