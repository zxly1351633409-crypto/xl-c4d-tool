import bpy


def _sanitize_var_name(name):
    """将节点名称转为合法的Python变量名"""
    result = []
    for c in name:
        if c.isalnum() or c == '_':
            result.append(c)
        else:
            result.append('_')
    var = ''.join(result).lower()
    while '__' in var:
        var = var.replace('__', '_')
    return var.strip('_') or 'node'


def _get_socket_type_str(socket):
    """获取插槽类型的标准字符串"""
    stype = socket.bl_idname if hasattr(socket, 'bl_idname') else socket.socket_type
    mapping = {
        'NodeSocketFloat': 'NodeSocketFloat',
        'NodeSocketInt': 'NodeSocketInt',
        'NodeSocketBool': 'NodeSocketBool',
        'NodeSocketColor': 'NodeSocketColor',
        'NodeSocketVector': 'NodeSocketVector',
        'NodeSocketString': 'NodeSocketString',
        'NodeSocketShader': 'NodeSocketShader',
        'NodeSocketGeometry': 'NodeSocketGeometry',
        'NodeSocketObject': 'NodeSocketObject',
        'NodeSocketCollection': 'NodeSocketCollection',
        'NodeSocketTexture': 'NodeSocketTexture',
        'NodeSocketMaterial': 'NodeSocketMaterial',
        'NodeSocketImage': 'NodeSocketImage',
        'NodeSocketRotation': 'NodeSocketRotation',
        'NodeSocketMenu': 'NodeSocketMenu',
    }
    return mapping.get(stype, stype)


def _get_default_value(socket):
    """安全获取插槽默认值"""
    try:
        if hasattr(socket, 'default_value'):
            val = socket.default_value
            if isinstance(val, (int, float, bool, str)):
                return val
            if hasattr(val, '__len__'):
                return tuple(val)
            return val
    except Exception:
        pass
    return None


def _get_node_properties(node):
    """提取节点的自定义属性（排除内部属性和默认值）"""
    props = {}
    skip = {
        'rna_type', 'type', 'name', 'label', 'location', 'width', 'height',
        'dimensions', 'inputs', 'outputs', 'parent', 'use_custom_color',
        'color', 'select', 'show_options', 'show_preview', 'hide',
        'mute', 'show_texture', 'internal_links', 'socket_value_update',
        'location_absolute', 'warning_propagation',
        'bl_idname', 'bl_label', 'bl_description', 'bl_icon',
        'bl_width_default', 'bl_width_min', 'bl_width_max',
        'bl_height_default', 'bl_height_min', 'bl_height_max',
        'bl_rna', 'bl_static_type',
    }

    for prop in node.bl_rna.properties:
        if prop.identifier in skip:
            continue
        if prop.is_readonly:
            continue
        if not hasattr(node, prop.identifier):
            continue

        try:
            val = getattr(node, prop.identifier)
            if isinstance(val, bpy.types.Node):
                continue
            if isinstance(val, bpy.types.NodeTree):
                continue

            prop_type = prop.type
            if prop_type == 'ENUM':
                if isinstance(val, str) and val:
                    props[prop.identifier] = val
            elif prop_type == 'BOOLEAN':
                props[prop.identifier] = bool(val)
            elif prop_type in ('INT', 'FLOAT'):
                if val != prop.default:
                    props[prop.identifier] = val
            elif prop_type == 'STRING':
                if val and val != prop.default:
                    props[prop.identifier] = val
            elif prop_type == 'POINTER':
                if isinstance(val, bpy.types.Image):
                    props[prop.identifier + '_image_name'] = val.name
                elif isinstance(val, bpy.types.ColorRamp):
                    # 捕获颜色渐变的 interpolation 和 elements 色标
                    cr_data = {
                        'interpolation': val.interpolation,
                        'elements': []
                    }
                    for el in val.elements:
                        cr_data['elements'].append({
                            'position': el.position,
                            'color': tuple(el.color),
                        })
                    props[prop.identifier] = cr_data
        except Exception:
            continue

    return props


def _get_input_defaults(node):
    """获取未连接输入端口的默认值"""
    defaults = {}
    for i, inp in enumerate(node.inputs):
        if inp.is_linked:
            continue
        val = _get_default_value(inp)
        if val is not None:
            try:
                default_prop = inp.bl_rna.properties.get('default_value')
                if default_prop:
                    default_val = default_prop.default
                    if isinstance(val, tuple):
                        if any(abs(a - b) > 0.0001 for a, b in zip(val, default_prop.default)):
                            defaults[i] = val
                    elif val != default_val:
                        defaults[i] = val
                else:
                    defaults[i] = val
            except Exception:
                defaults[i] = val
    return defaults


