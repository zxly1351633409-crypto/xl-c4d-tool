"""【操作符：Cycles材质节点助手 — BL_扩展材质】
所有Cycles着色器节点组操作符，按分类组织"""
import bpy

try:
    from .cycles_nodes import (
        hs_metal_01a, hs_metal_02a, hs_metal_03a, hs_metal_04a, hs_metal_05a,
        hs_metal_polished_01a,
        hs_paint_01a, hs_paint_02a, hs_paint_03a, hs_paint_04a, hs_paint_05a,
        hs_paint_accent_01a,
        hs_glass_orange_01a, hs_glass_red_01a, hs_glass_white_01a,
        hs_plastic_01a,
        hs_rubber_01a, hs_rubber_02a,
        hs_rust_01a,
        hs_edges_01a,
        hs_dirt_cavity_01a, hs_dirt_streaks_01a,
        hs_bump_control,
        hs_camo_chunks, hs_camo_dazzle, hs_camo_eyes, hs_camo_urban,
    )
except ImportError as e:
    print(f"[xl_c4d_tool] Cycles节点导入失败: {e}")


def _make_op(op_idname, op_label, op_desc, create_fn):
    """工厂函数：创建材质节点添加操作符"""
    class Op(bpy.types.Operator):
        bl_idname = op_idname
        bl_label = op_label
        bl_description = op_desc
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            mat = context.object.active_material if context.object else None
            if not mat:
                self.report({"WARNING"}, "请先选择带有材质的物体")
                return {"CANCELLED"}
            mat.use_nodes = True
            node = mat.node_tree.nodes.new("ShaderNodeGroup")
            node.node_tree = create_fn()
            try:
                node.node_tree.color_tag = 'TEXTURE'
            except Exception:
                pass
            try:
                node.location = context.space_data.cursor_location
            except AttributeError:
                node.location = (0, 0)
            node.select = True
            mat.node_tree.nodes.active = node
            return {'FINISHED'}
    Op.__name__ = f"Op_{op_idname.replace('.', '_')}"
    return Op


OP_DEFS = [
    ("node.bl_metal_01", "BL_金属01", "金属材质-多层锈蚀", hs_metal_01a),
    ("node.bl_metal_02", "BL_金属02", "金属材质-工业磨损", hs_metal_02a),
    ("node.bl_metal_03", "BL_金属03", "金属材质-旧化氧化", hs_metal_03a),
    ("node.bl_metal_04", "BL_金属04", "金属材质-重度腐蚀", hs_metal_04a),
    ("node.bl_metal_05", "BL_金属05", "金属材质-白色锈蚀", hs_metal_05a),
    ("node.bl_metal_polished", "BL_抛光金属", "抛光金属材质", hs_metal_polished_01a),
    ("node.bl_paint_01", "BL_油漆01", "油漆材质-基础剥落", hs_paint_01a),
    ("node.bl_paint_02", "BL_油漆02", "油漆材质-中度磨损", hs_paint_02a),
    ("node.bl_paint_03", "BL_油漆03", "油漆材质-深度划痕", hs_paint_03a),
    ("node.bl_paint_04", "BL_油漆04", "油漆材质-清漆层", hs_paint_04a),
    ("node.bl_paint_05", "BL_油漆05", "油漆材质-多层叠加", hs_paint_05a),
    ("node.bl_paint_accent", "BL_强调色", "强调色油漆", hs_paint_accent_01a),
    ("node.bl_glass_orange", "BL_橙色玻璃", "橙色半透明玻璃", hs_glass_orange_01a),
    ("node.bl_glass_red", "BL_红色玻璃", "红色半透明玻璃", hs_glass_red_01a),
    ("node.bl_glass_white", "BL_白色玻璃", "白色半透明玻璃", hs_glass_white_01a),
    ("node.bl_plastic", "BL_塑料", "塑料材质-指纹磨损", hs_plastic_01a),
    ("node.bl_rubber_01", "BL_橡胶01", "橡胶材质-基础", hs_rubber_01a),
    ("node.bl_rubber_02", "BL_橡胶02", "橡胶材质-脏旧", hs_rubber_02a),
    ("node.bl_rust", "BL_生锈", "铁锈材质", hs_rust_01a),
    ("node.bl_edges", "BL_边缘磨损", "边缘磨损多层材质", hs_edges_01a),
    ("node.bl_dirt_cavity", "BL_脏污凹腔", "凹腔脏污多层混合", hs_dirt_cavity_01a),
    ("node.bl_dirt_streaks", "BL_脏污条纹", "条纹状脏污效果", hs_dirt_streaks_01a),
    ("node.bl_bump_control", "BL_凹凸控制", "凹凸效果开关", hs_bump_control),
    ("node.bl_camo_chunks", "BL_迷彩块状", "块状迷彩图案", hs_camo_chunks),
    ("node.bl_camo_dazzle", "BL_迷彩炫目", "炫目迷彩图案", hs_camo_dazzle),
    ("node.bl_camo_eyes", "BL_迷彩眼状", "眼状迷彩图案", hs_camo_eyes),
    ("node.bl_camo_urban", "BL_迷彩城市", "城市迷彩图案", hs_camo_urban),
]

cy_classes = tuple(_make_op(d[0], d[1], d[2], d[3]) for d in OP_DEFS)
