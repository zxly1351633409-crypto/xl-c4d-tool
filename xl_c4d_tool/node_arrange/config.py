# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket
from mathutils import Vector

from .properties import NA_PG_Settings

if TYPE_CHECKING:
    from .arrange.graph import Socket

# 全局状态：排列过程中使用的运行时数据

selected: list[BlenderNode] = []
linked_sockets: defaultdict[NodeSocket, set[NodeSocket]] = defaultdict(set)
multi_input_sort_ids: defaultdict[Socket, list[tuple[Socket, int]]] = defaultdict(list)

SETTINGS: NA_PG_Settings
MARGIN: Vector


def reset() -> None:
    selected.clear()
    linked_sockets.clear()
    multi_input_sort_ids.clear()

    global SETTINGS
    SETTINGS = None  # type: ignore

    global MARGIN
    MARGIN = None  # type: ignore
