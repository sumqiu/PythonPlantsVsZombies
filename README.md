# Python Plants vs. Zombies

一个使用 Python + Pygame 实现的植物大战僵尸（Plants vs. Zombies）2D 游戏克隆项目，具备完整的游戏循环、多关卡、多种植物与僵尸类型。

---

## 截图 / 演示

> 运行 `python main.py` 即可启动游戏。

---

## 功能特性

- **7 个关卡**（level_0 ～ level_6），由 JSON 文件驱动，便于自定义扩展
- **17 种可种植植物**（射手、防御、爆炸、蘑菇、特殊等类型）
- **5 种敌方僵尸**（普通、路障头、铁桶头、旗帜、报纸）
- **3 种可操控僵尸**（玩家可放置的僵尸卡牌：普通、路障头、铁桶头）
- 阳光生产与消耗系统、卡牌冷却
- 小车防线（最后一道防御）
- 魅惑蘑菇（HypnoShroom）效果：僵尸反水攻打同伴
- 冰冻（SnowPea / IceShroom）减速与全行冻结
- 暂停菜单（继续 / 重开 / 退出）
- 背景音乐系统（支持 m4a → ogg 自动转换）
- 夜晚关卡背景（background_type=1）

---

## 目录结构

```
PythonPlantsVsZombies/
├── main.py                    # 程序入口
├── pyproject.toml             # 项目依赖（uv/PEP 621）
├── uv.lock
├── resources/
│   ├── graphics/              # 精灵图、卡牌图、界面图
│   └── music/                 # 背景音乐（.ogg）
├── source/
│   ├── main.py                # 初始化 & 状态注册
│   ├── constants.py           # 全局常量（状态名、实体 ID、网格参数等）
│   ├── tool.py                # 基础设施（Control、State、资源加载、音乐管理）
│   ├── state/
│   │   ├── mainmenu.py        # 主菜单状态
│   │   ├── levelselect.py     # 关卡选择状态
│   │   ├── screen.py          # 胜利 / 失败画面
│   │   └── level/             # 关卡状态（拆分为多个子模块）
│   │       ├── level.py           # Level 主类，组合各子系统
│   │       ├── map_loader.py      # 读取关卡 JSON、初始化地图
│   │       ├── entity_manager.py  # 精灵组管理、僵尸生成
│   │       ├── input_handler.py   # 鼠标 / 键盘输入
│   │       ├── plant_manager.py   # 植物放置 / 铲除
│   │       ├── collision_handler.py # 子弹-僵尸、僵尸-植物碰撞
│   │       ├── game_state_checker.py # 胜负判定
│   │       └── renderer.py        # 场景渲染
│   ├── component/
│   │   ├── base.py            # AnimatedSprite 基类
│   │   ├── map.py             # 网格地图（坐标转换、格子占用）
│   │   ├── pause_menu.py      # 暂停菜单 UI
│   │   ├── plants/            # 所有植物类
│   │   ├── zombies/           # 所有僵尸类
│   │   └── menubar/           # 菜单栏、卡牌面板、铲子等 UI
│   └── data/
│       ├── entity/
│       │   ├── plant.json     # 植物精灵裁剪坐标
│       │   └── zombie.json    # 僵尸精灵裁剪坐标
│       └── map/
│           ├── level_0.json   # 关卡 0 配置
│           ├── ...
│           └── level_6.json   # 关卡 6 配置
└── tests/
    └── test_zombie_cards.py
```

---

## 安装与运行

### 依赖

- Python >= 3.11
- pygame >= 2.6.1
- pydub >= 0.25.1（音频转换，可选）
- ffmpeg（系统级，用于 m4a → ogg 转换）

### 使用 uv（推荐）

```bash
# 安装 uv（如尚未安装）
pip install uv

# 同步依赖
uv sync

# 运行游戏
uv run python main.py
```

### 使用 pip

```bash
pip install pygame pydub
python main.py
```

---

## 关卡配置说明

关卡文件位于 `source/data/map/level_N.json`，格式示例：

