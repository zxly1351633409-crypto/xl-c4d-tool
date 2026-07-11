"""加载节点组专属彩色图标 + 运行时生成分类色标（方块）。"""

from __future__ import annotations

import os
import struct
import tempfile
import zlib

import bpy

from .library_catalog import icon_filename, CATEGORY_DEFS
from .node_discovery import NATIVE_CATEGORY_COLORS


_previews = None
_cat_icon_dir = None


# ───────────────────────── 运行时 PNG 生成 ─────────────────────────

def _make_square_png(r: int, g: int, b: int, size: int = 64,
                     corner_radius: int = 6) -> bytes:
    """生成抗锯齿圆角方块纯色 PNG 字节流。

    采用圆角矩形的有符号距离场（SDF）+ 1px 平滑过渡实现高精度抗锯齿边缘，
    避免旧实现的台阶状锯齿；并对颜色做直通 alpha（straight alpha）输出。
    """
    margin = max(1.5, size * 0.045)          # 透明边距，随分辨率缩放
    center = size / 2.0
    half = center - margin                    # 半边长（含圆角）
    radius = min(corner_radius, half)         # 圆角半径，避免越界
    inner = half - radius                     # 直边半长

    def coverage(px: float, py: float) -> float:
        # 圆角矩形 SDF（以中心为原点）
        qx = abs(px) - inner
        qy = abs(py) - inner
        ox = qx if qx > 0.0 else 0.0
        oy = qy if qy > 0.0 else 0.0
        outside = (ox * ox + oy * oy) ** 0.5
        inside = min(max(qx, qy), 0.0)
        dist = outside + inside - radius
        # 1px 宽线性过渡 → 平滑边缘
        return min(1.0, max(0.0, 0.5 - dist))

    raw = bytearray()
    for y in range(size):
        raw += b"\x00"  # filter byte
        py = y + 0.5 - center
        for x in range(size):
            px = x + 0.5 - center
            alpha = int(round(255 * coverage(px, py)))
            raw += struct.pack("BBBB", r, g, b, alpha)
    compressed = zlib.compress(bytes(raw), 9)

    def _chunk(tag: bytes, data: bytes) -> bytes:
        c = tag + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    out = b"\x89PNG\r\n\x1a\n"
    out += _chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    out += _chunk(b"IDAT", compressed)
    out += _chunk(b"IEND", b"")
    return out


def _boost_color(color):
    """轻度饱和度增强 + 提亮，保持莫兰迪色感。"""
    cr, cg, cb = color[0], color[1], color[2]
    avg = (cr + cg + cb) / 3.0
    boost = 1.25
    cr = min(1.0, avg + (cr - avg) * boost)
    cg = min(1.0, avg + (cg - avg) * boost)
    cb = min(1.0, avg + (cb - avg) * boost)
    brightness = 1.05
    r = int(min(255, cr * 255 * brightness))
    g = int(min(255, cg * 255 * brightness))
    b = int(min(255, cb * 255 * brightness))
    return r, g, b


_VALID_NODE_THEME = ("color_node","converter_node","geometry_node","input_node",
                     "texture_node","vector_node","attribute_node","output_node")


def _theme_nearest_ints(color):
    """把分类库色按色相匹配到最接近的原生节点主题色，返回 0-255 整数 (r,g,b)。"""
    import colorsys, bpy
    try:
        ne = bpy.context.preferences.themes[0].node_editor
        h, sat, _v = colorsys.rgb_to_hsv(color[0], color[1], color[2])
        if sat >= 0.12:
            best=None; bd=9.0
            for attr in _VALID_NODE_THEME:
                tc = getattr(ne, attr, None)
                if tc is None: continue
                th = colorsys.rgb_to_hsv(tc[0], tc[1], tc[2])[0]
                dh = abs(h-th); dh=min(dh,1.0-dh)
                if dh<bd: bd=dh; best=tc
            if best is not None:
                return (int(round(best[0]*255)), int(round(best[1]*255)), int(round(best[2]*255)))
    except Exception:
        pass
    return _boost_color(color)


