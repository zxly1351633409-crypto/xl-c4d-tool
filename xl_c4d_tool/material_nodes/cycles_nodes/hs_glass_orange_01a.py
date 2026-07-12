import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_19b_r import pf_grunge_19b_r
from .pf_grunge_22_r import pf_grunge_22_r


def hs_glass_orange_01a():
    """BL_橙色玻璃 - 橙色半透明玻璃材质
    基于Principled BSDF玻璃着色器，含凹凸控制/粗糙度脏污"""
    group_name = "BL_橙色玻璃"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="污渍缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="划痕缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="划痕强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "污垢: 表面污垢和脏旧效果")
    frame_001 = create_frame(nodes, "Frame.001", "划痕: 表面划痕效果遮罩")
    frame_002 = create_frame(nodes, "Frame.002", "凹凸: 凹凸贴图效果")

    # === 节点创建 ===
    color_ramp = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp | Color Ramp
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp.color_ramp.elements) > 2:
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])
    while len(color_ramp.color_ramp.elements) < 2:
        color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[0].position = 0.5347437262535095
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.5891242027282715
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp
    color_ramp.location = (695.5, -186.3)
    label_node(color_ramp, "", frame)
    group_028 = nodes.new("ShaderNodeGroup")
    group_028.location = (219.9, -101.9)
    label_node(group_028, "", frame_001)
    group_028.xl_c4d_gradient_type = '0'
    group_028.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_028.node_tree = pf_grunge_22_r()
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.0
    color_ramp_001.color_ramp.elements[0].color = (0.004703656770288944, 0.004703656770288944, 0.004703656770288944, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.2114802598953247
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (506.4, -101.9)
    label_node(color_ramp_001, "", frame_001)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (84.1, 37.8)
    bump.invert = False
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (-138.1, -92.1)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    group_029 = nodes.new("ShaderNodeGroup")
    group_029.location = (219.9, -226.7)
    label_node(group_029, "", frame_002)
    group_029.xl_c4d_gradient_type = '0'
    group_029.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_029.node_tree = pf_grunge_19b_r()
    color_ramp_002 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_002 | Color Ramp.002
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_002.color_ramp.elements) > 2:
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[-1])
    while len(color_ramp_002.color_ramp.elements) < 2:
        color_ramp_002.color_ramp.elements.new(0.5)
    color_ramp_002.color_ramp.elements[0].position = 0.25075528025627136
    color_ramp_002.color_ramp.elements[0].color = (0.004703656770288944, 0.004703656770288944, 0.004703656770288944, 1.0)
    color_ramp_002.color_ramp.elements[1].position = 0.3987920880317688
    color_ramp_002.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_002
    color_ramp_002.location = (508.2, -226.7)
    label_node(color_ramp_002, "", frame_002)
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (1171.8, 91.5)
    group_030 = nodes.new("ShaderNodeGroup")
    group_030.location = (383.5, -186.3)
    label_node(group_030, "", frame)
    group_030.xl_c4d_gradient_type = '0'
    group_030.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_030.node_tree = pf_grunge_19_r()
    diffuse_bsdf = nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_bsdf.location = (441.1, -621.1)
    diffuse_bsdf.inputs[0].default_value = (0.0730, 0.0268, 0.0138, 1.0000)
    diffuse_bsdf.inputs[1].default_value = 0.7755101919174194
    diffuse_bsdf.inputs[2].default_value = (0.0000, 0.0000, 0.0000)
    reroute = nodes.new("NodeReroute")
    reroute.location = (775.7, -7.5)
    reroute.socket_idname = 'NodeSocketShader'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (945.7, 33.6)
    reroute_001.socket_idname = 'NodeSocketColor'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (775.7, 12.8)
    reroute_002.socket_idname = 'NodeSocketShader'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (55.6, 681.0)
    reroute_004.socket_idname = 'NodeSocketColor'
    principled_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.location = (351.7, 40.6)
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    principled_bsdf.inputs[0].default_value = (0.6480, 0.1215, 0.0041, 1.0000)
    principled_bsdf.inputs[2].default_value = 0.10725075006484985
    principled_bsdf.inputs[3].default_value = 1.5
    principled_bsdf.inputs[4].default_value = 1.0
    principled_bsdf.inputs[8].default_value = 1.0
    principled_bsdf.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    principled_bsdf.inputs[13].default_value = 0.5
    principled_bsdf.inputs[14].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[17].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    principled_bsdf.inputs[21].default_value = 1.5
    principled_bsdf.inputs[22].default_value = (1.0000, 0.7152, 0.3616, 1.0000)
    principled_bsdf.inputs[23].default_value = (0.0000, 0.0000, 0.0000)
    principled_bsdf.inputs[25].default_value = 0.5
    principled_bsdf.inputs[26].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[27].default_value = (1.0000, 1.0000, 1.0000, 1.0000)
    principled_bsdf.inputs[30].default_value = 1.3300000429153442
    group_031 = nodes.new("ShaderNodeGroup")
    group_031.location = (219.9, -357.3)
    label_node(group_031, "", frame_001)
    group_031.xl_c4d_gradient_type = '0'
    group_031.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_031.node_tree = pf_grunge_22_r()
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'CARDINAL'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.35347437858581543
    color_ramp_003.color_ramp.elements[0].color = (0.004703656770288944, 0.004703656770288944, 0.004703656770288944, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.45921289920806885
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (506.4, -357.3)
    label_node(color_ramp_003, "", frame_001)
    math_001 = nodes.new("ShaderNodeMath")
    math_001.location = (118.2, -435.0)
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (-645.2, -754.0)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 100.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math = nodes.new("ShaderNodeMath")
    math.location = (118.0, -278.4)
    math.operation = 'ADD'
    math.use_clamp = True
    math.inputs[2].default_value = 0.5
    math_002 = nodes.new("ShaderNodeMath")
    math_002.location = (-230.6, -337.7)
    math_002.operation = 'SUBTRACT'
    math_002.use_clamp = False
    math_002.inputs[0].default_value = 1.0
    math_002.inputs[2].default_value = 0.5
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (-426.4, -787.1)
    reroute_005.socket_idname = 'NodeSocketFloat'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-317.6, -559.6)
    reroute_006.socket_idname = 'NodeSocketFloat'
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (29.9, -101.9)
    label_node(map_range_001, "", frame_001)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.019999999552965164
    map_range_001.inputs[4].default_value = 0.20000000298023224
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (29.9, -357.3)
    label_node(map_range_002, "", frame_001)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.019999999552965164
    map_range_002.inputs[4].default_value = 0.5
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-1312.4, -504.4)
    reroute_007.socket_idname = 'NodeSocketFloatPercentage'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-1312.4, -378.5)
    reroute_008.socket_idname = 'NodeSocketFloatPercentage'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (-1312.4, -634.6)
    reroute_009.socket_idname = 'NodeSocketFloatPercentage'
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (-317.6, -353.5)
    reroute_010.socket_idname = 'NodeSocketFloat'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-33.6, -293.1)
    reroute_011.socket_idname = 'NodeSocketFloat'
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (30.2, -196.3)
    label_node(map_range_003, "", frame_002)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.019999999552965164
    map_range_003.inputs[4].default_value = 0.20000000298023224
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (29.7, -101.8)
    label_node(map_range_005, "", frame)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.05000000074505806
    map_range_005.inputs[4].default_value = 0.75
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (-303.9, 288.7)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    percentage_to_0_1 = nodes.new("ShaderNodeMapRange")
    percentage_to_0_1.location = (-309.4, -34.8)
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
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (-125.4, 76.3)
    reroute_003.socket_idname = 'NodeSocketColor'

    # === 节点连接 ===
    links.new(group_029.outputs[0], color_ramp_002.inputs[0])
    links.new(group_030.outputs[0], color_ramp.inputs[0])
    links.new(map_range_005.outputs[0], group_030.inputs[0])
    links.new(bevel.outputs[0], bump.inputs[4])
    links.new(group_028.outputs[0], color_ramp_001.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(reroute_004.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], mix_shader.inputs[2])
    links.new(reroute_001.outputs[0], mix_shader.inputs[0])
    links.new(reroute_002.outputs[0], mix_shader.inputs[1])
    links.new(color_ramp.outputs[0], reroute_004.inputs[0])
    links.new(diffuse_bsdf.outputs[0], reroute.inputs[0])
    links.new(bump.outputs[0], principled_bsdf.inputs[5])
    links.new(principled_bsdf.outputs[0], reroute_002.inputs[0])
    links.new(group_031.outputs[0], color_ramp_003.inputs[0])
    links.new(math_001.outputs[0], principled_bsdf.inputs[19])
    links.new(color_ramp_003.outputs[0], math_001.inputs[0])
    links.new(reroute_006.outputs[0], math_001.inputs[1])
    links.new(color_ramp_001.outputs[0], math.inputs[0])
    links.new(reroute_011.outputs[0], math.inputs[1])
    links.new(math.outputs[0], principled_bsdf.inputs[18])
    links.new(map_range.outputs[0], reroute_005.inputs[0])
    links.new(reroute_005.outputs[0], reroute_006.inputs[0])
    links.new(reroute_010.outputs[0], math_002.inputs[1])
    links.new(reroute_008.outputs[0], map_range_001.inputs[0])
    links.new(reroute_009.outputs[0], map_range_002.inputs[0])
    links.new(map_range_001.outputs[0], group_028.inputs[0])
    links.new(map_range_002.outputs[0], group_031.inputs[0])
    links.new(reroute_007.outputs[0], reroute_008.inputs[0])
    links.new(reroute_007.outputs[0], reroute_009.inputs[0])
    links.new(input_node.outputs[5], reroute_007.inputs[0])
    links.new(reroute_006.outputs[0], reroute_010.inputs[0])
    links.new(math_002.outputs[0], reroute_011.inputs[0])
    links.new(map_range_003.outputs[0], group_029.inputs[0])
    links.new(input_node.outputs[3], map_range_003.inputs[0])
    links.new(input_node.outputs[0], map_range_005.inputs[0])
    links.new(input_node.outputs[6], map_range.inputs[0])
    links.new(input_node.outputs[4], hs_bump_control.inputs[1])
    links.new(input_node.outputs[2], hs_bump_control.inputs[0])
    links.new(hs_bump_control.outputs[0], bump.inputs[0])
    links.new(reroute_003.outputs[0], bump.inputs[3])
    links.new(percentage_to_0_1.outputs[0], bevel.inputs[0])
    links.new(color_ramp_002.outputs[0], reroute_003.inputs[0])
    links.new(input_node.outputs[1], percentage_to_0_1.inputs[0])

    return group