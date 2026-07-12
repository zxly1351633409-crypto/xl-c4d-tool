"""【操作符：材质节点助手 — 添加各类OC/C4D节点组】
所有节点位于着色器编辑器，点击即在光标位置添加节点组"""
import bpy
from .dirt import create_oc_dirt_noise_group
from .curvature import create_oc_curvature_group
from .color_correction import create_oc_color_correction_group
from .falloff import create_oc_falloff_group
from .gaussian import create_oc_gaussian_spectrum_group
from .c4d_gradient import create_c4d_gradient_group
from .rgbspectrum import create_oc_rgbspectrum_group
from .cloud_layer import create_c4d_cloud_layer_group


def _cursor_location(context):
    space = getattr(context, "space_data", None)
    return getattr(space, "cursor_location", (0, 0))


class NODE_OT_xl_add_oc_dirt(bpy.types.Operator):
    """【操作符：OC_污渍】在光标位置添加Octane风格污垢/脏旧噪声节点组"""
    bl_idname = "node.xl_add_oc_dirt"
    bl_label = "OC_污渍"
    bl_description = "添加OC_污渍节点组（脏旧/磨损效果）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_oc_dirt_noise_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_oc_curvature(bpy.types.Operator):
    """【操作符：OC_曲率】在光标位置添加基于法线方向的凹面/凸面曲率节点组"""
    bl_idname = "node.xl_add_oc_curvature"
    bl_label = "OC_曲率"
    bl_description = "添加OC_曲率节点组（凹面/凸面检测）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_oc_curvature_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.width = 240
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_oc_color_correction(bpy.types.Operator):
    """【操作符：OC_颜色校正】调节亮度/对比度/色相/饱和度/伽马/曝光"""
    bl_idname = "node.xl_add_oc_color_correction"
    bl_label = "OC_颜色校正"
    bl_description = "添加OC_颜色校正节点组（亮度/对比度/色相/饱和度）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_oc_color_correction_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.width = 220
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_oc_falloff(bpy.types.Operator):
    """【操作符：OC_衰减】法线与视角/自定义方向的衰减效果"""
    bl_idname = "node.xl_add_oc_falloff"
    bl_label = "OC_衰减"
    bl_description = "添加OC_衰减节点组（法线/视角方向衰减）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_oc_falloff_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.width = 220
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_oc_gaussian_spectrum(bpy.types.Operator):
    """【操作符：OC_高斯光谱】基于波长的高斯分布光谱颜色生成器"""
    bl_idname = "node.xl_add_oc_gaussian_spectrum"
    bl_label = "OC_高斯光谱"
    bl_description = "添加OC_高斯光谱节点组（波长→颜色）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_oc_gaussian_spectrum_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.width = 240
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_c4d_gradient(bpy.types.Operator):
    """【操作符：C4D_渐变】11种渐变投影类型+可编辑颜色渐变"""
    bl_idname = "node.xl_add_c4d_gradient"
    bl_label = "C4D_渐变"
    bl_description = "添加C4D_渐变节点组（2D/3D/圆柱等11种投影）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_c4d_gradient_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.width = 200
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_oc_rgbspectrum(bpy.types.Operator):
    """【操作符：OC_RGB光谱】输出纯RGB颜色到材质通道"""
    bl_idname = "node.xl_add_oc_rgbspectrum"
    bl_label = "OC_RGB光谱"
    bl_description = "添加OC_RGB光谱节点组（纯色输出）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat = context.object.active_material
        if not mat:
            self.report({"WARNING"}, "请先选择带有材质的物体")
            return {"CANCELLED"}
        mat.use_nodes = True
        node = mat.node_tree.nodes.new("ShaderNodeGroup")
        node.node_tree = create_oc_rgbspectrum_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = context.space_data.cursor_location
        node.width = 180
        node.select = True
        mat.node_tree.nodes.active = node
        return {'FINISHED'}


class NODE_OT_xl_add_c4d_cloud_layer(bpy.types.Operator):
    """【操作符：C4D_云层材质】创建可用于平面的透明程序化云层材质节点组"""
    bl_idname = "node.xl_add_c4d_cloud_layer"
    bl_label = "C4D_云层材质"
    bl_description = "添加C4D_云层材质节点组（平面云层/透明遮罩/可受灯光影响）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({"WARNING"}, "请先选择一个物体")
            return {"CANCELLED"}
        if not hasattr(obj.data, "materials"):
            self.report({"WARNING"}, "请选择可添加材质的物体")
            return {"CANCELLED"}

        mat = obj.active_material
        if mat is None:
            mat = bpy.data.materials.new("C4D_云层材质")
            obj.data.materials.append(mat)
            obj.active_material = mat
        mat.use_nodes = True
        try:
            mat.blend_method = "BLEND"
        except Exception:
            pass
        try:
            mat.show_transparent_back = True
        except Exception:
            pass

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        node = nodes.new("ShaderNodeGroup")
        node.node_tree = create_c4d_cloud_layer_group()
        try:
            node.node_tree.color_tag = 'TEXTURE'
        except Exception:
            pass
        node.location = _cursor_location(context)
        node.width = 260
        node.select = True
        nodes.active = node

        output = next((n for n in nodes if n.bl_idname == "ShaderNodeOutputMaterial"), None)
        if output is None:
            output = nodes.new("ShaderNodeOutputMaterial")
            output.location = (node.location.x + 420, node.location.y)
        surface = output.inputs.get("Surface")
        shader = node.outputs.get("云层材质")
        if surface is not None and shader is not None:
            for link in list(surface.links):
                links.remove(link)
            links.new(shader, surface)

        self.report({"INFO"}, "已创建 C4D_云层材质")
        return {'FINISHED'}


classes = (
    NODE_OT_xl_add_oc_dirt,
    NODE_OT_xl_add_oc_curvature,
    NODE_OT_xl_add_oc_color_correction,
    NODE_OT_xl_add_oc_falloff,
    NODE_OT_xl_add_oc_gaussian_spectrum,
    NODE_OT_xl_add_c4d_gradient,
    NODE_OT_xl_add_oc_rgbspectrum,
    NODE_OT_xl_add_c4d_cloud_layer,
)
