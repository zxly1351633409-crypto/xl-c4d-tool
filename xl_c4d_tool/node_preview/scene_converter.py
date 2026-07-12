#
#     This file is part of NodePreview.
#     Copyright (C) 2021 Simon Wendsche
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import ceil

def scene_to_script(context, needs_more_samples, use_sphere_preview, thumb_resolution):
    # Упрощенная версия для Blender 5.0
    return f"""
scene = bpy.context.scene

# Базовые настройки рендера
scene.render.engine = '{context.scene.render.engine}'

# Настройки Cycles
if '{context.scene.render.engine}' == 'CYCLES':
    scene.cycles.samples = {4 if needs_more_samples else 1}
    scene.render.use_compositing = {needs_more_samples}

# Настройки EEVEE  
if '{context.scene.render.engine}' == 'BLENDER_EEVEE':
    scene.eevee.taa_render_samples = {4 if needs_more_samples else 1}

scene.render.threads = {4 if needs_more_samples else 1}

# Оптимизация для маленьких превью
if {needs_more_samples} and bpy.app.version < (3, 0, 0):
    scene.render.tile_x = {ceil(thumb_resolution / 2)}
    scene.render.tile_y = {ceil(thumb_resolution / 2)}

# Переключение между сферой и плоскостью
bpy.data.objects["Sphere"].hide_render = {not use_sphere_preview}
bpy.data.objects["Light"].hide_render = {not use_sphere_preview}
bpy.data.objects["Plane"].hide_render = {use_sphere_preview}
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs["Strength"].default_value = {0.025 if use_sphere_preview else 1}
"""