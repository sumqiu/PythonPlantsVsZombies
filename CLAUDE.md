# CLAUDE.md — Claude 项目上下文指南

本文件帮助 Claude 快速建立对本项目的完整认知，减少探索成本，提高代码修改的准确性。

---

## 项目身份

**Python Plants vs. Zombies** — 用 Python 3.11 + Pygame 2.x 实现的植物大战僵尸 2D 游戏克隆，约 3000 行代码，模块化程度较高。

---

## 立即可用的关键事实

```
启动方式:    python main.py  （或 uv run python main.py）
包管理:      uv（pyproject.toml）
主依赖:      pygame >= 2.6.1，pydub >= 0.25.1
Python版本:  >= 3.11
测试:        pytest tests/
```

---

## 架构概览（优先阅读这部分）

### 两层状态机

**第一层：全局场景切换**（`tool.Control`）
```
MAIN_MENU ──► LEVEL_SELECT ──► LEVEL ──► GAME_VICTORY ──► MAIN_MENU
                                    └──► GAME_LOSE    ──► MAIN_MENU
```

**第二层：关卡内状态**（`Level.state`）
```
CHOOSE（选卡）──► PLAY（游戏中）──► PAUSE（暂停）
                    ▲___________________________│（恢复）
```

### 模块职责速查

| 模块 | 职责 | 关键类 |
|------|------|--------|
| `source/tool.py` | 游戏生命周期、资源管理 | `Control`, `State`, `MusicManager` |
| `source/constants.py` | **唯一**的常量源头 | 所有字符串 ID |
| `source/state/level/level.py` | 关卡主类，组合子系统 | `Level` |
| `source/state/level/entity_manager.py` | 精灵组、僵尸波次 | `EntityManager` |
| `source/state/level/collision_handler.py` | 碰撞逻辑 | `CollisionHandler` |
| `source/component/base.py` | 动画精灵基类 | `AnimatedSprite` |
| `source/component/map.py` | 5×9 网格坐标系 | `Map` |
| `source/component/plants/base.py` | 植物基类 | `Plant`, `Bullet`, `Sun`, `Car` |
| `source/component/zombies/base.py` | 僵尸基类 | `Zombie` |
| `source/component/menubar/constants.py` | 卡牌-植物映射表 | `CARD_CONFIG` |

---

## 实体目录

### 植物（`source/component/plants/`）

| 文件 | 包含的植物类 |
|------|------------|
| `shooters.py` | PeaShooter, RepeaterPea, ThreePeaShooter, SnowPeaShooter |
| `mushrooms.py` | PuffShroom, ScaredyShroom, SunShroom, IceShroom, HypnoShroom |
| `defensive.py` | WallNut, Spikeweed |
| `explosive.py` | CherryBomb, PotatoMine, Jalapeno |
| `special.py` | SunFlower, Chomper, Squash |
| `bowling.py` | WallNutBowling, RedWallNutBowling |

### 僵尸（`source/component/zombies/`）

| 文件 | 包含的僵尸类 |
|------|------------|
| `normal.py` | NormalZombie, FlagZombie |
| `armored.py` | ConeHeadZombie, BucketHeadZombie |
| `special.py` | NewspaperZombie, ZombieHead |
| `playable.py` | PlayableNormalZombie, PlayableConeHeadZombie, PlayableBucketHeadZombie |

---

## 代码规范（Claude 必须遵守）

### 1. 常量不内联
任何字符串 ID（植物名、僵尸名、状态名）**必须**来自 `source/constants.py`：
```python
# 正确
import source.constants as c
plant_name = c.PEASHOOTER

# 错误
plant_name = "Peashooter"
```

### 2. 资源访问时机
`tool.GFX`、`tool.ZOMBIE_RECT`、`tool.PLANT_RECT`、`tool.MUSIC` 在 `tool.init()` 后才可用。**不要在类定义或模块顶层直接访问**：
```python
# 正确（在方法内）
def setup(self):
    self.image = tool.GFX[c.PEASHOOTER]

# 错误（模块顶层）
IMAGE = tool.GFX[c.PEASHOOTER]  # init() 未调用时会崩溃
```

