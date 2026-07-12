"""C4D 节点组资产库与目录数据。"""

from __future__ import annotations

import json
import os

import bpy

from .library_catalog import enrich_item, grouped_items


ADDON_ROOT = os.path.dirname(os.path.dirname(__file__))
ASSET_BLEND = os.path.join(ADDON_ROOT, "assets", "C4D生成器复刻.blend")
MANIFEST_PATH = os.path.join(ADDON_ROOT, "assets", "node_groups.json")

_manifest_cache = None


def load_modifier_manifest(force=False):
    global _manifest_cache
    if _manifest_cache is not None and not force:
        return _manifest_cache
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as stream:
            payload = json.load(stream)
        _manifest_cache = [enrich_item(item) for item in payload.get("groups", [])]
    except (OSError, ValueError, TypeError):
        _manifest_cache = []
    return _manifest_cache


def ensure_node_group(group_name):
    """返回本地节点组；不存在时从随插件附带的资产文件追加。"""
    group = bpy.data.node_groups.get(group_name)
    if group is not None:
        return group
    if not os.path.isfile(ASSET_BLEND):
        raise FileNotFoundError(f"找不到节点资产库：{ASSET_BLEND}")
    directory = os.path.join(ASSET_BLEND, "NodeTree") + os.sep
    bpy.ops.wm.append(
        filepath=os.path.join(directory, group_name),
        directory=directory,
        filename=group_name,
        do_reuse_local_id=True,
    )
    group = bpy.data.node_groups.get(group_name)
    if group is None:
        raise RuntimeError(f"资产库中找不到节点组：{group_name}")
    return group


def modifier_categories():
    names = {item.get("category", "其他") for item in load_modifier_manifest()}
    preferred = ["生成器", "建模工具", "克隆器", "效果器", "域", "散布", "变形器", "动画", "其他"]
    return [name for name in preferred if name in names]


def grouped_modifier_manifest():
    return grouped_items(load_modifier_manifest())
