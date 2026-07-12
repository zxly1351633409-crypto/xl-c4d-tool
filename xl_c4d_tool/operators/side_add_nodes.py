"""原生节点鼠标放置、收藏与稳定的侧栏自动显隐。"""

from __future__ import annotations

import time

import bpy
from bpy.app.handlers import persistent
from bpy.props import BoolProperty, StringProperty

from ..utils.addon_preferences import get_addon_preferences
from ..utils.node_discovery import get_category_color_prop_name, get_complete_node_data, resolve_tree_type


def _split_ids(value):
    return [item for item in (value or "").split("|") if item]


class XL_OT_add_catalog_node(bpy.types.Operator):
    bl_idname = "node.xl_add_catalog_node"
    bl_label = "添加节点"
    bl_description = "节点跟随鼠标；在画布左键放下，右键或 Esc 取消"
    bl_options = {"REGISTER", "UNDO"}
    node_type: StringProperty()
    category: StringProperty(options={"HIDDEN"})
    _node = None
    _tree = None
    _window_region = None

    def _resolved_category(self, context):
        if self.category not in {"", "搜索", "收藏", "最近", "其他"}:
            return self.category
        catalog = get_complete_node_data(context).get(resolve_tree_type(context), {})
        for category, payload in catalog.items():
            if any(node_id == self.node_type for node_id, _label in payload.get("nodes", ())):
                return category
        return "其他"

    def _move_to_mouse(self, event):
        if self._node is None or self._window_region is None:
            return
        x = event.mouse_x - self._window_region.x
        y = event.mouse_y - self._window_region.y
        self._node.location = self._window_region.view2d.region_to_view(x, y)

    def invoke(self, context, event):
        tree = getattr(context.space_data, "edit_tree", None)
        if tree is None:
            self.report({"WARNING"}, "请先打开可编辑节点树")
            return {"CANCELLED"}
        prefs = get_addon_preferences(context)
        if prefs is not None:
            recent = [self.node_type] + [x for x in _split_ids(prefs.node_recent) if x != self.node_type]
            prefs.node_recent = "|".join(recent[:16])
        self._window_region = next((region for region in context.area.regions if region.type == "WINDOW"), None)
        if self._window_region is None:
            return {"CANCELLED"}
        try:
            self._tree = tree
            for node in tree.nodes:
                node.select = False
            self._node = tree.nodes.new(self.node_type)
            self._node.select = True
            tree.nodes.active = self._node
            # 快捷节点(T面板)：保持原生节点原样，不自动上色（用户偏好）
            self._node["_xl_category"] = self._resolved_category(context)
            self._move_to_mouse(event)
            context.window.cursor_modal_set("CROSSHAIR")
            context.window_manager.modal_handler_add(self)
            context.area.header_text_set("移动鼠标定位 · 左键放下 · 右键/Esc 取消")
            return {"RUNNING_MODAL"}
        except (RuntimeError, TypeError) as exc:
            self.report({"ERROR"}, f"当前节点树不能添加该节点：{exc}")
            return {"CANCELLED"}

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self._move_to_mouse(event)
            context.area.tag_redraw()
            return {"RUNNING_MODAL"}
        if event.type == "LEFTMOUSE" and event.value == "PRESS":
            self._finish(context)
            return {"FINISHED"}
        if event.type in {"RIGHTMOUSE", "ESC"} and event.value == "PRESS":
            if self._tree is not None and self._node is not None:
                try:
                    self._tree.nodes.remove(self._node)
                except (ReferenceError, RuntimeError):
                    pass
            self._finish(context)
            return {"CANCELLED"}
        return {"RUNNING_MODAL"}

    def _finish(self, context):
        try:
            context.window.cursor_modal_restore()
            context.area.header_text_set(None)
            context.area.tag_redraw()
        except (ReferenceError, RuntimeError):
            pass
        self._node = None
        self._tree = None
        self._window_region = None


