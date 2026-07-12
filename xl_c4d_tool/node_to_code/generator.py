import os


def _py_repr(val):
    """将Python值转为可执行的字符串表示"""
    if isinstance(val, bool):
        return "True" if val else "False"
    if isinstance(val, str):
        return repr(val)
    if isinstance(val, tuple):
        if len(val) == 2:
            return f"({val[0]}, {val[1]})"
        if len(val) == 3:
            return f"({val[0]:.4f}, {val[1]:.4f}, {val[2]:.4f})"
        if len(val) == 4:
            return f"({val[0]:.4f}, {val[1]:.4f}, {val[2]:.4f}, {val[3]:.4f})"
        return repr(val)
    if isinstance(val, float):
        if val == int(val) and abs(val) < 10000:
            return f"{int(val)}.0"
        return f"{val}"
    if isinstance(val, int):
        return str(val)
    return repr(val)


def _get_tree_type_str(bl_idname):
    """将节点树bl_idname映射为标准类型字符串"""
    mapping = {
        'ShaderNodeTree': 'ShaderNodeTree',
        'GeometryNodeTree': 'GeometryNodeTree',
        'CompositorNodeTree': 'CompositorNodeTree',
        'TextureNodeTree': 'TextureNodeTree',
    }
    return mapping.get(bl_idname, bl_idname or 'ShaderNodeTree')


def _get_func_name(group_name):
    """将节点组名称转为合法的Python函数名"""
    name = group_name.replace(' ', '_').replace('-', '_')
    result = []
    for c in name:
        if c.isalnum() or c == '_':
            result.append(c.lower())
    return ''.join(result) or 'create_group'


def _indent(lines, level=1):
    """缩进代码行"""
    prefix = "    " * level
    return [prefix + line for line in lines]


