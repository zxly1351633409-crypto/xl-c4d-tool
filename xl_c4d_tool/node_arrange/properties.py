from bpy.props import (
    BoolProperty, EnumProperty, FloatProperty,
    IntProperty, IntVectorProperty, PointerProperty,
)
from bpy.types import PropertyGroup, Scene
import bpy

_MODE_KWARGS = dict(
    items=(
        ('NODES', "Nodes", "Selected nodes in the current node tree"),
        ('TREES', "Trees", "All node trees in the current .blend file")),
    name="Mode",
    default='NODES',
    options=set())


class NA_PG_Settings(PropertyGroup):
    arrange_mode: EnumProperty(**_MODE_KWARGS, description="What to arrange")
    margin: IntVectorProperty(
        name="Spacing", description="Space between nodes",
        default=(50, 50), min=0, options=set(), subtype='XYZ', size=2)
    iterations: IntProperty(
        name="Iterations",
        description="Number of times to reduce crossings between links",
        default=25, min=1, options=set())
    direction: EnumProperty(
        items=(
            ('LEFT_DOWN', "Bottom Left", ""),
            ('RIGHT_DOWN', "Bottom Right", ""),
            ('LEFT_UP', "Top Left", ""),
            ('RIGHT_UP', "Top Right", ""),
            None,
            ('BALANCED', "Balanced", "Combine four extreme layouts")),
        name="Node Alignment", description="Direction of layout",
        default='BALANCED', options=set())
    socket_alignment: EnumProperty(
        items=(
            ('NONE', "None", "Only try to align the tops of nodes"),
            ('MODERATE', "Moderate", "Align sockets or node tops"),
            ('FULL', "Full", "Always try to align sockets")),
        name="Socket Alignment", description="Method to align sockets",
        default='MODERATE', options=set())
    add_reroutes: BoolProperty(
        name="Add Reroutes", description="Insert reroutes into links",
        default=True, options=set())
    keep_reroutes_outside_frames: BoolProperty(
        name="Place Reroutes Outside Frames",
        description="Attach reroutes to lowest common frame",
        default=False, options=set())
    stack_collapsed: BoolProperty(
        name="Stack Collapsed Nodes",
        description="Stack collapsed math nodes",
        default=False, options=set())
    stack_margin_y_fac: FloatProperty(
        name="Spacing Y Factor",
        description="Factor for vertical spacing between stacked nodes",
        default=0.5, min=0, max=1, subtype='FACTOR', options=set())
    recenter_mode: EnumProperty(**_MODE_KWARGS, description="What to recenter")
    origin: EnumProperty(
        items=(
            ('CENTER', "Center", "Move selected nodes by average location"),
            ('ACTIVE_OUTPUT', "Active Output", "Move by active output location"),
            ('ACTIVE_NODE', "Active Node", "Move by active node location")),
        name="Origin", default='CENTER', options=set())


def register() -> None:
    try:
        bpy.utils.register_class(NA_PG_Settings)
    except Exception:
        pass
    try:
        Scene.na_settings = PointerProperty(type=NA_PG_Settings)
    except Exception:
        pass


def unregister() -> None:
    try:
        del Scene.na_settings
    except Exception:
        pass
    try:
        bpy.utils.unregister_class(NA_PG_Settings)
    except Exception:
        pass