### 3. 继承链
- 所有植物 → 继承 `Plant`（`component/plants/base.py`）
- 所有子弹 → 继承 `Bullet`（`component/plants/base.py`）
- 所有僵尸 → 继承 `Zombie`（`component/zombies/base.py`）
- 所有场景 → 继承 `tool.State`
- 动画精灵 → 继承 `AnimatedSprite`（`component/base.py`）

### 4. 网格坐标
地图为 **5 行（map_y: 0-4）× 9 列（map_x: 0-8）**，坐标转换通过 `component/map.py` 的 `Map` 类处理，不要手动计算像素位置。

---

## 常见任务的修改清单

### 添加新植物
- [ ] `source/data/entity/plant.json` — 精灵裁剪坐标
- [ ] `source/constants.py` — 添加 `PLANT_NAME = "PlantName"` 和 `CARD_PLANT_NAME = "card_plant_name"`
- [ ] `source/component/plants/<分类>.py` — 实现植物类
- [ ] `source/component/plants/__init__.py` — `from .分类 import PlantClass`
- [ ] `source/component/menubar/constants.py` — `CARD_CONFIG` 新增条目

### 添加新僵尸
- [ ] `source/data/entity/zombie.json` — 精灵裁剪坐标
- [ ] `source/constants.py` — 添加 `ZOMBIE_NAME = "ZombieName"`
- [ ] `source/component/zombies/<分类>.py` — 实现僵尸类
- [ ] `source/component/zombies/__init__.py` — 导出新类
- [ ] `source/state/level/entity_manager.py` — `createZombie` 方法中注册名称

### 添加新关卡
- [ ] `source/data/map/level_N.json` — 关卡配置 JSON
- [ ] `source/state/levelselect.py` — 新增关卡按钮

### 修改碰撞逻辑
- 入口：`source/state/level/collision_handler.py`
- 子弹打僵尸：`handleBulletZombieCollision`
- 僵尸吃植物：`handleZombiePlantCollision`

### 修改游戏胜负条件
- 入口：`source/state/level/game_state_checker.py`

---

## 关卡 JSON 完整格式参考

```json
{
    "background_type": 0,
    "init_sun_value": 500,
    "card_pool": [0, 1, 2, 3, 4],
    "zombie_list": [
        {"time": 5000,  "map_y": 2, "name": "Zombie"},
        {"time": 15000, "map_y": 0, "name": "ConeheadZombie"},
        {"time": 30000, "map_y": 4, "name": "BucketheadZombie"},
        {"time": 45000, "map_y": 1, "name": "FlagZombie"},
        {"time": 60000, "map_y": 3, "name": "NewspaperZombie"}
    ]
}
```

可用僵尸名：`"Zombie"` `"ConeheadZombie"` `"BucketheadZombie"` `"FlagZombie"` `"NewspaperZombie"`

---

## 调试提示

**游戏启动失败时**：
- 检查 pygame 是否安装：`python -c "import pygame"`
- 检查 `resources/` 目录是否完整（精灵图、音乐文件）

**精灵不显示时**：
- 核对 `source/data/entity/plant.json` 中的 `x/y/width/height` 是否与实际精灵表匹配
- 确认 `tool.init()` 已被调用

**音乐不播放时**：
- 确认 `resources/music/` 下有对应 `.ogg` 文件
- 若有 `.m4a` 文件，需要系统安装 ffmpeg 才能自动转换

**测试中 import 失败时**：
- 在测试文件顶部 mock `pygame.init()` 和 `tool.init()`，避免触发显示初始化

---

## 不要做的事

- **不要**创建 `requirements.txt`（项目使用 uv，用 `pyproject.toml`）
- **不要**在 `constants.py` 之外硬编码实体名称字符串
- **不要**在模块顶层访问 `tool.GFX` 等资源全局变量
- **不要**手动计算网格像素坐标（用 `Map` 类）
- **不要**修改 `source/state/level_old.py.bak`（这是历史备份文件）
