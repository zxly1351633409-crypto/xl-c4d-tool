"""XL 物理天空核心。

PSA 节点组作为第三方 GPL 核心资产保留；本文件只负责中文包装、预设映射与独立控制。
"""

from __future__ import annotations

import json
import math
import os

import bpy
from mathutils import Euler, Vector


STARLIGHT_ATMOSPHERE = "PSA_StarlightAtmosphere"
PHYSICAL_CLOUDS = ". PSA_PhysicalClouds"
PHYSICAL_STARS = ". PSA_PhysicalStars"
PHYSICAL_INPUTS = ". PSA_PhysicalInputs"
PHYSICAL_COORDINATES = ". PSA_PhysicalCoordinates"
PHYSICAL_PLANET_DATA = ". PSA_PhysicalPlanetData"
ACES_CONVERTER = ". PSA_sRGBtoAP1"

PSA_GROUPS = (
    STARLIGHT_ATMOSPHERE,
    PHYSICAL_COORDINATES,
    PHYSICAL_PLANET_DATA,
    PHYSICAL_CLOUDS,
    PHYSICAL_STARS,
    PHYSICAL_INPUTS,
    ACES_CONVERTER,
)

GROUP_LABELS = {
    STARLIGHT_ATMOSPHERE: "PSA 大气天空核心",
    PHYSICAL_COORDINATES: "PSA 太阳/星空坐标",
    PHYSICAL_PLANET_DATA: "PSA 行星与地平线",
    PHYSICAL_CLOUDS: "PSA 物理云",
    PHYSICAL_STARS: "PSA 星空",
    PHYSICAL_INPUTS: "PSA 物理输入",
    ACES_CONVERTER: "PSA ACES 转换",
}

XL_SUN_NAME = "XL_物理天空日光"
XL_LEGACY_SUN_NAME = "XL_物理天空太阳"
XL_SUN_TARGET_NAME = "XL_物理天空太阳目标"
XL_SUN_CONSTRAINT = "XL_指向天空目标"
XL_NODE_PREFIX = "XL_物理天空_"

CLOUD_LINKS = (
    ("Result", "in_clouds"),
    ("Scattering", "in_cloud_scatter"),
    ("Val1", "val1"),
    ("Val2", "val2"),
    ("Normal", "Normal"),
    ("Intensity", "intensity"),
)

CLOUD_DISABLED_DEFAULTS = {
    "in_clouds": 0.0,
    "in_cloud_scatter": (0.0, 0.0, 0.0, 1.0),
    "val1": 0.0,
    "val2": 0.0,
    "Normal": (0.0, 0.0, 1.0),
    "intensity": 0.0,
}

OLD_BACKGROUND_NODES = (
    XL_NODE_PREFIX + "屏幕坐标",
    XL_NODE_PREFIX + "天空渐变",
    XL_NODE_PREFIX + "渐变颜色",
    XL_NODE_PREFIX + "物理层混合",
)

CAMERA_BACKGROUND_NODES = (
    XL_NODE_PREFIX + "画面坐标",
    XL_NODE_PREFIX + "画面渐变",
    XL_NODE_PREFIX + "画面背景颜色",
    XL_NODE_PREFIX + "云光保留混合",
)

OBSOLETE_BACKGROUND_NODES = OLD_BACKGROUND_NODES + CAMERA_BACKGROUND_NODES

GRADIENT_BACKGROUND_NODES = (
    XL_NODE_PREFIX + "渐变窗口坐标",
    XL_NODE_PREFIX + "渐变垂直坐标",
    XL_NODE_PREFIX + "画面背景色带",
    XL_NODE_PREFIX + "轻量云噪声",
    XL_NODE_PREFIX + "轻量云遮罩",
    XL_NODE_PREFIX + "轻量云颜色",
    XL_NODE_PREFIX + "轻量云混合",
)

HEAVY_BACKGROUND_MASK_NODES = (
    XL_NODE_PREFIX + "渐变保留太阳云",
    XL_NODE_PREFIX + "PSA亮度",
    XL_NODE_PREFIX + "太阳亮度阈值",
    XL_NODE_PREFIX + "太阳亮度蒙版",
    XL_NODE_PREFIX + "云蒙版强度",
    XL_NODE_PREFIX + "太阳云蒙版合并",
)

INPUT_NODE_MAP = {
    "sun_diameter": "sun_diameter",
    "binary_diameter": "binary_sun_diameter",
    "binary_phase": "binary_phase",
    "binary_distance": "binary_distance",
    "sun_intensity": "sun_intensity",
    "binary_intensity": "binary_sun_intensity",
    "sun_lamp": "sun_lamp",
    "sun_disk": "sun_disk",
    "enable_binary_sun": "enable_binary_sun",
    "night_intensity": "night_radiance",
    "atmosphere_height": "atmosphere_height",
    "atmosphere_density": "atmosphere_density",
    "atmosphere_intensity": "atmosphere_intensity",
    "atmosphere_color": "atmosphere_color",
    "atmosphere_inscattering": "atmosphere_inscattering",
    "atmosphere_extinction": "atmosphere_extinction",
    "atmosphere_mie": "atmosphere_mie",
    "atmosphere_mie_dir": "atmosphere_mie_dir",
    "atmosphere_distance": "atmosphere_distance",
    "atmosphere_falloff": "atmosphere_falloff",
    "ground_visible": "ground_visible",
    "ground_albedo": "ground_albedo",
    "ground_offset": "ground_offset",
    "horizon_offset": "horizon_offset",
    "stars_intensity": "stars_radiance_intensity",
    "stars_gamma": "stars_radiance_gamma",
    "stars_seed": "stars_seed_value",
    "stars_amount": "stars_amount",
    "stars_scale": "stars_scale",
    "stars_temperature_min": "stars_temp_min",
    "stars_temperature_max": "stars_temp_max",
}

CLOUD_INPUT_MAP = {
    "clouds_scale": "Scale",
    "clouds_min": "Min",
    "clouds_max": "Max",
    "clouds_thickness": "Thickness",
    "clouds_scattering": "Scattering",
    "clouds_amount": "Val1",
    "clouds_power": "Val2",
    "clouds_lighting_intensity": "Intensity",
    "clouds_location": "Location",
    "clouds_rotation": "Rotation",
    "clouds_detail": "Detail",
    "clouds_dimension": "Dimension",
    "clouds_lacunarity": "Lacunarity",
}

