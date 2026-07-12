"""XL C4D 节点组的统一分类、排序、颜色与图标元数据。"""

from __future__ import annotations

import hashlib
from collections import OrderedDict
from functools import cmp_to_key


# 色相沿用 C4D 的功能辨识习惯，饱和度压低到莫兰迪区间。这里的颜色同时用于
# 分类图标、节点助手和从助手放置出来的组节点表头，避免同一功能在三处变色。
CATEGORY_DEFS = OrderedDict((
    ("generator.mesh", ("生成器/网格参数体", (0.38, 0.56, 0.38, 1.0), "MESH_CUBE")),
    ("generator.spline_primitive", ("生成器/样条参数体", (0.33, 0.50, 0.60, 1.0), "CURVE_BEZCIRCLE")),
    ("generator.spline", ("生成器/样条生成器", (0.33, 0.57, 0.52, 1.0), "SURFACE_DATA")),
    ("generator.modeling", ("生成器/建模生成器", (0.58, 0.48, 0.35, 1.0), "MODIFIER")),
    ("mograph.generator", ("MoGraph/生成器", (0.56, 0.36, 0.52, 1.0), "MOD_PARTICLE_INSTANCE")),
    ("mograph.deformer", ("MoGraph/变形器", (0.58, 0.40, 0.46, 1.0), "MOD_WAVE")),
    ("particle", ("粒子/生成器", (0.60, 0.46, 0.32, 1.0), "PARTICLES")),
    ("volume", ("体积/生成器", (0.46, 0.40, 0.58, 1.0), "VOLUME_DATA")),
    ("deformer", ("变形器", (0.62, 0.46, 0.33, 1.0), "MOD_SIMPLEDEFORM")),
    ("effector", ("MoGraph/效果器", (0.60, 0.38, 0.46, 1.0), "FORCE_TURBULENCE")),
    ("field", ("域", (0.36, 0.54, 0.40, 1.0), "SHADERFX")),
    ("scatter", ("散布", (0.50, 0.56, 0.34, 1.0), "OUTLINER_OB_POINTCLOUD")),
    ("animation", ("动画与工具", (0.40, 0.46, 0.58, 1.0), "ACTION")),
    ("other", ("其他", (0.48, 0.46, 0.44, 1.0), "GEOMETRY_NODES")),
))

MESH_PRIMITIVES = {
    "C4D_圆柱", "C4D_圆环", "C4D_圆盘", "C4D_圆锥", "C4D_平面", "C4D_柏拉图体",
    "C4D_油罐", "C4D_球体", "C4D_立方体", "C4D_管", "C4D_胶囊", "C4D_金字塔",
}
SPLINE_GENERATORS = {"XL_扫描", "XL_挤压", "XL_放样", "XL_旋转", "XL_样条蒙版"}
MOGRAPH_GENERATORS = {
    "XL_克隆_对象", "XL_克隆_放射", "XL_克隆_沿样条", "XL_克隆_线性", "XL_克隆_网格",
    "XL_克隆_蜂窝", "XL_克隆转矩阵", "XL_克隆镜像", "XL_分裂实例", "XL_多边形FX",
    "XL_实例", "XL_实例化", "XL_矩阵", "XL_运动实例", "XL_运动文本",
    "XL_挤出套娃",
}
PARTICLE_GENERATORS = {"XL_粒子发射"}
VOLUME_GENERATORS = {"XL_融球", "XL_体积生成", "XL_体积网格"}


def classify_group(name: str, fallback: str = "其他") -> str:
    if name in {"Exact Fracture [CGM]", "XL_精确破碎", "XL_破碎2.001（勉强算完成版）"}:
        return "generator.modeling"
    if "重网格" in name or "重拓扑" in name or "四边化" in name:
        return "generator.modeling"
    if name in MESH_PRIMITIVES:
        return "generator.mesh"
    if name == "XL_运动挤压":
        return "mograph.deformer"
    if name.startswith("C4D_样条_"):
        return "generator.spline_primitive"
    if name in SPLINE_GENERATORS:
        return "generator.spline"
    if name in MOGRAPH_GENERATORS or "克隆" in name or "实例化" in name or "加权" in name:
        return "mograph.generator"
    if name in PARTICLE_GENERATORS:
        return "particle"
    if name in VOLUME_GENERATORS:
        return "volume"
    if "效果器" in name or name == "XL_跟随效果":
        return "effector"
    if "域" in name:
        return "field"
    if "散布" in name:
        return "scatter"
    if fallback == "变形器":
        return "deformer"
    if fallback in {"建模工具", "生成器"}:
        return "generator.modeling"
    if fallback == "动画" or name in {"XL_摄像机工具", "XL_追踪", "XL_加速度", "XL_运动动画"}:
        return "animation"
    return "other"


def category_definition(key: str):
    return CATEGORY_DEFS.get(key, CATEGORY_DEFS["other"])


def category_path(item: dict) -> str:
    key = item.get("category_key") or classify_group(item.get("name", ""), item.get("category", "其他"))
    return category_definition(key)[0]


def icon_filename(name: str) -> str:
    return hashlib.sha1(name.encode("utf-8")).hexdigest()[:16] + ".png"


def enrich_item(item: dict) -> dict:
    result = dict(item)
    key = classify_group(result.get("name", ""), result.get("category", "其他"))
    path, color, fallback_icon = category_definition(key)
    result.update({
        "category_key": key,
        "category_path": path,
        "color": list(color),
        "fallback_icon": fallback_icon,
        "icon_file": icon_filename(result.get("name", "")),
    })
    return result


def _windows_compare(left: str, right: str) -> int:
    """按中文拼音规则比较；非 Windows 环境自动回退 Unicode 顺序。"""
    try:
        import ctypes
        value = ctypes.windll.kernel32.CompareStringEx(
            "zh-CN", 0, left, len(left), right, len(right), None, None, 0
        )
        return {-1: -1, 0: 0, 1: 0, 2: -1, 3: 1}.get(value, 0)
    except (AttributeError, OSError):
        return (left > right) - (left < right)


def sort_items(items):
    def compare(a, b):
        left = (a.get("label") or a.get("name") or "").casefold()
        right = (b.get("label") or b.get("name") or "").casefold()
        return _windows_compare(left, right)
    return sorted(items, key=cmp_to_key(compare))


def grouped_items(items):
    groups = OrderedDict((key, []) for key in CATEGORY_DEFS)
    for raw in items:
        item = enrich_item(raw)
        groups[item["category_key"]].append(item)
    return OrderedDict((key, sort_items(values)) for key, values in groups.items() if values)
