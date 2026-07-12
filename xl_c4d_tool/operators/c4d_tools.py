import bpy
import bmesh
from bpy_extras import view3d_utils
from ..utils.logger import logger


class SeparateAndKeepLinesOperator(bpy.types.Operator):
    bl_idname = "object.xl_separate_and_keep_lines"
    bl_label = "提取样条线"
    bl_description = "将选中的线段分离为新物体并删除面"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "请选中一个网格物体！")
            return {'CANCELLED'}

        if context.object.mode != 'EDIT':
            self.report({'WARNING'}, "请先进入编辑模式")
            return {'CANCELLED'}

        logger.info("===== 开始提取样条线 =====")

        bpy.ops.mesh.duplicate()
        logger.info("副本创建成功")

        bpy.ops.mesh.separate(type='SELECTED')
        logger.info("分离成功")

        bpy.ops.object.mode_set(mode='OBJECT')

        all_objects = context.view_layer.objects
        active_object = context.view_layer.objects.active

        new_obj = None
        for obj_item in all_objects:
            if obj_item.select_get() and obj_item != active_object:
                new_obj = obj_item
                break

        if new_obj is None:
            self.report({'WARNING'}, "没有成功分离物体！")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')

        suffix = context.scene.xl_c4d_tool_props.new_object_suffix if context.scene.xl_c4d_tool_props else "_new"
        new_obj.name = new_obj.name + suffix
        active_object.name = active_object.name + "_old"
        logger.info(f"新物体: {new_obj.name}，原始物体: {active_object.name}")

        context.view_layer.objects.active = new_obj
        new_obj.select_set(True)

        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.mode_set(mode='OBJECT')

        context.view_layer.objects.active = new_obj
        new_obj.select_set(True)
        bpy.ops.object.convert(target='CURVE')
        new_obj = context.view_layer.objects.active

        new_obj.name = new_obj.name.replace(suffix, "")
        active_object.name = active_object.name.replace("_old", "")

        logger.info("===== 提取样条线完成 =====")
        self.report({'INFO'}, "提取样条线完成")
        return {'FINISHED'}


class AlignObjectsOperator(bpy.types.Operator):
    bl_idname = "object.xl_align_objects"
    bl_label = "对齐物体"
    bl_description = "将选中的物体对齐到活动物体的位置和旋转"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.view_layer.objects.active
        selected_objects = context.selected_objects

        if not active:
            self.report({'WARNING'}, "没有活动物体")
            return {'CANCELLED'}

        if len(selected_objects) < 2:
            self.report({'WARNING'}, "请选中至少两个物体")
            return {'CANCELLED'}

        logger.info(f"===== 对齐物体到 {active.name} =====")
        for obj in selected_objects:
            if obj != active:
                obj.location = active.location
                obj.rotation_euler = active.rotation_euler
                logger.debug(f"对齐: {obj.name}")

        logger.info("===== 对齐物体完成 =====")
        self.report({'INFO'}, "对齐物体已执行")
        return {'FINISHED'}


class AlignOriginOperator(bpy.types.Operator):
    bl_idname = "object.xl_align_origin"
    bl_label = "对齐几何中心"
    bl_description = "将选定物体的原点对齐到几何中心"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if obj is None:
            self.report({'WARNING'}, "没有选中的物体！")
            return {'CANCELLED'}

        if obj.type != 'MESH':
            self.report({'WARNING'}, "请选择一个网格物体！")
            return {'CANCELLED'}

        logger.info(f"===== 对齐原点到几何中心: {obj.name} =====")

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        logger.info("===== 对齐原点完成 =====")
        self.report({'INFO'}, f"原点已对齐到 {obj.name} 的几何中心")
        return {'FINISHED'}