SOCKET_TRANSLATIONS = {
    "out_world": "最终天空",
    "in_world": "画面底色输入",
    "in_material": "材质输入",
    "out_material": "材质输出",
    "in_clouds": "云遮罩输入",
    "in_cloud_scatter": "云散射输入",
    "in_stars": "星空输入",
    "SunVec": "太阳向量",
    "SunCosTheta": "太阳夹角",
    "StarCoordinates": "星空坐标",
    "PlanetShadow": "行星阴影",
    "PlanetHorizon": "行星地平线",
    "AboveBelow": "上下遮罩",
    "CloudCoordinates": "云坐标",
    "Result": "结果",
    "Scattering": "散射",
    "Val1": "云自阴影",
    "Val2": "云方向性",
    "Normal": "法线",
    "Intensity": "受光强度",
    "Vector": "向量",
    "Scale": "缩放",
    "Min": "最小阈值",
    "Max": "最大阈值",
    "Thickness": "厚度",
    "Location": "位置",
    "Rotation": "旋转",
    "Detail": "细节",
    "Dimension": "维度",
    "Lacunarity": "细节层级",
    "SunAngularDiameter": "太阳角直径",
    "SunColor": "太阳颜色",
    "SunColor*FogColor": "太阳雾色",
    "SunIntensity*sterid": "太阳辐射强度",
    "BinaryDistance": "双星距离",
    "BinaryPhase": "双星相位",
    "BinarySunDiameter": "双星角直径",
    "BinaryIntensity*Steridian": "双星辐射强度",
    "BinarySunColor": "双星颜色",
    "atmosphere_density": "大气密度",
    "ScaleHeight": "大气高度",
    "atmosphere_intensity": "大气强度",
    "NightRadiance": "夜空亮度",
    "AtmosphereInscattering": "天顶散射色",
    "AtmosphererExtinction": "地平吸收色",
    "atmosphere_mie": "霞光散射",
    "atmosphere_mie_dir": "霞光方向性",
    "StarsRadianceIntensity": "星空强度",
    "StarsRadianceGamma": "星空伽马",
    "StarsSeedValue": "星空种子",
    "StarsAmount": "星星数量",
    "StarsScale": "星图尺度",
    "StarsTempMin": "星温最小值",
    "StarsTempMax": "星温最大值",
    "GroundVisible": "地面可见",
    "GroundColor": "地面颜色",
    "GroundPlaneOffset": "地平面偏移",
    "DistanceScalar": "距离倍率",
    "FogFalloff": "雾衰减",
    "HorizonOffset": "地平线偏移",
    "SunLight": "太阳受光色",
    "SunLightUpper": "高空太阳受光色",
    "Intensity_Multiplier": "强度倍率",
    "Value": "值",
    "Image": "图像",
    "Mie": "米氏散射",
    "CosTheta": "夹角余弦",
    "cosTheta": "夹角余弦",
    "Margin": "边距",
    "cos_theta": "夹角余弦",
    "Angle": "角度",
    "pos": "位置",
    "dir": "方向",
    "fog": "雾量",
    "viewer": "视线距离",
    "density": "密度",
    "scaleHeight": "高度尺度",
    "groundOffset": "地面偏移",
    "horizonOffset": "地平线偏移",
    "plane_pos": "平面位置",
    "view_distance": "视距",
    "ground": "地面遮罩",
    "groundVisible": "地面可见",
    "Fog Color": "雾颜色",
    "Fog Amount": "雾量",
    "Input": "输入颜色",
    "Extinction Color": "吸收颜色",
    "Inscattering Color": "散射颜色",
    "distance": "距离",
    "intensity": "强度",
    "OutputShaderFog": "雾材质输出",
    "InputShader": "材质输入",
    "Strength": "强度",
    "Val": "值",
    "minVal": "最小值",
    "maxVal": "最大值",
    "clouds": "云层颜色",
    "Color": "颜色",
    "mask": "遮罩",
    "INDIRECT": "间接光",
    "RGB": "颜色RGB",
    "Alpha": "透明度",
    "val1": "云自阴影",
    "val2": "云方向性",
    "View": "视线",
    "Light": "光线",
    "direct": "直射光",
    "indirect": "间接光",
    "fog_color": "雾颜色",
    "earth_shadow": "地影",
    "above_below": "上下遮罩",
    "sphere_direction": "球体方向",
    "light_direction": "光线方向",
    "sphere_radius": "球体半径",
    "sphere_distance": "球体距离",
    "light_distance": "光源距离",
    "Base": "底数",
    "Fac": "系数",
    "Object": "物体向量",
    "infinity": "无限距离",
    "planet_radius": "行星半径",
    "planet_pos": "行星位置",
    "offset": "偏移",
    "position": "位置",
    "camera_vec": "相机向量",
    "camera_distance": "相机距离",
    "ground/sky": "地面天空遮罩",
    "planeDepth": "平面深度",
    "mie": "米氏散射",
    "shadow": "阴影",
    "mieDirG": "米氏方向",
    "rayleigh": "瑞利散射",
    "near": "近点",
    "far": "远点",
    "distance_from_surface": "距表面距离",
    "horizon": "地平线",
    "Plane": "平面",
    "LineP": "线位置",
    "LineN": "线方向",
    "PlaneN": "平面法线",
    "PlaneD": "平面距离",
    "val": "值",
    "edge0": "边界0",
    "edge1": "边界1",
    "sphere_vec": "球体向量",
    "light_color": "光颜色",
    "light_vec": "光向量",
    "light_radius": "光半径",
    "terminator": "明暗边界",
    "angular diameter degrees": "角直径度数",
    "ul": "边缘暗化U",
    "vl": "边缘暗化V",
    "alpha": "透明度",
}

GROUP_NAME_LABELS = {
    ". PSA_B": "PSA 方程B",
    ". PSA_C": "PSA 方程C",
    ". PSA_D": "PSA 方程D",
    ". PSA_NumericMie": "PSA 数值米氏散射",
    ". PSA_PreventZero": "PSA 防零保护",
    ". PSA_PreventZero.001": "PSA 防零保护",
    ". PSA_binary_star_position": "PSA 双星位置",
    ". PSA_calculate_fog_noground": "PSA 无地面雾计算",
    ". PSA_calculate_fog_noground.001": "PSA 无地面雾计算",
    ". PSA_calculate_fog_ob": "PSA 物体雾计算",
    ". PSA_calculate_fog_world": "PSA 世界雾计算",
    ". PSA_calculate_scattering": "PSA 散射计算",
    ". PSA_calculate_scattering.001": "PSA 散射计算",
    ". PSA_calculate_scattering_object": "PSA 物体散射计算",
    ". PSA_clamp": "PSA 钳制",
    ". PSA_clamp()": "PSA 钳制",
    ". PSA_clouds_lighting": "PSA 云层光照",
    ". PSA_cubify": "PSA 立方化坐标",
    ". PSA_d": "PSA 半影距离",
    ". PSA_exp()": "PSA 指数",
    ". PSA_exp().001": "PSA 指数",
    ". PSA_exp2()": "PSA 二次指数",
    ". PSA_fbm": "PSA 分形噪声",
    ". PSA_flat_world": "PSA 平面世界",
    ". PSA_get_planet": "PSA 行星数据",
    ". PSA_intersect_plane": "PSA 平面相交",
    ". PSA_mie_scattering": "PSA 米氏散射",
    ". PSA_near_far": "PSA 近远点",
    ". PSA_phase_rayleigh": "PSA 瑞利相位",
    ". PSA_phase_rayleigh.001": "PSA 瑞利相位",
    ". PSA_planet_intersect": "PSA 行星相交",
    ". PSA_ray_plane_intersection": "PSA 射线平面相交",
    ". PSA_smoothstep": "PSA 平滑阶跃",
    ". PSA_smoothstep()": "PSA 平滑阶跃",
    ". PSA_sphere_penumbra": "PSA 球体半影",
    ". PSA_sun_limb_darkening_radiance": "PSA 太阳边缘暗化",
    ". PSA_xyz_to_cube_coords": "PSA 立方体坐标",
    "PSA_StarlightAtmosphereMaterial": "PSA 大气材质核心",
}

