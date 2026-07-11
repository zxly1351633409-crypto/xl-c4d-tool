"""xl_c4d_tool 全局偏好设置。"""

from __future__ import annotations

import bpy

from .utils.node_discovery import get_category_color_prop_name, get_node_data


class XL_C4D_Tool_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "xl_c4d_tool"

    node_show_in_t_panel: bpy.props.BoolProperty(
        name="在 T 面板显示快捷节点", default=True,
    )
    node_show_in_n_panel: bpy.props.BoolProperty(
        name="在 N 面板显示快捷节点", default=False,
    )
    node_show_category_colors: bpy.props.BoolProperty(
        name="显示分类提示色", default=True,
    )
    node_columns: bpy.props.IntProperty(
        name="节点按钮列数", default=2, min=1, max=4,
    )
    node_max_search_results: bpy.props.IntProperty(
        name="搜索结果上限", default=24, min=6, max=100,
    )
    node_favorites: bpy.props.StringProperty(
        name="收藏节点", default="",
        description="由快捷节点面板管理的节点类型列表",
    )
    node_recent: bpy.props.StringProperty(
        name="最近节点", default="",
        description="由快捷节点面板自动维护",
    )
    auto_show_toolbar: bpy.props.BoolProperty(
        name="自动显示/隐藏节点侧栏", default=False,
    )
    auto_show_panel_type: bpy.props.EnumProperty(
        name="自动侧栏类型",
        items=(
            ("BOTH", "T + N", "同时控制工具栏与侧栏"),
            ("TOOLS", "仅 T", "只控制左侧工具栏"),
            ("UI", "仅 N", "只控制右侧侧栏"),
        ),
        default="BOTH",
    )
    auto_show_distance: bpy.props.IntProperty(
        name="显示距离", default=80, min=10, max=300,
    )
    auto_hide_distance: bpy.props.IntProperty(
        name="隐藏距离", default=360, min=30, max=800,
    )
    previews_enabled_by_default: bpy.props.BoolProperty(
        name="默认显示节点预览",
        default=True,
        description="开启后，着色器节点默认显示渲染缩略图；关闭后只对手动开启的节点显示",
    )
    update_during_animation_playback: bpy.props.BoolProperty(
        name="播放动画时更新预览",
        default=True,
        description="复杂材质场景中可关闭，以减少动画播放时的预览计算",
    )
    thumb_scale: bpy.props.FloatProperty(
        name="预览缩放",
        default=50,
        min=1,
        max=100,
        subtype="PERCENTAGE",
        description="节点上方缩略图的显示尺寸",
    )
    thumb_resolution: bpy.props.IntProperty(
        name="预览分辨率",
        default=150,
        min=50,
        soft_max=300,
        max=500,
        description="越高越清晰，但更新会更慢",
    )
    background_pattern: bpy.props.EnumProperty(
        name="透明背景",
        items=(
            ("CHECKER", "棋盘格", "透明材质使用棋盘格背景"),
            ("WHITE", "纯色", "透明材质使用单色背景"),
        ),
        default="CHECKER",
    )
    background_color_1: bpy.props.FloatVectorProperty(
        name="背景色 1",
        subtype="COLOR",
        size=3,
        min=0.0,
        max=1.0,
        default=(0.994, 0.994, 0.994),
    )
    background_color_2: bpy.props.FloatVectorProperty(
        name="背景色 2",
        subtype="COLOR",
        size=3,
        min=0.0,
        max=1.0,
        default=(0.8086, 0.8086, 0.8086),
    )
    show_help: bpy.props.BoolProperty(
        name="显示预览提示",
        default=True,
        description="当纹理缩放过大时，在缩略图旁显示可忽略缩放的提示",
    )
    enable_debug_output: bpy.props.BoolProperty(
        name="节点预览调试输出",
        default=False,
        description="输出节点预览后台进程日志；通常保持关闭",
    )
    modifier_columns: bpy.props.IntProperty(
        name="修改器按钮列数", default=2, min=1, max=3,
    )
    show_modifier_descriptions: bpy.props.BoolProperty(
        name="修改器库显示说明", default=True,
    )

    def draw(self, _context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        node_box = layout.box()
        node_box.label(text="快捷节点浏览器", icon="NODETREE")
        node_box.prop(self, "node_show_in_t_panel")
        node_box.prop(self, "node_show_in_n_panel")
        node_box.prop(self, "node_show_category_colors")
        node_box.prop(self, "node_columns")
        node_box.prop(self, "node_max_search_results")

        color_header, color_body = node_box.panel("xl_preferences_node_colors", default_closed=True)
        color_header.label(text="分类颜色", icon="COLOR")
        if color_body:
            seen = set()
            for categories in get_node_data().values():
                for category, payload in categories.items():
                    if category in seen:
                        continue
                    seen.add(category)
                    prop = get_category_color_prop_name(category)
                    if hasattr(self, prop):
                        color_body.prop(self, prop, text=category)

        auto_box = layout.box()
        auto_box.label(text="侧栏自动显示", icon="MENU_PANEL")
        auto_box.prop(self, "auto_show_toolbar")
        auto_box.prop(self, "auto_show_panel_type")
        auto_box.prop(self, "auto_show_distance")
        auto_box.prop(self, "auto_hide_distance")

        preview_box = layout.box()
        preview_box.label(text="节点显示 / 渲染缩略图", icon="IMAGE_DATA")
        preview_box.prop(self, "previews_enabled_by_default")
        preview_box.prop(self, "update_during_animation_playback")
        row = preview_box.row(align=True)
        row.prop(self, "thumb_scale")
        row.prop(self, "thumb_resolution")
        preview_box.prop(self, "background_pattern", expand=True)
        row = preview_box.row(align=True)
        row.prop(self, "background_color_1")
        if self.background_pattern == "CHECKER":
            row.prop(self, "background_color_2")
        preview_box.prop(self, "show_help")
        preview_box.prop(self, "enable_debug_output")
        preview_box.label(text="基于 Node Preview v1.21，作者 Simon Wendsche (B.Y.O.B.)，GPL-3.0-or-later。", icon="INFO")

        modifier_box = layout.box()
        modifier_box.label(text="C4D 修改器库", icon="MODIFIER")
        modifier_box.prop(self, "modifier_columns")
        modifier_box.prop(self, "show_modifier_descriptions")
        modifier_box.label(text="节点资产随插件打包；首次使用某节点组时自动追加到当前文件。", icon="INFO")

        repair_box = layout.box()
        repair_box.label(text="安装与编码诊断", icon="FILE_SCRIPT")
        repair_box.label(text="用于其他旧插件的 addon_zh.py 非 UTF-8 警告；转换前会自动备份。")
        repair_box.operator("preferences.xl_repair_python_encoding", icon="FILE_REFRESH")

        info = layout.box()
        info.label(text="模块入口", icon="OUTLINER")
        info.label(text="3D 视图 > N > c4d小工具：节点组赋予、修改器栈、重拓扑与常用工具")
        info.label(text="节点编辑器：彩色折叠分类 + 搜索 + 收藏/最近 + 鼠标跟随放置")
        info.label(text="节点组右键：查看节点组描述")
        info.label(text="xl_c4d_tool v3.4.0 · Blender 5.1")


def _install_category_color_properties():
    annotations = XL_C4D_Tool_AddonPreferences.__annotations__
    seen = set()
    for categories in get_node_data().values():
        for category, payload in categories.items():
            if category in seen:
                continue
            seen.add(category)
            prop = get_category_color_prop_name(category)
            annotations[prop] = bpy.props.FloatVectorProperty(
                name=f"{category}颜色",
                subtype="COLOR",
                size=4,
                min=0.0,
                max=1.0,
                default=tuple(payload.get("color", [0.5, 0.5, 0.5, 1.0])),
            )


_install_category_color_properties()


classes = (XL_C4D_Tool_AddonPreferences,)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