```json
{
    "background_type": 0,
    "init_sun_value": 500,
    "card_pool": [{"name": "Peashooter"}, {"name": "SnowPea"}],
    "zombie_list": [
        {"time": 1000, "map_y": 2, "name": "Zombie"}
    ]
}
```

| 字段 | 说明 |
|------|------|
| `background_type` | 背景类型（0=白天，1=夜晚） |
| `init_sun_value` | 初始阳光值 |
| `choosebar_type` | 可选。0=选卡面板（缺省）、1=传送带、2=保龄球。只在 0 时需要省略 |
| `card_pool` | 卡池，元素是 `{"name": "<植物名或实体名>"}`。**仅 `choosebar_type != 0` 时生效** |
| `zombie_list` | 僵尸波次，`time` 为毫秒，`map_y` 为行（0-4） |

> `choosebar_type` 为 0（静态选卡面板）时，选卡列表固定来自
> `menubar.constants.all_card_list`，`card_pool` 不被读取。历史关卡文件里残留的
> `[0, 1, 2, ...]` 索引写法属于无效数据。

### 植物卡牌索引表

| 索引 | 植物 | 阳光消耗 | 冷却(ms) |
|------|------|----------|----------|
| 0 | 向日葵 SunFlower | 50 | 7500 |
| 1 | 豌豆射手 Peashooter | 100 | 7500 |
| 2 | 寒冰射手 SnowPeaShooter | 175 | 7500 |
| 3 | 坚果墙 WallNut | 50 | 30000 |
| 4 | 樱桃炸弹 CherryBomb | 150 | 50000 |
| 5 | 三发射手 ThreePeaShooter | 325 | 7500 |
| 6 | 双发射手 RepeaterPea | 200 | 7500 |
| 7 | 食人花 Chomper | 150 | 7500 |
| 8 | 小喷菇 PuffShroom | 0 | 7500 |
| 9 | 土豆雷 PotatoMine | 25 | 30000 |
| 10 | 倭瓜 Squash | 50 | 30000 |
| 11 | 地刺 Spikeweed | 100 | 7500 |
| 12 | 火爆辣椒 Jalapeno | 125 | 50000 |
| 13 | 胆小菇 ScaredyShroom | 25 | 7500 |
| 14 | 阳光菇 SunShroom | 25 | 7500 |
| 15 | 冰蘑菇 IceShroom | 75 | 50000 |
| 16 | 魅惑菇 HypnoShroom | 75 | 30000 |
| 19 | 铁桶僵尸（可放置）| 150 | 20000 |
| 20 | 路障僵尸（可放置）| 75 | 15000 |
| 21 | 普通僵尸（可放置）| 50 | 10000 |

---

## 游戏操作

| 操作 | 说明 |
|------|------|
| 鼠标左键 | 选择卡牌、放置植物、点击界面按钮 |
| 鼠标右键 | 取消当前选中 |
| 铲子按钮 | 移除已种植的植物 |
| ESC | 暂停 / 恢复游戏 |

---

## 开发说明

### 添加新植物

1. 在 `source/data/entity/plant.json` 中添加精灵裁剪坐标
2. 在 `source/component/plants/` 对应分类文件中创建新类（继承 `Plant`）
3. 在 `source/component/plants/__init__.py` 中导出
4. 在 `source/component/menubar/constants.py` 的 `CARD_CONFIG` 中添加卡牌配置
5. 在 `source/constants.py` 中添加对应的字符串常量

### 添加新关卡

只需在 `source/data/map/` 下创建 `level_N.json` 文件，并在 `source/state/levelselect.py` 中注册按钮即可。

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.11+ | 主语言 |
| Pygame 2.x | 窗口、渲染、事件、声音 |
| pydub | 音频格式转换 |
| JSON | 关卡数据与精灵配置 |

---

## 致谢

本项目基于原版 Plants vs. Zombies 游戏（PopCap Games / EA）进行学习目的复刻，仅供非商业使用。