def generate_group_code(data):
    """【代码生成核心】将解析后的节点组数据转为可执行的Python代码
    输入 data: parser.parse_node_group() 返回的解析数据
    输出: 完整的 .py 文件内容字符串"""
    group_name = data['name']
    func_name = _get_func_name(group_name)
    tree_type = _get_tree_type_str(data.get('bl_idname', 'ShaderNodeTree'))

    lines = []
    lines.append("import bpy")
    lines.append("from ...utils.node_utils import get_mix_f_ports, create_frame, label_node")

    sub_group_names = set()
    for node in data['nodes']:
        sgn = node.get('sub_group_name')
        if sgn:
            sub_group_names.add(sgn)
    for sub_name in sorted(sub_group_names):
        sub_mod = _sanitize_module_name(sub_name)
        sub_fn = _get_func_name(sub_name)
        lines.append(f"from .{sub_mod} import {sub_fn}")

    lines.append("")
    lines.append("")
    lines.append(f"def {func_name}():")
    lines.append(f'    """')
    lines.append(f"    节点组: {group_name}")
    lines.append(f'    """')
    lines.append(f'    group_name = "{group_name}"')
    lines.append(f'    if group_name in bpy.data.node_groups:')
    lines.append(f'        return bpy.data.node_groups[group_name]')
    lines.append(f'    group = bpy.data.node_groups.new(group_name, "{tree_type}")')

    if data['inputs']:
        lines.append("")
        for inp in data['inputs']:
            dv = inp.get('default_value')
            if dv is not None:
                lines.append(
                    f'    group.interface.new_socket('
                    f'name="{inp["name"]}", in_out="INPUT", socket_type="{inp["socket_type"]}"'
                    f').default_value = {_py_repr(dv)}'
                )
            else:
                lines.append(
                    f'    group.interface.new_socket('
                    f'name="{inp["name"]}", in_out="INPUT", socket_type="{inp["socket_type"]}"'
                    f')'
                )

    if data['outputs']:
        for out in data['outputs']:
            lines.append(
                f'    group.interface.new_socket('
                f'name="{out["name"]}", in_out="OUTPUT", socket_type="{out["socket_type"]}"'
                f')'
            )

    lines.append("")
    lines.append("    nodes = group.nodes")
    lines.append("    links = group.links")
    lines.append("    input_node = nodes.new('NodeGroupInput')")
    lines.append("    output_node = nodes.new('NodeGroupOutput')")

    frame_map = {}
    if data['frames']:
        lines.append("")
        lines.append("    # === 注释框 ===")
        for frame in data['frames']:
            fvar = frame['var_name']
            frame_map[frame['name']] = fvar
            flabel = frame['label'] or frame['name']
            color = frame.get('color')
            if color and frame.get('use_custom_color'):
                lines.append(
                    f'    {fvar} = create_frame(nodes, "{frame["name"]}", '
                    f'"{flabel}", ({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}))'
                )
            else:
                lines.append(
                    f'    {fvar} = create_frame(nodes, "{frame["name"]}", "{flabel}")'
                )

    input_node_vars = set()
    output_node_vars = set()
    for node in data['nodes']:
        if node['bl_idname'] == 'NodeGroupInput':
            input_node_vars.add(node['var_name'])
        elif node['bl_idname'] == 'NodeGroupOutput':
            output_node_vars.add(node['var_name'])

    regular_nodes = [n for n in data['nodes']
                     if n['bl_idname'] not in ('NodeGroupInput', 'NodeGroupOutput')]

    if regular_nodes:
        lines.append("")
        lines.append("    # === 节点创建 ===")
        for node in regular_nodes:
            var = node['var_name']
            ntype = node['bl_idname']
            parent_var = node.get('parent_frame')
            parent_arg = f", {parent_var}" if parent_var and parent_var in frame_map.values() else ""

            lines.append(f'    {var} = nodes.new("{ntype}")')

            loc = node.get('location')
            if loc and len(loc) >= 2:
                lines.append(f'    {var}.location = ({loc[0]:.1f}, {loc[1]:.1f})')

            if node.get('label'):
                lines.append(
                    f'    label_node({var}, "{node["label"]}"{parent_arg})'
                )
            elif parent_var and parent_var in frame_map.values():
                lines.append(f'    label_node({var}, ""{parent_arg})')

            for prop_name, prop_val in node.get('properties', {}).items():
                if prop_name.endswith('_image_name'):
                    continue
                # ColorRamp 色标需要特殊处理
                if prop_name == 'color_ramp' and isinstance(prop_val, dict):
                    cr = prop_val
                    lines.append(f'    {var}.color_ramp.interpolation = "{cr["interpolation"]}"')
                    if cr.get('elements'):
                        lines.append(f'    stops = {var}.color_ramp.elements')
                        # 清除默认色标只保留第一个
                        lines.append(f'    while len(stops) > 1:')
                        lines.append(f'        stops.remove(stops[0])')
                        # 设置第一个色标
                        el0 = cr['elements'][0]
                        pos0 = f"{el0['position']:.6f}".rstrip('0').rstrip('.')
                        col0 = el0['color']
                        lines.append(f'    stops[0].position = {pos0}')
                        lines.append(f'    stops[0].color = ({col0[0]:.4f}, {col0[1]:.4f}, {col0[2]:.4f}, {col0[3]:.4f})')
                        # 添加剩余色标
                        for el in cr['elements'][1:]:
                            pos = f"{el['position']:.6f}".rstrip('0').rstrip('.')
                            col = el['color']
                            lines.append(f'    stop = stops.new({pos})')
                            lines.append(f'    stop.color = ({col[0]:.4f}, {col[1]:.4f}, {col[2]:.4f}, {col[3]:.4f})')
                    continue
                lines.append(f'    {var}.{prop_name} = {_py_repr(prop_val)}')

            if node.get('sub_group_name'):
                sub_func = _get_func_name(node['sub_group_name'])
                lines.append(f'    {var}.node_tree = {sub_func}()')

            for idx, val in node.get('input_defaults', {}).items():
                lines.append(f'    {var}.inputs[{idx}].default_value = {_py_repr(val)}')

    if data['links']:
        lines.append("")
        lines.append("    # === 节点连接 ===")
        for link in data['links']:
            from_var = link['from_node']
            to_var = link['to_node']
            from_idx = link['from_socket_idx']
            to_idx = link['to_socket_idx']

            if from_var in input_node_vars:
                from_var = 'input_node'
            if to_var in output_node_vars:
                to_var = 'output_node'

            from_ref = f'{from_var}.outputs[{from_idx}]'
            to_ref = f'{to_var}.inputs[{to_idx}]'
            lines.append(f'    links.new({from_ref}, {to_ref})')

    lines.append("")
    lines.append("    return group")

    return "\n".join(lines)


