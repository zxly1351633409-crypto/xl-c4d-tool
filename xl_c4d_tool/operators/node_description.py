"""节点组说明覆盖层。

右键后把说明固定绘制在节点右侧；再次右键可隐藏。状态保存在节点自身，保存文件后仍然
有效。实现方式参考用户给出的 HoTools 交互，但代码为适配普通 Blender 节点树的独立实现。
"""

from __future__ import annotations

import textwrap

import blf
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from bpy.props import StringProperty


_DRAW_HANDLE = None
_VISIBLE_KEY = "_xl_description_visible"
_WRAP_WIDTH = 34


def _active_group_node(context):
    node = getattr(context, "active_node", None)
    tree = getattr(node, "node_tree", None) if node else None
    return node, tree


def _description(tree):
    if tree is None:
        return ""
    text = (getattr(tree, "description", "") or "").strip()
    asset_data = getattr(tree, "asset_data", None)
    if not text and asset_data is not None:
        text = (asset_data.description or "").strip()
    return text


def _interface_sockets(tree):
    """返回 (inputs, outputs)，每项为 (name, description)。"""
    ins, outs = [], []
    try:
        for item in tree.interface.items_tree:
            if getattr(item, "item_type", "") != "SOCKET":
                continue
            entry = (item.name or "", (getattr(item, "description", "") or "").strip())
            if getattr(item, "in_out", "") == "INPUT":
                ins.append(entry)
            else:
                outs.append(entry)
    except (AttributeError, ReferenceError):
        pass
    return ins, outs


def _structured_lines(tree, category_label=""):
    """构建结构化说明行：[(style, text), ...]。

    style: 'title' 标题 / 'sub' 小节标题 / 'body' 正文 / 'item' 列表项 / 'dim' 次要信息。
    内容直接复用节点组已有的手册式 description 与逐项 socket 说明，做到“新手手册”级别。
    """
    lines = [("title", tree.name)]
    if category_label:
        lines.append(("dim", "分类：" + category_label))

    description = _description(tree)
    if description:
        lines.append(("sub", "用途说明"))
        for paragraph in description.splitlines():
            paragraph = paragraph.rstrip()
            if not paragraph:
                continue
            stripped = paragraph.lstrip("•·-  ")
            style = "item" if paragraph.lstrip().startswith(("•", "·", "-")) else "body"
            for chunk in textwrap.wrap(stripped, width=_WRAP_WIDTH) or [""]:
                lines.append((style, ("• " + chunk) if style == "item" else chunk))
                style = "body" if style == "item" else style  # 续行不再加项目符号
    else:
        lines.append(("body", "此节点组暂未填写说明。"))

    ins, outs = _interface_sockets(tree)
    if ins:
        lines.append(("sub", f"输入参数 · {len(ins)} 项"))
        for name, desc in ins[:14]:
            head = "• " + name + ("：" if desc else "")
            wrapped = textwrap.wrap(desc, width=_WRAP_WIDTH - 2) if desc else []
            lines.append(("item", head + (wrapped[0] if wrapped else "")))
            for cont in wrapped[1:]:
                lines.append(("dim", "  " + cont))
        if len(ins) > 14:
            lines.append(("dim", f"……另有 {len(ins) - 14} 项输入"))
    if outs:
        names = "、".join(n for n, _ in outs[:6])
        lines.append(("sub", "输出"))
        lines.append(("item", "• " + names))
    return lines


def _absolute_location(node):
    x, y = node.location
    parent = node.parent
    while parent is not None:
        x += parent.location[0]
        y += parent.location[1]
        parent = parent.parent
    return float(x), float(y)


def _tag_node_editors():
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        return
    for window in wm.windows:
        for area in window.screen.areas:
            if area.type == "NODE_EDITOR":
                area.tag_redraw()


def _category_label(node):
    try:
        from ..utils.library_catalog import classify_group, category_definition
        key = node.get("_xl_category_key") or classify_group(node.node_tree.name)
        return category_definition(key)[0]
    except Exception:
        return ""


def _draw_rect(x0, y0, x1, y1, color):
    shader = gpu.shader.from_builtin("UNIFORM_COLOR")
    gpu.state.blend_set("ALPHA")
    batch = batch_for_shader(
        shader, "TRIS",
        {"pos": [(x0, y0), (x1, y0), (x1, y1), (x0, y0), (x1, y1), (x0, y1)]},
    )
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)
    gpu.state.blend_set("NONE")


