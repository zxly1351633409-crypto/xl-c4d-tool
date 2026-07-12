"""【属性定义：材质节点助手 — 渐变类型和RGB预设】"""
import bpy
from .c4d_gradient import GRADIENT_TYPES

gradient_items = [(gt[0], gt[1], gt[2]) for gt in GRADIENT_TYPES]

rgb_preset_items = [
    ("1.0,1.0,1.0,1.0", "纯白", ""),
    ("0.8,0.2,0.2,1.0", "红色", ""),
    ("0.2,0.8,0.2,1.0", "绿色", ""),
    ("0.2,0.2,0.8,1.0", "蓝色", ""),
    ("1.0,0.9,0.0,1.0", "黄色", ""),
    ("0.0,0.0,0.0,1.0", "黑色", ""),
]


def update_c4d_grad_type(self, context):
    """渐变类型更新回调：根据选择更新节点内部的Type端口值"""
    if self.node_tree and "C4D_渐变" in self.node_tree.name:
        for inp in self.inputs:
            if inp.name == "Type":
                inp.default_value = int(self.xl_c4d_gradient_type)
                break


def update_rgb_preset(self, context):
    """RGB预设更新回调：根据选择更新RGB节点颜色"""
    if self.node_tree and "OC_RGB光谱" in self.node_tree.name:
        rgb_node = self.node_tree.nodes.get("RGB")
        if rgb_node:
            try:
                color = [float(c) for c in self.xl_rgbspectrum_preset.split(",")]
                rgb_node.outputs[0].default_value = tuple(color)
            except Exception:
                pass


def register():
    bpy.types.ShaderNodeGroup.xl_c4d_gradient_type = bpy.props.EnumProperty(
        name="C4D Gradient Type", items=gradient_items, update=update_c4d_grad_type
    )
    bpy.types.ShaderNodeGroup.xl_rgbspectrum_preset = bpy.props.EnumProperty(
        name="RGB Preset", items=rgb_preset_items, update=update_rgb_preset,
        description="快速选择预设颜色"
    )


def unregister():
    del bpy.types.ShaderNodeGroup.xl_c4d_gradient_type
    del bpy.types.ShaderNodeGroup.xl_rgbspectrum_preset