ANNOTATION_LABELS = {
    PHYSICAL_INPUTS: {
        "Atmosphere": "大气参数 - Frame: 天空底色/散射/吸收",
        "Sun": "太阳参数 - Frame: 太阳盘/太阳辐射",
        "Binary Sun": "双星参数 - Frame: 第二太阳预留",
        "Ground": "地面参数 - Frame: 地平线与反照色",
        "Stars.001": "星空参数 - Frame: 星图亮度/数量",
        "atmosphere_color": "天空背景 - RGB: PSA 大气底色",
        "atmosphere_inscattering": "天顶散射 - RGB: 蓝天散射色",
        "atmosphere_extinction": "地平吸收 - RGB: 霞光/雾吸收",
        "atmosphere_density": "大气密度 - Value: 雾与天空厚度",
        "atmosphere_height": "大气高度 - Value: 散射层高度",
        "atmosphere_intensity": "大气强度 - Value: 天空整体亮度",
        "atmosphere_mie": "霞光散射 - Value: 近太阳雾光",
        "atmosphere_mie_dir": "霞光方向 - Value: 前向散射",
        "night_radiance": "夜空亮度 - Value: 夜间背景",
        "sun_diameter": "太阳盘 - Value: 视觉角直径",
        "sun_intensity": "太阳天空强度 - Value: 核心辐射",
        "sun_color": "太阳颜色 - RGB: 色温结果",
        "sun_light": "太阳下光 - RGB: 云/大气受光",
        "sun_light_upper": "太阳上光 - RGB: 高空受光",
        "ground_albedo": "地面反照 - RGB: 地平线底色",
        "ground_offset": "地平面偏移 - Value: 地面高度",
        "horizon_offset": "地平线偏移 - Value: 天际线位置",
    },
    PHYSICAL_COORDINATES: {
        "vec": "太阳方向Z - Mapping: 旋转天空坐标",
        "vec1": "太阳方向Y - Mapping: 旋转天空坐标",
        "vec2": "太阳方向X - Mapping: 旋转天空坐标",
        "Combine XYZ": "太阳向量 - CombineXYZ: 合成 SunVec",
        "Vector Math": "太阳夹角X - VectorMath: 点积",
        "Vector Math.001": "太阳夹角Y - VectorMath: 点积",
        "Vector Math.002": "太阳夹角Z - VectorMath: 点积",
        "Group Output": "坐标输出 - GroupOutput: 太阳/星空",
    },
    PHYSICAL_CLOUDS: {
        "Group Input": "云输入 - GroupInput: 疏密/大小/细节",
        "Mapping": "云坐标 - Mapping: 云层位置旋转",
        "Map Range": "云疏密 - MapRange: Min/Max 阈值",
        "PSA_fbm": "云噪声A - Group: 大形体",
        "PSA_fbm.001": "云噪声B - Group: 次级形体",
        "PSA_fbm.002": "云噪声C - Group: 细节扰动",
        "PSA_fbm.003": "云噪声D - Group: 云遮罩",
        "Group Output": "云输出 - GroupOutput: 遮罩/散射/法线",
    },
    STARLIGHT_ATMOSPHERE: {
        "Data Input": "核心输入 - Frame: PSA 物理参数入口",
        "Sun Disks": "太阳盘 - Frame: 日轮与边缘变暗",
        "Optical Depth World": "光学深度 - Frame: 大气路径厚度",
        "Frame": "瑞利相位 - Frame: 蓝天散射",
        "Frame.002": "天空背景 - Frame: 世界底色与天空",
        "Ground Radiance": "地面辐射 - Frame: 地平反照",
        "Direct Light": "直射光 - Frame: 太阳直射",
        "indirect": "间接光 - Frame: 天空反弹光",
        "Frame.005": "米氏相位 - Frame: 霞光/雾光",
        "Everything without atmosphere": "无大气层 - Frame: 星/地面底层",
        "mix stars with stars": "星空混合 - Frame: 夜空星光",
        "mix stars with ground": "地面星空混合 - Frame: 地平线遮挡",
        "Frame.001": "云混合 - Frame: 云遮罩和受光",
        "Frame.004": "视线向量 - Frame: 相机方向",
        "Group Input": "核心输入 - GroupInput: 云/太阳/行星",
        "Group Input.002": "核心输入 - GroupInput: 云/太阳/行星",
        "Group Output": "核心输出 - GroupOutput: 最终天空颜色",
        "PSA_clouds_lighting": "云受光 - Group: 云光照与阴影",
        "PSA_caclulate_fog_world": "天空雾 - Group: 大气可见度",
    },
}

NOTE_FRAMES = {
    PHYSICAL_INPUTS: (
        (
            "XL_注释_天空颜色",
            "天空背景控制\natmosphere_color = 背景底色\natmosphere_inscattering = 天顶散射\natmosphere_extinction = 地平吸收",
            (-1050, 440),
        ),
    ),
    STARLIGHT_ATMOSPHERE: (
        (
            "XL_注释_天空核心",
            "PSA 大气天空核心\nSunVec/SunCosTheta 来自日光对象\nin_clouds 控制云遮罩\nout_world 输出相机可见天空",
            (-1250, 720),
        ),
    ),
    PHYSICAL_CLOUDS: (
        (
            "XL_注释_云控制",
            "云控制\nMin/Max 控制疏密\nScale 控制云块大小\nDetail/Dimension 控制细节形状",
            (-900, 420),
        ),
    ),
    PHYSICAL_COORDINATES: (
        (
            "XL_注释_太阳控制",
            "太阳方向\n三个 Mapping 共用日光对象旋转\n移动日光或目标空物体即可更新天空太阳",
            (-620, 300),
        ),
    ),
}

_APPLYING = False


def addon_dir():
    return os.path.dirname(__file__)


def atmosphere_blend_path():
    return os.path.join(addon_dir(), "assets", "atmosphere.blend")


def presets_dir():
    return os.path.join(addon_dir(), "presets")


def list_presets():
    path = presets_dir()
    if not os.path.isdir(path):
        return []
    return sorted(
        os.path.splitext(name)[0]
        for name in os.listdir(path)
        if name.lower().endswith(".json")
    )


def preset_label(name):
    labels = {
        "earth": "地球",
        "earth2": "地球 2",
        "earth3": "地球 3",
        "hazy summer": "雾霾夏日",
        "mars": "火星",
        "nishita": "Nishita",
        "retrowave": "复古霓虹",
        "tatooine": "塔图因",
        "thick fog": "浓雾",
        "thick haze": "厚霾",
    }
    return labels.get(name, name)


def load_preset(name):
    path = os.path.join(presets_dir(), name + ".json")
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_world(context):
    world = context.scene.world
    if world is None:
        world = bpy.data.worlds.new("XL_物理天空")
        context.scene.world = world
    world.use_nodes = True
    return world


def append_group(group_name):
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    directory = atmosphere_blend_path() + "\\NodeTree\\"
    bpy.ops.wm.append(
        filepath=directory + group_name,
        directory=directory,
        filename=group_name,
        do_reuse_local_id=True,
    )
    return bpy.data.node_groups.get(group_name)


def _is_psa_group(group):
    return group.name.startswith("PSA") or group.name.startswith(". PSA")


def _localized_group_label(group_name):
    return GROUP_LABELS.get(group_name) or GROUP_NAME_LABELS.get(group_name) or group_name


def _socket_label(name):
    if not name:
        return name
    if name in SOCKET_TRANSLATIONS:
        return SOCKET_TRANSLATIONS[name]
    if any("\u4e00" <= char <= "\u9fff" for char in name):
        return name
    return "接口"


