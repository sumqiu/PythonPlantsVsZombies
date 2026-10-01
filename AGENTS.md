# AGENTS.md — AI 编码助手快速参考

本文件供 Cursor、Copilot、Aider 等 AI 编码工具快速理解本项目的架构与约定，避免产生错误假设。

---

## 项目一句话概述

Python + Pygame 实现的植物大战僵尸 2D 游戏，7 个 JSON 驱动的关卡，17 种植物，8 种僵尸，完整游戏循环。

---

## 技术栈与运行环境

- **Python**: >= 3.11（`.python-version` 文件指定）
- **包管理**: uv（`pyproject.toml` + `uv.lock`），无 `requirements.txt`
- **核心依赖**: `pygame >= 2.6.1`、`pydub >= 0.25.1`
- **系统依赖**: ffmpeg（音频转换，可选）
- **启动命令**: `python main.py` 或 `uv run python main.py`
- **测试**: `tests/` 目录，使用标准 pytest

---

## 项目架构图

```
main.py (根入口)
└── source/main.py
    ├── source/tool.py          ← 基础设施层（Control/State/资源加载/音乐）
    ├── source/constants.py     ← 全局常量（所有字符串 ID 集中于此）
    └── source/state/           ← 场景/状态层
        ├── mainmenu.py
        ├── levelselect.py
        ├── screen.py
        └── level/              ← 关卡（拆分为 8 个子模块）
            ├── level.py            主类，组合子系统
            ├── map_loader.py       加载 JSON 关卡配置
            ├── entity_manager.py   精灵组 & 僵尸波次生成
            ├── input_handler.py    鼠标 / 键盘输入
            ├── plant_manager.py    植物放置 / 铲除
            ├── collision_handler.py 碰撞检测
            ├── game_state_checker.py 胜负判定
            └── renderer.py         渲染

source/component/              ← 实体 & UI 组件层
    ├── base.py                AnimatedSprite 基类
    ├── map.py                 网格坐标系
    ├── pause_menu.py          暂停菜单
    ├── plants/                所有植物类（按功能分文件）
    ├── zombies/               所有僵尸类（按功能分文件）
    └── menubar/               菜单栏、卡牌面板等 UI

source/data/                   ← 纯数据层（JSON，无逻辑）
    ├── entity/plant.json      植物精灵裁剪坐标
    ├── entity/zombie.json     僵尸精灵裁剪坐标
    └── map/level_N.json       关卡配置（N = 0-6）
```

---

## 全局状态机

`tool.Control` 维护全局状态字典，通过 `State.done` + `State.next` 切换：

```
MAIN_MENU → LEVEL_SELECT → LEVEL → GAME_VICTORY / GAME_LOSE → MAIN_MENU
```

关卡内子状态（`Level.state`）：
- `CHOOSE` — 选卡阶段（Panel UI）
- `PLAY` — 游戏进行中（MenuBar / MoveBar）
- `PAUSE` — 暂停（PauseMenu 覆盖层）

---

## 关键约定

### 常量管理
**所有字符串 ID 必须在 `source/constants.py` 中定义**，其他文件通过 `import source.constants as c` 引用，绝不硬编码字符串。

### 资源延迟加载
`tool.GFX`、`tool.ZOMBIE_RECT`、`tool.PLANT_RECT`、`tool.MUSIC` 在 `tool.init()` 调用后才有效，**不要在模块顶层使用这些全局变量**（会导致测试无法 import）。

### 新增植物流程（必须完整执行以下 5 步）
1. `source/data/entity/plant.json` — 添加精灵裁剪坐标
2. `source/component/plants/<分类>.py` — 创建类，继承 `Plant`（来自 `plants/base.py`）
3. `source/component/plants/__init__.py` — 导出新类
4. `source/constants.py` — 添加植物名字符串常量 & 对应卡牌名常量
5. `source/component/menubar/constants.py` — 在 `CARD_CONFIG` 末尾追加卡牌配置

