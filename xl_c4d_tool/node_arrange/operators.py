import bpy

try:
    from bl_operators.node_editor.node_functions import node_editor_poll
except ImportError:
    def node_editor_poll(cls, context):
        return (context.space_data.type == 'NODE_EDITOR'
                and context.space_data.edit_tree is not None)

from bpy.types import Context, Operator
from mathutils import Vector
from operator import attrgetter
from statistics import fmean
from collections.abc import Iterable
from typing import Type, cast

from . import config
from .utils import abs_loc, get_ntree

try:
    from .arrange.sugiyama import sugiyama_layout
    HAS_SUGIYAMA = True
except ImportError:
    sugiyama_layout = None
    HAS_SUGIYAMA = False


class NodeOperator:
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls: Type[Operator], context: Context) -> bool:
        if not node_editor_poll(cls, context):
            return False
        if get_ntree().bl_idname == 'NodeTreeUndefined':
            cls.poll_message_set("当前节点树未定义")
            return False
        return True


class NA_OT_ArrangeSelected(NodeOperator, Operator):
    bl_idname = "node.na_arrange_selected"
    bl_label = "排列选中"
    bl_description = "排列选中的节点"

    def execute(self, context: Context) -> set[str]:
        if not HAS_SUGIYAMA:
            self.report({'ERROR'}, "需要networkx库: pip install networkx")
            return {'CANCELLED'}
        ntree = get_ntree()
        selected = [n for n in ntree.nodes if n.select]
        if not selected:
            self.report({'WARNING'}, "没有选中节点")
            return {'CANCELLED'}
        config.selected = selected
        config.SETTINGS = context.scene.na_settings
        config.MARGIN = Vector(config.SETTINGS.margin).freeze()
        try:
            sugiyama_layout(ntree)
        finally:
            config.reset()
        return {'FINISHED'}


def get_all_ntrees() -> list:
    bl_data = []
    for key, prop in bpy.types.BlendData.bl_rna.properties.items():
        if prop.type != 'COLLECTION' or key == 'scenes':
            continue
        props = prop.fixed_type.bl_rna.properties
        if {'node_tree', 'nodes'}.intersection(props.keys()):
            bl_data.extend(getattr(bpy.data, key))
    return bl_data


def batch_modify(bl_data, cls, *, redraw_ui: bool) -> int:
    context = cast(Context, bpy.context)
    area = context.area
    space = cast(bpy.types.SpaceNodeEditor, context.space_data)
    path = space.path
    old_path = [p.node_tree for p in path]
    if redraw_ui:
        old_ui_type = area.ui_type
        area.ui_type = 'ShaderNodeTree'
    op = attrgetter(cls.bl_idname)(bpy.ops)
    count = 0
    for id_data in bl_data:
        if not getattr(id_data, 'use_nodes', True):
            continue
        ntree = cast(bpy.types.NodeTree, getattr(id_data, 'node_tree', id_data))
        path.append(ntree)
        if space.edit_tree != ntree:
            path.append(ntree)
        if not cls.poll(context):
            path.pop()
            continue
        nodes = ntree.nodes
        old_selection = {n for n in nodes if n.select}
        for node in nodes:
            node.select = True
        old_view_center = ntree.view_center.copy()
        if redraw_ui:
            bpy.ops.wm.redraw_timer(type='DRAW', iterations=0)
        op()
        count += 1
        vec = ntree.view_center - old_view_center
        bpy.ops.transform.translate(value=(*vec, 0))
        for node in nodes:
            node.select = node in old_selection
        path.pop()
    if redraw_ui:
        path.clear()
        area.ui_type = old_ui_type
        path.start(old_path[0])
        for ntree in old_path[1:]:
            path.append(ntree)
    return count


class NA_OT_BatchArrange(NodeOperator, Operator):
    bl_idname = "node.na_batch_arrange"
    bl_label = "批量排列所有节点树"
    bl_description = "排列当前.blend文件中所有节点树"

    def execute(self, context: Context):
        if not HAS_SUGIYAMA:
            self.report({'ERROR'}, "需要networkx库: pip install networkx")
            return {'CANCELLED'}
        bl_data = get_all_ntrees()
        count = batch_modify(bl_data, NA_OT_ArrangeSelected, redraw_ui=True)
        self.report({'INFO'}, f"已排列 {count} 个节点树")
        return {'FINISHED'}