def _socket_aliases(name):
    aliases = [name]
    translated = SOCKET_TRANSLATIONS.get(name)
    if translated and translated not in aliases:
        aliases.append(translated)
    for original, chinese in SOCKET_TRANSLATIONS.items():
        if name == chinese and original not in aliases:
            aliases.append(original)
    return aliases


def _socket(sockets, name):
    for alias in _socket_aliases(name):
        socket = sockets.get(alias)
        if socket is not None:
            return socket
    return None


def _input(node, name):
    return _socket(node.inputs, name) if node is not None else None


def _output(node, name):
    return _socket(node.outputs, name) if node is not None else None


def _rgba_scaled(color, strength=1.0):
    return (
        float(color[0]) * strength,
        float(color[1]) * strength,
        float(color[2]) * strength,
        float(color[3]) if len(color) > 3 else 1.0,
    )


def localize_psa_interfaces():
    for group in bpy.data.node_groups:
        if not _is_psa_group(group):
            continue
        for item in group.interface.items_tree:
            if getattr(item, "item_type", None) != "SOCKET":
                continue
            old_name = item.name
            new_name = _socket_label(old_name)
            if new_name and new_name != old_name:
                item.name = new_name
            if hasattr(item, "description") and new_name:
                item.description = f"PSA 中文接口：{new_name}"
        try:
            group.interface_update(bpy.context)
        except Exception:
            pass


def annotate_psa_node_groups():
    localize_psa_interfaces()
    for group in bpy.data.node_groups:
        if not _is_psa_group(group):
            continue
        for node in group.nodes:
            if node.type == "GROUP" and getattr(node, "node_tree", None):
                node.label = _localized_group_label(node.node_tree.name)
            elif node.type == "GROUP_INPUT":
                node.label = "组输入 - GroupInput: 中文接口入口"
            elif node.type == "GROUP_OUTPUT":
                node.label = "组输出 - GroupOutput: 中文接口出口"
        for node_name, label in ANNOTATION_LABELS.get(group.name, {}).items():
            node = group.nodes.get(node_name)
            if node is not None:
                node.label = label
        for frame_name, frame_label, location in NOTE_FRAMES.get(group.name, ()):
            frame = group.nodes.get(frame_name)
            if frame is None:
                frame = group.nodes.new("NodeFrame")
                frame.name = frame_name
            frame.label = frame_label
            frame.location = location
            frame.width = 520
            frame.height = 220
            frame.use_custom_color = True
            frame.color = (0.08, 0.10, 0.14)


def ensure_group_node(node_tree, group_name, x, y):
    group = append_group(group_name)
    if group is None:
        raise RuntimeError(f"缺少 PSA 节点组: {group_name}")
    node = node_tree.nodes.get(group_name)
    if node is None:
        node = node_tree.nodes.new("ShaderNodeGroup")
        node.name = group_name
    node.label = _localized_group_label(group_name)
    node.node_tree = group
    node.location = (x, y)
    return node


def _first_output(world):
    node_tree = world.node_tree
    output = node_tree.get_output_node("ALL")
    if output is None:
        output = node_tree.nodes.new("ShaderNodeOutputWorld")
        output.name = "世界输出"
        output.location = (760, 0)
    return output


def _remove_links_to(socket):
    if socket is None:
        return
    for link in list(socket.links):
        socket.id_data.links.remove(link)


def _connect(node_tree, output_socket, input_socket, replace=True):
    if output_socket is None or input_socket is None:
        return
    if replace:
        _remove_links_to(input_socket)
    node_tree.links.new(output_socket, input_socket)


def _clear_socket_driver(socket):
    try:
        data_path = socket.path_from_id("default_value")
    except Exception:
        return
    owner = socket.id_data
    try:
        owner.driver_remove(data_path)
        return
    except Exception:
        pass
    for index in range(4):
        try:
            owner.driver_remove(data_path, index)
        except Exception:
            pass


def _set_socket_value(socket, value):
    if socket is None or not hasattr(socket, "default_value"):
        return
    _clear_socket_driver(socket)
    try:
        socket.default_value = value
    except TypeError:
        try:
            current = socket.default_value
            for index, item in enumerate(value):
                if index < len(current):
                    current[index] = item
        except Exception:
            pass


def _set_input_node(group_name, node_name, value):
    group = bpy.data.node_groups.get(group_name)
    if group is None:
        return
    node = group.nodes.get(node_name)
    if node is None or not node.outputs:
        return
    _set_socket_value(node.outputs[0], value)


def _blackbody_rgb(kelvin):
    t = max(1000.0, min(40000.0, kelvin)) / 100.0
    if t <= 66.0:
        r = 255.0
        g = 99.4708025861 * math.log(t) - 161.1195681661
        b = 0.0 if t <= 19.0 else 138.5177312231 * math.log(t - 10.0) - 305.0447927307
    else:
        r = 329.698727446 * ((t - 60.0) ** -0.1332047592)
        g = 288.1221695283 * ((t - 60.0) ** -0.0755148492)
        b = 255.0
    return tuple(max(0.0, min(1.0, channel / 255.0)) for channel in (r, g, b))


def _unique_name(base):
    if base not in bpy.data.objects:
        return base
    index = 1
    while f"{base}.{index:03d}" in bpy.data.objects:
        index += 1
    return f"{base}.{index:03d}"


def _valid_sun(obj):
    return obj is not None and obj.type == "LIGHT" and obj.data and obj.data.type == "SUN"


def _valid_empty(obj):
    return obj is not None and obj.type == "EMPTY"


def _initial_sun_location(settings, target):
    rotation = Euler((settings.sun_elevation, 0.0, settings.sun_azimuth), "XYZ")
    direction = rotation.to_matrix() @ Vector((0.0, 0.0, -1.0))
    if direction.length < 1e-6:
        direction = Vector((0.0, -1.0, 1.0))
    return target.location - direction.normalized() * 10.0


def _sun_direction_from_rotation(rotation):
    direction = rotation.to_matrix() @ Vector((0.0, 0.0, -1.0))
    if direction.length < 1e-6:
        return Vector((0.0, -1.0, 1.0)).normalized()
    return direction.normalized()


def _set_sun_location_from_rotation(sun, target, rotation, distance=10.0):
    direction = _sun_direction_from_rotation(rotation)
    sun.location = target.location - direction * distance


def ensure_sun_control(context, settings):
    target = settings.sun_target if _valid_empty(settings.sun_target) else bpy.data.objects.get(XL_SUN_TARGET_NAME)
    if target is None:
        target = bpy.data.objects.new(XL_SUN_TARGET_NAME, None)
        target.empty_display_type = "PLAIN_AXES"
        target.empty_display_size = 1.2
        target.location = (0.0, 0.0, 0.0)
        context.scene.collection.objects.link(target)
    target["xl_physical_atmosphere_target"] = True

    sun = settings.sun_object if _valid_sun(settings.sun_object) else bpy.data.objects.get(XL_SUN_NAME)
    legacy = bpy.data.objects.get(XL_LEGACY_SUN_NAME)
    if not _valid_sun(sun) and _valid_sun(legacy) and legacy.get("xl_physical_atmosphere_sun"):
        if XL_SUN_NAME not in bpy.data.objects:
            legacy.name = XL_SUN_NAME
        sun = legacy

    created = False
    if not _valid_sun(sun):
        light = bpy.data.lights.new(_unique_name(XL_SUN_NAME), "SUN")
        sun = bpy.data.objects.new(XL_SUN_NAME, light)
        context.scene.collection.objects.link(sun)
        created = True
    if created:
        _set_sun_location_from_rotation(
            sun,
            target,
            Euler((settings.sun_elevation, 0.0, settings.sun_azimuth), "XYZ"),
        )
    sun["xl_physical_atmosphere_sun"] = True

    if settings.sun_target != target:
        settings.sun_target = target
    if settings.sun_object != sun:
        settings.sun_object = sun

    constraint = sun.constraints.get(XL_SUN_CONSTRAINT)
    if constraint is None or constraint.type != "TRACK_TO":
        constraint = sun.constraints.new("TRACK_TO")
        constraint.name = XL_SUN_CONSTRAINT
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"

    sun.data.energy = settings.sun_energy
    sun.data.angle = max(0.0001, settings.sun_diameter)
    sun.data.color = tuple(settings.sun_light_color[:3])
    return sun, target