### 新增僵尸流程（必须完整执行以下 4 步）
1. `source/data/entity/zombie.json` — 添加精灵裁剪坐标
2. `source/component/zombies/<分类>.py` — 创建类，继承 `Zombie`（来自 `zombies/base.py`）
3. `source/component/zombies/__init__.py` — 导出新类
4. `source/state/level/entity_manager.py` — 在 `createZombie` 中注册名称映射

### 新增关卡流程
1. 创建 `source/data/map/level_N.json`（参考现有关卡 JSON 格式）
2. `source/state/levelselect.py` — 添加关卡按钮

---

## 数据格式

### 关卡 JSON（`source/data/map/level_N.json`）
```json
{
    "background_type": 0,
    "init_sun_value": 500,
    "card_pool": [0, 1, 2, 3],
    "zombie_list": [
        {"time": 5000, "map_y": 2, "name": "Zombie"}
    ]
}
```
- `background_type`: 0=白天，1=夜晚
- `card_pool`: 卡牌索引（见 `menubar/constants.py` 中的 `CARD_CONFIG`）
- `zombie_list[].time`: 距关卡开始的毫秒数
- `zombie_list[].map_y`: 行号（0-4，共 5 行）
- `zombie_list[].name`: 对应 `entity_manager.createZombie` 中的映射键

### 植物精灵 JSON（`source/data/entity/plant.json`）
```json
{"plant_name": {"x": 0, "y": 0, "width": 80, "height": 80}}
```

### 僵尸精灵 JSON（`source/data/entity/zombie.json`）
```json
{"zombie_name": {"walk": {"x": 0, "width": 64}, "attack": {...}}}
```

---

## 网格坐标系

- 地图：5 行 × 9 列（`map_y` 0-4，`map_x` 0-8）
- 网格单元尺寸：由 `constants.py` 中的 `GRID_X_SIZE` / `GRID_Y_SIZE` 定义
- 坐标转换：使用 `component/map.py` 中的 `Map` 类

---

## 精灵组织结构（`entity_manager`）

| 精灵组 | 说明 |
|--------|------|
| `zombie_groups[y]` | 每行的敌方僵尸列表 |
| `plant_groups[y]` | 每行的植物精灵组 |
| `bullet_groups[y]` | 每行的子弹精灵组 |
| `hypno_zombie_groups[y]` | 被魅惑的僵尸（攻击普通僵尸） |
| `sun_groups` | 阳光精灵组 |
| `car_groups[y]` | 每行的小车 |

---

## 音乐系统

- 音频文件放在 `resources/music/`，格式为 `.ogg`（pygame 原生支持）
- `m4a` 文件通过 `MusicManager`（tool.py）调用 `pydub` + `ffmpeg` 自动转换为 `.ogg`
- 常量在 `constants.py` 中以 `MUSIC_*` 前缀定义

---

## 常见陷阱

| 问题 | 说明 |
|------|------|
| import 时 pygame 报错 | `tool.GFX` 等需要 `tool.init()` 后才能访问，测试时注意 mock |
| 添加植物后不显示卡牌 | 检查是否在 `CARD_CONFIG` 和 `constants.py` 中都添加了 |
| 新僵尸不出现 | 检查 `entity_manager.createZombie` 的名称映射 |
| 背景不对 | `level_N.json` 中 `background_type` 仅支持 0 和 1 |
| 精灵图显示错误 | 检查 `plant.json`/`zombie.json` 中的裁剪坐标是否正确 |

---

## 文件修改高频区域

当 AI 助手需要添加功能时，最常修改的文件：

1. `source/constants.py` — 几乎每次添加实体都要改
2. `source/component/menubar/constants.py` — 卡牌配置
3. `source/component/plants/` 或 `source/component/zombies/` — 实体逻辑
4. `source/state/level/entity_manager.py` — 僵尸注册
5. `source/data/map/level_N.json` — 关卡设计
