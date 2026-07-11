"""节点发现：合并静态中文目录与 Blender 当前版本的全部注册节点。"""

from __future__ import annotations

import json
import os
import hashlib

import bpy


_data_cache = None
_registered_cache = None

CATEGORY_NAMES = {
    "Input": "输入", "Output": "输出", "Shader": "着色器", "Texture": "纹理",
    "Color": "颜色", "Vector": "矢量", "Converter": "转换", "Script": "脚本",
    "Group": "组", "Layout": "布局", "Attribute": "属性", "Geometry": "几何",
    "Curve": "曲线", "Mesh": "网格", "Point": "点", "Volume": "体积",
    "Instances": "实例", "Material": "材质", "Utilities": "实用工具",
    "Distort": "变形", "Filter": "滤镜", "Matte": "遮罩", "Transform": "变换",
    "Keying": "抠像", "Tracking": "跟踪", "Channel": "通道",
    # 补全 Blender 5.x 新增分类，避免侧栏出现英文标题
    "Closure": "闭包", "SDF": "SDF", "Text": "文本", "Grease Pencil": "蜡笔",
    "Primitives": "基本体", "Gizmo": "操控器", "Import": "导入", "Bundle": "集束",
    "List": "列表", "Simulation": "模拟", "Repeat": "重复", "Foreach": "遍历",
}

# 原生节点侧栏：按属性分色相（同属性同色系、不同倾向、按色环顺序），
# 饱和度压低到莫兰迪区间。键为本地化后的中文分类名。
NATIVE_CATEGORY_COLORS = {
    # 几何类型 —— 绿色系（黄绿→墨绿→青绿）
    "几何": (0.462, 0.660, 0.470, 1.0), "网格": (0.502, 0.660, 0.462, 1.0),
    "曲线": (0.462, 0.660, 0.541, 1.0), "点": (0.462, 0.660, 0.589, 1.0),
    "体积": (0.462, 0.660, 0.624, 1.0), "实例": (0.537, 0.660, 0.462, 1.0),
    "SDF": (0.462, 0.660, 0.648, 1.0), "基本体": (0.478, 0.660, 0.462, 1.0),
    "文本": (0.462, 0.660, 0.506, 1.0), "蜡笔": (0.462, 0.660, 0.565, 1.0),
    # 数据输入 —— 陶土/赭橙系
    "输入": (0.660, 0.527, 0.462, 1.0), "属性": (0.660, 0.575, 0.462, 1.0),
    "导入": (0.660, 0.486, 0.462, 1.0), "集束": (0.660, 0.605, 0.462, 1.0),
    "列表": (0.660, 0.587, 0.462, 1.0),
    # 输出 —— 紫
    "输出": (0.620, 0.462, 0.660, 1.0),
    # 着色 / 材质 / 纹理 / 颜色 —— 蓝青系
    "着色器": (0.462, 0.517, 0.660, 1.0), "材质": (0.513, 0.462, 0.660, 1.0),
    "纹理": (0.462, 0.601, 0.660, 1.0), "颜色": (0.462, 0.636, 0.660, 1.0),
    "闭包": (0.462, 0.470, 0.660, 1.0),
    # 工具 / 转换 / 矢量 —— 橄榄金系
    "实用工具": (0.660, 0.640, 0.462, 1.0), "转换": (0.660, 0.622, 0.462, 1.0),
    "矢量": (0.650, 0.660, 0.462, 1.0), "脚本": (0.640, 0.660, 0.470, 1.0),
    # 控制流 —— 中性蓝灰
    "模拟": (0.504, 0.554, 0.600, 1.0), "重复": (0.504, 0.542, 0.600, 1.0),
    "遍历": (0.504, 0.525, 0.600, 1.0), "操控器": (0.504, 0.600, 0.600, 1.0),
    "组": (0.550, 0.528, 0.528, 1.0), "布局": (0.550, 0.528, 0.528, 1.0),
    # 合成器 / 纹理树额外分类
    "滤镜": (0.620, 0.660, 0.462, 1.0), "遮罩": (0.660, 0.462, 0.652, 1.0),
    "变形": (0.660, 0.462, 0.581, 1.0), "抠像": (0.597, 0.462, 0.660, 1.0),
    "跟踪": (0.462, 0.660, 0.612, 1.0), "通道": (0.660, 0.646, 0.462, 1.0),
}