def generate_init_code(group_data_list):
    """生成整个插件的 __init__.py 代码"""
    lines = []
    lines.append("bl_info = {")
    lines.append(f'    "name": "节点转代码生成",')
    lines.append(f'    "description": "自动生成的节点组插件",')
    lines.append(f'    "author": "节点转代码",')
    lines.append(f'    "version": (1, 0, 0),')
    lines.append(f'    "blender": (5, 1, 0),')
    lines.append(f'    "location": "Node Editor > Sidebar",')
    lines.append(f'    "category": "Node",')
    lines.append("}")
    lines.append("")
    lines.append("import bpy")

    func_names = []
    for data in group_data_list:
        fn = _get_func_name(data['name'])
        module_name = _sanitize_module_name(data['name'])
        func_names.append((fn, module_name))

    lines.append("")

    for fn, mod in func_names:
        lines.append(f"from .nodes.{mod} import {fn}")

    lines.append("")
    lines.append("")

    for fn, mod in func_names:
        lines.append(f"class NODE_OT_add_{fn}(bpy.types.Operator):")
        lines.append(f'    bl_idname = "node.add_{fn}"')
        lines.append(f'    bl_label = "添加 {fn}"')
        lines.append("")
        lines.append(f"    def execute(self, context):")
        lines.append(f"        mat = context.object.active_material")
        lines.append(f"        mat.use_nodes = True")
        lines.append(f"        node = mat.node_tree.nodes.new('ShaderNodeGroup')")
        lines.append(f"        node.node_tree = {fn}()")
        lines.append(f"        node.location = context.space_data.cursor_location")
        lines.append(f"        return {{'FINISHED'}}")
        lines.append("")
        lines.append("")

    lines.append("classes = [")
    for fn, mod in func_names:
        lines.append(f"    NODE_OT_add_{fn},")
    lines.append("]")
    lines.append("")
    lines.append("")
    lines.append("def register():")
    lines.append("    for cls in classes:")
    lines.append("        bpy.utils.register_class(cls)")
    lines.append("")
    lines.append("")
    lines.append("def unregister():")
    lines.append("    for cls in reversed(classes):")
    lines.append("        bpy.utils.unregister_class(cls)")
    lines.append("")
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    register()")

    return "\n".join(lines)


def _sanitize_module_name(name):
    """将节点组名转为合法的Python模块名"""
    result = []
    for c in name:
        if c.isalnum() or c == '_':
            result.append(c.lower())
        else:
            result.append('_')
    name = ''.join(result)
    while '__' in name:
        name = name.replace('__', '_')
    name = name.strip('_')
    if not name or not name[0].isalpha():
        name = 'node_' + name
    return name or 'node_group'


def save_group_code(data, output_dir):
    """保存单个节点组的代码文件"""
    os.makedirs(output_dir, exist_ok=True)
    nodes_dir = os.path.join(output_dir, "nodes")
    os.makedirs(nodes_dir, exist_ok=True)

    module_name = _sanitize_module_name(data['name'])
    code = generate_group_code(data)

    filepath = os.path.join(nodes_dir, f"{module_name}.py")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

    return filepath


def save_all_groups(group_data_list, output_dir):
    """保存所有节点组为完整的Blender插件项目"""
    os.makedirs(output_dir, exist_ok=True)

    nodes_dir = os.path.join(output_dir, "nodes")
    os.makedirs(nodes_dir, exist_ok=True)

    saved_files = []

    init_imports = []
    for data in group_data_list:
        module_name = _sanitize_module_name(data['name'])
        filepath = save_group_code(data, output_dir)
        saved_files.append(filepath)
        init_imports.append((module_name, _get_func_name(data['name'])))

    nodes_init_lines = []
    for mod_name, func_name in init_imports:
        nodes_init_lines.append(f"from .{mod_name} import {func_name}")
    nodes_init_path = os.path.join(nodes_dir, "__init__.py")
    with open(nodes_init_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(nodes_init_lines))
    saved_files.append(nodes_init_path)

    init_code = generate_init_code(group_data_list)
    init_path = os.path.join(output_dir, "__init__.py")
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(init_code)
    saved_files.append(init_path)

    return saved_files
