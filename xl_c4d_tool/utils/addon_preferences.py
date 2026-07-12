"""访问 xl_c4d_tool 的全局偏好设置。"""

from __future__ import annotations

import bpy


def get_addon_preferences(context=None):
    """返回插件偏好设置；未注册完成时返回 ``None``。"""
    context = context or bpy.context
    addons = getattr(getattr(context, "preferences", None), "addons", {})
    for key in (__package__.split(".")[0], "xl_c4d_tool"):
        addon = addons.get(key)
        if addon is not None:
            return addon.preferences
    return None
