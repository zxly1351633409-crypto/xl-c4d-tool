"""【面板：c4d_自动排列节点】
使用Sugiyama算法自动排列选中节点，支持批量处理全部节点树
位置：Node Editor > Sidebar > c4d小工具（最顶部）"""
from bpy.types import Context, Panel
from bpy.utils import register_class, unregister_class
from .utils import get_ntree
from .operators import HAS_SUGIYAMA


class NA_PT_ArrangeSelected(Panel):
    """【面板：c4d_自动排列节点 + 重新居中】
    排列选中节点 / 批量排列所有节点树 / 重新居中"""
    bl_label = "c4d_自动排列节点"
    bl_idname = "NA_PT_ArrangeSelected"
    bl_description = "Sugiyama自动排列节点布局，支持选中节点/全部节点排列及重新居中"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "c4d小工具"
    bl_order = 0

    @classmethod
    def poll(cls, context: Context) -> bool:
        return context.space_data.type == 'NODE_EDITOR' and get_ntree() is not None

    def draw(self, context: Context) -> None:
        layout = self.layout
        settings = context.scene.na_settings
        props = context.scene.xl_c4d_tool_props

        # 折叠开关
        layout.prop(props, "node_arrange_folded", text="",
                     icon='RIGHTARROW' if props.node_arrange_folded else 'DOWNARROW_HLT',
                     emboss=False, toggle=True)
        if props.node_arrange_folded:
            return

        layout.use_property_split = True

        # === 排列参数 ===
        header, panel = layout.panel("spacing", default_closed=True)
        header.label(text="间距")
        if panel:
            panel.prop(settings, "margin", text=" ")

        header, panel = layout.panel("alignment", default_closed=True)
        header.label(text="对齐")
        if panel:
            col = panel.column()
            col.prop(settings, "direction", text="节点")
            col.prop(settings, "socket_alignment", text="插槽")

        header, panel = layout.panel("crossed_links", default_closed=True)
        header.label(text="交叉连线优化")
        if panel:
            col = panel.column()
            col.prop(settings, "iterations")

        header, panel = layout.panel("reroutes", default_closed=True)
        header.label(text="重路由")
        if panel:
            col = panel.column(heading="重路由")
            col.prop(settings, "add_reroutes", text="添加")
            sub = col.row()
            sub.active = settings.add_reroutes
            sub.prop(settings, "keep_reroutes_outside_frames", text="放置在框外")

        header, panel = layout.panel("collapsed_nodes", default_closed=True)
        header.label(text="折叠节点")
        if panel:
            col = panel.column()
            col.prop(settings, "stack_collapsed")
            sub = col.row()
            sub.active = settings.stack_collapsed
            sub.prop(settings, "stack_margin_y_fac")

        layout.use_property_split = False
        layout.prop(settings, "arrange_mode", expand=True)
        layout.use_property_split = True
        if not HAS_SUGIYAMA:
            layout.operator("node.na_install_networkx", text="安装networkx库以启用排列功能", icon='ERROR')
        elif settings.arrange_mode == 'NODES':
            layout.operator("node.na_arrange_selected", text="排列选中节点")
        else:
            layout.operator("node.na_batch_arrange")

        # === 重新居中 ===
        layout.separator()
        layout.use_property_split = True
        header, panel = layout.panel("recenter", default_closed=True)
        header.label(text="重新居中")
        if panel:
            panel.prop(settings, "origin")
            panel.use_property_split = False
            panel.prop(settings, "recenter_mode", expand=True)
            if settings.recenter_mode == 'NODES':
                panel.operator("node.na_recenter_selected", text="重新居中选中节点")
            else:
                panel.operator("node.na_batch_recenter")


classes = (
    NA_PT_ArrangeSelected,
)


def register() -> None:
    for cls in classes:
        register_class(cls)


def unregister() -> None:
    for cls in reversed(classes):
        unregister_class(cls)