_NATIVE_DEFAULT_COLOR = (0.48, 0.46, 0.44, 1.0)

# 本地化分类名 -> Blender 主题 node_editor 的对应"原生节点头部色"属性名。
# 用它让快捷节点(T面板)的分类色 = 原生节点实际头部色（用户要求）。
_CAT_TO_THEME = {
    "输入": "input_node", "属性": "attribute_node", "导入": "input_node",
    "集束": "input_node", "列表": "input_node",
    "输出": "output_node",
    "着色器": "shader_node", "材质": "shader_node", "闭包": "shader_node",
    "纹理": "texture_node", "颜色": "color_node", "矢量": "vector_node",
    "转换": "converter_node", "实用工具": "converter_node", "脚本": "script_node",
    "几何": "geometry_node", "网格": "geometry_node", "曲线": "geometry_node",
    "点": "geometry_node", "体积": "geometry_node", "实例": "geometry_node",
    "SDF": "geometry_node", "基本体": "geometry_node", "文本": "geometry_node",
    "蜡笔": "geometry_node", "模拟": "geometry_node", "重复": "geometry_node",
    "遍历": "geometry_node", "操控器": "geometry_node",
    "组": "group_node", "布局": "group_node",
    "滤镜": "filter_node", "遮罩": "matte_node", "变形": "distor_node",
    "抠像": "matte_node", "跟踪": "distor_node", "通道": "color_node",
}


def native_category_color(category):
    """返回该分类对应的"原生节点头部色"(读 Blender 主题)；读不到则回退莫兰迪色。"""
    attr = _CAT_TO_THEME.get(category)
    if attr:
        try:
            import bpy
            ne = bpy.context.preferences.themes[0].node_editor
            c = getattr(ne, attr, None)
            if c is not None:
                return (c[0], c[1], c[2], 1.0)
        except Exception:
            pass
    return NATIVE_CATEGORY_COLORS.get(category, _NATIVE_DEFAULT_COLOR)


def _load_static_data():
    global _data_cache
    if _data_cache is not None:
        return _data_cache
    path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "node_data.json"))
    try:
        with open(path, "r", encoding="utf-8") as stream:
            raw = json.load(stream)
    except (OSError, ValueError, TypeError):
        raw = {}
    localized = {}
    for tree_type, categories in raw.items():
        localized[tree_type] = {}
        for category, payload in categories.items():
            name = CATEGORY_NAMES.get(category, category)
            localized[tree_type][name] = payload
    _data_cache = localized
    return _data_cache


def _registered_node_types():
    global _registered_cache
    if _registered_cache is not None:
        return _registered_cache
    result = {}
    for attribute in dir(bpy.types):
        cls = getattr(bpy.types, attribute, None)
        try:
            if not isinstance(cls, type) or not issubclass(cls, bpy.types.Node):
                continue
            if not cls.is_registered_node_type():
                continue
            node_id = cls.bl_rna.identifier
            if node_id in {"Node", "NodeInternal"}:
                continue
            label = bpy.app.translations.pgettext_iface(getattr(cls, "bl_label", "") or node_id)
            result[node_id] = label
        except (AttributeError, TypeError, RuntimeError):
            continue
    _registered_cache = result
    return result


# 各编辑器允许的节点族前缀。没有活动 edit_tree 时（poll 无法判定），
# 用它把跨编辑器的节点挡在目录之外，避免着色器侧栏混入大量几何/函数节点的英文按钮。
_TREE_FAMILY = {
    "ShaderNodeTree": ("ShaderNode",),
    "CompositorNodeTree": ("CompositorNode",),
    "TextureNodeTree": ("TextureNode",),
    "GeometryNodeTree": ("GeometryNode", "FunctionNode"),
}
_SHARED_NODES = {
    "NodeReroute", "NodeFrame", "NodeGroupInput", "NodeGroupOutput",
    "ShaderNodeGroup", "GeometryNodeGroup", "CompositorNodeGroup", "TextureNodeGroup",
}


def _node_type_compatible(node_id, tree_type):
    if node_id in _SHARED_NODES:
        return True
    prefixes = _TREE_FAMILY.get(tree_type)
    if not prefixes:
        return True
    return node_id.startswith(prefixes)