def _effective_sun_rotation(context, sun):
    try:
        context.view_layer.update()
    except Exception:
        pass
    try:
        depsgraph = context.evaluated_depsgraph_get()
        evaluated = sun.evaluated_get(depsgraph)
        return evaluated.matrix_world.to_euler("XYZ")
    except Exception:
        return sun.matrix_world.to_euler("XYZ")


def _sync_coordinates_from_sun(context, sun):
    coords = bpy.data.node_groups.get(PHYSICAL_COORDINATES)
    if coords is None:
        return None
    rotation = _effective_sun_rotation(context, sun)
    for node_name in ("vec", "vec1", "vec2"):
        node = coords.nodes.get(node_name)
        if node is not None:
            _set_socket_value(node.inputs.get("Rotation"), rotation)
    return rotation


def ensure_psa_graph(context, settings):
    world = ensure_world(context)
    node_tree = world.node_tree
    output = _first_output(world)

    for group_name in PSA_GROUPS:
        append_group(group_name)
    annotate_psa_node_groups()

    coords = ensure_group_node(node_tree, PHYSICAL_COORDINATES, -980, 80)
    planet = ensure_group_node(node_tree, PHYSICAL_PLANET_DATA, -740, 20)
    clouds = ensure_group_node(node_tree, PHYSICAL_CLOUDS, -500, -120)
    stars = ensure_group_node(node_tree, PHYSICAL_STARS, -500, 170)
    atmosphere = ensure_group_node(node_tree, STARLIGHT_ATMOSPHERE, -210, 10)

    _connect(node_tree, _output(coords, "SunVec"), _input(planet, "SunVec"))
    _connect(node_tree, _output(coords, "SunVec"), _input(atmosphere, "SunVec"))
    _connect(node_tree, _output(coords, "SunCosTheta"), _input(atmosphere, "SunCosTheta"))
    _connect(node_tree, _output(coords, "StarCoordinates"), _input(stars, "StarCoordinates"))
    _connect(node_tree, _output(planet, "PlanetShadow"), _input(atmosphere, "PlanetShadow"))
    _connect(node_tree, _output(planet, "PlanetHorizon"), _input(atmosphere, "PlanetHorizon"))
    _connect(node_tree, _output(planet, "AboveBelow"), _input(atmosphere, "AboveBelow"))
    _connect(node_tree, _output(planet, "CloudCoordinates"), _input(clouds, "Vector"))
    _connect(node_tree, _output(stars, "Color"), _input(atmosphere, "in_stars"))
    apply_cloud_links(node_tree, settings)

    ensure_output_nodes(world, settings, atmosphere, output)
    world["xl_physical_atmosphere_ready"] = True
    apply_settings_to_world(world, settings, context)
    return world


def _node(node_tree, bl_idname, name, label, location):
    node = node_tree.nodes.get(name)
    if node is None:
        node = node_tree.nodes.new(bl_idname)
        node.name = name
    node.label = label
    node.location = location
    return node


def _remove_old_background_nodes(node_tree):
    for name in OBSOLETE_BACKGROUND_NODES:
        node = node_tree.nodes.get(name)
        if node is not None:
            node_tree.nodes.remove(node)


def _color_ramp_elements(ramp, count):
    elements = ramp.color_ramp.elements
    while len(elements) < count:
        elements.new(1.0)
    while len(elements) > count and len(elements) > 2:
        elements.remove(elements[-1])
    return elements


def _set_background_ramp(ramp, settings):
    elements = _color_ramp_elements(ramp, 4)
    white_region = _clamp01(settings.background_white_amount)
    blue_region = _clamp01(settings.background_blue_amount)
    shift = max(-0.45, min(0.45, float(settings.background_white_height) * 0.22))

    white_end = _clamp01(white_region * 0.86 + shift)
    blue_start = _clamp01(1.0 - blue_region * 0.86 + shift)
    if white_end > blue_start - 0.02:
        center = _clamp01((white_end + blue_start) * 0.5)
        white_end = max(0.0, center - 0.01)
        blue_start = min(1.0, center + 0.01)

    ramp.color_ramp.interpolation = "B_SPLINE" if settings.background_gradient_softness > 0.72 else "EASE"
    elements[0].position = 0.0
    elements[0].color = settings.background_horizon_white
    elements[1].position = white_end
    elements[1].color = settings.background_horizon_white
    elements[2].position = blue_start
    elements[2].color = settings.background_sky_fade
    elements[3].position = 1.0
    elements[3].color = settings.background_sky_blue


def ensure_gradient_background_color(node_tree, settings, atmosphere):
    for name in HEAVY_BACKGROUND_MASK_NODES:
        node = node_tree.nodes.get(name)
        if node is not None:
            node_tree.nodes.remove(node)

    ramp_existed = node_tree.nodes.get(XL_NODE_PREFIX + "画面背景色带") is not None

    texcoord = _node(
        node_tree,
        "ShaderNodeTexCoord",
        XL_NODE_PREFIX + "渐变窗口坐标",
        "渐变窗口坐标 - TexCoord: 画面上下",
        (-620, 430),
    )
    separate = _node(
        node_tree,
        "ShaderNodeSeparateXYZ",
        XL_NODE_PREFIX + "渐变垂直坐标",
        "渐变垂直坐标 - SeparateXYZ: 取Y高度",
        (-410, 430),
    )
    ramp = _node(
        node_tree,
        "ShaderNodeValToRGB",
        XL_NODE_PREFIX + "画面背景色带",
        "画面背景色带 - ColorRamp: 白色/蓝色区域",
        (-190, 430),
    )
    cloud_noise = _node(
        node_tree,
        "ShaderNodeTexNoise",
        XL_NODE_PREFIX + "轻量云噪声",
        "轻量云噪声 - Noise: 不连接 PSA 核心",
        (40, 120),
    )
    cloud_mask = _node(
        node_tree,
        "ShaderNodeValToRGB",
        XL_NODE_PREFIX + "轻量云遮罩",
        "轻量云遮罩 - ColorRamp: 云疏密/边缘",
        (260, 120),
    )
    cloud_color = _node(
        node_tree,
        "ShaderNodeRGB",
        XL_NODE_PREFIX + "轻量云颜色",
        "轻量云颜色 - RGB: 太阳受光近似",
        (260, -40),
    )
    cloud_mix = _node(
        node_tree,
        "ShaderNodeMixRGB",
        XL_NODE_PREFIX + "轻量云混合",
        "轻量云混合 - MixRGB: 渐变背景+轻量云",
        (500, 260),
    )

    if not ramp_existed and not ramp.get("xl_gradient_initialized"):
        _set_background_ramp(ramp, settings)
        ramp["xl_gradient_initialized"] = True

    _connect(node_tree, texcoord.outputs.get("Window"), separate.inputs.get("Vector"))
    _connect(node_tree, separate.outputs.get("Y"), ramp.inputs.get("Factor") or ramp.inputs.get("Fac"))
    _connect(node_tree, texcoord.outputs.get("Window"), cloud_noise.inputs.get("Vector"))
    _connect(node_tree, cloud_noise.outputs.get("Fac"), cloud_mask.inputs.get("Factor") or cloud_mask.inputs.get("Fac"))
    _connect(node_tree, cloud_mask.outputs.get("Alpha"), cloud_mix.inputs.get("Fac") or cloud_mix.inputs.get("Factor"))
    _connect(node_tree, ramp.outputs.get("Color"), cloud_mix.inputs.get("Color1"))
    _connect(node_tree, cloud_color.outputs.get("Color"), cloud_mix.inputs.get("Color2"))
    update_lightweight_cloud_values(node_tree, settings)
    return cloud_mix.outputs.get("Color")