class LoopSelectionOperator(bpy.types.Operator):
    bl_idname = "mesh.xl_loop_selection"
    bl_label = "循环选择"
    bl_description = "在编辑模式下按当前点/边/面选择模式扩展循环选择"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH' and context.object.mode == 'EDIT'

    @staticmethod
    def _opposite_edge(face, edge):
        if len(face.verts) != 4:
            return None
        for loop in face.loops:
            if loop.edge == edge:
                return loop.link_loop_next.link_loop_next.edge
        return None

    @classmethod
    def _edge_loop_edges(cls, edge):
        result = {edge}
        for start_loop in edge.link_loops:
            current_loop = start_loop
            while True:
                opposite = cls._opposite_edge(current_loop.face, current_loop.edge)
                if opposite is None or opposite in result:
                    break
                result.add(opposite)
                next_loops = [loop for loop in opposite.link_loops if loop.face != current_loop.face]
                if not next_loops:
                    break
                current_loop = next_loops[0]
        return result

    @classmethod
    def _walk_faces(cls, face, cross_edge, result):
        current_face = face
        edge = cross_edge
        while edge is not None:
            next_loops = [loop for loop in edge.link_loops if loop.face != current_face]
            if not next_loops:
                break
            next_face = next_loops[0].face
            if next_face in result:
                break
            result.add(next_face)
            edge = cls._opposite_edge(next_face, edge)
            current_face = next_face

    @classmethod
    def _face_loop_faces(cls, selected_faces):
        result = set(selected_faces)
        selected_set = set(selected_faces)
        used_pairs = False

        for face in selected_faces:
            for edge in face.edges:
                neighbors = [loop.face for loop in edge.link_loops if loop.face != face and loop.face in selected_set]
                for neighbor in neighbors:
                    used_pairs = True
                    result.add(face)
                    result.add(neighbor)
                    cls._walk_faces(face, cls._opposite_edge(face, edge), result)
                    cls._walk_faces(neighbor, cls._opposite_edge(neighbor, edge), result)

        if used_pairs:
            return result

        for face in selected_faces:
            if len(face.edges) != 4:
                continue
            edges = list(face.edges)
            for edge in (edges[0], edges[2], edges[1], edges[3]):
                cls._walk_faces(face, edge, result)
        return result

    def execute(self, context):
        obj = context.object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        vert_mode, edge_mode, face_mode = context.tool_settings.mesh_select_mode
        changed = False

        if face_mode:
            selected_faces = [face for face in bm.faces if face.select]
            if not selected_faces:
                self.report({'WARNING'}, "请先选择一个面")
                return {'CANCELLED'}
            for face in self._face_loop_faces(selected_faces):
                face.select_set(True)
                changed = True
        elif edge_mode:
            selected_edges = [edge for edge in bm.edges if edge.select]
            if not selected_edges:
                self.report({'WARNING'}, "请先选择一条边")
                return {'CANCELLED'}
            for edge in selected_edges:
                for loop_edge in self._edge_loop_edges(edge):
                    loop_edge.select_set(True)
                    changed = True
        elif vert_mode:
            selected_edges = [edge for edge in bm.edges if all(v.select for v in edge.verts)]
            selected_verts = [vert for vert in bm.verts if vert.select]
            loop_edges = set()
            if selected_edges:
                for edge in selected_edges:
                    loop_edges.update(self._edge_loop_edges(edge))
            else:
                for vert in selected_verts:
                    for edge in vert.link_edges:
                        loop_edges.update(self._edge_loop_edges(edge))
            if not loop_edges:
                self.report({'WARNING'}, "点模式请先选择点，最好选择相邻两点")
                return {'CANCELLED'}
            for edge in loop_edges:
                for vert in edge.verts:
                    vert.select_set(True)
                    changed = True
        else:
            self.report({'WARNING'}, "请切换到点、边或面选择模式")
            return {'CANCELLED'}

        if changed:
            if not (vert_mode and not edge_mode and not face_mode):
                bm.select_flush_mode()
            bmesh.update_edit_mesh(obj.data)
            self.report({'INFO'}, "循环选择完成")
            return {'FINISHED'}

        self.report({'WARNING'}, "没有找到可扩展的循环")
        return {'CANCELLED'}


