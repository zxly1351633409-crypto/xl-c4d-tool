import bpy
from ..utils.logger import logger
from ..utils.addon_preferences import get_addon_preferences
from ..utils.icon_manager import icon_value
from ..utils.library_catalog import category_definition, enrich_item, sort_items
from ..utils.modifier_library import grouped_modifier_manifest, load_modifier_manifest


class XlC4dToolPanel(bpy.types.Panel):
    bl_label = "c4d小工具"
    bl_idname = "VIEW3D_PT_xl_c4d_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'c4d小工具'

    def draw(self, context):
        layout = self.layout
        props = getattr(context.scene, "xl_c4d_tool_props", None)

        if not props:
            layout.label(text="属性未初始化", icon='ERROR')
            return

        try:
            from ..node_arrange.operators import HAS_SUGIYAMA as _HAS_NX
        except Exception:
            _HAS_NX = True
        if not _HAS_NX:
            box = layout.box()
            box.label(text="缺少依赖：networkx（节点自动排列）", icon='ERROR')
            box.operator("node.na_install_networkx", text="一键安装 networkx（内置离线包）", icon='IMPORT')
            box.label(text="装好后重启 Blender 或重启用插件", icon='INFO')

        mode_items = {'NORMAL': "正常", 'MATERIAL_ID': "材质ID", 'MIST': "雾场", 'LAYER_ID': "物体ID"}
        mode_icons = {'NORMAL': 'VIEW3D', 'MATERIAL_ID': 'MATERIAL', 'MIST': 'MOD_PHYSICS', 'LAYER_ID': 'GROUP'}
        current = props.current_mode
        layout.label(text=f"当前模式: {mode_items.get(current, current)}", icon=mode_icons.get(current, 'QUESTION'))

        row = layout.row(align=True)
        row.prop(props, "active_tab", expand=True)

        if props.active_tab == 'MODIFIERS':
            self._draw_modifier_library(layout, context, props)
        elif props.active_tab == 'EFFECTS':
            self._draw_effects(layout, props)
        elif props.active_tab == 'TOOLS':
            self._draw_tools(layout, context, props)

    def _draw_modifier_library(self, layout, context, props):
        prefs = get_addon_preferences(context)
        columns = getattr(prefs, "modifier_columns", 2)

        search = layout.row(align=True)
        search.prop(props, "modifier_search", text="", icon="VIEWZOOM")
        search.operator("preferences.xl_open_addon", text="", icon="PREFERENCES")
        query = props.modifier_search.strip().lower()

        if query:
            entries = []
            for item in load_modifier_manifest():
                haystack = f"{item.get('name', '')} {item.get('label', '')} {item.get('description', '')}".lower()
                if query in haystack:
                    entries.append(item)
            box = layout.box()
            box.label(text=f"搜索结果 · {len(entries)} 项", icon="VIEWZOOM")
            self._draw_modifier_buttons(box, sort_items([enrich_item(e) for e in entries]), columns)
        else:
            for key, entries in grouped_modifier_manifest().items():
                path, color, icon = category_definition(key)
                panel_id = "xl_modifier_library_" + key.replace(".", "_")
                header, body = layout.panel(
                    panel_id,
                    default_closed=key not in {"generator.mesh", "generator.spline_primitive"},
                )
                header.scale_y = 1.35
                cat_icon = icon_value(f"__cat_color_{key}")
                if cat_icon:
                    header.label(text=f"{path.replace('/', ' · ')} · {len(entries)}", icon_value=cat_icon)
                else:
                    header.label(text=f"{path.replace('/', ' · ')} · {len(entries)}", icon=icon)
                if body:
                    self._draw_modifier_buttons(body, entries, columns)

        obj = context.active_object
        stack_header, stack_body = layout.panel("xl_c4d_modifier_stack", default_closed=False)
        stack_header.label(text="当前对象修改器栈", icon="MODIFIER")
        if stack_body:
            if obj is None:
                stack_body.label(text="请选择一个对象", icon="INFO")
            else:
                stack_body.label(text=obj.name, icon="OBJECT_DATA")
                node_modifiers = [m for m in obj.modifiers if m.type == "NODES"]
                if not node_modifiers:
                    stack_body.label(text="尚未添加几何节点修改器")
                for modifier in node_modifiers:
                    group = modifier.node_group
                    row = stack_body.row(align=True)
                    row.label(text=group.name if group else modifier.name, icon="GEOMETRY_NODES")
                    row.prop(modifier, "show_viewport", text="", icon="RESTRICT_VIEW_OFF")
                    row.prop(modifier, "show_render", text="", icon="RESTRICT_RENDER_OFF")
                    up = row.operator("object.modifier_move_up", text="", icon="TRIA_UP")
                    up.modifier = modifier.name
                    down = row.operator("object.modifier_move_down", text="", icon="TRIA_DOWN")
                    down.modifier = modifier.name
                    dup = row.operator("object.xl_duplicate_modifier", text="", icon="DUPLICATE")
                    dup.modifier_name = modifier.name
                    remove = row.operator("object.modifier_remove", text="", icon="X")
                    remove.modifier = modifier.name
                stack_body.label(text="详细参数请在属性编辑器的修改器标签中调整", icon="INFO")

    @staticmethod
    def _draw_modifier_buttons(layout, entries, columns):
        if not entries:
            layout.label(text="没有匹配的节点组", icon="INFO")
            return
        grid = layout.grid_flow(
            row_major=True, columns=columns, even_columns=True, even_rows=True, align=True,
        )
        for item in entries:
            grid.scale_y = 1.55
            kwargs = {"text": item.get("label") or item["name"]}
            # 优先使用分类彩色方块图标
            cat_key = item.get("category_key", "other")
            btn_icon = icon_value(f"__cat_btn_{cat_key}")
            if btn_icon:
                kwargs["icon_value"] = btn_icon
            else:
                kwargs["icon"] = item.get("fallback_icon", "GEOMETRY_NODES")
            op = grid.operator("object.xl_apply_c4d_node_group", **kwargs)
            op.group_name = item["name"]
            op.tooltip = item.get("description", "")

    def _draw_effects(self, layout, props):
        # --- 物体ID图效果 (内含集合实例转材质) ---
        box = layout.box()
        row = box.row()
        icon_expand = 'DOWNARROW_HLT' if props.expand_layer_id else 'RIGHTARROW'
        row.prop(props, "expand_layer_id", icon=icon_expand, text="物体ID图效果", emboss=False)

        if props.expand_layer_id:
            col = box.column(align=True)
            col.operator("object.xl_layer_id_setup", text="物体ID图", icon='COLOR')
            col.prop(props, "skip_prefix", text="跳过前缀")
            col.prop(props, "show_object_outline", text="显示物体轮廓")

            # 嵌套子box: 集合实例转材质
            sub_box = col.box()
            sub_row = sub_box.row()
            sub_icon = 'DOWNARROW_HLT' if props.expand_collection_instance else 'RIGHTARROW'
            sub_row.prop(props, "expand_collection_instance", icon=sub_icon, text="集合实例转材质", emboss=False)

            if props.expand_collection_instance:
                sub_col = sub_box.column(align=True)
                sub_col.operator("object.xl_collection_instance_to_material", text="实例→材质平面", icon='NODETREE')
                btn_row = sub_col.row(align=True)
                op = btn_row.operator("object.xl_restore_collection_instances", text="恢复实例", icon='LOOP_BACK')
                op.remove_planes = False
                op2 = btn_row.operator("object.xl_restore_collection_instances", text="恢复+删平面", icon='TRASH')
                op2.remove_planes = True
                sub_col.label(text="选择集合实例后点击转换", icon='INFO')

        # --- 材质ID效果 ---
        box = layout.box()
        row = box.row()
        icon_expand = 'DOWNARROW_HLT' if props.expand_material_id else 'RIGHTARROW'
        row.prop(props, "expand_material_id", icon=icon_expand, text="材质ID效果", emboss=False)

        if props.expand_material_id:
            col = box.column(align=True)
            row_btn = col.row(align=True)
            row_btn.operator("object.xl_material_id_mode", text="材质ID", icon='COLORSET_13_VEC')
            row_btn.operator("object.xl_normal_from_material_id", text="正常", icon='VIEW3D')
            col.prop(props, "show_object_outline", text="显示物体轮廓")

        box = layout.box()
        row = box.row()
        icon_expand = 'DOWNARROW_HLT' if props.expand_mist else 'RIGHTARROW'
        row.prop(props, "expand_mist", icon=icon_expand, text="雾场效果", emboss=False)

        if props.expand_mist:
            col = box.column(align=True)
            row_btn = col.row(align=True)
            row_btn.operator("object.xl_mist_mode", text="雾场", icon='MOD_PHYSICS')
            row_btn.operator("object.xl_normal_from_mist", text="正常", icon='VIEW3D')

            col.separator()
            col.label(text="雾场参数:", icon='SETTINGS')
            col.prop(props, "mist_start", text="起始")
            col.prop(props, "mist_depth", text="深度")
            col.prop(props, "mist_falloff", text="衰减")

        box = layout.box()
        row = box.row()
        icon_expand = 'DOWNARROW_HLT' if props.expand_claymate else 'RIGHTARROW'
        row.prop(props, "expand_claymate", icon=icon_expand, text="一键粘土效果", emboss=False)

        if props.expand_claymate:
            col = box.column(align=True)
            row_btn = col.row(align=True)
            row_btn.operator("object.xl_claymate_enable", text="启用粘土", icon='MATERIAL')
            row_btn.operator("object.xl_claymate_dissolve", text="移除粘土", icon='TRASH')
            try:
                from ..operators.claymate import active_claymate_group
                claymate_group = active_claymate_group()
            except Exception:
                claymate_group = None
            if claymate_group:
                cm_mix_node = next((node for node in claymate_group.nodes if node.name.startswith("CM Mix")), None)
                if cm_mix_node:
                    if len(cm_mix_node.inputs) > 1:
                        col.prop(cm_mix_node.inputs[1], "default_value", text="粘土颜色")
                    if len(cm_mix_node.inputs) > 0:
                        col.prop(cm_mix_node.inputs[0], "default_value", text="启用")

    def _draw_tools(self, layout, context, props):
        header, body = layout.panel("xl_tools_modeling", default_closed=False)
        header.label(text="建模与重拓扑", icon="MESH_GRID")
        if body:
            body.operator("object.xlrt_open_dialog", text="四边重拓扑…", icon="MESH_GRID")
            body.operator("mesh.xl_smart_extrude", text="智能挤出", icon="FACESEL")
            row_loop = body.row(align=True)
            op = row_loop.operator("mesh.xl_loop_selection", text="左右循环", icon="LOOP_FORWARDS")
            op.direction = 'A'
            op = row_loop.operator("mesh.xl_loop_selection", text="上下循环", icon="LOOP_FORWARDS")
            op.direction = 'B'
            body.operator("object.xl_separate_and_keep_lines", text="提取样条线", icon="CURVE_DATA")

        header, body = layout.panel("xl_tools_organization", default_closed=False)
        header.label(text="场景整理", icon="OUTLINER_COLLECTION")
        if body:
            grid = body.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
            grid.operator("object.xl_group_to_empty", icon="EMPTY_AXIS")
            grid.operator("object.xl_ungroup_keep_transform", icon="UNLINKED")
            grid.operator("object.xl_parent_to_active", icon="CON_CHILDOF")
            grid.operator("object.xl_collection_from_selection", icon="NEWFOLDER")
            grid.operator("object.xl_toggle_display_mode", icon="SHADING_WIRE")
            grid.operator("object.xl_align_objects", text="对齐", icon="ALIGN_CENTER")
            grid.operator("object.xl_align_origin", text="原点对齐", icon="OBJECT_ORIGIN")

classes = [
    XlC4dToolPanel,
]


def register():
    for cls in classes:
        # Clean up any stale registrations first
        existing = getattr(bpy.types, cls.bl_idname, None)
        if existing and existing is not cls:
            try:
                bpy.utils.unregister_class(existing)
            except RuntimeError:
                pass
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    logger.info("面板注册完成")


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("面板注销完成")