class XL_OT_toggle_node_favorite(bpy.types.Operator):
    bl_idname = "node.xl_toggle_favorite"
    bl_label = "收藏节点"
    bl_description = "加入或移出收藏节点"
    node_type: StringProperty()

    def execute(self, context):
        prefs = get_addon_preferences(context)
        if prefs is None:
            return {"CANCELLED"}
        favorites = _split_ids(prefs.node_favorites)
        if self.node_type in favorites:
            favorites.remove(self.node_type)
        else:
            favorites.append(self.node_type)
        prefs.node_favorites = "|".join(favorites)
        return {"FINISHED"}


class XL_OT_auto_show_toolbar(bpy.types.Operator):
    bl_idname = "node.xl_auto_show_toolbar"
    bl_label = "自动显示节点侧栏"
    bl_description = "使用显示/隐藏双阈值和冷却时间，稳定控制 T/N 面板"
    bl_options = {"REGISTER"}
    enable: BoolProperty(default=True)
    _running = False
    _last_change = {}

    @staticmethod
    def _region_attr(region_type):
        return "show_region_toolbar" if region_type == "TOOLS" else "show_region_ui"

    def _update_region(self, area, region_type, desired):
        key = (area.as_pointer(), region_type)
        now = time.monotonic()
        if now - self._last_change.get(key, 0.0) < 0.30:
            return
        attr = self._region_attr(region_type)
        for space in area.spaces:
            if space.type != "NODE_EDITOR" or not hasattr(space, attr):
                continue
            if bool(getattr(space, attr)) == desired:
                return
            setattr(space, attr, desired)
            self._last_change[key] = now
            area.tag_redraw()
            return

    def modal(self, context, event):
        prefs = get_addon_preferences(context)
        if prefs is None or not prefs.auto_show_toolbar:
            self.cancel(context)
            return {"CANCELLED"}
        if event.type != "MOUSEMOVE":
            return {"PASS_THROUGH"}
        show_at = prefs.auto_show_distance
        hide_at = max(prefs.auto_hide_distance, show_at + 80)
        modes = {"BOTH": ("TOOLS", "UI"), "TOOLS": ("TOOLS",), "UI": ("UI",)}[prefs.auto_show_panel_type]
        for area in context.screen.areas:
            if area.type != "NODE_EDITOR":
                continue
            inside = area.x <= event.mouse_x <= area.x + area.width and area.y <= event.mouse_y <= area.y + area.height
            if not inside:
                continue
            left = event.mouse_x - area.x
            right = area.x + area.width - event.mouse_x
            for region_type in modes:
                distance = left if region_type == "TOOLS" else right
                attr = self._region_attr(region_type)
                current = bool(getattr(area.spaces.active, attr, False))
                if not current and distance <= show_at:
                    self._update_region(area, region_type, True)
                elif current and distance >= hide_at:
                    self._update_region(area, region_type, False)
        return {"PASS_THROUGH"}

    def execute(self, context):
        prefs = get_addon_preferences(context)
        if prefs is None:
            return {"CANCELLED"}
        prefs.auto_show_toolbar = self.enable
        if not self.enable:
            self.cancel(context)
            return {"FINISHED"}
        if not self.__class__._running:
            self.__class__._running = True
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        return {"FINISHED"}

    def cancel(self, _context):
        self.__class__._running = False
        self.__class__._last_change.clear()


@persistent
def _on_load_post(_dummy):
    prefs = get_addon_preferences()
    if prefs is not None and prefs.auto_show_toolbar and not XL_OT_auto_show_toolbar._running:
        try:
            bpy.ops.node.xl_auto_show_toolbar(enable=True)
        except RuntimeError:
            pass


classes = (XL_OT_add_catalog_node, XL_OT_toggle_node_favorite, XL_OT_auto_show_toolbar)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    if _on_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(_on_load_post)


def unregister():
    if _on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_on_load_post)
    XL_OT_auto_show_toolbar._running = False
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
