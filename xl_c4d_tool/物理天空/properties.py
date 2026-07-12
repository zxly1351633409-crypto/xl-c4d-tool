"""XL 物理天空属性。"""

from __future__ import annotations

import bpy


def _update_live(self, context):
    world = getattr(context.scene, "world", None)
    if not world or not world.get("xl_physical_atmosphere_ready"):
        return
    from .core import apply_settings_to_world
    apply_settings_to_world(world, self, context)


def _poll_sun_object(_self, obj):
    return obj is not None and obj.type == "LIGHT" and obj.data and obj.data.type == "SUN"


def _poll_empty_object(_self, obj):
    return obj is not None and obj.type == "EMPTY"


def preset_items(_self, _context):
    from .core import list_presets, preset_label
    items = [(name, preset_label(name), f"应用 PSA 预设: {name}") for name in list_presets()]
    return items or [("NONE", "无预设", "未找到内置预设")]


class XLAtmosphereSettings(bpy.types.PropertyGroup):
    preset: bpy.props.EnumProperty(
        name="天空预设",
        description="内置 Physical Starlight and Atmosphere v1.8.3 预设",
        items=preset_items,
    )
    apply_preset_sun: bpy.props.BoolProperty(
        name="应用预设太阳方向",
        description="应用预设时把日光对象移动到对应方向",
        default=True,
    )
    control_mode: bpy.props.EnumProperty(
        name="控制模式",
        description="联动模式直接输出 PSA 天空；独立模式把相机天空和环境照明颜色分开",
        items=(
            ("LINKED", "联动", "保留 PSA 原始天空直接输出到世界"),
            ("INDEPENDENT", "独立", "相机看到 PSA 核心天空，环境照明使用单独颜色"),
        ),
        default="INDEPENDENT",
        update=_update_live,
    )
    background_control_mode: bpy.props.EnumProperty(
        name="画面背景模式",
        description="直观颜色会把蓝天和白色渐变自动写入 PSA 核心；核心参数用于精细物理调节",
        items=(
            ("INTUITIVE", "直观颜色", "用蓝色、浅蓝和白色渐变来调画面背景"),
            ("PHYSICAL", "核心参数", "直接调 PSA 核心的散射、吸收和地平参数"),
        ),
        default="INTUITIVE",
        update=_update_live,
    )

    background_sky_blue: bpy.props.FloatVectorProperty(
        name="天空蓝色",
        description="直观背景模式下的主要蓝天颜色，会写入 PSA 核心散射色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.22, 0.42, 1.0, 1.0),
        update=_update_live,
    )
    background_sky_fade: bpy.props.FloatVectorProperty(
        name="浅蓝渐变",
        description="直观背景模式下的蓝天过渡色，会写入 PSA 核心天空底色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.62, 0.78, 1.0, 1.0),
        update=_update_live,
    )
    background_horizon_white: bpy.props.FloatVectorProperty(
        name="地平白色",
        description="直观背景模式下的白色渐变颜色，会写入 PSA 核心地平吸收和反照色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.96, 0.86, 1.0),
        update=_update_live,
    )
    background_white_amount: bpy.props.FloatProperty(
        name="白色区域",
        description="直观背景模式下地平白色占画面的高度；调大后白色更多、蓝色更少",
        default=0.42,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
        update=_update_live,
    )
    background_blue_amount: bpy.props.FloatProperty(
        name="蓝色区域",
        description="直观背景模式下天空蓝色占画面的高度；调大后蓝色更多、白色更少",
        default=0.42,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
        update=_update_live,
    )
    background_gradient_softness: bpy.props.FloatProperty(
        name="过渡柔和",
        description="直观背景模式下蓝色到白色的过渡柔和程度",
        default=0.62,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
        update=_update_live,
    )
    background_white_height: bpy.props.FloatProperty(
        name="白色高度",
        description="直观背景模式下地平白色渐变的位置",
        default=0.0,
        soft_min=-2.0,
        soft_max=2.0,
        update=_update_live,
    )
    background_detail_strength: bpy.props.FloatProperty(
        name="旧版PSA叠加",
        description="已停用；为避免拖动背景色带时重编译 PSA 大气核心导致卡死，独立背景不再使用此参数",
        default=0.0,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
        update=_update_live,
    )

    atmosphere_color: bpy.props.FloatVectorProperty(
        name="核心天空底色",
        description="写入 PSA 核心 atmosphere_color，真实控制画面天空底色，不再额外混合渐变",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.75, 0.8, 1.0, 1.0),
        update=_update_live,
    )
    atmosphere_inscattering: bpy.props.FloatVectorProperty(
        name="核心天顶散射",
        description="写入 PSA 核心 atmosphere_inscattering，控制蓝天/上方散射色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0573, 0.1001, 0.1971, 1.0),
        update=_update_live,
    )
    atmosphere_extinction: bpy.props.FloatVectorProperty(
        name="核心地平吸收",
        description="写入 PSA 核心 atmosphere_extinction，控制地平线暖色、雾吸收和天空渐变感",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.9427, 0.8999, 0.8029, 1.0),
        update=_update_live,
    )
    sky_strength: bpy.props.FloatProperty(
        name="天空显示强度",
        description="相机可见天空背景的亮度",
        default=1.0,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )
    environment_color: bpy.props.FloatVectorProperty(
        name="天空环境色",
        description="独立模式下非相机射线使用的世界环境照明颜色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.62, 0.66, 0.58, 1.0),
        update=_update_live,
    )
    environment_strength: bpy.props.FloatProperty(
        name="环境强度",
        description="独立模式下世界环境照明强度",
        default=0.65,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )

    sun_object: bpy.props.PointerProperty(
        name="日光对象",
        description="用于控制天空太阳方向的 Sun 灯；可选择你自己新建的日光",
        type=bpy.types.Object,
        poll=_poll_sun_object,
        update=_update_live,
    )
    sun_target: bpy.props.PointerProperty(
        name="目标空物体",
        description="日光的 Track To 目标；移动日光或目标空物体即可改变天空太阳方向",
        type=bpy.types.Object,
        poll=_poll_empty_object,
        update=_update_live,
    )
    sun_azimuth: bpy.props.FloatProperty(
        name="太阳方位",
        description="旧版预设兼容值；新控制以日光对象方向为准",
        default=0.692023,
        unit="ROTATION",
        update=_update_live,
    )
    sun_elevation: bpy.props.FloatProperty(
        name="太阳高度",
        description="旧版预设兼容值；新控制以日光对象方向为准",
        default=-1.519047,
        unit="ROTATION",
        update=_update_live,
    )
    sun_diameter: bpy.props.FloatProperty(
        name="太阳盘大小",
        description="太阳盘角直径，同时控制 PSA 太阳盘和日光角度",
        default=0.00918,
        min=0.001,
        soft_max=0.1,
        unit="ROTATION",
        update=_update_live,
    )
    sun_temperature: bpy.props.FloatProperty(
        name="太阳色温",
        description="用黑体色近似控制太阳盘和大气核心太阳颜色",
        default=5700.0,
        min=1000.0,
        soft_max=12000.0,
        update=_update_live,
    )
    sun_light_color: bpy.props.FloatVectorProperty(
        name="太阳受光颜色",
        description="单独控制云层受光和场景日光颜色，不影响画面背景渐变",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.945, 0.895, 1.0),
        update=_update_live,
    )
    sun_light_strength: bpy.props.FloatProperty(
        name="太阳受光强度",
        description="写入 PSA sun_light / sun_light_upper，单独影响云层和大气受光",
        default=1.0,
        min=0.0,
        soft_max=8.0,
        update=_update_live,
    )
    sun_intensity: bpy.props.FloatProperty(
        name="太阳天空强度",
        description="写入 PSA 天空内部的太阳辐射强度",
        default=200000.0,
        min=0.0,
        soft_max=300000.0,
        update=_update_live,
    )
    sun_energy: bpy.props.FloatProperty(
        name="日光强度",
        description="场景日光对象的实际照明强度",
        default=1.0,
        min=0.0,
        soft_max=20.0,
        update=_update_live,
    )

    atmosphere_density: bpy.props.FloatProperty(
        name="大气密度",
        default=1.2,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )
    atmosphere_height: bpy.props.FloatProperty(
        name="大气高度",
        default=8000.0,
        min=2.0,
        soft_max=20000.0,
        unit="LENGTH",
        update=_update_live,
    )
    atmosphere_intensity: bpy.props.FloatProperty(
        name="大气强度",
        default=2.0,
        min=0.0,
        soft_max=50.0,
        update=_update_live,
    )
    atmosphere_mie: bpy.props.FloatProperty(
        name="霞光散射",
        description="PSA atmosphere_mie，控制靠近太阳方向的雾光强度",
        default=2.0,
        min=0.0,
        soft_max=20.0,
        update=_update_live,
    )
    atmosphere_mie_dir: bpy.props.FloatProperty(
        name="霞光方向性",
        description="PSA atmosphere_mie_dir，越高越集中在太阳方向",
        default=0.7,
        min=0.0,
        max=0.99,
        update=_update_live,
    )
    night_intensity: bpy.props.FloatProperty(
        name="夜空强度",
        default=0.02,
        min=0.0,
        soft_max=1.0,
        update=_update_live,
    )
    ground_albedo: bpy.props.FloatVectorProperty(
        name="地面反照色",
        description="写入 PSA 核心 GroundColor，影响地平线和低空背景反照色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.25, 0.25, 0.25, 1.0),
        update=_update_live,
    )
    ground_visible: bpy.props.BoolProperty(
        name="显示地平/地面",
        description="写入 PSA 核心 GroundVisible，控制画面背景是否参与地平/地面遮罩",
        default=True,
        update=_update_live,
    )
    ground_offset: bpy.props.FloatProperty(
        name="地平面偏移",
        default=-100.0,
        soft_min=-500000.0,
        soft_max=1000.0,
        unit="LENGTH",
        update=_update_live,
    )
    atmosphere_distance: bpy.props.FloatProperty(
        name="背景距离倍率",
        description="写入 PSA 核心 DistanceScalar，控制天空背景和雾层的距离尺度",
        default=1.0,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )
    atmosphere_falloff: bpy.props.FloatProperty(
        name="背景衰减",
        description="写入 PSA 核心 FogFalloff，控制天空背景/雾色过渡衰减",
        default=1.0,
        min=0.0,
        soft_max=5.0,
        update=_update_live,
    )
    horizon_offset: bpy.props.FloatProperty(
        name="地平线偏移",
        default=0.0,
        soft_min=-5.0,
        soft_max=5.0,
        update=_update_live,
    )

    cloud_enabled: bpy.props.BoolProperty(
        name="启用云",
        description="真正断开或恢复 PSA 云输入",
        default=True,
        update=_update_live,
    )
    cloud_coverage: bpy.props.FloatProperty(
        name="云疏密",
        description="越高云越密，越低云越稀疏",
        default=0.85,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
        update=_update_live,
    )
    cloud_size: bpy.props.FloatProperty(
        name="云块大小",
        description="越大云块越大，越小纹理越碎",
        default=3.0,
        min=0.05,
        soft_max=10.0,
        update=_update_live,
    )
    cloud_softness: bpy.props.FloatProperty(
        name="云层过渡",
        description="控制云边缘和疏密过渡范围",
        default=1.6,
        min=0.05,
        soft_max=3.0,
        update=_update_live,
    )
    cloud_thickness: bpy.props.FloatProperty(
        name="云厚度",
        default=15.0,
        min=0.0,
        soft_max=50.0,
        update=_update_live,
    )
    cloud_detail: bpy.props.FloatProperty(
        name="云细节",
        default=8.0,
        min=0.0,
        soft_max=12.0,
        update=_update_live,
    )
    cloud_dimension: bpy.props.FloatProperty(
        name="云形维度",
        default=1.0,
        min=0.0,
        soft_max=3.0,
        update=_update_live,
    )
    cloud_lacunarity: bpy.props.FloatProperty(
        name="细节层级",
        default=2.1,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )
    cloud_scattering: bpy.props.FloatVectorProperty(
        name="云散射色",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.4, 0.45, 0.8, 1.0),
        update=_update_live,
    )
    cloud_shadow: bpy.props.FloatProperty(
        name="云自阴影",
        default=5.0,
        min=0.0,
        soft_max=100.0,
        update=_update_live,
    )
    cloud_directional_power: bpy.props.FloatProperty(
        name="云方向性",
        default=5.0,
        min=0.0,
        soft_max=100.0,
        update=_update_live,
    )
    cloud_lighting: bpy.props.FloatProperty(
        name="云受光强度",
        default=1.0,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )

    stars_intensity: bpy.props.FloatProperty(
        name="星空强度",
        default=0.02,
        min=0.0,
        soft_max=10.0,
        update=_update_live,
    )
    stars_amount: bpy.props.FloatProperty(
        name="星星数量",
        default=1.0,
        min=0.0,
        soft_max=2.0,
        update=_update_live,
    )
    stars_scale: bpy.props.FloatProperty(
        name="星图尺度",
        default=1.0,
        min=0.001,
        soft_max=5.0,
        update=_update_live,
    )

    show_background: bpy.props.BoolProperty(name="天空/环境", default=True)
    show_sun: bpy.props.BoolProperty(name="太阳", default=True)
    show_atmosphere: bpy.props.BoolProperty(name="大气", default=False)
    show_clouds: bpy.props.BoolProperty(name="云", default=True)
    show_stars: bpy.props.BoolProperty(name="星空", default=False)


classes = (XLAtmosphereSettings,)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    if not hasattr(bpy.types.World, "xl_atmosphere_settings"):
        bpy.types.World.xl_atmosphere_settings = bpy.props.PointerProperty(type=XLAtmosphereSettings)


def unregister():
    if hasattr(bpy.types.World, "xl_atmosphere_settings"):
        del bpy.types.World.xl_atmosphere_settings
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