def _lightweight_cloud_color(settings):
    sun = tuple(settings.sun_light_color)
    scatter = tuple(settings.cloud_scattering)
    warmth = _clamp01(0.45 + settings.sun_light_strength * 0.08)
    light = _mix_rgba(scatter, sun, warmth)
    light = _mix_rgba((1.0, 1.0, 1.0, 1.0), light, 0.45)
    gain = max(0.18, min(1.45, 0.62 + settings.cloud_lighting * 0.16 + settings.sun_light_strength * 0.08))
    shadow = max(0.55, 1.0 - min(0.35, settings.cloud_shadow * 0.012))
    return tuple(max(0.0, min(1.0, light[i] * gain * shadow)) for i in range(3)) + (1.0,)


def update_lightweight_cloud_values(node_tree, settings):
    cloud_noise = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云噪声")
    cloud_mask = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云遮罩")
    cloud_color = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云颜色")
    if cloud_noise:
        scale = max(0.15, min(35.0, 8.0 / max(0.05, settings.cloud_size)))
        _set_socket_value(cloud_noise.inputs.get("Scale"), scale)
        _set_socket_value(cloud_noise.inputs.get("Detail"), max(0.0, min(15.0, settings.cloud_detail)))
        _set_socket_value(cloud_noise.inputs.get("Roughness"), _clamp01(0.28 + settings.cloud_dimension * 0.22))
        _set_socket_value(cloud_noise.inputs.get("Lacunarity"), max(0.0, min(12.0, settings.cloud_lacunarity)))
    if cloud_mask:
        elements = _color_ramp_elements(cloud_mask, 2)
        coverage = _clamp01(settings.cloud_coverage if settings.cloud_enabled else 0.0)
        softness = max(0.015, min(0.62, settings.cloud_softness * 0.16))
        low = max(0.0, min(0.98, 1.0 - coverage))
        high = max(low + 0.01, min(1.0, low + softness))
        opacity = _clamp01(0.25 + settings.cloud_thickness * 0.018 + settings.cloud_lighting * 0.035) if coverage > 0.0 else 0.0
        cloud_mask.color_ramp.interpolation = "EASE"
        elements[0].position = low
        elements[0].color = (0.0, 0.0, 0.0, 0.0)
        elements[1].position = high
        elements[1].color = (1.0, 1.0, 1.0, opacity)
    if cloud_color:
        _set_socket_value(cloud_color.outputs.get("Color"), _lightweight_cloud_color(settings))


def update_output_node_values(world, settings):
    node_tree = world.node_tree
    if node_tree is None:
        return

    linked_bg = node_tree.nodes.get(XL_NODE_PREFIX + "联动背景")
    if linked_bg:
        _set_socket_value(linked_bg.inputs.get("Strength"), settings.sky_strength)

    camera_bg = node_tree.nodes.get(XL_NODE_PREFIX + "相机背景")
    if camera_bg:
        _set_socket_value(camera_bg.inputs.get("Strength"), settings.sky_strength)

    env_bg = node_tree.nodes.get(XL_NODE_PREFIX + "环境颜色")
    if env_bg:
        _set_socket_value(env_bg.inputs.get("Color"), settings.environment_color)
        _set_socket_value(env_bg.inputs.get("Strength"), settings.environment_strength)

    update_lightweight_cloud_values(node_tree, settings)

def _socket_has_link_from(input_socket, from_node, output_socket_name):
    if input_socket is None or from_node is None:
        return False
    output_socket = _output(from_node, output_socket_name)
    if output_socket is None:
        return False
    return any(link.from_node == from_node and link.from_socket == output_socket for link in input_socket.links)


def _background_output_needs_repair(node_tree, settings):
    if settings.control_mode == "LINKED":
        return False

    if any(node_tree.nodes.get(name) is not None for name in HEAVY_BACKGROUND_MASK_NODES):
        return True

    texcoord = node_tree.nodes.get(XL_NODE_PREFIX + "渐变窗口坐标")
    separate = node_tree.nodes.get(XL_NODE_PREFIX + "渐变垂直坐标")
    ramp = node_tree.nodes.get(XL_NODE_PREFIX + "画面背景色带")
    cloud_noise = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云噪声")
    cloud_mask = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云遮罩")
    cloud_color = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云颜色")
    cloud_mix = node_tree.nodes.get(XL_NODE_PREFIX + "轻量云混合")
    camera_bg = node_tree.nodes.get(XL_NODE_PREFIX + "相机背景")

    if node_tree.nodes.get(XL_NODE_PREFIX + "渐变保留太阳云") is not None:
        return True

    if not all((texcoord, separate, ramp, cloud_noise, cloud_mask, cloud_color, cloud_mix, camera_bg)):
        return True

    if not _socket_has_link_from(separate.inputs.get("Vector"), texcoord, "Window"):
        return True
    if not _socket_has_link_from(ramp.inputs.get("Factor") or ramp.inputs.get("Fac"), separate, "Y"):
        return True
    if not _socket_has_link_from(cloud_noise.inputs.get("Vector"), texcoord, "Window"):
        return True
    if not _socket_has_link_from(cloud_mask.inputs.get("Factor") or cloud_mask.inputs.get("Fac"), cloud_noise, "Fac"):
        return True
    if not _socket_has_link_from(cloud_mix.inputs.get("Fac") or cloud_mix.inputs.get("Factor"), cloud_mask, "Alpha"):
        return True
    if not _socket_has_link_from(cloud_mix.inputs.get("Color1"), ramp, "Color"):
        return True
    if not _socket_has_link_from(cloud_mix.inputs.get("Color2"), cloud_color, "Color"):
        return True
    if not _socket_has_link_from(camera_bg.inputs.get("Color"), cloud_mix, "Color"):
        return True

    return False


