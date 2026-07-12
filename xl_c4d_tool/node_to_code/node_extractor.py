"""【工具脚本：Blender节点总览提取器】
功能：提取当前Blender版本中所有可用节点的信息并导出为JSON
用途：当Blender更新后，运行此脚本可以获取最新节点的完整列表，
     确保"任意节点转代码"功能能够正确识别和转换所有新节点类型。

使用方法：
    在Blender脚本编辑器中打开此文件并运行，会在桌面生成 blender_all_nodes.json
"""
import bpy
import json
import os


def get_all_node_classes():
    """获取所有继承自 bpy.types.Node 的节点类（不限前缀）"""
    nodes = []
    for cls_name in sorted(dir(bpy.types)):
        cls = getattr(bpy.types, cls_name)
        if not hasattr(cls, 'bl_rna'):
            continue
        if not issubclass(cls, bpy.types.Node):
            continue
        if cls_name in ('Node', 'NodeInternal'):
            continue
        identifier = cls.bl_rna.identifier
        label = getattr(cls, 'bl_label', identifier)
        nodes.append([identifier, label])
    return nodes


def get_asset_node_groups():
    """从内置资产库中提取可添加的节点组资产"""
    assets = []
    datafiles = bpy.utils.system_resource('DATAFILES')
    asset_libs = {
        "Shading": os.path.join(datafiles, "assets", "shading_nodes_essentials.blend"),
        "Compositing": os.path.join(datafiles, "assets", "compositing_nodes_essentials.blend"),
        "Geometry": os.path.join(datafiles, "assets", "geometry_nodes_essentials.blend"),
    }
    for lib_name, lib_path in asset_libs.items():
        if not os.path.exists(lib_path):
            continue
        try:
            with bpy.data.libraries.load(lib_path) as (data_from, data_to):
                for node_group_name in data_from.node_groups:
                    assets.append([node_group_name, f"{lib_name} Asset: {node_group_name}"])
        except:
            pass
    return assets


def get_zone_nodes():
    """手动补充区域节点对（确保不遗漏特殊节点）"""
    zones = [
        ["GeometryNodeSimulationInput", "模拟输入"],
        ["GeometryNodeSimulationOutput", "模拟输出"],
        ["GeometryNodeRepeatInput", "重复输入"],
        ["GeometryNodeRepeatOutput", "重复输出"],
        ["GeometryNodeForeachGeometryElementInput", "遍历几何元素输入"],
        ["GeometryNodeForeachGeometryElementOutput", "遍历几何元素输出"],
        ["NodeClosureInput", "闭合输入"],
        ["NodeClosureOutput", "闭合输出"],
    ]
    return zones


def extract_all_nodes(output_path=None):
    """执行全部节点提取，保存到指定路径（默认桌面）"""
    if output_path is None:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        output_path = os.path.join(desktop, "blender_all_nodes.json")

    all_nodes = get_all_node_classes()
    asset_nodes = get_asset_node_groups()
    zone_nodes = get_zone_nodes()

    existing_ids = {n[0] for n in all_nodes}
    for a in asset_nodes:
        if a[0] not in existing_ids:
            all_nodes.append(a)
    for z in zone_nodes:
        if z[0] not in existing_ids:
            all_nodes.append(z)

    result = {
        "all_nodes": all_nodes,
        "total_count": len(all_nodes)
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return output_path, len(all_nodes)


if __name__ == "__main__":
    path, count = extract_all_nodes()
    print(f"总节点数: {count}，已保存到 {path}")
