# xl_c4d_tool

面向 Blender 5.1 的中文 C4D 风格工作流工具集。

> Cinema 4D / C4D 是其权利人的商标。本项目是独立 Blender 工具，与 Maxon、Blender Foundation 或文中第三方项目没有官方隶属、赞助或背书关系。

## 功能入口

- `3D 视图 > N > c4d小工具 > 修改器库`：选择网格对象，搜索并添加项目几何节点修改器。
- `3D 视图 > N > c4d小工具 > C4D工具`：场景整理、样条提取、物体/原点对齐等辅助工具。
- `3D 视图 > N > c4d小工具 > C4D工具 > 四边重拓扑`：打开四边重拓扑设置并确认执行。
- `几何节点编辑器 > N > c4d小工具`：按 C4D 风格分类、搜索并放置项目节点组。
- `着色器节点编辑器 > N > c4d小工具`：材质节点助手与 Node Preview 节点缩略图。
- `编辑 > 偏好设置 > 插件 > xl_c4d_tool`：节点浏览器、面板布局、列数和节点预览设置。

## 当前版本特性 (3.4.0)

### 修改器库（115 项分类）

| 分类 | 数量 | 内容 |
|---|---:|---|
| 生成器 | 28 | 参数体、样条、挤压、扫描、放样、旋转、运动文本、融球等 |
| 建模工具 | 16 | 布尔、连接、破碎、精确破碎、细分、加厚、LOD、四边重网格等 |
| 克隆器 | 11 | 对象、放射、沿样条、线性、网格、蜂窝、实例与矩阵工具 |
| 效果器 | 15 | 普通、随机、步进、推开、时间、声音、目标、图像、样条等 |
| 域 | 16 | 基础、随机、图像、声音、对象邻近、时间、步进及域修改层 |
| 散布 | 6 | 顶点、边、面、体积、随机与完整系统 |
| 变形器 | 11 | 弯曲、扭曲、收缩包裹、样条约束、置换、浮雕、融化等 |
| 动画 | 4 | 加速度、运动动画、运动实例、追踪 |
| MoGraph | 3 | 克隆增强器、衰减效果器、加权实例化 |
| 其他 | 5 | 多边形 FX、挤出套娃、摄像机工具、样条蒙版、矩阵 |

### XL_置换 2.0（重制亮点）

旧置换默认高度场为 0.5 时产生零位移，用户添加后看不到效果。3.4.0 重建为完整图像驱动链路：

- 图像输入，命名 UV 与位置坐标回退
- 平铺、偏移、灰度或 Alpha 通道
- 底部/顶部级别、中心、高度、反转
- 点选择、0–6 级安全细分
- 表面法线或固定方向位移
- 可选平滑着色
- 未指定图像时保持原几何

节点组：18 个接口（含几何输出）、32 个节点、45 条连线、7 段中文语义注释框。

### 集成工具

- **Node Preview v1.21**（Simon Wendsche / B.Y.O.B.，GPL-3.0）：着色器节点编辑器缩略图
- **Node Arrange**：节点自动排列与批处理
- **QRemeshify / QuadWild / QuadPatches**：四边重拓扑入口
- **Sugiyama 自动排列**：基于 NetworkX 3.4.2 的节点排列算法
- **材质助手**：含 C4D 云层、OC 风格等材质节点
- **节点转 Python 代码**：支持预览、当前节点组、当前文件和外部 .blend 批量转换

### 场景辅助

- 布尔操作源自动线框/名称/隐藏渲染联动
- 四边重拓扑质量预设
- 智能挤出、样条提取、物体对齐
- 场景整理、分组/解组/设父级/建集合

## 安装

1. 使用 Blender 5.1。
2. 将发布 ZIP 作为整体安装：`编辑 > 偏好设置 > 扩展/插件 > 从磁盘安装`，不要把 ZIP 内文件单独拆散。
3. 启用 `xl_c4d_tool`。
4. 在 3D 视图或节点编辑器按 `N`，确认出现 `c4d小工具` 标签页。

升级前请备份正在制作的 `.blend` 文件。若由旧版本升级，先关闭 Blender，再覆盖或重新安装；不要同时保留多个同名插件目录。

