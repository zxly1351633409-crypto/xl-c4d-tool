"""【Cycles着色器节点组（BL_前缀）】
整合Blender Cycles着色器节点代码到材质节点助手
包含: 金属/油漆/玻璃/塑料/橡胶/生锈/边缘磨损/脏污/迷彩等
底层依赖: pf_grunge纹理 / perlin_noise噪声 / dent_noise凹痕 / cavity凹腔 / edge边缘"""
import bpy

from .hs_metal_01a import hs_metal_01a
from .hs_metal_02a import hs_metal_02a
from .hs_metal_03a import hs_metal_03a
from .hs_metal_04a import hs_metal_04a
from .hs_metal_05a import hs_metal_05a
from .hs_metal_polished_01a import hs_metal_polished_01a
from .hs_paint_01a import hs_paint_01a
from .hs_paint_02a import hs_paint_02a
from .hs_paint_03a import hs_paint_03a
from .hs_paint_04a import hs_paint_04a
from .hs_paint_05a import hs_paint_05a
from .hs_paint_accent_01a import hs_paint_accent_01a
from .hs_glass_orange_01a import hs_glass_orange_01a
from .hs_glass_red_01a import hs_glass_red_01a
from .hs_glass_white_01a import hs_glass_white_01a
from .hs_plastic_01a import hs_plastic_01a
from .hs_rubber_01a import hs_rubber_01a
from .hs_rubber_02a import hs_rubber_02a
from .hs_rust_01a import hs_rust_01a
from .hs_edges_01a import hs_edges_01a
from .hs_dirt_cavity_01a import hs_dirt_cavity_01a
from .hs_dirt_streaks_01a import hs_dirt_streaks_01a
from .hs_bump_control import hs_bump_control
from .hs_camo_chunks import hs_camo_chunks
from .hs_camo_dazzle import hs_camo_dazzle
from .hs_camo_eyes import hs_camo_eyes
from .hs_camo_urban import hs_camo_urban