def _generate_category_icons():
    """为每个分类生成方块色标（标题用64px + 按钮用32px）。"""
    global _cat_icon_dir
    _cat_icon_dir = tempfile.mkdtemp(prefix="xl_cat_icons_")
    for key, (_path, color, _icon) in CATEGORY_DEFS.items():
        r, g, b = _theme_nearest_ints(color)
        # 标题用大方块（高分辨率，UI 缩放更锐利）
        png_data = _make_square_png(r, g, b, size=128, corner_radius=18)
        filepath = os.path.join(_cat_icon_dir, f"{key}.png")
        with open(filepath, "wb") as fp:
            fp.write(png_data)
        try:
            _previews.load(f"__cat_color_{key}", filepath, "IMAGE")
        except Exception:
            pass
        # 按钮用小方块
        png_sm = _make_square_png(r, g, b, size=64, corner_radius=10)
        sm_path = os.path.join(_cat_icon_dir, f"{key}_sm.png")
        with open(sm_path, "wb") as fp:
            fp.write(png_sm)
        try:
            _previews.load(f"__cat_btn_{key}", sm_path, "IMAGE")
        except Exception:
            pass


def _native_key(category: str) -> str:
    """原生分类名 → 文件/预览安全键。"""
    import hashlib
    return hashlib.sha1(category.encode("utf-8")).hexdigest()[:12]


def _generate_native_category_icons():
    """为原生节点侧栏的每个分类生成莫兰迪方块色标（标题 64px + 按钮 32px）。"""
    global _cat_icon_dir
    if _cat_icon_dir is None:
        _cat_icon_dir = tempfile.mkdtemp(prefix="xl_cat_icons_")
    from .node_discovery import native_category_color
    for category in NATIVE_CATEGORY_COLORS:
        color = native_category_color(category)  # 取原生节点头部主题色，与原生节点一致
        r = max(0, min(255, int(round(color[0] * 255))))
        g = max(0, min(255, int(round(color[1] * 255))))
        b = max(0, min(255, int(round(color[2] * 255))))
        digest = _native_key(category)
        png_data = _make_square_png(r, g, b, size=128, corner_radius=18)
        fp_path = os.path.join(_cat_icon_dir, f"node_{digest}.png")
        with open(fp_path, "wb") as fp:
            fp.write(png_data)
        try:
            _previews.load(f"__node_cat_color_{digest}", fp_path, "IMAGE")
        except Exception:
            pass
        png_sm = _make_square_png(r, g, b, size=64, corner_radius=10)
        sm_path = os.path.join(_cat_icon_dir, f"node_{digest}_sm.png")
        with open(sm_path, "wb") as fp:
            fp.write(png_sm)
        try:
            _previews.load(f"__node_cat_btn_{digest}", sm_path, "IMAGE")
        except Exception:
            pass


# ───────────────────────── 注册 / 注销 ─────────────────────────

def register():
    global _previews
    if _previews is not None:
        return
    import bpy.utils.previews
    _previews = bpy.utils.previews.new()

    icon_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "icons", "node_groups")
    )
    if os.path.isdir(icon_dir):
        for filename in os.listdir(icon_dir):
            if not filename.lower().endswith(".png"):
                continue
            key = os.path.splitext(filename)[0]
            try:
                _previews.load(key, os.path.join(icon_dir, filename), "IMAGE")
            except (KeyError, OSError, RuntimeError):
                continue

    _generate_category_icons()
    _generate_native_category_icons()


def unregister():
    global _previews, _cat_icon_dir
    if _previews is None:
        return
    import bpy.utils.previews
    bpy.utils.previews.remove(_previews)
    _previews = None
    if _cat_icon_dir and os.path.isdir(_cat_icon_dir):
        import shutil
        try:
            shutil.rmtree(_cat_icon_dir, ignore_errors=True)
        except Exception:
            pass
    _cat_icon_dir = None


def icon_value(name: str) -> int:
    """获取图标 ID。支持 __cat_color_<key> 和 __cat_btn_<key> 格式。"""
    if _previews is None:
        register()
    if _previews is None:
        return 0
    if name.startswith("__cat_color_") or name.startswith("__cat_btn_") \
            or name.startswith("__node_cat_color_") or name.startswith("__node_cat_btn_"):
        preview = _previews.get(name)
        return preview.icon_id if preview else 0
    key = os.path.splitext(icon_filename(name))[0]
    preview = _previews.get(key)
    return preview.icon_id if preview else 0


def native_category_icon(category: str, button: bool = True) -> int:
    """获取原生分类的方块色标图标 ID。button=True 用按钮小方块，否则标题大方块。"""
    if _previews is None:
        register()
    if _previews is None:
        return 0
    digest = _native_key(category)
    prefix = "__node_cat_btn_" if button else "__node_cat_color_"
    preview = _previews.get(prefix + digest)
    return preview.icon_id if preview else 0
