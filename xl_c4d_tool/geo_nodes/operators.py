"""在几何节点编辑器中以 C4D 式“拿起后放下”方式添加项目节点组。"""

from __future__ import annotations

import bpy
from bpy.props import StringProperty

from ..utils.library_catalog import category_definition, classify_group
from ..utils.modifier_library import ensure_node_group


import colorsys

# 几何节点树 color_tag 实际可用的取值（子集）-> 对应主题色属性名。
# color_tag 决定“节点头部/标签底色”（展开时标签名那条），用 Blender 固定主题色板。
# 注意：几何节点树不接受 SHADER/DISTORT/FILTER/GROUP 等，仅以下有效。
_VALID_TAG_THEME = {
    "COLOR": "color_node",
    "CONVERTER": "converter_node",
    "GEOMETRY": "geometry_node",
    "INPUT": "input_node",
    "TEXTURE": "texture_node",
    "VECTOR": "vector_node",
    "ATTRIBUTE": "attribute_node",
    "OUTPUT": "output_node",
}


def _nearest_color_tag(rgb):
    """按色相把分类库色匹配到最接近的有效 color_tag，使节点头部色与库标签色一致。"""
    try:
        import bpy
        ne = bpy.context.preferences.themes[0].node_editor
    except Exception:
        return "NONE"
    h, s, _v = colorsys.rgb_to_hsv(*rgb[:3])
    if s < 0.12:  # 近灰色 -> 默认头色
        return "NONE"
    best, best_d = "NONE", 9.0
    for tag, attr in _VALID_TAG_THEME.items():
        try:
            th = colorsys.rgb_to_hsv(*[c for c in getattr(ne, attr)[:3]])[0]
        except Exception:
            continue
        dh = abs(h - th)
        dh = min(dh, 1.0 - dh)  # 色相环形距离
        if dh < best_d:
            best_d, best = dh, tag
    return best


def apply_group_header_color(node) -> bool:
    """只设置节点组的“头部色标签(color_tag)”，使其与该组在修改器库里的分类标签色一致；
    不再给节点主体(node.color)上色。返回是否成功设置。
    """
    tree = getattr(node, "node_tree", None)
    if node.bl_idname != "GeometryNodeGroup" or tree is None:
        return False
    name = tree.name
    if not (name.startswith("XL_") or name.startswith("C4D_")):
        return False
    key = classify_group(name)
    _path, lib_color, _icon = category_definition(key)
    tag = _nearest_color_tag(lib_color)
    try:
        if hasattr(tree, "color_tag"):
            tree.color_tag = tag
    except Exception:
        pass
    # 只改头部(color_tag)，不给节点主体上色（用户要求）
    try:
        node.use_custom_color = False
    except Exception:
        pass
    node["_xl_category_key"] = key
    return True


class NODE_OT_xl_unify_group_colors(bpy.types.Operator):
    bl_idname = "node.xl_unify_group_colors"
    bl_label = "统一节点表头颜色"
    bl_description = "按分类重新给本工程所有 XL/C4D 节点组实例的表头上色，修复历史不一致"
    bl_options = {"REGISTER", "UNDO"}

    all_trees: bpy.props.BoolProperty(
        name="处理全部节点树",
        description="勾选则处理整个文件的所有几何节点树；否则仅当前编辑的树",
        default=True,
    )

    def execute(self, context):
        trees = []
        if self.all_trees:
            trees = [t for t in bpy.data.node_groups if t.bl_idname == "GeometryNodeTree"]
        else:
            tree = getattr(context.space_data, "edit_tree", None)
            if tree is not None:
                trees = [tree]
        count = 0
        for tree in trees:
            for node in tree.nodes:
                if apply_group_header_color(node):
                    count += 1
        self.report({"INFO"}, f"已统一 {count} 个节点组表头颜色")
        return {"FINISHED"}


class NODE_OT_xl_place_asset_group(bpy.types.Operator):
    bl_idname = "node.xl_place_asset_group"
    bl_label = "放置 C4D 节点组"
    bl_description = "节点会跟随鼠标；左键放下，右键或 Esc 取消"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    group_name: StringProperty(name="节点组")
    tooltip: StringProperty(options={"HIDDEN"})
    _node = None
    _tree = None
    _window_region = None

    @classmethod
    def description(cls, _context, properties):
        return properties.tooltip or cls.bl_description

    @classmethod
    def poll(cls, context):
        space = getattr(context, "space_data", None)
        return bool(
            context.area and context.area.type == "NODE_EDITOR"
            and space and space.tree_type == "GeometryNodeTree"
            and space.edit_tree
        )

    def _move_to_mouse(self, context, event):
        if self._node is None or self._window_region is None:
            return
        region_x = event.mouse_x - self._window_region.x
        region_y = event.mouse_y - self._window_region.y
        self._node.location = self._window_region.view2d.region_to_view(
            region_x, region_y
        )

    def invoke(self, context, event):
        try:
            group = ensure_node_group(self.group_name)
        except (OSError, RuntimeError) as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self._tree = context.space_data.edit_tree
        self._window_region = next((region for region in context.area.regions if region.type == "WINDOW"), None)
        if self._window_region is None:
            return {"CANCELLED"}
        for other in self._tree.nodes:
            other.select = False
        self._node = self._tree.nodes.new("GeometryNodeGroup")
        self._node.node_tree = group
        self._node.label = group.name.replace("XL_", "", 1)
        # 几何节点助手放置：按分类给节点上色（用户偏好）。
        apply_group_header_color(self._node)
        self._node.width = max(180.0, self._node.width)
        self._node.select = True
        self._tree.nodes.active = self._node
        self._move_to_mouse(context, event)
        context.window.cursor_modal_set("CROSSHAIR")
        context.window_manager.modal_handler_add(self)
        context.area.header_text_set("移动鼠标定位 · 左键放下 · 右键/Esc 取消")
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            self._move_to_mouse(context, event)
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


classes = (NODE_OT_xl_place_asset_group, NODE_OT_xl_unify_group_colors)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