def ensure_output_nodes(world, settings, atmosphere, output):
    node_tree = world.node_tree
    nodes = node_tree.nodes
    _remove_old_background_nodes(node_tree)

    if settings.control_mode == "LINKED":
        bg = _node(
            node_tree,
            "ShaderNodeBackground",
            XL_NODE_PREFIX + "联动背景",
            "联动背景 - Background: PSA 核心输出",
            (90, 20),
        )
        _set_socket_value(bg.inputs.get("Strength"), settings.sky_strength)
        _connect(node_tree, _output(atmosphere, "out_world"), bg.inputs.get("Color"))
        _connect(node_tree, bg.outputs.get("Background"), output.inputs.get("Surface"))
        return

    camera_bg = _node(
        node_tree,
        "ShaderNodeBackground",
        XL_NODE_PREFIX + "相机背景",
        "相机背景 - Background: PSA核心天空",
        (330, 170),
    )
    env_bg = _node(
        node_tree,
        "ShaderNodeBackground",
        XL_NODE_PREFIX + "环境颜色",
        "环境色 - Background: 非相机照明",
        (330, -90),
    )
    light_path = _node(
        node_tree,
        "ShaderNodeLightPath",
        XL_NODE_PREFIX + "射线路径",
        "射线分离 - LightPath: 相机/环境",
        (330, 390),
    )
    mix_shader = _node(
        node_tree,
        "ShaderNodeMixShader",
        XL_NODE_PREFIX + "背景环境分离",
        "天空环境分离 - MixShader: 相机天空+环境色",
        (620, 50),
    )

    _set_socket_value(env_bg.inputs.get("Color"), settings.environment_color)
    _set_socket_value(env_bg.inputs.get("Strength"), settings.environment_strength)
    _set_socket_value(camera_bg.inputs.get("Strength"), settings.sky_strength)

    camera_color = ensure_gradient_background_color(node_tree, settings, atmosphere)
    _connect(node_tree, camera_color, camera_bg.inputs.get("Color"))
    _connect(node_tree, light_path.outputs.get("Is Camera Ray"), mix_shader.inputs[0])
    _connect(node_tree, env_bg.outputs.get("Background"), mix_shader.inputs[1])
    _connect(node_tree, camera_bg.outputs.get("Background"), mix_shader.inputs[2])
    _connect(node_tree, mix_shader.outputs.get("Shader"), output.inputs.get("Surface"))

    linked_bg = nodes.get(XL_NODE_PREFIX + "联动背景")
    if linked_bg:
        for link in list(linked_bg.outputs["Background"].links):
            node_tree.links.remove(link)


def apply_cloud_links(node_tree, settings):
    clouds = node_tree.nodes.get(PHYSICAL_CLOUDS)
    atmosphere = node_tree.nodes.get(STARLIGHT_ATMOSPHERE)
    if clouds is None or atmosphere is None:
        return
    if settings.cloud_enabled:
        for output_name, input_name in CLOUD_LINKS:
            _connect(node_tree, _output(clouds, output_name), _input(atmosphere, input_name))
        return
    for _output_name, input_name in CLOUD_LINKS:
        socket = _input(atmosphere, input_name)
        _remove_links_to(socket)
        _set_socket_value(socket, CLOUD_DISABLED_DEFAULTS.get(input_name, 0.0))


def _cloud_thresholds(settings):
    coverage = max(0.0, min(1.0, settings.cloud_coverage))
    softness = max(0.05, settings.cloud_softness)
    low = -1.0 + (1.0 - coverage) * 1.3
    high = min(1.0, low + softness)
    return low, high


def _clamp01(value):
    return max(0.0, min(1.0, float(value)))


def _mix_rgba(a, b, factor):
    factor = _clamp01(factor)
    inv = 1.0 - factor
    return tuple(float(a[i]) * inv + float(b[i]) * factor for i in range(4))


def _background_core_values(settings):
    if getattr(settings, "background_control_mode", "INTUITIVE") != "INTUITIVE":
        return {
            "atmosphere_color": settings.atmosphere_color,
            "atmosphere_inscattering": settings.atmosphere_inscattering,
            "atmosphere_extinction": settings.atmosphere_extinction,
            "ground_albedo": settings.ground_albedo,
            "ground_visible": 1.0 if settings.ground_visible else 0.0,
            "ground_offset": settings.ground_offset,
            "horizon_offset": settings.horizon_offset,
            "atmosphere_distance": settings.atmosphere_distance,
            "atmosphere_falloff": settings.atmosphere_falloff,
        }

    sky_blue = tuple(settings.background_sky_blue)
    sky_fade = tuple(settings.background_sky_fade)
    horizon_white = tuple(settings.background_horizon_white)
    white_amount = _clamp01(settings.background_white_amount)
    blue_amount = _clamp01(settings.background_blue_amount)
    softness = _clamp01(settings.background_gradient_softness)

    return {
        "atmosphere_color": _mix_rgba(sky_fade, horizon_white, white_amount * 0.25),
        "atmosphere_inscattering": _mix_rgba(sky_blue, sky_fade, softness * 0.25),
        "atmosphere_extinction": _mix_rgba(horizon_white, sky_fade, (1.0 - white_amount) * 0.12),
        "ground_albedo": _mix_rgba(horizon_white, sky_fade, 0.12),
        "ground_visible": 1.0,
        "ground_offset": settings.ground_offset,
        "horizon_offset": settings.background_white_height,
        "atmosphere_distance": 0.45 + white_amount * 2.8,
        "atmosphere_falloff": 0.35 + (1.0 - softness) * 1.25 + (1.0 - blue_amount) * 0.4,
    }


def apply_settings_to_world(world, settings, context=None):
    global _APPLYING
    if _APPLYING:
        return
    _APPLYING = True
    try:
        context = context or bpy.context
        node_tree = world.node_tree
        if node_tree is None or node_tree.nodes.get(STARLIGHT_ATMOSPHERE) is None:
            return

        sun, _target = ensure_sun_control(context, settings)
        _sync_coordinates_from_sun(context, sun)
        apply_cloud_links(node_tree, settings)

        low, high = _cloud_thresholds(settings)
        cloud_node = node_tree.nodes.get(PHYSICAL_CLOUDS)
        if cloud_node:
            cloud_scale = 6.0 / max(0.05, settings.cloud_size)
            cloud_values = {
                "Scale": cloud_scale,
                "Min": low,
                "Max": high,
                "Thickness": settings.cloud_thickness,
                "Scattering": settings.cloud_scattering,
                "Val1": settings.cloud_shadow,
                "Val2": settings.cloud_directional_power,
                "Intensity": settings.cloud_lighting,
                "Detail": settings.cloud_detail,
                "Dimension": settings.cloud_dimension,
                "Lacunarity": settings.cloud_lacunarity,
            }
            for socket_name, value in cloud_values.items():
                _set_socket_value(_input(cloud_node, socket_name), value)

        background = _background_core_values(settings)
        sun_color = tuple(_blackbody_rgb(settings.sun_temperature)) + (1.0,)
        sun_light = _rgba_scaled(settings.sun_light_color, settings.sun_light_strength)
        _set_input_node(PHYSICAL_INPUTS, "sun_diameter", settings.sun_diameter)
        _set_input_node(PHYSICAL_INPUTS, "sun_intensity", settings.sun_intensity)
        _set_input_node(PHYSICAL_INPUTS, "sun_color", sun_color)
        _set_input_node(PHYSICAL_INPUTS, "sun_light", sun_light)
        _set_input_node(PHYSICAL_INPUTS, "sun_light_upper", sun_light)
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_color", background["atmosphere_color"])
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_inscattering", background["atmosphere_inscattering"])
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_extinction", background["atmosphere_extinction"])
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_density", settings.atmosphere_density)
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_height", settings.atmosphere_height)
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_intensity", settings.atmosphere_intensity)
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_mie", settings.atmosphere_mie)
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_mie_dir", settings.atmosphere_mie_dir)
        _set_input_node(PHYSICAL_INPUTS, "night_radiance", settings.night_intensity)
        _set_input_node(PHYSICAL_INPUTS, "ground_albedo", background["ground_albedo"])
        _set_input_node(PHYSICAL_INPUTS, "ground_visible", background["ground_visible"])
        _set_input_node(PHYSICAL_INPUTS, "ground_offset", background["ground_offset"])
        _set_input_node(PHYSICAL_INPUTS, "horizon_offset", background["horizon_offset"])
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_distance", background["atmosphere_distance"])
        _set_input_node(PHYSICAL_INPUTS, "atmosphere_falloff", background["atmosphere_falloff"])
        _set_input_node(PHYSICAL_INPUTS, "stars_radiance_intensity", settings.stars_intensity)
        _set_input_node(PHYSICAL_INPUTS, "stars_amount", settings.stars_amount)
        _set_input_node(PHYSICAL_INPUTS, "stars_scale", settings.stars_scale)

        atmosphere = node_tree.nodes.get(STARLIGHT_ATMOSPHERE)
        if atmosphere is not None:
            _set_socket_value(_input(atmosphere, "in_world"), background["atmosphere_color"])
            if _background_output_needs_repair(node_tree, settings):
                ensure_output_nodes(world, settings, atmosphere, _first_output(world))
        update_output_node_values(world, settings)
        world.color = settings.environment_color[:3]

        screen = getattr(context, "screen", None) or getattr(bpy.context, "screen", None)
        if screen:
            for area in screen.areas:
                if area.type in {"VIEW_3D", "NODE_EDITOR"}:
                    area.tag_redraw()
    finally:
        _APPLYING = False


