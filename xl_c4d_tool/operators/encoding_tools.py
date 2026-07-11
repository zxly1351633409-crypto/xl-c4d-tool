"""显式修复旧式 GBK/ANSI Python 文件造成的 Blender 插件列表 UTF-8 警告。"""

from __future__ import annotations

import shutil
from pathlib import Path

import bpy
from bpy.props import StringProperty


def _addon_roots():
    roots = set()
    for path in bpy.utils.script_paths():
        root = Path(path)
        for child in (root / "addons", root / "addons_core"):
            if child.is_dir():
                roots.add(child)
    # Blender 4.2+ 扩展目录也可能含非 UTF-8 文件
    for getter in ("EXTENSIONS",):
        try:
            ext = Path(bpy.utils.user_resource(getter))
            if ext.is_dir():
                roots.add(ext)
        except (TypeError, ValueError):
            pass
    return sorted(roots)


class PREFERENCES_OT_xl_repair_python_encoding(bpy.types.Operator):
    bl_idname = "preferences.xl_repair_python_encoding"
    bl_label = "修复非 UTF-8 插件编码"
    bl_description = ("扫描插件/扩展目录下的 Python 文件；把 addon_zh.py 等 GB18030/GBK 文件"
                     "先备份再转为 UTF-8。文件名留空可扫描全部 .py，定位任何编码警告来源")
    bl_options = {"REGISTER"}

    filename: StringProperty(
        name="文件名",
        description="只修复该名称的文件；留空则扫描全部 .py 找出所有非 UTF-8 文件",
        default="addon_zh.py",
    )

    def execute(self, _context):
        targets = []
        pattern = self.filename.strip() or "*.py"
        for root in _addon_roots():
            try:
                targets.extend(path for path in root.rglob(pattern) if path.is_file())
            except OSError:
                continue
        # 扫描全部 .py 时，仅保留确实非 UTF-8 的文件，避免改动正常文件
        if pattern == "*.py":
            filtered = []
            for path in targets:
                try:
                    path.read_bytes().decode("utf-8")
                except UnicodeDecodeError:
                    filtered.append(path)
                except OSError:
                    continue
            targets = filtered
        if not targets:
            hint = self.filename.strip() or "任何文件"
            self.report({"WARNING"}, f"当前电脑没有找到需要修复的 {hint}；xl_c4d_tool 自身已是 UTF-8")
            return {"CANCELLED"}

        repaired = 0
        already_utf8 = 0
        failed = []
        for path in targets:
            try:
                raw = path.read_bytes()
                try:
                    raw.decode("utf-8")
                    already_utf8 += 1
                    continue
                except UnicodeDecodeError:
                    pass
                text = None
                for encoding in ("gb18030", "gbk", "big5", "cp1252"):
                    try:
                        text = raw.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                if text is None:
                    failed.append(path.name)
                    continue
                backup = path.with_suffix(path.suffix + ".encoding_backup")
                if not backup.exists():
                    shutil.copy2(path, backup)
                path.write_text(text, encoding="utf-8", newline="\n")
                repaired += 1
            except OSError:
                failed.append(path.name)

        if failed:
            self.report({"WARNING"}, f"已修复 {repaired} 个，{len(failed)} 个无法判定编码；原文件未覆盖")
        else:
            self.report({"INFO"}, f"已修复 {repaired} 个；已有 UTF-8 文件 {already_utf8} 个，旁边保留 encoding_backup")
        return {"FINISHED"}


classes = (PREFERENCES_OT_xl_repair_python_encoding,)


def register():
    for cls in classes:
        if not cls.is_registered:
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        if cls.is_registered:
            bpy.utils.unregister_class(cls)
