"""僵尸卡牌配置自检。

运行：uv run python tests/test_zombie_cards.py
"""

import sys
from pathlib import Path

# 允许从仓库根目录直接跑本文件（否则 source 包不在 sys.path 上）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from source import constants as c
from source.component.menubar import constants as menu_c

# (card index, 卡面图, 实体名, 阳光价, 冷却 ms)
EXPECTED = [
    (menu_c.ZOMBIE_CARD_BUCKETHEAD, c.CARD_BUCKETHEAD_ZOMBIE, c.BUCKETHEAD_ZOMBIE, 150, 20000),
    (menu_c.ZOMBIE_CARD_CONEHEAD,   c.CARD_CONEHEAD_ZOMBIE,   c.CONEHEAD_ZOMBIE,    75, 15000),
    (menu_c.ZOMBIE_CARD_NORMAL,     c.CARD_NORMAL_ZOMBIE,     c.NORMAL_ZOMBIE,      50, 10000),
]

CARDS_DIR = Path(__file__).resolve().parent.parent / 'resources' / 'graphics' / 'Cards'


def test_card_config():
    for idx, card, entity, sun, cd in EXPECTED:
        cfg = menu_c.CARD_CONFIG[idx]
        assert cfg['card'] == card, f'卡面图错配 @{idx}: {cfg["card"]} != {card}'
        assert cfg['plant'] == entity, f'实体名错配 @{idx}: {cfg["plant"]} != {entity}'
        assert cfg['sun'] == sun, f'阳光价错配 @{idx}: {cfg["sun"]} != {sun}'
        assert cfg['cd'] == cd, f'冷却错配 @{idx}: {cfg["cd"]} != {cd}'
        print(f'  [{idx}] {entity:<16} {sun:>4} sun  {cd // 1000:>3}s  card={card}')


def test_card_index_range():
    """僵尸卡索引必须落在 all_card_list 选卡范围内，否则玩家在面板上够不到。"""
    for idx, *_ in EXPECTED:
        assert 0 <= idx < len(menu_c.CARD_CONFIG), f'索引 {idx} 越界'
        assert idx in menu_c.all_card_list, f'索引 {idx} 不在 all_card_list 里'


def test_card_images_exist():
    """卡面图必须是真实存在的资源：tool.GFX 要 display 才能查，这里直接查磁盘。"""
    for _, card, *_ in EXPECTED:
        path = CARDS_DIR / f'{card}.png'
        assert path.is_file(), f'缺少卡面图: {path}'
        print(f'  {path.name}  {path.stat().st_size} bytes')


def test_playable_zombies_reachable():
    """三种可放置僵尸都要在 plant_manager 的工厂表里有对应实现。"""
    import inspect
    import source.constants as cmod
    from source.state.level import plant_manager
    src = inspect.getsource(plant_manager.PlantManager._createPlayableZombie)
    for _, _, entity, _, _ in EXPECTED:
        attr = next(n for n, v in vars(cmod).items()
                    if v == entity and n.endswith('_ZOMBIE'))
        assert f'c.{attr}' in src, f'_createPlayableZombie 未处理 {entity}'
        print(f'  {entity:<16} -> c.{attr}')


if __name__ == '__main__':
    for fn in (test_card_config, test_card_index_range,
               test_card_images_exist, test_playable_zombies_reachable):
        print(f'\n{fn.__name__}')
        fn()
    print('\n僵尸卡牌配置自检通过。')
