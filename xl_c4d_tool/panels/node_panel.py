"""彩色、可折叠、可搜索的原生节点助手。"""

from __future__ import annotations

import bpy
from bpy.props import StringProperty
from bpy.types import Panel

from ..utils.addon_preferences import get_addon_preferences
from ..utils.icon_manager import native_category_icon
from ..utils.node_discovery import (
    get_category_color_prop_name,
    get_complete_node_data,
    resolve_tree_type,
)


def _ids(value):
    return [item for item in (value or "").split("|") if item]


def _catalog(context):
    return get_complete_node_data(context).get(resolve_tree_type(context), {})


def _lookup(catalog):
    result = {}
    for category, payload in catalog.items():
        for node_id, label in payload.get("nodes", []):
            result[node_id] = (label, category)
    return result


def _draw_color_header(header, prefs, category, count):
    header.scale_y = 1.35
    cat_icon = native_category_icon(category, button=False)
    if cat_icon:
        header.label(text=f"{category} · {count}", icon_value=cat_icon)
    else:
        header.label(text=f"{category} · {count}", icon="NODETREE")


def _draw_node_button(layout, node_id, label, category, favorites):
    row = layout.row(align=True)
    row.scale_y = 1.5
    btn_icon = native_category_icon(category, button=True)
    if btn_icon:
        op = row.operator("node.xl_add_catalog_node", text=label, icon_value=btn_icon)
    else:
        op = row.operator("node.xl_add_catalog_node", text=label, icon="NODE")
    op.node_type = node_id
    op.category = category
    star = row.operator(
        "node.xl_toggle_favorite", text="",
        icon="SOLO_ON" if node_id in favorites else "SOLO_OFF",
        depress=node_id in favorites,
    )
    star.node_type = node_id


def _draw_nodes(layout, nodes, favorites, columns, category="其他"):
    grid = layout.grid_flow(row_major=True, columns=columns, even_columns=True, even_rows=True, align=True)
    for node_id, label in nodes:
        _draw_node_button(grid, node_id, label, category, favorites)


def draw_browser(layout, context):
    prefs = get_addon_preferences(context)
    catalog = _catalog(context)
    if prefs is None or not catalog:
        layout.label(text="当前编辑器没有可用节点", icon="INFO")
        return
    search = layout.row(align=True)
    search.prop(context.window_manager, "xl_node_search_query", text="", icon="VIEWZOOM")
    search.operator("preferences.xl_open_addon", text="", icon="PREFERENCES")
    lookup = _lookup(catalog)
    favorites = set(_ids(prefs.node_favorites))
    query = context.window_manager.xl_node_search_query.strip().casefold()
    if query:
        nodes = [
            (node_id, label) for node_id, (label, category) in lookup.items()
            if query in node_id.casefold() or query in label.casefold() or query in category.casefold()
        ]
        nodes.sort(key=lambda item: item[0].casefold())
        nodes = nodes[:prefs.node_max_search_results]
        box = layout.box()
        box.label(text=f"搜索结果 · {len(nodes)}", icon="VIEWZOOM")
        _draw_nodes(box, nodes, favorites, prefs.node_columns, "搜索")
        return

    for special, ids, icon, closed in (
        ("收藏", _ids(prefs.node_favorites), "SOLO_ON", False),
        ("最近", _ids(prefs.node_recent), "RECOVER_LAST", True),
    ):
        nodes = [(node_id, lookup[node_id][0]) for node_id in ids if node_id in lookup]
        if not nodes:
            continue
        header, body = layout.panel("xl_native_" + special, default_closed=closed)
        header.label(text=f"{special} · {len(nodes)}", icon=icon)
        if body:
            _draw_nodes(body, nodes, favorites, prefs.node_columns, special)

    for index, (category, payload) in enumerate(catalog.items()):
        nodes = payload.get("nodes", [])
        panel_id = f"xl_native_category_{index}_{resolve_tree_type(context)}"
        header, body = layout.panel(panel_id, default_closed=category not in {"输入", "几何"})
        _draw_color_header(header, prefs, category, len(nodes))
        if body:
            _draw_nodes(body, nodes, favorites, prefs.node_columns, category)


class XlNodeToolsNPanel(Panel):
    bl_label = "快捷节点"
    bl_idname = "NODE_EDITOR_PT_xl_node_tools_npanel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "快捷节点"

    @classmethod
    def poll(cls, context):
        prefs = get_addon_preferences(context)
        return bool(prefs and prefs.node_show_in_n_panel and resolve_tree_type(context))

    def draw(self, context):
        draw_browser(self.layout, context)


def add_to_node_tools_active(self, context):
    prefs = get_addon_preferences(context)
    if prefs is None or not prefs.node_show_in_t_panel or not resolve_tree_type(context):
        return
    self.layout.separator()
    draw_browser(self.layout, context)


def add_auto_show_button(self, context):
    if getattr(context.space_data, "type", None) != "NODE_EDITOR":
        return
    prefs = get_addon_preferences(context)
    if prefs is None:
        return
    op = self.layout.operator("node.xl_auto_show_toolbar", text="", icon="MENU_PANEL", depress=prefs.auto_show_toolbar)
    op.enable = not prefs.auto_show_toolbar


classes = (XlNodeToolsNPanel,)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    bpy.types.WindowManager.xl_node_search_query = StringProperty(name="节点搜索", default="")
    if hasattr(bpy.types, "NODE_PT_tools_active"):
        bpy.types.NODE_PT_tools_active.append(add_to_node_tools_active)
    bpy.types.NODE_HT_header.append(add_auto_show_button)


def unregister():
    if hasattr(bpy.types, "NODE_PT_tools_active"):
        try:
            bpy.types.NODE_PT_tools_active.remove(add_to_node_tools_active)
        except (ValueError, RuntimeError):
            pass
    try:
        bpy.types.NODE_HT_header.remove(add_auto_show_button)
    except (ValueError, RuntimeError):
        pass
    if hasattr(bpy.types.WindowManager, "xl_node_search_query"):
        del bpy.types.WindowManager.xl_node_search_query
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