def _node_allowed(node_id, tree, tree_type=None):
    cls = getattr(bpy.types, node_id, None)
    if cls is None:
        cls = bpy.types.Node.bl_rna_get_subclass_py(node_id)
    if cls is None:
        return False
    try:
        if not cls.is_registered_node_type():
            return False
    except (AttributeError, RuntimeError):
        return False
    poll = getattr(cls, "poll", None)
    if poll is None or tree is None:
        # 没有可用的活动节点树时，退化为按编辑器族前缀过滤
        return _node_type_compatible(node_id, tree_type)
    try:
        return bool(poll(tree))
    except (TypeError, RuntimeError):
        return _node_type_compatible(node_id, tree_type)


def _node_registered(node_id):
    """节点类型是否已注册(可创建)。用于静态目录过滤，避免不可靠的 poll 误杀。"""
    cls = getattr(bpy.types, node_id, None)
    if cls is None:
        try:
            cls = bpy.types.Node.bl_rna_get_subclass_py(node_id)
        except Exception:
            cls = None
    if cls is None:
        return False
    try:
        return bool(cls.is_registered_node_type())
    except (AttributeError, RuntimeError):
        return True


def get_complete_node_data(context):
    """返回完整中文目录；新增节点补入原有分类而不是堆进单独的长列表。"""
    tree_type = resolve_tree_type(context)
    tree = getattr(getattr(context, "space_data", None), "edit_tree", None)
    static = _load_static_data().get(tree_type, {})
    result = {}
    known = set()
    for category, payload in static.items():
        nodes = []
        for node_id, label in payload.get("nodes", []):
            if node_id in known or not _node_registered(node_id):
                continue
            nodes.append((node_id, label))
            known.add(node_id)
        if nodes:
            result[category] = {
                "color": payload.get("color", [0.5, 0.5, 0.5, 1.0]),
                "nodes": sorted(nodes, key=lambda item: item[0].casefold()),
            }

    extras = {}
    for node_id, label in sorted(_registered_node_types().items(), key=lambda item: item[1]):
        # extras 必须既通过 poll/族过滤，又严格属于当前编辑器族，杜绝跨编辑器英文节点混入
        if (node_id not in known and _node_allowed(node_id, tree, tree_type)
                and _node_type_compatible(node_id, tree_type)):
            category = _guess_existing_category(node_id, result)
            extras.setdefault(category, []).append((node_id, label))
    for category, nodes in extras.items():
        payload = result.setdefault(category, {"color": [0.22, 0.42, 0.62, 1.0], "nodes": []})
        payload["nodes"].extend(nodes)
        payload["nodes"].sort(key=lambda item: item[0].casefold())
    return {tree_type: result} if tree_type else {}


def _guess_existing_category(node_id, catalog):
    rules = (
        (("Input", "Value", "RGB", "TexCoord", "ObjectInfo", "CollectionInfo"), "输入"),
        (("Output",), "输出"),
        (("Curve", "Spline", "String"), "曲线"),
        (("Mesh",), "网格"),
        (("Instance",), "实例"),
        (("Material", "SetMaterial"), "材质"),
        (("Point",), "点"),
        (("Volume", "SDF"), "体积"),
        (("Attribute", "Capture", "StoreNamed"), "属性"),
        (("Simulation",), "模拟"),
        (("Repeat",), "重复"),
        (("Foreach",), "遍历"),
        (("Group",), "组"),
        (("Frame", "Reroute"), "布局"),
        (("ShaderNodeTex",), "纹理"),
        (("ShaderNodeVector",), "矢量"),
        (("ShaderNodeBsdf", "ShaderNodeEmission", "ShaderNodeMixShader"), "着色器"),
    )
    for needles, category in rules:
        if any(needle in node_id for needle in needles) and category in catalog:
            return category
    for fallback in ("实用工具", "转换", "几何", "输入"):
        if fallback in catalog:
            return fallback
    return next(iter(catalog), "其他")


def get_node_data():
    return _load_static_data()


def resolve_tree_type(context):
    space = getattr(context, "space_data", None)
    return space.tree_type if space and space.type == "NODE_EDITOR" else None


def get_category_color_prop_name(category):
    digest = hashlib.sha1(category.encode("utf-8")).hexdigest()[:10]
    return f"node_category_color_{digest}"


def get_category_folded_prop_name(category):
    return f"{category.replace(' ', '_').lower()}_folded"
