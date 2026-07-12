"""XL 物理天空面板绘制。"""

from __future__ import annotations

import bpy

from .core import XL_NODE_PREFIX


def _draw_prop_pair(layout, owner, left, right):
    row = layout.row(align=True)
    row.prop(owner, left)
    row.prop(owner, right)


def _background_ramp_node(world):
    node_tree = getattr(world, "node_tree", None)
    if node_tree is None:
        return None
    return node_tree.nodes.get(XL_NODE_PREFIX + "画面背景色带")


def draw_inline_atmosphere_panel(layout, context):
    world = context.scene.world
    if world is None or not hasattr(world, "xl_atmosphere_settings"):
        layout.operator("world.xl_setup_atmosphere", icon="WORLD_DATA")
        return

    settings = world.xl_atmosphere_settings

    header, body = layout.panel("xl_physical_atmosphere_main", default_closed=False)
    header.label(text="物理天空", icon="WORLD")
    if not body:
        return

    row = body.row(align=True)
    row.operator("world.xl_setup_atmosphere", text="创建/更新", icon="WORLD_DATA")
    row.operator("world.xl_refresh_atmosphere", text="", icon="FILE_REFRESH")

    row = body.row(align=True)
    row.prop(settings, "preset", text="")
    row.prop(settings, "apply_preset_sun", text="", icon="LIGHT_SUN")
    row.operator("world.xl_apply_atmosphere_preset", text="", icon="IMPORT")

    body.prop(settings, "control_mode", expand=True)

    header, section = body.panel("xl_physical_atmosphere_background", default_closed=not settings.show_background)
    header.prop(settings, "show_background", text="天空 / 环境", emboss=False)
    if section:
        section.label(text="画面背景", icon="IMAGE_DATA")
        ramp = _background_ramp_node(world)
        if ramp:
            section.template_color_ramp(ramp, "color_ramp", expand=True)
        else:
            section.operator("world.xl_setup_atmosphere", text="创建背景渐变", icon="WORLD_DATA")
        section.prop(settings, "sky_strength")
        section.separator()
        section.label(text="天空环境色", icon="LIGHT")
        section.prop(settings, "environment_color")
        section.prop(settings, "environment_strength")

    header, section = body.panel("xl_physical_atmosphere_sun", default_closed=not settings.show_sun)
    header.prop(settings, "show_sun", text="太阳", emboss=False)
    if section:
        section.prop(settings, "sun_object")
        section.prop(settings, "sun_target")
        _draw_prop_pair(section, settings, "sun_diameter", "sun_temperature")
        section.prop(settings, "sun_light_color")
        section.prop(settings, "sun_light_strength")
        _draw_prop_pair(section, settings, "sun_intensity", "sun_energy")

    header, section = body.panel("xl_physical_atmosphere_clouds", default_closed=not settings.show_clouds)
    header.prop(settings, "show_clouds", text="云", emboss=False)
    if section:
        section.prop(settings, "cloud_enabled")
        _draw_prop_pair(section, settings, "cloud_coverage", "cloud_size")
        _draw_prop_pair(section, settings, "cloud_softness", "cloud_thickness")
        _draw_prop_pair(section, settings, "cloud_detail", "cloud_lacunarity")
        section.prop(settings, "cloud_dimension")
        section.prop(settings, "cloud_scattering")
        _draw_prop_pair(section, settings, "cloud_shadow", "cloud_directional_power")
        section.prop(settings, "cloud_lighting")

    header, section = body.panel("xl_physical_atmosphere_core", default_closed=not settings.show_atmosphere)
    header.prop(settings, "show_atmosphere", text="大气", emboss=False)
    if section:
        _draw_prop_pair(section, settings, "atmosphere_density", "atmosphere_intensity")
        _draw_prop_pair(section, settings, "atmosphere_mie", "atmosphere_mie_dir")
        _draw_prop_pair(section, settings, "atmosphere_height", "night_intensity")

    header, section = body.panel("xl_physical_atmosphere_stars", default_closed=not settings.show_stars)
    header.prop(settings, "show_stars", text="星空", emboss=False)
    if section:
        _draw_prop_pair(section, settings, "stars_intensity", "stars_amount")
        section.prop(settings, "stars_scale")


classes = ()


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