class NA_OT_RecenterSelected(NodeOperator, Operator):
    bl_idname = "node.na_recenter_selected"
    bl_label = "重新居中选中"
    bl_description = "将选中节点的位置归零居中"

    def execute(self, context: Context) -> set[str]:
        nodes = get_ntree().nodes
        selected = [n for n in nodes if n.select]
        if not selected:
            self.report({'WARNING'}, "没有选中节点")
            return {'CANCELLED'}
        non_frames = [n for n in selected if n.bl_idname != 'NodeFrame']
        if not non_frames:
            self.report({'WARNING'}, "没有有效节点")
            return {'CANCELLED'}
        origin_type = context.scene.na_settings.origin
        if origin_type == 'ACTIVE_NODE':
            if nodes.active in non_frames:
                origin = abs_loc(nodes.active)
            else:
                self.report({'WARNING'}, "没有有效的活动节点")
                return {'CANCELLED'}
        else:
            if origin_type == 'ACTIVE_OUTPUT':
                if active_outputs := [n for n in nodes if getattr(n, 'is_active_output', False)]:
                    origin_nodes = active_outputs
                else:
                    self.report({'WARNING'}, "没有活动输出")
                    return {'CANCELLED'}
            else:
                origin_nodes = non_frames
            origin = Vector(map(fmean, zip(*map(abs_loc, origin_nodes))))
        ui_scale = context.preferences.system.ui_scale
        bpy.ops.transform.translate(value=(*-origin * ui_scale, 0))
        return {'FINISHED'}


class NA_OT_BatchRecenter(NodeOperator, Operator):
    bl_idname = "node.na_batch_recenter"
    bl_label = "批量重新居中所有节点树"
    bl_description = "重新居中当前.blend文件中所有节点树"

    def execute(self, context: Context) -> set[str]:
        bl_data = get_all_ntrees()
        count = batch_modify(bl_data, NA_OT_RecenterSelected, redraw_ui=False)
        self.report({'INFO'}, f"已重新居中 {count} 个节点树")
        return {'FINISHED'}


class NA_OT_InstallNetworkX(Operator):
    bl_idname = "node.na_install_networkx"
    bl_label = "安装networkx库"
    bl_description = "从插件内置wheel安装networkx到Blender Python环境"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return not HAS_SUGIYAMA

    def execute(self, context):
        import subprocess, sys, os, importlib
        py = sys.executable
        try:
            subprocess.run([py, "-m", "ensurepip", "--upgrade"],
                           capture_output=True, text=True, timeout=120)
        except Exception:
            pass
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        wheel_path = os.path.join(addon_dir, "node_arrange", "wheels",
                                  "networkx-3.4.2-py3-none-any.whl")
        target = wheel_path if os.path.exists(wheel_path) else "networkx"
        attempts = [
            [py, "-m", "pip", "install", "--no-deps", target],
            [py, "-m", "pip", "install", "--no-deps", "--user", target],
            [py, "-m", "pip", "install", "networkx"],
            [py, "-m", "pip", "install", "--user", "networkx"],
        ]
        last = ""
        for cmd in attempts:
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                if r.returncode == 0:
                    try:
                        importlib.invalidate_caches()
                        import networkx  # noqa: F401
                        ok_now = True
                    except Exception:
                        ok_now = False
                    msg = "networkx 安装成功" + ("，排列功能已可用" if ok_now else "，请重启 Blender 或停用再启用本插件")
                    self.report({'INFO'}, msg)
                    return {'FINISHED'}
                last = (r.stderr or r.stdout or "")[-300:]
            except subprocess.TimeoutExpired:
                last = "安装超时"
            except Exception as e:
                last = str(e)
        self.report({'ERROR'}, ("自动安装失败，请在终端手动执行： \"%s\" -m pip install networkx | %s" % (py, last))[:400])
        return {'CANCELLED'}


classes = (
    NA_OT_ArrangeSelected,
    NA_OT_BatchArrange,
    NA_OT_RecenterSelected,
    NA_OT_BatchRecenter,
    NA_OT_InstallNetworkX,
)


def register() -> None:
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass


def unregister() -> None:
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