def apply_preset_to_nodes(context, preset_data):
    world = ensure_world(context)
    atmosphere = preset_data.get("atmosphere", {})
    for prop_name, node_name in INPUT_NODE_MAP.items():
        if prop_name in atmosphere:
            _set_input_node(PHYSICAL_INPUTS, node_name, atmosphere[prop_name])

    cloud_node = world.node_tree.nodes.get(PHYSICAL_CLOUDS) if world.node_tree else None
    if cloud_node:
        for prop_name, socket_name in CLOUD_INPUT_MAP.items():
            if prop_name in atmosphere:
                _set_socket_value(_input(cloud_node, socket_name), atmosphere[prop_name])

    sun_data = preset_data.get("sun", {})
    rotation = sun_data.get("rotation_euler")
    settings = world.xl_atmosphere_settings
    if rotation and len(rotation) >= 3 and settings.apply_preset_sun:
        sun, target = ensure_sun_control(context, settings)
        _set_sun_location_from_rotation(sun, target, Euler(rotation[:3], "XYZ"))
    apply_settings_to_world(world, settings, context)


def apply_preset_to_settings(settings, preset_data):
    atmosphere = preset_data.get("atmosphere", {})
    if "atmosphere_color" in atmosphere:
        settings.atmosphere_color = atmosphere["atmosphere_color"]
        settings.background_sky_fade = atmosphere["atmosphere_color"]
    if "atmosphere_inscattering" in atmosphere:
        settings.atmosphere_inscattering = atmosphere["atmosphere_inscattering"]
        settings.background_sky_blue = atmosphere["atmosphere_inscattering"]
    if "atmosphere_extinction" in atmosphere:
        settings.atmosphere_extinction = atmosphere["atmosphere_extinction"]
        settings.background_horizon_white = atmosphere["atmosphere_extinction"]
    if "atmosphere_density" in atmosphere:
        settings.atmosphere_density = atmosphere["atmosphere_density"]
    if "atmosphere_height" in atmosphere:
        settings.atmosphere_height = atmosphere["atmosphere_height"]
    if "atmosphere_intensity" in atmosphere:
        settings.atmosphere_intensity = atmosphere["atmosphere_intensity"]
    if "atmosphere_mie" in atmosphere:
        settings.atmosphere_mie = atmosphere["atmosphere_mie"]
    if "atmosphere_mie_dir" in atmosphere:
        settings.atmosphere_mie_dir = atmosphere["atmosphere_mie_dir"]
    if "horizon_offset" in atmosphere:
        settings.horizon_offset = atmosphere["horizon_offset"]
        settings.background_white_height = atmosphere["horizon_offset"]
    if "night_intensity" in atmosphere:
        settings.night_intensity = atmosphere["night_intensity"]
    if "ground_albedo" in atmosphere:
        settings.ground_albedo = atmosphere["ground_albedo"]
        settings.background_horizon_white = atmosphere["ground_albedo"]
    if "ground_visible" in atmosphere:
        settings.ground_visible = bool(atmosphere["ground_visible"])
    if "ground_offset" in atmosphere:
        settings.ground_offset = atmosphere["ground_offset"]
    if "atmosphere_distance" in atmosphere:
        settings.atmosphere_distance = atmosphere["atmosphere_distance"]
        settings.background_white_amount = _clamp01((atmosphere["atmosphere_distance"] - 0.45) / 2.8)
    if "atmosphere_falloff" in atmosphere:
        settings.atmosphere_falloff = atmosphere["atmosphere_falloff"]
        settings.background_gradient_softness = _clamp01(1.0 - ((atmosphere["atmosphere_falloff"] - 0.35) / 1.65))
    if "sun_diameter" in atmosphere:
        settings.sun_diameter = atmosphere["sun_diameter"]
    if "sun_temperature" in atmosphere:
        settings.sun_temperature = atmosphere["sun_temperature"]
        settings.sun_light_color = tuple(_blackbody_rgb(atmosphere["sun_temperature"])) + (1.0,)
    if "sun_intensity" in atmosphere:
        settings.sun_intensity = atmosphere["sun_intensity"]
    if "stars_intensity" in atmosphere:
        settings.stars_intensity = atmosphere["stars_intensity"]
    if "stars_amount" in atmosphere:
        settings.stars_amount = atmosphere["stars_amount"]
    if "stars_scale" in atmosphere:
        settings.stars_scale = atmosphere["stars_scale"]
    if "clouds_scale" in atmosphere:
        settings.cloud_size = max(0.05, 6.0 / max(0.05, atmosphere["clouds_scale"]))
    if "clouds_min" in atmosphere:
        settings.cloud_coverage = max(0.0, min(1.0, 1.0 - (atmosphere["clouds_min"] + 1.0) / 1.3))
    if "clouds_max" in atmosphere and "clouds_min" in atmosphere:
        settings.cloud_softness = max(0.05, atmosphere["clouds_max"] - atmosphere["clouds_min"])
    if "clouds_thickness" in atmosphere:
        settings.cloud_thickness = atmosphere["clouds_thickness"]
    if "clouds_detail" in atmosphere:
        settings.cloud_detail = atmosphere["clouds_detail"]
    if "clouds_dimension" in atmosphere:
        settings.cloud_dimension = atmosphere["clouds_dimension"]
    if "clouds_lacunarity" in atmosphere:
        settings.cloud_lacunarity = atmosphere["clouds_lacunarity"]
    if "clouds_scattering" in atmosphere:
        settings.cloud_scattering = atmosphere["clouds_scattering"]
    if "clouds_amount" in atmosphere:
        settings.cloud_shadow = atmosphere["clouds_amount"]
    if "clouds_power" in atmosphere:
        settings.cloud_directional_power = atmosphere["clouds_power"]
    if "clouds_lighting_intensity" in atmosphere:
        settings.cloud_lighting = atmosphere["clouds_lighting_intensity"]
