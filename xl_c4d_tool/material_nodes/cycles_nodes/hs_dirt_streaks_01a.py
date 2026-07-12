import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .cavity import cavity
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_18d_r import pf_grunge_18d_r
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_19c_r import pf_grunge_19c_r
from .pf_grunge_20_r import pf_grunge_20_r


def hs_dirt_streaks_01a():
    """BL_脏污条纹 - 条纹状脏污效果材质
    基于Principled BSDF，含凹凸开关/条纹脏污检测"""
    group_name = "BL_脏污条纹"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="着色器", in_out="INPUT", socket_type="NodeSocketShader")
    group.interface.new_socket(name="油漆颜色", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0865, 0.0160, 0.0252, 1.0000)
    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆变色_变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆变色_扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆条纹_变化", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="油漆条纹_大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="XYZ遮罩旋转", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.0000, 0.0000, 0.0000)
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame_001 = create_frame(nodes, "Frame.001", "凹凸独立缩放: 需要单独调整凹凸缩放，可使用独立贴图")
    frame_012 = create_frame(nodes, "Frame.012", "基础着色器输入: 底层着色器信号输入")
    frame_013 = create_frame(nodes, "Frame.013", "条纹: 竖向条纹状脏污效果")
    frame_014 = create_frame(nodes, "Frame.014", "油漆: 油漆材质基础设置")
    frame_015 = create_frame(nodes, "Frame.015", "变色: 表面颜色偏移和褪色效果")
    frame_016 = create_frame(nodes, "Frame.016", "Z方向遮罩: 基于Z轴方向生成遮罩")
    frame_017 = create_frame(nodes, "Frame.017", "基础污渍: 底层污渍纹理")

    # === 节点创建 ===
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (680.0, -195.6)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.1435045301914215
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
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (1380.4, -65.0)
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (-796.5, -403.8)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_19_r()
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.3353476822376251
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.4199398458003998
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (30.3, -37.5)
    label_node(color_ramp, "", frame_001)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (355.3, -35.7)
    label_node(bump, "", frame_001)
    bump.invert = True
    bump.inputs[1].default_value = 0.0010000000474974513
    bump.inputs[2].default_value = 0.10000000149011612
    bump.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 6:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.0
    color_ramp_002.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.12311187386512756
    color_ramp_002.color_ramp.elements[1].color = (0.25, 0.25, 0.25, 1.0)
    color_ramp_002.color_ramp.elements[2].position = 0.18844419717788696
    color_ramp_002.color_ramp.elements[2].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[3].position = 0.2203551083803177
    color_ramp_002.color_ramp.elements[3].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_002.color_ramp.elements[4].position = 0.2522660195827484
    color_ramp_002.color_ramp.elements[4].color = (0.5, 0.5, 0.5, 1.0)
    color_ramp_002.color_ramp.elements[5].position = 0.44410908222198486
    color_ramp_002.color_ramp.elements[5].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (-272.0, -253.3)
    group_032 = nodes.new("ShaderNodeGroup")
    group_032.location = (974.3, -398.1)
    label_node(group_032, "", frame_013)
    group_032.xl_c4d_gradient_type = '0'
    group_032.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_032.node_tree = pf_grunge_19_r()
    group_033 = nodes.new("ShaderNodeGroup")
    group_033.location = (985.0, -150.1)
    label_node(group_033, "", frame_013)
    group_033.xl_c4d_gradient_type = '0'
    group_033.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_033.node_tree = pf_grunge_20_r()
    color_ramp_004 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_004 | Color Ramp.004
    color_ramp_004.color_ramp.color_mode = 'RGB'
    color_ramp_004.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_004.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_004.color_ramp.elements) > 2:
        color_ramp_004.color_ramp.elements.remove(color_ramp_004.color_ramp.elements[-1])
    while len(color_ramp_004.color_ramp.elements) < 2:
        color_ramp_004.color_ramp.elements.new(0.5)
    color_ramp_004.color_ramp.elements[0].position = 0.38368576765060425
    color_ramp_004.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_004.color_ramp.elements[1].position = 0.6193354725837708
    color_ramp_004.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_004
    color_ramp_004.location = (1368.0, -150.1)
    label_node(color_ramp_004, "", frame_013)
    separate_xyz = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (697.1, -102.7)
    label_node(separate_xyz, "", frame_016)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (468.5, -101.8)
    label_node(mapping, "", frame_016)
    mapping.vector_type = 'VECTOR'
    mapping.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    mapping.inputs[3].default_value = (1.0000, 1.0000, 1.0000)
    color_ramp_005 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_005 | Color Ramp.005
    color_ramp_005.color_ramp.color_mode = 'RGB'
    color_ramp_005.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_005.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_005.color_ramp.elements) > 2:
        color_ramp_005.color_ramp.elements.remove(color_ramp_005.color_ramp.elements[-1])
    while len(color_ramp_005.color_ramp.elements) < 2:
        color_ramp_005.color_ramp.elements.new(0.5)
    color_ramp_005.color_ramp.elements[0].position = 0.29003018140792847
    color_ramp_005.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_005.color_ramp.elements[1].position = 0.9969788789749146
    color_ramp_005.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_005
    color_ramp_005.location = (913.4, -102.7)
    label_node(color_ramp_005, "", frame_016)
    vector_transform = nodes.new("ShaderNodeVectorTransform")
    vector_transform.location = (235.9, -102.7)
    label_node(vector_transform, "", frame_016)
    vector_transform.vector_type = 'VECTOR'
    vector_transform.convert_from = 'OBJECT'
    vector_transform.convert_to = 'OBJECT'
    group_034 = nodes.new("ShaderNodeGroup")
    group_034.location = (549.9, -102.1)
    label_node(group_034, "", frame_017)
    group_034.xl_c4d_gradient_type = '0'
    group_034.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_034.node_tree = pf_grunge_19c_r()
    color_ramp_006 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_006 | Color Ramp.006
    color_ramp_006.color_ramp.color_mode = 'RGB'
    color_ramp_006.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_006.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_006.color_ramp.elements) > 2:
        color_ramp_006.color_ramp.elements.remove(color_ramp_006.color_ramp.elements[-1])
    while len(color_ramp_006.color_ramp.elements) < 2:
        color_ramp_006.color_ramp.elements.new(0.5)
    color_ramp_006.color_ramp.elements[0].position = 0.2809668779373169
    color_ramp_006.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_006.color_ramp.elements[1].position = 0.38972803950309753
    color_ramp_006.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_006
    color_ramp_006.location = (806.4, -102.1)
    label_node(color_ramp_006, "", frame_017)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (1266.7, -102.1)
    label_node(map_range_003, "", frame_017)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 1.0
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    mix_006 = nodes.new("ShaderNodeMix")
    mix_006.location = (-1085.2, 440.5)
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_006.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (-1472.2, 561.9)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[4].default_value = 1.4900000095367432
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    hue_saturation_value = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.location = (-2279.4, -41.0)
    hue_saturation_value.inputs[0].default_value = 0.5
    hue_saturation_value.inputs[1].default_value = 0.7199999690055847
    hue_saturation_value.inputs[2].default_value = 1.0
    hue_saturation_value.inputs[3].default_value = 1.0
    mix_007 = nodes.new("ShaderNodeMix")
    mix_007.location = (-1595.6, -291.0)
    mix_007.data_type = 'RGBA'
    mix_007.factor_mode = 'UNIFORM'
    mix_007.blend_type = 'ADD'
    mix_007.clamp_factor = True
    mix_007.clamp_result = False
    mix_007.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_007.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    group_035 = nodes.new("ShaderNodeGroup")
    group_035.location = (277.4, -472.7)
    label_node(group_035, "", frame_014)
    group_035.xl_c4d_gradient_type = '0'
    group_035.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_035.node_tree = pf_grunge_18d_r()
    color_ramp_007 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_007 | Color Ramp.007
    color_ramp_007.color_ramp.color_mode = 'RGB'
    color_ramp_007.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_007.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_007.color_ramp.elements) > 2:
        color_ramp_007.color_ramp.elements.remove(color_ramp_007.color_ramp.elements[-1])
    while len(color_ramp_007.color_ramp.elements) < 2:
        color_ramp_007.color_ramp.elements.new(0.5)
    color_ramp_007.color_ramp.elements[0].position = 0.33232638239860535
    color_ramp_007.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_007.color_ramp.elements[1].position = 0.507552981376648
    color_ramp_007.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_007
    color_ramp_007.location = (564.7, -472.7)
    label_node(color_ramp_007, "", frame_014)
    hue_saturation_value_001 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_001.location = (-2279.4, -499.6)
    hue_saturation_value_001.inputs[0].default_value = 0.5
    hue_saturation_value_001.inputs[1].default_value = 0.8299999833106995
    hue_saturation_value_001.inputs[2].default_value = 1.0
    hue_saturation_value_001.inputs[3].default_value = 1.0
    group_036 = nodes.new("ShaderNodeGroup")
    group_036.location = (1081.9, -381.1)
    label_node(group_036, "", frame_015)
    group_036.xl_c4d_gradient_type = '0'
    group_036.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_036.node_tree = pf_grunge_19_r()
    cavity_015 = nodes.new("ShaderNodeGroup")
    cavity_015.location = (1676.3, -242.6)
    label_node(cavity_015, "", frame_015)
    cavity_015.xl_c4d_gradient_type = '0'
    cavity_015.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    cavity_015.node_tree = cavity()
    cavity_015.inputs[2].default_value = 10.0
    color_ramp_008 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_008 | Color Ramp.008
    color_ramp_008.color_ramp.color_mode = 'RGB'
    color_ramp_008.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_008.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_008.color_ramp.elements) > 2:
        color_ramp_008.color_ramp.elements.remove(color_ramp_008.color_ramp.elements[-1])
    while len(color_ramp_008.color_ramp.elements) < 2:
        color_ramp_008.color_ramp.elements.new(0.5)
    color_ramp_008.color_ramp.elements[0].position = 0.29003044962882996
    color_ramp_008.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_008.color_ramp.elements[1].position = 0.4380667507648468
    color_ramp_008.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_008
    color_ramp_008.location = (1377.9, -381.1)
    label_node(color_ramp_008, "", frame_015)
    mix_008 = nodes.new("ShaderNodeMix")
    mix_008.location = (-1595.6, 297.8)
    mix_008.data_type = 'RGBA'
    mix_008.factor_mode = 'UNIFORM'
    mix_008.blend_type = 'ADD'
    mix_008.clamp_factor = True
    mix_008.clamp_result = False
    mix_008.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    mix_008.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    mix_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    hue_saturation_value_002 = nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_002.location = (-2279.4, -245.7)
    hue_saturation_value_002.inputs[0].default_value = 0.5
    hue_saturation_value_002.inputs[2].default_value = 1.9300000667572021
    hue_saturation_value_002.inputs[3].default_value = 1.0
    reroute = nodes.new("NodeReroute")
    reroute.location = (972.1, -143.3)
    reroute.socket_idname = 'NodeSocketShader'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1096.6, -122.8)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (1096.6, -163.9)
    reroute_002.socket_idname = 'NodeSocketShader'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (-25.0, 763.4)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (-2595.8, -479.2)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-1804.0, -445.3)
    reroute_006.socket_idname = 'NodeSocketColor'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-1804.0, -485.3)
    reroute_007.socket_idname = 'NodeSocketColor'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-1804.0, -465.3)
    reroute_008.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (-2200.1, -878.3)
    reroute_005.socket_idname = 'NodeSocketColor'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (524.0, -248.7)
    reroute_009.socket_idname = 'NodeSocketColor'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (399.6, -352.0)
    reroute_010.socket_idname = 'NodeSocketVector'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-1633.0, 755.3)
    reroute_011.socket_idname = 'NodeSocketFloat'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-1318.9, 264.7)
    reroute_012.socket_idname = 'NodeSocketColor'
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (-1194.4, 286.1)
    reroute_013.socket_idname = 'NodeSocketFloat'
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (-1318.9, 242.3)
    reroute_014.socket_idname = 'NodeSocketColor'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (-518.7, 407.4)
    reroute_015.socket_idname = 'NodeSocketColor'
    reroute_016 = nodes.new("NodeReroute")
    reroute_016.location = (-350.2, -929.6)
    reroute_016.socket_idname = 'NodeSocketColor'
    reroute_017 = nodes.new("NodeReroute")
    reroute_017.location = (-1845.5, 754.6)
    reroute_017.socket_idname = 'NodeSocketFloat'
    reroute_019 = nodes.new("NodeReroute")
    reroute_019.location = (-3098.5, 143.1)
    reroute_019.socket_idname = 'NodeSocketFloat'
    reroute_020 = nodes.new("NodeReroute")
    reroute_020.location = (-1638.3, 100.5)
    reroute_020.socket_idname = 'NodeSocketColor'
    reroute_021 = nodes.new("NodeReroute")
    reroute_021.location = (-1753.3, 122.4)
    reroute_021.socket_idname = 'NodeSocketColor'
    reroute_022 = nodes.new("NodeReroute")
    reroute_022.location = (-2028.8, -74.0)
    reroute_022.socket_idname = 'NodeSocketColor'
    reroute_023 = nodes.new("NodeReroute")
    reroute_023.location = (-2028.8, -279.5)
    reroute_023.socket_idname = 'NodeSocketColor'
    reroute_025 = nodes.new("NodeReroute")
    reroute_025.location = (-2447.1, -385.3)
    reroute_025.socket_idname = 'NodeSocketColor'
    reroute_027 = nodes.new("NodeReroute")
    reroute_027.location = (-2911.0, -479.2)
    reroute_027.socket_idname = 'NodeSocketColor'
    reroute_028 = nodes.new("NodeReroute")
    reroute_028.location = (-2468.4, -476.7)
    reroute_028.socket_idname = 'NodeSocketColor'
    reroute_024 = nodes.new("NodeReroute")
    reroute_024.location = (-2587.9, -180.5)
    reroute_024.socket_idname = 'NodeSocketColor'
    reroute_026 = nodes.new("NodeReroute")
    reroute_026.location = (-2361.1, -640.6)
    reroute_026.socket_idname = 'NodeSocketColor'
    reroute_029 = nodes.new("NodeReroute")
    reroute_029.location = (670.7, -107.0)
    label_node(reroute_029, "", frame_014)
    reroute_029.socket_idname = 'NodeSocketColor'
    reroute_032 = nodes.new("NodeReroute")
    reroute_032.location = (-2192.8, 1474.6)
    reroute_032.socket_idname = 'NodeSocketFloat'
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (307.0, -105.4)
    label_node(percentage_to_0_1, "百分比转0-1", frame_017)
    percentage_to_0_1.clamp = True
    percentage_to_0_1.interpolation_type = 'LINEAR'
    percentage_to_0_1.data_type = 'FLOAT'
    percentage_to_0_1.inputs[2].default_value = 100.0
    percentage_to_0_1.inputs[3].default_value = 0.05000000074505806
    percentage_to_0_1.inputs[4].default_value = 0.8500000238418579
    percentage_to_0_1.inputs[5].default_value = 4.0
    percentage_to_0_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_1.location = (308.0, -350.8)
    label_node(percentage_to_0_1_1, "百分比转0-1", frame_017)
    percentage_to_0_1_1.clamp = True
    percentage_to_0_1_1.interpolation_type = 'LINEAR'
    percentage_to_0_1_1.data_type = 'FLOAT'
    percentage_to_0_1_1.inputs[2].default_value = 100.0
    percentage_to_0_1_1.inputs[3].default_value = 0.009999999776482582
    percentage_to_0_1_1.inputs[4].default_value = 0.800000011920929
    percentage_to_0_1_1.inputs[5].default_value = 4.0
    percentage_to_0_1_1.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_1.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_1.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_033 = nodes.new("NodeReroute")
    reroute_033.location = (1127.5, -383.2)
    label_node(reroute_033, "", frame_017)
    reroute_033.socket_idname = 'NodeSocketFloat'
    percentage_to_0_1_2 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_2.location = (342.7, -102.0)
    label_node(percentage_to_0_1_2, "百分比转0-1", frame_013)
    percentage_to_0_1_2.clamp = True
    percentage_to_0_1_2.interpolation_type = 'LINEAR'
    percentage_to_0_1_2.data_type = 'FLOAT'
    percentage_to_0_1_2.inputs[2].default_value = 100.0
    percentage_to_0_1_2.inputs[3].default_value = 0.009999999776482582
    percentage_to_0_1_2.inputs[4].default_value = 0.3199999928474426
    percentage_to_0_1_2.inputs[5].default_value = 4.0
    percentage_to_0_1_2.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_2.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_2.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_3 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_3.location = (343.6, -381.8)
    label_node(percentage_to_0_1_3, "百分比转0-1", frame_013)
    percentage_to_0_1_3.clamp = True
    percentage_to_0_1_3.interpolation_type = 'LINEAR'
    percentage_to_0_1_3.data_type = 'FLOAT'
    percentage_to_0_1_3.inputs[2].default_value = 100.0
    percentage_to_0_1_3.inputs[3].default_value = 0.03999999910593033
    percentage_to_0_1_3.inputs[4].default_value = 0.6000000238418579
    percentage_to_0_1_3.inputs[5].default_value = 4.0
    percentage_to_0_1_3.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_3.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_3.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    texture_coordinate_001 = nodes.new("ShaderNodeTexCoord")
    texture_coordinate_001.location = (30.1, -104.8)
    label_node(texture_coordinate_001, "", frame_016)
    texture_coordinate_001.from_instancer = False
    color_ramp_009 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_009 | Color Ramp.009
    color_ramp_009.color_ramp.color_mode = 'RGB'
    color_ramp_009.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_009.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_009.color_ramp.elements) > 2:
        color_ramp_009.color_ramp.elements.remove(color_ramp_009.color_ramp.elements[-1])
    while len(color_ramp_009.color_ramp.elements) < 2:
        color_ramp_009.color_ramp.elements.new(0.5)
    color_ramp_009.color_ramp.elements[0].position = 0.30815717577934265
    color_ramp_009.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_009.color_ramp.elements[1].position = 0.6435044407844543
    color_ramp_009.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_009
    color_ramp_009.location = (1357.5, -380.7)
    label_node(color_ramp_009, "", frame_013)
    math = nodes.new("ShaderNodeMath")
    math.location = (1716.4, -249.6)
    label_node(math, "", frame_013)
    math.operation = 'SUBTRACT'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.location = (690.7, -110.1)
    label_node(vector_math, "", frame_013)
    vector_math.operation = 'MULTIPLY'
    vector_math.inputs[1].default_value = (1.0000, 1.0000, 0.0500)
    vector_math.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    vector_math.inputs[3].default_value = 1.0
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (-2609.3, 1508.0)
    math_001.operation = 'SUBTRACT'
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (-2968.1, 1489.8)
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    math_002.inputs[2].default_value = 0.5
    percentage_to_0_1_4 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_4.location = (547.0, -101.9)
    label_node(percentage_to_0_1_4, "百分比转0-1", frame_015)
    percentage_to_0_1_4.clamp = True
    percentage_to_0_1_4.interpolation_type = 'LINEAR'
    percentage_to_0_1_4.data_type = 'FLOAT'
    percentage_to_0_1_4.inputs[2].default_value = 100.0
    percentage_to_0_1_4.inputs[3].default_value = 0.03999999910593033
    percentage_to_0_1_4.inputs[4].default_value = 0.6100000739097595
    percentage_to_0_1_4.inputs[5].default_value = 4.0
    percentage_to_0_1_4.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_4.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_4.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_4.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_5 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_5.location = (547.0, -363.5)
    label_node(percentage_to_0_1_5, "百分比转0-1", frame_015)
    percentage_to_0_1_5.clamp = False
    percentage_to_0_1_5.interpolation_type = 'LINEAR'
    percentage_to_0_1_5.data_type = 'FLOAT'
    percentage_to_0_1_5.inputs[2].default_value = 100.0
    percentage_to_0_1_5.inputs[3].default_value = 0.03999999910593033
    percentage_to_0_1_5.inputs[4].default_value = 0.8500000238418579
    percentage_to_0_1_5.inputs[5].default_value = 4.0
    percentage_to_0_1_5.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_5.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_5.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_5.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_5.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_5.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_018 = nodes.new("NodeReroute")
    reroute_018.location = (962.2, -324.2)
    label_node(reroute_018, "", frame_015)
    reroute_018.socket_idname = 'NodeSocketFloat'
    reroute_030 = nodes.new("NodeReroute")
    reroute_030.location = (800.5, -456.7)
    label_node(reroute_030, "", frame_015)
    reroute_030.socket_idname = 'NodeSocketFloat'
    reroute_031 = nodes.new("NodeReroute")
    reroute_031.location = (915.2, -457.2)
    label_node(reroute_031, "", frame_015)
    reroute_031.socket_idname = 'NodeSocketFloat'
    reroute_034 = nodes.new("NodeReroute")
    reroute_034.location = (35.0, -548.9)
    label_node(reroute_034, "", frame_014)
    reroute_034.socket_idname = 'NodeSocketFloat'
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (-189.9, -555.0)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    group_031 = nodes.new("ShaderNodeGroup")
    group_031.location = (-736.8, -814.2)
    group_031.xl_c4d_gradient_type = '0'
    group_031.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_031.node_tree = pf_grunge_19_r()
    percentage_to_0_1_6 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_6.location = (-971.4, -784.4)
    label_node(percentage_to_0_1_6, "百分比转0-1")
    percentage_to_0_1_6.clamp = False
    percentage_to_0_1_6.interpolation_type = 'LINEAR'
    percentage_to_0_1_6.data_type = 'FLOAT'
    percentage_to_0_1_6.inputs[2].default_value = 100.0
    percentage_to_0_1_6.inputs[3].default_value = 0.20000000298023224
    percentage_to_0_1_6.inputs[4].default_value = 1.25
    percentage_to_0_1_6.inputs[5].default_value = 4.0
    percentage_to_0_1_6.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_6.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_6.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_6.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_6.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_6.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    percentage_to_0_1_7 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1_7.location = (-975.7, -445.3)
    label_node(percentage_to_0_1_7, "百分比转0-1")
    percentage_to_0_1_7.clamp = False
    percentage_to_0_1_7.interpolation_type = 'LINEAR'
    percentage_to_0_1_7.data_type = 'FLOAT'
    percentage_to_0_1_7.inputs[2].default_value = 100.0
    percentage_to_0_1_7.inputs[3].default_value = 0.10000000149011612
    percentage_to_0_1_7.inputs[4].default_value = 1.25
    percentage_to_0_1_7.inputs[5].default_value = 4.0
    percentage_to_0_1_7.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_7.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_7.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_7.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    percentage_to_0_1_7.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    percentage_to_0_1_7.inputs[11].default_value = (4.0000, 4.0000, 4.0000)

    # === 节点连接 ===
    links.new(reroute_010.outputs[0], principled_bsdf.inputs[5])
    links.new(reroute_002.outputs[0], mix_shader.inputs[2])
    links.new(reroute_016.outputs[0], color_ramp.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(vector_transform.outputs[0], mapping.inputs[0])
    links.new(separate_xyz.outputs[2], color_ramp_005.inputs[0])
    links.new(mapping.outputs[0], separate_xyz.inputs[0])
    links.new(color_ramp_006.outputs[0], map_range_003.inputs[0])
    links.new(reroute_013.outputs[0], mix_006.inputs[0])
    links.new(reroute_009.outputs[0], principled_bsdf.inputs[0])
    links.new(reroute_012.outputs[0], mix_006.inputs[6])
    links.new(reroute_014.outputs[0], mix_006.inputs[7])
    links.new(reroute_006.outputs[0], mix_007.inputs[0])
    links.new(reroute_008.outputs[0], mix_007.inputs[6])
    links.new(reroute_007.outputs[0], mix_007.inputs[7])
    links.new(color_ramp_002.outputs[0], principled_bsdf.inputs[2])
    links.new(color_ramp.outputs[0], bump.inputs[3])
    links.new(reroute_021.outputs[0], mix_008.inputs[6])
    links.new(reroute_019.outputs[0], mix_008.inputs[0])
    links.new(reroute_025.outputs[0], hue_saturation_value_002.inputs[4])
    links.new(reroute_020.outputs[0], mix_008.inputs[7])
    links.new(reroute_001.outputs[0], mix_shader.inputs[0])
    links.new(reroute.outputs[0], mix_shader.inputs[1])
    links.new(input_node.outputs[0], reroute.inputs[0])
    links.new(reroute_003.outputs[0], reroute_001.inputs[0])
    links.new(principled_bsdf.outputs[0], reroute_002.inputs[0])
    links.new(reroute_011.outputs[0], reroute_003.inputs[0])
    links.new(reroute_027.outputs[0], reroute_004.inputs[0])
    links.new(reroute_005.outputs[0], reroute_006.inputs[0])
    links.new(hue_saturation_value_001.outputs[0], reroute_007.inputs[0])
    links.new(reroute_028.outputs[0], reroute_008.inputs[0])
    links.new(color_ramp_007.outputs[0], reroute_005.inputs[0])
    links.new(reroute_015.outputs[0], reroute_009.inputs[0])
    links.new(bump.outputs[0], reroute_010.inputs[0])
    links.new(reroute_017.outputs[0], reroute_011.inputs[0])
    links.new(reroute_011.outputs[0], map_range_001.inputs[0])
    links.new(mix_008.outputs[2], reroute_012.inputs[0])
    links.new(map_range_001.outputs[0], reroute_013.inputs[0])
    links.new(mix_007.outputs[2], reroute_014.inputs[0])
    links.new(mix_006.outputs[2], reroute_015.inputs[0])
    links.new(reroute_032.outputs[0], reroute_017.inputs[0])
    links.new(reroute_023.outputs[0], reroute_020.inputs[0])
    links.new(reroute_022.outputs[0], reroute_021.inputs[0])
    links.new(hue_saturation_value.outputs[0], reroute_022.inputs[0])
    links.new(hue_saturation_value_002.outputs[0], reroute_023.inputs[0])
    links.new(reroute_004.outputs[0], reroute_025.inputs[0])
    links.new(reroute_029.outputs[0], reroute_027.inputs[0])
    links.new(reroute_024.outputs[0], hue_saturation_value.inputs[4])
    links.new(reroute_004.outputs[0], reroute_028.inputs[0])
    links.new(reroute_026.outputs[0], hue_saturation_value_001.inputs[4])
    links.new(reroute_027.outputs[0], reroute_024.inputs[0])
    links.new(reroute_028.outputs[0], reroute_026.inputs[0])
    links.new(input_node.outputs[1], reroute_029.inputs[0])
    links.new(input_node.outputs[6], percentage_to_0_1.inputs[0])
    links.new(input_node.outputs[7], percentage_to_0_1_1.inputs[0])
    links.new(reroute_033.outputs[0], map_range_003.inputs[4])
    links.new(percentage_to_0_1_1.outputs[0], reroute_033.inputs[0])
    links.new(input_node.outputs[12], mapping.inputs[2])
    links.new(color_ramp_004.outputs[0], math.inputs[0])
    links.new(color_ramp_009.outputs[0], math.inputs[1])
    links.new(percentage_to_0_1_2.outputs[0], vector_math.inputs[0])
    links.new(math.outputs[0], math_001.inputs[1])
    links.new(math_001.outputs[0], reroute_032.inputs[0])
    links.new(color_ramp_005.outputs[0], math_002.inputs[1])
    links.new(map_range_003.outputs[0], math_002.inputs[0])
    links.new(math_002.outputs[0], math_001.inputs[0])
    links.new(texture_coordinate_001.outputs[0], vector_transform.inputs[0])
    links.new(input_node.outputs[11], percentage_to_0_1_2.inputs[0])
    links.new(input_node.outputs[10], percentage_to_0_1_3.inputs[0])
    links.new(input_node.outputs[8], percentage_to_0_1_5.inputs[0])
    links.new(input_node.outputs[9], percentage_to_0_1_4.inputs[0])
    links.new(percentage_to_0_1_4.outputs[0], reroute_018.inputs[0])
    links.new(percentage_to_0_1_5.outputs[0], reroute_030.inputs[0])
    links.new(reroute_030.outputs[0], reroute_031.inputs[0])
    links.new(reroute_031.outputs[0], reroute_034.inputs[0])
    links.new(color_ramp_008.outputs[0], cavity_015.inputs[1])
    links.new(cavity_015.outputs[0], reroute_019.inputs[0])
    links.new(reroute_018.outputs[0], cavity_015.inputs[0])
    links.new(group_030.outputs[0], color_ramp_002.inputs[0])
    links.new(percentage_to_0_1_3.outputs[0], group_032.inputs[0])
    links.new(group_032.outputs[0], color_ramp_009.inputs[0])
    links.new(group_036.outputs[0], color_ramp_008.inputs[0])
    links.new(reroute_031.outputs[0], group_036.inputs[0])
    links.new(group_034.outputs[0], color_ramp_006.inputs[0])
    links.new(percentage_to_0_1.outputs[0], group_034.inputs[0])
    links.new(group_033.outputs[0], color_ramp_004.inputs[0])
    links.new(vector_math.outputs[0], group_033.inputs[0])
    links.new(group_035.outputs[0], color_ramp_007.inputs[0])
    links.new(reroute_034.outputs[0], group_035.inputs[0])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[0])
    links.new(input_node.outputs[4], hs_bump_control.inputs[1])
    links.new(percentage_to_0_1_6.outputs[0], group_031.inputs[0])
    links.new(group_031.outputs[0], reroute_016.inputs[0])
    links.new(percentage_to_0_1_7.outputs[0], group_030.inputs[0])
    links.new(input_node.outputs[5], percentage_to_0_1_6.inputs[0])
    links.new(input_node.outputs[2], percentage_to_0_1_7.inputs[0])

    return group