import bpy
import os
from .parser import parse_node_group
from .generator import save_all_groups


def batch_process_blend_file(filepath, output_dir):
    """【批量处理】打开指定.blend文件，转换其中所有节点组"""
    results = []
    current_file = bpy.data.filepath

    try:
        bpy.ops.wm.open_mainfile(filepath=filepath)
    except Exception as e:
        return False, f"无法打开文件: {e}"

    all_groups = []
    parsed = set()

    for ng in bpy.data.node_groups:
        if ng.name in parsed:
            continue
        data = parse_node_group(ng, parsed)
        if data:
            all_groups.append(data)

    if not all_groups:
        return False, "文件中未找到节点组"

    try:
        saved_files = save_all_groups(all_groups, output_dir)
    except Exception as e:
        return False, f"保存失败: {e}"

    if current_file:
        try:
            bpy.ops.wm.open_mainfile(filepath=current_file)
        except Exception:
            pass

    return True, f"成功转换 {len(all_groups)} 个节点组, 生成 {len(saved_files)} 个文件"


def batch_process_current_file(output_dir):
    """【批量处理】转换当前.blend文件中的所有节点组"""
    all_groups = []
    parsed = set()

    for ng in bpy.data.node_groups:
        if ng.name in parsed:
            continue
        data = parse_node_group(ng, parsed)
        if data:
            all_groups.append(data)

    if not all_groups:
        return False, "当前文件中未找到节点组"

    try:
        saved_files = save_all_groups(all_groups, output_dir)
    except Exception as e:
        return False, f"保存失败: {e}"

    return True, f"成功转换 {len(all_groups)} 个节点组, 生成 {len(saved_files)} 个文件"


def batch_process_current_editor(output_dir):
    """【批量处理】转换当前节点编辑器中的节点组（含嵌套子组）"""
    from .parser import parse_current_editor_group

    results, err = parse_current_editor_group(bpy.context)
    if err:
        return False, err

    try:
        saved_files = save_all_groups(results, output_dir)
    except Exception as e:
        return False, f"保存失败: {e}"

    return True, f"成功转换 {len(results)} 个节点组(含嵌套), 生成 {len(saved_files)} 个文件"


def preview_current_editor():
    """【预览】生成当前节点编辑器中节点组的代码预览"""
    from .parser import parse_current_editor_group
    from .generator import generate_group_code

    results, err = parse_current_editor_group(bpy.context)
    if err:
        return None, err

    code_preview = ""
    for data in results:
        code_preview += generate_group_code(data)
        code_preview += "\n\n"

    return code_preview, None


def list_blend_node_groups(filepath):
    """列出.blend文件中的所有节点组信息"""
    info = []
    current_file = bpy.data.filepath

    try:
        bpy.ops.wm.open_mainfile(filepath=filepath)
    except Exception as e:
        return None, f"无法打开文件: {e}"

    for ng in bpy.data.node_groups:
        node_count = len(ng.nodes)
        has_sub = any(getattr(n, 'node_tree', None) is not None for n in ng.nodes)
        info.append({
            'name': ng.name,
            'type': ng.bl_idname,
            'nodes': node_count,
            'has_sub_groups': has_sub,
        })

    if current_file:
        try:
            bpy.ops.wm.open_mainfile(filepath=current_file)
        except Exception:
            pass

    return info, None
