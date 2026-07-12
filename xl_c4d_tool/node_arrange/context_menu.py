"""【菜单模块：节点编辑器菜单 — 自动排列+居中按钮】
在节点编辑器顶部菜单栏添加排列和居中按钮"""
import bpy


class NODE_MT_xl_arrange_menu(bpy.types.Menu):
    bl_label = "c4d_排列"
    bl_idname = "NODE_MT_xl_arrange_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.na_arrange_selected", text="排列选中节点", icon='NODE_MATERIAL')
        layout.operator("node.na_recenter_selected", text="重新居中", icon='PIVOT_CURSOR')
        layout.separator()
        layout.operator("node.na_batch_arrange", text="排列所有节点树", icon='FILE_FOLDER')
        layout.operator("node.na_batch_recenter", text="居中所有节点树", icon='CENTER_ONLY')


def draw_node_header(self, context):
    """在节点编辑器顶部菜单栏添加排列按钮"""
    if context.space_data.type == 'NODE_EDITOR':
        layout = self.layout
        layout.separator()
        layout.menu(NODE_MT_xl_arrange_menu.bl_idname, text="c4d_排列")


def draw_node_context(self, context):
    """在节点编辑器右键菜单添加排列选项"""
    if context.space_data.type == 'NODE_EDITOR':
        layout = self.layout
        layout.separator()
        layout.menu(NODE_MT_xl_arrange_menu.bl_idname, text="c4d_排列节点")


classes = (NODE_MT_xl_arrange_menu,)


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass
    try:
        bpy.types.NODE_HT_header.append(draw_node_header)
    except Exception:
        pass
    try:
        bpy.types.NODE_MT_context_menu.append(draw_node_context)
    except Exception:
        pass


def unregister():
    try:
        bpy.types.NODE_MT_context_menu.remove(draw_node_context)
    except Exception:
        pass
    try:
        bpy.types.NODE_HT_header.remove(draw_node_header)
    except Exception:
        pass
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