def _draw_overlay():
    space = getattr(bpy.context, "space_data", None)
    region = getattr(bpy.context, "region", None)
    if space is None or space.type != "NODE_EDITOR" or region is None:
        return
    tree = getattr(space, "edit_tree", None) or getattr(space, "node_tree", None)
    if tree is None:
        return

    ui_scale = bpy.context.preferences.system.ui_scale
    font_id = 0
    size_body = max(11, int(12 * ui_scale))
    size_title = max(13, int(15 * ui_scale))
    size_sub = max(12, int(13 * ui_scale))
    line_h = int(17 * ui_scale)
    pad = int(10 * ui_scale)

    style_color = {
        "title": None,                       # 用分类色
        "sub": (0.85, 0.90, 0.95, 1.0),
        "body": (0.86, 0.87, 0.88, 1.0),
        "item": (0.78, 0.82, 0.86, 1.0),
        "dim": (0.62, 0.65, 0.69, 1.0),
    }
    style_size = {"title": size_title, "sub": size_sub, "body": size_body,
                  "item": size_body, "dim": max(10, size_body - 1)}

    for node in tree.nodes:
        group = getattr(node, "node_tree", None)
        if group is None or not bool(node.get(_VISIBLE_KEY, False)):
            continue
        lines = _structured_lines(group, _category_label(node))
        cat_color = tuple(node.color) if getattr(node, "use_custom_color", False) else (0.45, 0.62, 0.58)
        title_color = (min(1.0, cat_color[0] + 0.34), min(1.0, cat_color[1] + 0.34),
                       min(1.0, cat_color[2] + 0.34), 1.0)

        x, y = _absolute_location(node)
        x += float(getattr(node, "width", 160.0)) + 16.0
        try:
            rx, ry = region.view2d.view_to_region(x, y, clip=False)
        except (AttributeError, RuntimeError):
            continue

        # 计算文本块尺寸
        max_w = 10
        for style, text in lines:
            blf.size(font_id, style_size[style])
            max_w = max(max_w, blf.dimensions(font_id, text)[0])
        block_w = max_w + pad * 2
        block_h = len(lines) * line_h + pad * 2

        top = ry + line_h
        # 背景面板 + 分类色顶条
        _draw_rect(rx - pad, top - block_h, rx - pad + block_w, top, (0.10, 0.11, 0.13, 0.92))
        _draw_rect(rx - pad, top - 4, rx - pad + block_w, top,
                   (cat_color[0], cat_color[1], cat_color[2], 0.95))

        blf.enable(font_id, blf.SHADOW)
        blf.shadow(font_id, 3, 0.0, 0.0, 0.0, 0.55)
        blf.shadow_offset(font_id, 1, -1)
        cy = ry
        for style, text in lines:
            blf.size(font_id, style_size[style])
            col = title_color if style == "title" else style_color[style]
            blf.color(font_id, *col)
            blf.position(font_id, rx, cy, 0)
            blf.draw(font_id, text)
            cy -= line_h
        blf.disable(font_id, blf.SHADOW)


class NODE_OT_xl_toggle_group_description(bpy.types.Operator):
    bl_idname = "node.xl_toggle_group_description"
    bl_label = "显示/隐藏节点组说明"
    bl_description = "把该节点组的用途与主要输入固定显示在节点右侧"

    tree_name: StringProperty(options={"HIDDEN"})
    node_name: StringProperty(options={"HIDDEN"})

    def execute(self, context):
        tree = bpy.data.node_groups.get(self.tree_name)
        if tree is None:
            tree = getattr(context.space_data, "edit_tree", None)
        node = tree.nodes.get(self.node_name) if tree is not None else None
        if node is None or getattr(node, "node_tree", None) is None:
            self.report({"WARNING"}, "找不到要显示说明的节点组")
            return {"CANCELLED"}
        node[_VISIBLE_KEY] = not bool(node.get(_VISIBLE_KEY, False))
        _tag_node_editors()
        return {"FINISHED"}


def draw_node_context_menu(self, context):
    node, tree = _active_group_node(context)
    if node is None or tree is None:
        return
    self.layout.separator()
    visible = bool(node.get(_VISIBLE_KEY, False))
    op = self.layout.operator(
        NODE_OT_xl_toggle_group_description.bl_idname,
        text="隐藏节点组说明" if visible else "显示节点组说明",
        icon="HIDE_OFF" if visible else "INFO",
    )
    op.tree_name = getattr(node.id_data, "name", "")
    op.node_name = node.name


classes = (NODE_OT_xl_toggle_group_description,)


def register():
    global _DRAW_HANDLE
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    bpy.types.NODE_MT_context_menu.append(draw_node_context_menu)
    if _DRAW_HANDLE is None:
        _DRAW_HANDLE = bpy.types.SpaceNodeEditor.draw_handler_add(_draw_overlay, (), "WINDOW", "POST_PIXEL")


def unregister():
    global _DRAW_HANDLE
    try:
        bpy.types.NODE_MT_context_menu.remove(draw_node_context_menu)
    except (ValueError, RuntimeError):
        pass
    if _DRAW_HANDLE is not None:
        try:
            bpy.types.SpaceNodeEditor.draw_handler_remove(_DRAW_HANDLE, "WINDOW")
        except (ValueError, RuntimeError):
            pass
        _DRAW_HANDLE = None
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
