import bpy
from ...utils.node_utils import get_mix_f_ports, create_frame, label_node
from .cavity import cavity as _cavity_fn
from .edge import edge
from .hs_bump_control import hs_bump_control as _hs_bump_control_fn
from .pf_grunge_17c_r import pf_grunge_17c_r
from .pf_grunge_19_r import pf_grunge_19_r
from .pf_grunge_20_r import pf_grunge_20_r
from .pf_grunge_21c_r import pf_grunge_21c_r
from .pf_grunge_22b_r import pf_grunge_22b_r
from .pf_grunge_23_r import pf_grunge_23_r


def hs_rubber_02a():
    """BL_橡胶02 - 脏旧橡胶材质
    基于Principled BSDF，含凹凸开关/粗糙度脏污/边缘磨损/脏污混合"""
    group_name = "BL_橡胶02"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    group.interface.new_socket(name="粗糙度缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="颜色: 材质颜色通道", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.0000, 0.0000, 0.0000, 1.0000)
    group.interface.new_socket(name="倒角大小", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸开关", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="凹凸缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="凹凸强度", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污缩放", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="脏污扩散", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘磨损", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="边缘损伤", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    group.interface.new_socket(name="着色器", in_out="OUTPUT", socket_type="NodeSocketShader")

    nodes = group.nodes
    links = group.links
    input_node = nodes.new('NodeGroupInput')
    output_node = nodes.new('NodeGroupOutput')

    # === 注释框 ===
    frame = create_frame(nodes, "主节点: 所有操作节点集合", "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    frame_001 = create_frame(nodes, "Frame.001", "凹腔: AO采样检测凹面/凸面区域生成遮罩")
    frame_002 = create_frame(nodes, "Frame.002", "脏污: 基于AO的凹腔和表面脏污效果遮罩")
    frame_003 = create_frame(nodes, "Frame.003", "边缘损伤: 模拟边缘磕碰和损伤效果的遮罩")
    frame_004 = create_frame(nodes, "Frame.004", "凹凸: 凹凸贴图效果")
    frame_005 = create_frame(nodes, "Frame.005", "粗糙度: 表面粗糙度控制")

    # === 节点创建 ===
    principled_bsdf_001 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.location = (1899.7, 53.3)
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_001.inputs[3].default_value = 1.5
    principled_bsdf_001.inputs[4].default_value = 1.0
    principled_bsdf_001.inputs[9].default_value = (1.0000, 0.2000, 0.1000)
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    principled_bsdf_001.inputs[11].default_value = 1.399999976158142
    principled_bsdf_001.inputs[13].default_value = 0.04891504347324371
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
    group_002 = nodes.new("ShaderNodeGroup")
    group_002.location = (1032.8, -355.5)
    label_node(group_002, "", frame_001)
    group_002.xl_c4d_gradient_type = '0'
    group_002.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_002.node_tree = _cavity_fn()
    group_002.inputs[2].default_value = 2.0
    color_ramp_001 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_001 | Color Ramp.001
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_001.color_ramp.elements) > 2:
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[-1])
    while len(color_ramp_001.color_ramp.elements) < 2:
        color_ramp_001.color_ramp.elements.new(0.5)
    color_ramp_001.color_ramp.elements[0].position = 0.27794569730758667
    color_ramp_001.color_ramp.elements[0].color = (0.0052530644461512566, 0.0052530644461512566, 0.0052530644461512566, 1.0)
    color_ramp_001.color_ramp.elements[1].position = 0.4996162950992584
    color_ramp_001.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_001
    color_ramp_001.location = (636.2, -355.5)
    label_node(color_ramp_001, "", frame_001)
    group_003 = nodes.new("ShaderNodeGroup")
    group_003.location = (283.2, -355.5)
    label_node(group_003, "", frame_001)
    group_003.xl_c4d_gradient_type = '0'
    group_003.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_003.node_tree = pf_grunge_19_r()
    group_009 = nodes.new("ShaderNodeGroup")
    group_009.location = (1044.8, -345.1)
    label_node(group_009, "", frame)
    group_009.xl_c4d_gradient_type = '0'
    group_009.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_009.node_tree = edge()
    group_009.inputs[2].default_value = 1.0
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
    color_ramp_002.location = (585.0, -345.1)
    label_node(color_ramp_002, "", frame)
    group_004 = nodes.new("ShaderNodeGroup")
    group_004.location = (232.0, -345.1)
    label_node(group_004, "", frame)
    group_004.xl_c4d_gradient_type = '0'
    group_004.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_004.node_tree = pf_grunge_21c_r()
    cavity = nodes.new("ShaderNodeMix")
    cavity.location = (-112.4, 32.6)
    label_node(cavity, "凹腔: AO采样检测凹面/凸面区域生成遮罩")
    cavity.data_type = 'RGBA'
    cavity.factor_mode = 'UNIFORM'
    cavity.blend_type = 'MIX'
    cavity.clamp_factor = True
    cavity.clamp_result = False
    cavity.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    cavity.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    cavity.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    cavity.inputs[7].default_value = (0.0459, 0.0166, 0.0060, 1.0000)
    cavity.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    cavity.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    edges = nodes.new("ShaderNodeMix")
    edges.location = (-636.8, 32.6)
    label_node(edges, "边缘磨损: 基于倒角检测的边缘磨损效果遮罩")
    edges.data_type = 'RGBA'
    edges.factor_mode = 'UNIFORM'
    edges.blend_type = 'MIX'
    edges.clamp_factor = True
    edges.clamp_result = False
    edges.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    edges.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    edges.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    edges.inputs[7].default_value = (0.0186, 0.0186, 0.0186, 1.0000)
    edges.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    edges.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    bevel = nodes.new("ShaderNodeBevel")
    bevel.location = (754.6, -656.6)
    label_node(bevel, "", frame_004)
    bevel.samples = 32
    bevel.inputs[1].default_value = (0.0000, 0.0000, 0.0000)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (1144.9, -266.9)
    label_node(bump, "", frame_004)
    bump.invert = True
    bump.inputs[1].default_value = 1.0
    bump.inputs[2].default_value = 0.10000000149011612
    color_ramp_003 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_003 | Color Ramp.003
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_003.color_ramp.elements) > 2:
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[-1])
    while len(color_ramp_003.color_ramp.elements) < 2:
        color_ramp_003.color_ramp.elements.new(0.5)
    color_ramp_003.color_ramp.elements[0].position = 0.22054387629032135
    color_ramp_003.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_003.color_ramp.elements[1].position = 0.7842899560928345
    color_ramp_003.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_003
    color_ramp_003.location = (654.2, -265.4)
    label_node(color_ramp_003, "", frame_004)
    group_005 = nodes.new("ShaderNodeGroup")
    group_005.location = (451.7, -265.4)
    label_node(group_005, "", frame_004)
    group_005.xl_c4d_gradient_type = '0'
    group_005.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_005.node_tree = pf_grunge_23_r()
    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (3099.7, 98.3)
    principled_bsdf_002 = nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.location = (2631.0, -60.1)
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    principled_bsdf_002.inputs[0].default_value = (0.0081, 0.0081, 0.0081, 1.0000)
    principled_bsdf_002.inputs[2].default_value = 1.0
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
    color_ramp_006 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_006 | Color Ramp.006
    color_ramp_006.color_ramp.color_mode = 'RGB'
    color_ramp_006.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_006.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_006.color_ramp.elements) > 2:
        color_ramp_006.color_ramp.elements.remove(color_ramp_006.color_ramp.elements[-1])
    while len(color_ramp_006.color_ramp.elements) < 2:
        color_ramp_006.color_ramp.elements.new(0.5)
    color_ramp_006.color_ramp.elements[0].position = 0.20241709053516388
    color_ramp_006.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_006.color_ramp.elements[1].position = 0.6555889844894409
    color_ramp_006.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_006
    color_ramp_006.location = (845.5, -115.1)
    label_node(color_ramp_006, "", frame_005)
    group_006 = nodes.new("ShaderNodeGroup")
    group_006.location = (563.9, -115.1)
    label_node(group_006, "", frame_005)
    group_006.xl_c4d_gradient_type = '0'
    group_006.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_006.node_tree = pf_grunge_22b_r()
    group_010 = nodes.new("ShaderNodeGroup")
    group_010.location = (742.7, -290.7)
    label_node(group_010, "", frame_003)
    group_010.xl_c4d_gradient_type = '0'
    group_010.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_010.node_tree = edge()
    group_010.inputs[2].default_value = 5.0
    color_ramp_008 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_008 | Color Ramp.008
    color_ramp_008.color_ramp.color_mode = 'RGB'
    color_ramp_008.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_008.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_008.color_ramp.elements) > 2:
        color_ramp_008.color_ramp.elements.remove(color_ramp_008.color_ramp.elements[-1])
    while len(color_ramp_008.color_ramp.elements) < 2:
        color_ramp_008.color_ramp.elements.new(0.5)
    color_ramp_008.color_ramp.elements[0].position = 0.5110411047935486
    color_ramp_008.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp_008.color_ramp.elements[1].position = 0.5861438512802124
    color_ramp_008.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_008
    color_ramp_008.location = (445.7, -455.7)
    label_node(color_ramp_008, "", frame_003)
    group_008 = nodes.new("ShaderNodeGroup")
    group_008.location = (243.2, -555.5)
    label_node(group_008, "", frame_003)
    group_008.xl_c4d_gradient_type = '0'
    group_008.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_008.node_tree = pf_grunge_20_r()
    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.location = (2347.3, -183.6)
    bump_001.invert = True
    bump_001.inputs[1].default_value = 0.009999999776482582
    bump_001.inputs[2].default_value = 0.10000000149011612
    dirt = nodes.new("ShaderNodeMix")
    dirt.location = (484.9, 32.6)
    label_node(dirt, "脏污: 基于AO的凹腔和表面脏污效果遮罩")
    dirt.data_type = 'RGBA'
    dirt.factor_mode = 'UNIFORM'
    dirt.blend_type = 'MIX'
    dirt.clamp_factor = True
    dirt.clamp_result = False
    dirt.inputs[1].default_value = (0.5000, 0.5000, 0.5000)
    dirt.inputs[4].default_value = (0.0000, 0.0000, 0.0000)
    dirt.inputs[5].default_value = (0.0000, 0.0000, 0.0000)
    dirt.inputs[7].default_value = (0.0361, 0.0314, 0.0278, 1.0000)
    dirt.inputs[8].default_value = (0.0000, 0.0000, 0.0000)
    dirt.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    color_ramp_005 = nodes.new("ShaderNodeValToRGB")
    # XL_PF_RAMP_BEGIN color_ramp_005 | Color Ramp.005
    color_ramp_005.color_ramp.color_mode = 'RGB'
    color_ramp_005.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_005.color_ramp.interpolation = 'LINEAR'
    while len(color_ramp_005.color_ramp.elements) > 2:
        color_ramp_005.color_ramp.elements.remove(color_ramp_005.color_ramp.elements[-1])
    while len(color_ramp_005.color_ramp.elements) < 2:
        color_ramp_005.color_ramp.elements.new(0.5)
    color_ramp_005.color_ramp.elements[0].position = 0.37105220556259155
    color_ramp_005.color_ramp.elements[0].color = (0.0052530644461512566, 0.0052530644461512566, 0.0052530644461512566, 1.0)
    color_ramp_005.color_ramp.elements[1].position = 0.8217524290084839
    color_ramp_005.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    # XL_PF_RAMP_END color_ramp_005
    color_ramp_005.location = (931.9, -102.2)
    label_node(color_ramp_005, "", frame_002)
    group_011 = nodes.new("ShaderNodeGroup")
    group_011.location = (272.9, -102.2)
    label_node(group_011, "", frame_002)
    group_011.xl_c4d_gradient_type = '0'
    group_011.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    group_011.node_tree = pf_grunge_17c_r()
    reroute = nodes.new("NodeReroute")
    reroute.location = (1649.0, -1415.6)
    reroute.socket_idname = 'NodeSocketVector'
    reroute_001 = nodes.new("NodeReroute")
    reroute_001.location = (1111.0, 673.5)
    reroute_001.socket_idname = 'NodeSocketFloat'
    reroute_002 = nodes.new("NodeReroute")
    reroute_002.location = (2916.9, 39.5)
    reroute_002.socket_idname = 'NodeSocketFloat'
    reroute_003 = nodes.new("NodeReroute")
    reroute_003.location = (2270.6, 674.0)
    reroute_003.socket_idname = 'NodeSocketFloat'
    reroute_004 = nodes.new("NodeReroute")
    reroute_004.location = (1126.2, -42.3)
    reroute_004.socket_idname = 'NodeSocketColor'
    reroute_005 = nodes.new("NodeReroute")
    reroute_005.location = (1819.1, -104.1)
    reroute_005.socket_idname = 'NodeSocketVector'
    reroute_007 = nodes.new("NodeReroute")
    reroute_007.location = (-581.8, 315.8)
    reroute_007.socket_idname = 'NodeSocketFloat'
    reroute_008 = nodes.new("NodeReroute")
    reroute_008.location = (-581.8, 949.7)
    reroute_008.socket_idname = 'NodeSocketColor'
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.location = (29.7, -102.2)
    label_node(map_range, "", frame_002)
    map_range.clamp = True
    map_range.interpolation_type = 'LINEAR'
    map_range.data_type = 'FLOAT'
    map_range.inputs[2].default_value = 100.0
    map_range.inputs[3].default_value = 0.03999999910593033
    map_range.inputs[4].default_value = 0.5
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.location = (29.7, -355.5)
    label_node(map_range_001, "", frame_001)
    map_range_001.clamp = True
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.data_type = 'FLOAT'
    map_range_001.inputs[2].default_value = 100.0
    map_range_001.inputs[3].default_value = 0.009999999776482582
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_001.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_001.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.location = (29.7, -345.1)
    label_node(map_range_002, "", frame)
    map_range_002.clamp = True
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.data_type = 'FLOAT'
    map_range_002.inputs[2].default_value = 100.0
    map_range_002.inputs[3].default_value = 0.009999999776482582
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_002.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_002.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.location = (29.7, -359.3)
    label_node(map_range_003, "", frame_003)
    map_range_003.clamp = True
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.data_type = 'FLOAT'
    map_range_003.inputs[2].default_value = 100.0
    map_range_003.inputs[3].default_value = 0.019999999552965164
    map_range_003.inputs[4].default_value = 0.5
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_003.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_003.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.location = (35.1, -101.7)
    label_node(map_range_004, "", frame_003)
    map_range_004.clamp = True
    map_range_004.interpolation_type = 'LINEAR'
    map_range_004.data_type = 'FLOAT'
    map_range_004.inputs[2].default_value = 100.0
    map_range_004.inputs[3].default_value = 0.009999999776482582
    map_range_004.inputs[4].default_value = 0.20000000298023224
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_004.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_004.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    math = nodes.new("ShaderNodeMath")
    math.location = (951.6, -309.9)
    label_node(math, "", frame_004)
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[2].default_value = 0.5
    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.location = (297.5, -102.0)
    label_node(map_range_005, "", frame_005)
    map_range_005.clamp = True
    map_range_005.interpolation_type = 'LINEAR'
    map_range_005.data_type = 'FLOAT'
    map_range_005.inputs[2].default_value = 100.0
    map_range_005.inputs[3].default_value = 0.03999999910593033
    map_range_005.inputs[4].default_value = 0.800000011920929
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_005.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_005.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.location = (727.5, -102.4)
    label_node(map_range_006, "", frame_001)
    map_range_006.clamp = True
    map_range_006.interpolation_type = 'LINEAR'
    map_range_006.data_type = 'FLOAT'
    map_range_006.inputs[2].default_value = 100.0
    map_range_006.inputs[3].default_value = 0.009999999776482582
    map_range_006.inputs[4].default_value = 0.20000001788139343
    map_range_006.inputs[5].default_value = 4.0
    map_range_006.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_006.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_006.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.location = (863.8, -102.3)
    label_node(map_range_007, "", frame)
    map_range_007.clamp = True
    map_range_007.interpolation_type = 'LINEAR'
    map_range_007.data_type = 'FLOAT'
    map_range_007.inputs[2].default_value = 100.0
    map_range_007.inputs[3].default_value = 0.009999999776482582
    map_range_007.inputs[4].default_value = 0.6000000238418579
    map_range_007.inputs[5].default_value = 4.0
    map_range_007.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_007.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_007.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_010 = nodes.new("NodeReroute")
    reroute_010.location = (75.0, -233.2)
    label_node(reroute_010, "", frame)
    reroute_010.socket_idname = 'NodeSocketFloatPercentage'
    reroute_006 = nodes.new("NodeReroute")
    reroute_006.location = (-2168.9, 540.0)
    reroute_006.socket_idname = 'NodeSocketFloatPercentage'
    reroute_011 = nodes.new("NodeReroute")
    reroute_011.location = (-2168.9, 850.7)
    reroute_011.socket_idname = 'NodeSocketFloatPercentage'
    reroute_012 = nodes.new("NodeReroute")
    reroute_012.location = (-2168.9, 216.3)
    reroute_012.socket_idname = 'NodeSocketFloatPercentage'
    reroute_009 = nodes.new("NodeReroute")
    reroute_009.location = (2046.9, 673.8)
    reroute_009.socket_idname = 'NodeSocketFloat'
    map_range_008 = nodes.new("ShaderNodeMapRange")
    map_range_008.location = (272.6, -264.0)
    label_node(map_range_008, "", frame_004)
    map_range_008.clamp = True
    map_range_008.interpolation_type = 'LINEAR'
    map_range_008.data_type = 'FLOAT'
    map_range_008.inputs[2].default_value = 100.0
    map_range_008.inputs[3].default_value = 0.25
    map_range_008.inputs[4].default_value = 1.2400000095367432
    map_range_008.inputs[5].default_value = 4.0
    map_range_008.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_008.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_008.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    reroute_013 = nodes.new("NodeReroute")
    reroute_013.location = (896.3, -1021.2)
    reroute_013.socket_idname = 'NodeSocketVector'
    map_range_010 = nodes.new("ShaderNodeMapRange")
    map_range_010.location = (277.9, -546.3)
    label_node(map_range_010, "", frame_004)
    map_range_010.clamp = True
    map_range_010.interpolation_type = 'LINEAR'
    map_range_010.data_type = 'FLOAT'
    map_range_010.inputs[2].default_value = 100.0
    map_range_010.inputs[3].default_value = 0.0010000000474974513
    map_range_010.inputs[4].default_value = 0.019999999552965164
    map_range_010.inputs[5].default_value = 4.0
    map_range_010.inputs[6].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[7].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[8].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[9].default_value = (0.0000, 0.0000, 0.0000)
    map_range_010.inputs[10].default_value = (1.0000, 1.0000, 1.0000)
    map_range_010.inputs[11].default_value = (4.0000, 4.0000, 4.0000)
    hs_bump_control = nodes.new("ShaderNodeGroup")
    hs_bump_control.location = (750.6, -101.8)
    label_node(hs_bump_control, "", frame_004)
    hs_bump_control.xl_c4d_gradient_type = '0'
    hs_bump_control.xl_rgbspectrum_preset = '1.0,1.0,1.0,1.0'
    hs_bump_control.node_tree = _hs_bump_control_fn()
    hs_bump_control.inputs[2].default_value = 0.4000000059604645
    reroute_014 = nodes.new("NodeReroute")
    reroute_014.location = (1031.3, -135.6)
    label_node(reroute_014, "", frame_004)
    reroute_014.socket_idname = 'NodeSocketFloat'
    reroute_015 = nodes.new("NodeReroute")
    reroute_015.location = (1779.8, -855.8)
    reroute_015.socket_idname = 'NodeSocketFloat'

    # === 节点连接 ===
    links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[1])
    links.new(principled_bsdf_002.outputs[0], mix_shader.inputs[2])
    links.new(reroute_004.outputs[0], principled_bsdf_001.inputs[2])
    links.new(edges.outputs[2], cavity.inputs[6])
    links.new(reroute.outputs[0], bump_001.inputs[4])
    links.new(reroute_008.outputs[0], dirt.inputs[0])
    links.new(group_011.outputs[0], color_ramp_005.inputs[0])
    links.new(cavity.outputs[2], dirt.inputs[6])
    links.new(group_006.outputs[0], color_ramp_006.inputs[0])
    links.new(color_ramp_008.outputs[0], group_010.inputs[1])
    links.new(map_range_005.outputs[0], group_006.inputs[0])
    links.new(group_008.outputs[0], color_ramp_008.inputs[0])
    links.new(bump_001.outputs[0], principled_bsdf_002.inputs[5])
    links.new(group_003.outputs[0], color_ramp_001.inputs[0])
    links.new(group_005.outputs[0], color_ramp_003.inputs[0])
    links.new(reroute_007.outputs[0], cavity.inputs[0])
    links.new(bevel.outputs[0], bump.inputs[4])
    links.new(color_ramp_001.outputs[0], group_002.inputs[1])
    links.new(group_009.outputs[0], edges.inputs[0])
    links.new(dirt.outputs[2], principled_bsdf_001.inputs[0])
    links.new(reroute_005.outputs[0], principled_bsdf_001.inputs[5])
    links.new(group_004.outputs[0], color_ramp_002.inputs[0])
    links.new(math.outputs[0], bump.inputs[3])
    links.new(reroute_002.outputs[0], mix_shader.inputs[0])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(bevel.outputs[0], reroute.inputs[0])
    links.new(group_010.outputs[0], reroute_001.inputs[0])
    links.new(reroute_003.outputs[0], reroute_002.inputs[0])
    links.new(reroute_009.outputs[0], reroute_003.inputs[0])
    links.new(color_ramp_006.outputs[0], reroute_004.inputs[0])
    links.new(reroute_013.outputs[0], reroute_005.inputs[0])
    links.new(group_002.outputs[0], reroute_007.inputs[0])
    links.new(color_ramp_005.outputs[0], reroute_008.inputs[0])
    links.new(map_range.outputs[0], group_011.inputs[0])
    links.new(map_range_002.outputs[0], group_004.inputs[0])
    links.new(map_range_003.outputs[0], group_008.inputs[0])
    links.new(map_range_004.outputs[0], group_010.inputs[0])
    links.new(color_ramp_003.outputs[0], math.inputs[0])
    links.new(reroute_011.outputs[0], map_range.inputs[0])
    links.new(reroute_012.outputs[0], map_range_001.inputs[0])
    links.new(input_node.outputs[8], map_range_002.inputs[0])
    links.new(input_node.outputs[9], map_range_003.inputs[0])
    links.new(input_node.outputs[9], map_range_004.inputs[0])
    links.new(input_node.outputs[3], math.inputs[1])
    links.new(input_node.outputs[0], map_range_005.inputs[0])
    links.new(map_range_001.outputs[0], group_003.inputs[0])
    links.new(input_node.outputs[7], map_range_006.inputs[0])
    links.new(map_range_006.outputs[0], group_002.inputs[0])
    links.new(color_ramp_002.outputs[0], group_009.inputs[1])
    links.new(reroute_010.outputs[0], map_range_007.inputs[0])
    links.new(input_node.outputs[8], reroute_010.inputs[0])
    links.new(input_node.outputs[6], reroute_006.inputs[0])
    links.new(reroute_006.outputs[0], reroute_011.inputs[0])
    links.new(reroute_006.outputs[0], reroute_012.inputs[0])
    links.new(map_range_007.outputs[0], group_009.inputs[0])
    links.new(input_node.outputs[1], edges.inputs[6])
    links.new(reroute_001.outputs[0], reroute_009.inputs[0])
    links.new(reroute_009.outputs[0], bump_001.inputs[3])
    links.new(input_node.outputs[4], map_range_008.inputs[0])
    links.new(map_range_008.outputs[0], group_005.inputs[0])
    links.new(bump.outputs[0], reroute_013.inputs[0])
    links.new(input_node.outputs[2], map_range_010.inputs[0])
    links.new(map_range_010.outputs[0], bevel.inputs[0])
    links.new(reroute_014.outputs[0], bump.inputs[0])
    links.new(hs_bump_control.outputs[0], reroute_014.inputs[0])
    links.new(input_node.outputs[3], hs_bump_control.inputs[0])
    links.new(input_node.outputs[5], hs_bump_control.inputs[1])
    links.new(reroute_015.outputs[0], bump_001.inputs[0])
    links.new(reroute_014.outputs[0], reroute_015.inputs[0])

    return group