"""几何节点助手：分类、搜索、彩色专属图标与鼠标放置。"""

from __future__ import annotations

import bpy

from ..utils.icon_manager import icon_value
from ..utils.library_catalog import category_definition
from ..utils.modifier_library import grouped_modifier_manifest, load_modifier_manifest


def _draw_button(layout, item):
    layout.scale_y = 1.55
    kwargs = {"text": item.get("label") or item["name"]}
    # 优先使用分类彩色方块图标
    cat_key = item.get("category_key", "other")
    btn_icon = icon_value(f"__cat_btn_{cat_key}")
    if btn_icon:
        kwargs["icon_value"] = btn_icon
    else:
        kwargs["icon"] = item.get("fallback_icon", "GEOMETRY_NODES")
    op = layout.operator("node.xl_place_asset_group", **kwargs)
    op.group_name = item["name"]
    op.tooltip = item.get("description", "")


class NODE_PT_xl_geo_assistant(bpy.types.Panel):
    bl_label = "C4D 几何节点助手"
    bl_idname = "NODE_PT_xl_geo_assistant"
    bl_description = "项目节点组：分类浏览、搜索、鼠标跟随放置"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "c4d小工具"

    @classmethod
    def poll(cls, context):
        return getattr(context.space_data, "tree_type", None) == "GeometryNodeTree"

    def draw(self, context):
        layout = self.layout
        props = context.scene.xl_c4d_tool_props

        search = layout.row(align=True)
        search.prop(props, "modifier_search", text="", icon="VIEWZOOM")
        search.label(text=f"{len(load_modifier_manifest())} 组")
        query = props.modifier_search.strip().casefold()
        if query:
            items = []
            for item in load_modifier_manifest():
                text = " ".join((item.get("name", ""), item.get("label", ""), item.get("description", ""))).casefold()
                if query in text:
                    items.append(item)
            box = layout.box()
            box.label(text=f"搜索结果 · {len(items)}", icon="VIEWZOOM")
            grid = box.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
            for item in items:
                _draw_button(grid, item)
            return

        for key, items in grouped_modifier_manifest().items():
            path, color, icon = category_definition(key)
            panel_id = "xl_geo_" + key.replace(".", "_")
            header, body = layout.panel(panel_id, default_closed=key not in {"generator.mesh", "generator.spline_primitive"})
            header.scale_y = 1.35
            cat_icon = icon_value(f"__cat_color_{key}")
            if cat_icon:
                header.label(text=f"{path.replace('/', ' · ')} · {len(items)}", icon_value=cat_icon)
            else:
                header.label(text=f"{path.replace('/', ' · ')} · {len(items)}", icon=icon)
            if body:
                grid = body.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
                for item in items:
                    _draw_button(grid, item)

        layout.label(text="左键按钮后移动鼠标；在画布左键放下", icon="MOUSE_LMB")
        layout.separator()
        layout.operator("node.xl_unify_group_colors", text="统一节点表头颜色", icon="COLOR")


classes = (NODE_PT_xl_geo_assistant,)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
