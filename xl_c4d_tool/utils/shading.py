"""【工具模块：着色器控制】
设置3D视图着色方式、随机颜色生成、集合遍历"""
import bpy
from .logger import logger


def _iter_view3d_spaces(screen):
    """遍历屏幕中所有3D视图空间"""
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    yield area, space


def set_shading_for_all_areas(context, light=None, color_type=None, shading_type=None, render_pass=None, show_object_outline=None):
    """统一设置所有3D视图的着色参数"""
    for area, space in _iter_view3d_spaces(context.screen):
        if shading_type:
            space.shading.type = shading_type
        if light:
            try:
                space.shading.light = light
            except AttributeError:
                logger.warning(f"无法设置光照模式为 {light}")
        if color_type:
            try:
                space.shading.color_type = color_type
            except AttributeError:
                logger.warning(f"无法设置颜色类型为 {color_type}")
        if render_pass:
            try:
                space.shading.render_pass = render_pass
            except AttributeError:
                logger.warning(f"无法设置渲染通道为 {render_pass}")
        if show_object_outline is not None:
            space.shading.show_object_outline = show_object_outline


def generate_random_color():
    """生成HSV空间的随机鲜艳颜色(RGB)"""
    import random
    import colorsys
    h = random.random()
    s = random.uniform(0.5, 1.0)
    v = random.uniform(0.6, 1.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (r, g, b)


def get_all_collections(scene):
    """递归获取场景中所有子集合及路径"""
    result = []
    def collect(col, parent_path=""):
        path = f"{parent_path}/{col.name}" if parent_path else col.name
        result.append((col, path))
        for child in col.children:
            collect(child, path)
    for col in scene.collection.children:
        collect(col)
    return result