def parse_node_group(node_tree, parsed_groups=None):
    """【核心解析器】将单个节点树解析为结构化数据
    递归处理嵌套的子节点组
    输入: bpy.types.NodeTree
    输出: dict {name, bl_idname, inputs, outputs, nodes, links, frames, sub_groups, node_types}"""
    if parsed_groups is None:
        parsed_groups = set()

    group_name = node_tree.name
    if group_name in parsed_groups:
        return None
    parsed_groups.add(group_name)

    result = {
        'name': group_name,
        'bl_idname': node_tree.bl_idname,
        'inputs': [],
        'outputs': [],
        'nodes': [],
        'links': [],
        'frames': [],
        'sub_groups': [],
        'node_types': set(),
    }

    for item in node_tree.interface.items_tree:
        if item.item_type != 'SOCKET':
            continue
        socket_info = {
            'name': item.name,
            'socket_type': _get_socket_type_str(item),
            'in_out': item.in_out,
        }
        if hasattr(item, 'default_value') and item.in_out == 'INPUT':
            dv = _get_default_value(item)
            if dv is not None:
                socket_info['default_value'] = dv
        if item.in_out == 'INPUT':
            result['inputs'].append(socket_info)
        else:
            result['outputs'].append(socket_info)

    var_counter = {}
    node_var_map = {}

    for node in node_tree.nodes:
        ntype = node.bl_idname
        result['node_types'].add(ntype)

        if ntype == 'NodeFrame':
            frame_info = {
                'var_name': _sanitize_var_name(node.name or node.label or 'frame'),
                'name': node.name,
                'label': node.label or '',
                'color': tuple(node.color) if node.use_custom_color else None,
                'use_custom_color': node.use_custom_color,
            }
            result['frames'].append(frame_info)
            continue

        base_var = _sanitize_var_name(node.label or node.name or ntype)
        if base_var in var_counter:
            var_counter[base_var] += 1
            var_name = f"{base_var}_{var_counter[base_var]}"
        else:
            var_counter[base_var] = 0
            var_name = base_var

        node_info = {
            'var_name': var_name,
            'name': node.name,
            'bl_idname': ntype,
            'label': node.label or '',
            'location': tuple(node.location),
            'properties': _get_node_properties(node),
            'input_defaults': _get_input_defaults(node),
            'parent_frame': None,
        }

        if node.parent and node.parent.bl_idname == 'NodeFrame':
            node_info['parent_frame'] = _sanitize_var_name(
                node.parent.name or node.parent.label or 'frame'
            )

        if getattr(node, 'node_tree', None) is not None:
            sub_name = node.node_tree.name
            node_info['sub_group_name'] = sub_name
            if sub_name not in result['sub_groups']:
                result['sub_groups'].append(sub_name)

        node_var_map[node.name] = var_name
        result['nodes'].append(node_info)

    for link in node_tree.links:
        from_node_name = link.from_node.name
        to_node_name = link.to_node.name

        from_var = node_var_map.get(from_node_name)
        to_var = node_var_map.get(to_node_name)
        if not from_var or not to_var:
            continue

        from_idx = None
        for i, out in enumerate(link.from_node.outputs):
            if out == link.from_socket:
                from_idx = i
                break

        to_idx = None
        for i, inp in enumerate(link.to_node.inputs):
            if inp == link.to_socket:
                to_idx = i
                break

        from_socket_name = link.from_socket.name if hasattr(link.from_socket, 'name') else ''
        to_socket_name = link.to_socket.name if hasattr(link.to_socket, 'name') else ''

        link_info = {
            'from_node': from_var,
            'from_socket_idx': from_idx,
            'from_socket_name': from_socket_name,
            'to_node': to_var,
            'to_socket_idx': to_idx,
            'to_socket_name': to_socket_name,
        }
        result['links'].append(link_info)

    return result


def _collect_sub_groups_recursive(data, parsed, all_results):
    """递归收集所有嵌套子节点组"""
    for sub_name in list(data.get('sub_groups', [])):
        if sub_name in parsed:
            continue
        sub_ng = bpy.data.node_groups.get(sub_name)
        if not sub_ng:
            continue
        sub_data = parse_node_group(sub_ng, parsed)
        if sub_data:
            all_results.append(sub_data)
            _collect_sub_groups_recursive(sub_data, parsed, all_results)


def parse_all_groups_in_file():
    """解析当前.blend文件中的所有节点组（含嵌套）"""
    results = []
    parsed = set()
    for ng in bpy.data.node_groups:
        if ng.name in parsed:
            continue
        data = parse_node_group(ng, parsed)
        if data:
            results.append(data)
            _collect_sub_groups_recursive(data, parsed, results)
    return results


def parse_current_editor_group(context):
    """解析当前节点编辑器中的节点组"""
    space = context.space_data
    if not space or space.type != 'NODE_EDITOR':
        return None, "当前不在节点编辑器中"
    if not space.node_tree:
        return None, "当前没有打开节点组"
    ng = space.node_tree
    parsed = set()
    data = parse_node_group(ng, parsed)
    if not data:
        return None, f"无法解析节点组: {ng.name}"

    all_results = [data]
    _collect_sub_groups_recursive(data, parsed, all_results)

    return all_results, None
