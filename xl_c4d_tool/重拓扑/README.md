# XL 四边重拓扑

这是 `C4D生成器复刻.blend` 的一次性四边面重拓扑工具，不是实时几何节点修改器。

- 核心算法：QRemeshify 1.1.0、QuadWild、QuadPatches。
- 界面：中文 B4D 风格分区，包含预处理、平滑、锐边、X/Y/Z 对称、尺寸、缓存和输出命名。
- 安全：始终创建新对象，不删除原始网格；可选择成功后隐藏原物体。
- 默认求解时限：60 秒；调试时建议从低模开始。

安装时将整个 `XL_重拓扑工具` 文件夹打包为 zip，通过 Blender 扩展安装器载入。面板位置：`3D视图 > 侧栏 > C4D工具`。

## 第三方来源

Vendor 目录来自 [QRemeshify 1.1.0](https://github.com/ksami/QRemeshify)，作者 ksami，GPL-3.0-or-later。其 DLL 封装 QuadWild/QuadPatches；本项目保留相同 GPL 许可，并重写了中文操作器与界面层。