## 设计参考与第三方组件

本项目借鉴、集成或研究了如下项目。详细来源与许可见 `xl_c4d_tool/THIRD_PARTY_LICENSES.md`。

### 直接集成

| 项目 | 作者 | 许可 | 用途 |
|---|---|---|---|
| Node Preview v1.21 | Simon Wendsche (B.Y.O.B.) | GPL-3.0 | 节点缩略图预览 |
| Node Arrange v1.12.1 | Leonardo Pike-Excell | GPL-2.0 / 3.0 | 节点自动排列 |
| NetworkX 3.4.2 | NetworkX Developers | BSD-3-Clause | Sugiyama 算法依赖 |
| QRemeshify 1.1.0 | ksami (QuadWild/QuadPatches) | GPL-3.0 | 四边重拓扑 |
| B4D Tools 1.5.0 | Manellopgar | GPL-2.0 | 克隆器/效果器/域基础语义 |
| Cashew Nodes | Con11 | GPL-3.0 | 破碎/置换/浮雕研究基础 |
| CGMatter Nodes 6.0.0 | CGMatter | GPL-2.0 / 3.0 | 精确破碎等依赖 |
| Physical Starlight 1.8.3 | Physical Addons | GPL-3.0 | 物理天空节点组（UI入口已移除） |
| SuperLoft | — | — | 放样核心依赖 |

### 研究后独立实现

| 参考项目 | 研究范围 | XL 实现方式 |
|---|---|---|
| Advanced Array Tool 2.6.1 | 克隆随机变换/权重 | 原生节点独立实现 |
| Geo-Scatter 5.6.3 | 分布/遮罩/LOD/代理 | 原生节点独立实现 |
| Conform Object 1.6 | 投射/偏移语义 | 独立 GN 路线 |
| Cinema 4D / Maxon | 产品行为/参数语义 | 作为行为规格，不复制源码或商标 |

### 功能说明与免责

本仓库为完整开发版。`material_nodes/`（含 PF Hardshell 等商业购买材质节点）、`物理天空/`（Physical Starlight and Atmosphere 资产）、`icons/`、`logs/` 等模块包含在研究或借鉴过程中使用的第三方资产。**若任何原项目的作者认为本仓库的对应功能存在不当使用，请提交 Issue 告知，我们将在核实后立即下架对应功能模块**。

## 仓库结构

```
xl_c4d_tool/          插件主模块
├── assets/           几何节点资产（C4D生成器复刻.blend）
├── geo_nodes/        几何节点分类/搜索/面板
├── handlers/         Blender 事件处理器
├── material_nodes/   材质节点（第三方参考）
├── node_arrange/     节点自动排列
├── node_preview/     节点缩略图预览
├── node_to_code/     节点转 Python 代码
├── operators/        操作器（修改器库/场景工具等）
├── panels/           面板注册
├── properties/       属性组
├── utils/            工具函数
├── 物理天空/           Physical Starlight 资产
├── 重拓扑/             四边重拓扑模块
├── 集合实例转材质/       集合实例材质转换
├── icons/            功能图标
├── logs/             日志
├── __init__.py       插件入口
├── preferences.py    偏好设置
├── README.md         插件说明
├── CHANGELOG.md      版本记录
├── DEVELOPMENT_LOG.md 开发日志
└── THIRD_PARTY_LICENSES.md 第三方许可
```

## 许可证

本仓库按 [GNU GPL v3](LICENSE) 发布。随附第三方组件仍保留各自版权声明和许可证。贡献代码必须与 GPL-3.0 兼容。

## 支持作者

如果这个工具帮到你，欢迎请作者喝杯奶茶。所有支持均为自愿，不影响插件功能、更新或开源许可。

<img src="docs/assets/wechat-donation.jpg" alt="微信赞赏码" width="360">

## 文档

- [版本记录](xl_c4d_tool/CHANGELOG.md)
- [开发与资产审计](xl_c4d_tool/DEVELOPMENT_LOG.md)
- [第三方许可与公开边界](xl_c4d_tool/THIRD_PARTY_LICENSES.md)
- [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md)