class InteractiveLoopSelectionOperator(bpy.types.Operator):
    bl_idname = "mesh.xl_loop_selection"
    bl_label = "循环选择"
    bl_description = "按左右或上下方向扩展循环选择；方向不对时按另一个按钮"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(
        name="方向",
        items=(
            ('A', "左右循环", "沿左右方向扩展循环"),
            ('B', "上下循环", "沿上下方向扩展循环"),
        ),
        default='A',
    )

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH' and context.object.mode == 'EDIT'

    @staticmethod
    def _opposite_edge(face, edge):
        if len(face.verts) != 4:
            return None
        for loop in face.loops:
            if loop.edge == edge:
                return loop.link_loop_next.link_loop_next.edge
        return None

    @classmethod
    def _edge_loop_edges(cls, edge):
        result = {edge}
        for start_loop in edge.link_loops:
            current_loop = start_loop
            while True:
                opposite = cls._opposite_edge(current_loop.face, current_loop.edge)
                if opposite is None or opposite in result:
                    break
                result.add(opposite)
                next_loops = [loop for loop in opposite.link_loops if loop.face != current_loop.face]
                if not next_loops:
                    break
                current_loop = next_loops[0]
        return result

    @classmethod
    def _walk_faces(cls, face, cross_edge, result):
        current_face = face
        edge = cross_edge
        while edge is not None:
            next_loops = [loop for loop in edge.link_loops if loop.face != current_face]
            if not next_loops:
                break
            next_face = next_loops[0].face
            if next_face in result:
                break
            result.add(next_face)
            edge = cls._opposite_edge(next_face, edge)
            current_face = next_face

    @classmethod
    def _face_loop_from_edge(cls, face, edge):
        result = {face}
        if len(face.edges) != 4:
            return result
        cls._walk_faces(face, edge, result)
        opposite = cls._opposite_edge(face, edge)
        if opposite is not None:
            cls._walk_faces(face, opposite, result)
        return result

    @staticmethod
    def _other_vert(edge, vert):
        return edge.verts[1] if edge.verts[0] == vert else edge.verts[0]

    @classmethod
    def _next_edge_through_vertex(cls, edge, vert, visited):
        candidates = [item for item in vert.link_edges if item != edge and item not in visited]
        if not candidates:
            return None
        other = cls._other_vert(edge, vert)
        incoming = vert.co - other.co
        if incoming.length == 0:
            return candidates[0]
        incoming.normalize()

        def score(candidate):
            next_vert = cls._other_vert(candidate, vert)
            outgoing = next_vert.co - vert.co
            if outgoing.length == 0:
                return -1.0
            outgoing.normalize()
            return incoming.dot(outgoing)

        best_edge = max(candidates, key=score)
        if score(best_edge) < 0.5:
            return None
        return best_edge

    @classmethod
    def _edge_loop_by_vertices(cls, edge):
        result = {edge}
        for start_vert in edge.verts:
            current_edge = edge
            current_vert = start_vert
            while True:
                next_edge = cls._next_edge_through_vertex(current_edge, current_vert, result)
                if next_edge is None:
                    break
                result.add(next_edge)
                current_vert = cls._other_vert(next_edge, current_vert)
                current_edge = next_edge
        return result

    @classmethod
    def _face_edge_for_direction(cls, face, direction):
        if not face.edges:
            return None
        edges = list(face.edges)
        if len(edges) < 4:
            return edges[0]
        return edges[0] if direction == 'A' else edges[1]

    @classmethod
    def _vertex_direction_edge(cls, vert, direction):
        linked_edges = list(vert.link_edges)
        if not linked_edges:
            return None
        if len(linked_edges) == 1:
            return linked_edges[0]

        def axis_score(edge, axis_index):
            other = cls._other_vert(edge, vert)
            vec = other.co - vert.co
            if vec.length == 0:
                return 0.0
            vec.normalize()
            return abs(vec[axis_index])

        if direction == 'A':
            return max(linked_edges, key=lambda edge: axis_score(edge, 0))
        return max(linked_edges, key=lambda edge: max(axis_score(edge, 1), axis_score(edge, 2)))

    @classmethod
    def _perpendicular_edge_at_vertex(cls, edge, vert):
        candidates = [item for item in vert.link_edges if item != edge]
        if not candidates:
            return None
        base_other = cls._other_vert(edge, vert)
        base = base_other.co - vert.co
        if base.length == 0:
            return candidates[0]
        base.normalize()

        def score(candidate):
            other = cls._other_vert(candidate, vert)
            vec = other.co - vert.co
            if vec.length == 0:
                return 1.0
            vec.normalize()
            return abs(base.dot(vec))

        return min(candidates, key=score)

    @staticmethod
    def _edge_distance_to_point(edge, point):
        start = edge.verts[0].co
        end = edge.verts[1].co
        direction = end - start
        length_squared = direction.length_squared
        if length_squared == 0:
            return (point - start).length
        factor = max(0.0, min(1.0, (point - start).dot(direction) / length_squared))
        nearest = start + direction * factor
        return (point - nearest).length

    @classmethod
    def _closest_edge(cls, face, point):
        if not face.edges:
            return None
        return min(face.edges, key=lambda edge: cls._edge_distance_to_point(edge, point))

    @staticmethod
    def _capture_selection(bm):
        return {
            "verts": {vert.index for vert in bm.verts if vert.select},
            "edges": {edge.index for edge in bm.edges if edge.select},
            "faces": {face.index for face in bm.faces if face.select},
        }

    @staticmethod
    def _restore_selection(bm, selection):
        for face in bm.faces:
            face.select_set(face.index in selection["faces"])
        for edge in bm.edges:
            edge.select_set(edge.index in selection["edges"])
        for vert in bm.verts:
            vert.select_set(vert.index in selection["verts"])

    @staticmethod
    def _clear_selection(bm):
        for face in bm.faces:
            face.select_set(False)
        for edge in bm.edges:
            edge.select_set(False)
        for vert in bm.verts:
            vert.select_set(False)

    @staticmethod
    def _ensure_bmesh(obj):
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        bm.verts.index_update()
        bm.edges.index_update()
        bm.faces.index_update()
        return bm

    def _raycast_face(self, context, event):
        obj = context.object
        region = self._region
        rv3d = self._rv3d
        if obj is None or region is None or rv3d is None:
            return None

        coord = (event.mouse_x - region.x, event.mouse_y - region.y)
        if coord[0] < 0 or coord[1] < 0 or coord[0] > region.width or coord[1] > region.height:
            return None

        origin_world = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        direction_world = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        matrix_inv = obj.matrix_world.inverted()
        origin_local = matrix_inv @ origin_world
        direction_local = matrix_inv.to_3x3() @ direction_world
        if direction_local.length == 0:
            return None
        direction_local.normalize()

        hit, location, _normal, face_index = obj.ray_cast(origin_local, direction_local)
        if not hit:
            return None

        bm = self._ensure_bmesh(obj)
        if face_index < 0 or face_index >= len(bm.faces):
            return None
        return bm, bm.faces[face_index], location

    def _preview_from_hover(self, context, event):
        hover = self._raycast_face(context, event)
        if hover is None:
            return False

        bm, face, location = hover
        vert_mode, edge_mode, face_mode = self._select_mode
        closest_edge = self._closest_edge(face, location)

        self._clear_selection(bm)
        changed = False

        if face_mode:
            for loop_face in self._face_loop_from_edge(face, closest_edge):
                loop_face.select_set(True)
                changed = True
        elif edge_mode:
            if closest_edge is not None:
                for loop_edge in self._edge_loop_edges(closest_edge):
                    loop_edge.select_set(True)
                    changed = True
        elif vert_mode:
            if closest_edge is not None:
                for loop_edge in self._edge_loop_edges(closest_edge):
                    for vert in loop_edge.verts:
                        vert.select_set(True)
                        changed = True

        if changed:
            if not (vert_mode and not edge_mode and not face_mode):
                bm.select_flush_mode()
            bmesh.update_edit_mesh(context.object.data)
            if self._area:
                self._area.tag_redraw()
        return changed

    def _finish(self, context, restore=False):
        obj = context.object
        if obj is not None and obj.type == 'MESH' and obj.mode == 'EDIT' and restore and self._initial_selection:
            bm = self._ensure_bmesh(obj)
            self._restore_selection(bm, self._initial_selection)
            bmesh.update_edit_mesh(obj.data)
        if self._area:
            self._area.header_text_set(None)
            self._area.tag_redraw()

    def invoke(self, context, event):
        return self.execute(context)

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            self._preview_from_hover(context, event)
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self._finish(context, restore=False)
            return {'FINISHED'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self._finish(context, restore=True)
            return {'CANCELLED'}
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE', 'WHEELOUTMOUSE'}:
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def execute(self, context):
        obj = context.object
        bm = self._ensure_bmesh(obj)
        vert_mode, edge_mode, face_mode = context.tool_settings.mesh_select_mode
        changed = False

        if face_mode:
            selected_faces = [face for face in bm.faces if face.select]
            if not selected_faces:
                self.report({'WARNING'}, "请先选择一个面")
                return {'CANCELLED'}
            for face in selected_faces:
                edge = self._face_edge_for_direction(face, self.direction)
                for loop_face in self._face_loop_from_edge(face, edge):
                    loop_face.select_set(True)
                    changed = True
        elif edge_mode:
            selected_edges = [edge for edge in bm.edges if edge.select]
            if not selected_edges:
                self.report({'WARNING'}, "请先选择一条边")
                return {'CANCELLED'}
            for edge in selected_edges:
                loop_edges = self._edge_loop_by_vertices(edge) if self.direction == 'A' else self._edge_loop_edges(edge)
                for loop_edge in loop_edges:
                    loop_edge.select_set(True)
                    changed = True
        elif vert_mode:
            selected_edges = [edge for edge in bm.edges if all(vert.select for vert in edge.verts)]
            selected_verts = [vert for vert in bm.verts if vert.select]
            seed_edges = set()
            if selected_edges and self.direction == 'A':
                seed_edges.update(selected_edges)
            elif selected_edges:
                for edge in selected_edges:
                    for vert in edge.verts:
                        alt_edge = self._perpendicular_edge_at_vertex(edge, vert)
                        if alt_edge is not None:
                            seed_edges.add(alt_edge)
            else:
                for vert in selected_verts:
                    edge = self._vertex_direction_edge(vert, self.direction)
                    if edge is not None:
                        seed_edges.add(edge)
            if not seed_edges:
                self.report({'WARNING'}, "点模式请先选择一个点；选择相邻两点会更准确")
                return {'CANCELLED'}
            for edge in seed_edges:
                loop_edges = self._edge_loop_by_vertices(edge)
                for loop_edge in loop_edges:
                    for vert in loop_edge.verts:
                        vert.select_set(True)
                        changed = True
        else:
            self.report({'WARNING'}, "请切换到点、边或面选择模式")
            return {'CANCELLED'}

        if changed:
            if not (vert_mode and not edge_mode and not face_mode):
                bm.select_flush_mode()
            bmesh.update_edit_mesh(obj.data)
            label = "左右循环" if self.direction == 'A' else "上下循环"
            self.report({'INFO'}, f"{label}完成")
            return {'FINISHED'}

        self.report({'WARNING'}, "没有找到可扩展的循环")
        return {'CANCELLED'}


classes = [
    SeparateAndKeepLinesOperator,
    AlignObjectsOperator,
    AlignOriginOperator,
    InteractiveLoopSelectionOperator,
]


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)
    logger.info("C4D工具操作符注册完成")


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
    logger.info("C4D工具操作符注销完成")
