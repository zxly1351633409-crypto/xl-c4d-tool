"""XL 物理天空场景同步。"""

from __future__ import annotations

import bpy
from bpy.app.handlers import persistent


_BUSY = False


def _tracked_object_names(settings):
    names = set()
    if settings.sun_object:
        names.add(settings.sun_object.name)
    if settings.sun_target:
        names.add(settings.sun_target.name)
    return names


@persistent
def xl_physical_atmosphere_depsgraph(scene, depsgraph):
    global _BUSY
    if _BUSY:
        return
    world = getattr(scene, "world", None)
    if not world or not world.get("xl_physical_atmosphere_ready"):
        return
    if not hasattr(world, "xl_atmosphere_settings"):
        return
    settings = world.xl_atmosphere_settings
    names = _tracked_object_names(settings)
    if not names:
        return
    changed = False
    for update in depsgraph.updates:
        data = getattr(update, "id", None)
        if getattr(data, "name", None) in names:
            changed = True
            break
    if not changed:
        return

    from .core import apply_settings_to_world

    _BUSY = True
    try:
        apply_settings_to_world(world, settings, bpy.context)
    finally:
        _BUSY = False


def register():
    if xl_physical_atmosphere_depsgraph not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(xl_physical_atmosphere_depsgraph)


def unregister():
    try:
        bpy.app.handlers.depsgraph_update_post.remove(xl_physical_atmosphere_depsgraph)
    except ValueError:
        pass
