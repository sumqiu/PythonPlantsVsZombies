"""关卡逻辑回归自检 —— 覆盖一批已修 bug，跑法：

    uv run python tests/test_level_regression.py

全程无头（SDL dummy 驱动），不需要显示器。任何一个 check 变成 FAIL 就会在结尾
汇总成非零结果。任何未捕获的异常会直接抛出来。
"""

import os
import sys
import traceback
from pathlib import Path

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pygame as pg
from source import tool, constants as c
from source.component import plant as pm
from source.component import menubar
from source.component.zombies import normal as zn
from source.state.level.level import Level

tool.init()
SCREEN = tool.SCREEN
FAILURES = []


def check(name, cond, detail=''):
    print(f'  [{"PASS" if cond else "FAIL"}] {name}{"  -> " + detail if detail else ""}')
    if not cond:
        FAILURES.append(name)


def make_level(num, cards=None):
    """起一个关卡并直接进入 PLAY 状态。"""
    lvl = Level()
    lvl.startup(0.0, {c.CURRENT_TIME: 0.0, c.LEVEL_NUM: num})
    if cards is None:
        pool = lvl.map_data.get(c.CARD_POOL)
        if lvl.bar_type == c.CHOOSEBAR_STATIC:
            cards = [0, 1, 2, 3, 4, 5, 6, 7]
        else:
            cards = menubar.getCardPool(pool)
    lvl.input_handler.initPlay(cards)
    return lvl


def frames(lvl, count, start_t=1000):
    t = start_t
    for _ in range(count):
        t += 16
        lvl.update(SCREEN, t, None, (False, False))


# ---------------------------------------------------------------- 字体
def test_level_startup_survives_broken_sysfont():
    """关卡能启动：曾因 pg.font.SysFont 在部分 Windows 上抛 TypeError 而必崩。"""
    lvl = Level()
    lvl.startup(0.0, {c.CURRENT_TIME: 0.0, c.LEVEL_NUM: 0})
    check('Level.startup 完成', lvl.state == c.CHOOSE, f'state={lvl.state}')
    lvl.input_handler.initPlay([0, 1, 2, 3, 4, 5, 6, 7])
    lvl.update(SCREEN, 100, None, (False, False))
    check('选卡面板 -> PLAY 正常', lvl.state == c.PLAY)


def test_first_frame_card_click():
    """开局第一帧点卡牌：MenuBar.current_time 曾未初始化。"""
    lvl = Level()
    lvl.startup(0.0, {c.CURRENT_TIME: 0.0, c.LEVEL_NUM: 0})
    lvl.input_handler.initPlay([0, 1, 2, 3, 4, 5, 6, 7])
    try:
        lvl.update(SCREEN, 100, lvl.menubar.card_list[0].rect.center, (True, False))
        check('首帧点卡牌不崩', True)
    except Exception as e:
        check('首帧点卡牌不崩', False, f'{type(e).__name__}: {e}')


# ---------------------------------------------------------------- 魅惑菇
def test_shovel_unbitten_hypnoshroom():
    """铲掉没被啃过的魅惑菇：曾因缺 kill_zombie 抛 AttributeError。"""
    lvl = make_level(0, [16, 0, 1, 2, 3, 4, 5, 6])
    x, y = lvl.map.getMapGridPos(3, 1)
    lvl.plant_groups[1].add(pm.HypnoShroom(x, y))
    lvl.map.setMapGridType(3, 1, c.MAP_EXIST)
    try:
        ok = lvl.input_handler.plant_manager.removePlantAtPosition((x, y - 20))
        check('铲除成功', ok is True)
        check('格子已释放', lvl.map.map[1][3] == c.MAP_EMPTY)
    except Exception as e:
        check('铲除不崩', False, f'{type(e).__name__}: {e}')


def test_bitten_hypnoshroom_still_hypnotizes():
    """正常被啃掉时魅惑效果不能被上面的守卫误伤。"""
    lvl = make_level(0, [16, 0, 1, 2, 3, 4, 5, 6])
    x, y = lvl.map.getMapGridPos(3, 1)
    shroom = pm.HypnoShroom(x, y)
    lvl.plant_groups[1].add(shroom)
    lvl.map.setMapGridType(3, 1, c.MAP_EXIST)
    z = zn.NormalZombie(x + 10, y, lvl.head_group)
    lvl.zombie_groups[1].add(z)
    z.setAttack(shroom)
    shroom.setDamage(1, z)
    lvl.entity_manager.killPlant(shroom)
    check('转入 hypno 组', z in lvl.hypno_zombie_groups[1])
    check('离开原组', z not in lvl.zombie_groups[1])
    check('is_hypno 置位', z.is_hypno is True)


# ---------------------------------------------------------------- 最后一关
def test_beating_last_level_does_not_crash():
    """打穿最后一关：LEVEL_NUM 会推到 7，曾去读不存在的 level_7.json。"""
    from source.state.screen import GameVictoryScreen
    lvl = make_level(6, [0, 1, 2, 3, 4, 5, 6, 7])
    lvl.zombie_list = []
    for g in lvl.zombie_groups:
        for z in list(g):
            z.kill()
    lvl.update(SCREEN, 100, None, (False, False))
    check('判胜', lvl.done and lvl.next == c.GAME_VICTORY)
    check('LEVEL_NUM 推到 7', lvl.game_info[c.LEVEL_NUM] == 7)
    screen = GameVictoryScreen()
    screen.startup(100, lvl.game_info)
    check('胜利画面回主菜单而非要 level_7', screen.next == c.MAIN_MENU,
          f'next={screen.next}')

    available = {p.stem for p in
                 (Path(__file__).resolve().parent.parent / 'source/data/map').glob('level_*.json')}
    check('磁盘关卡文件数 <= LEVEL_COUNT',
          len(available - {'level_zombie_test'}) <= c.LEVEL_COUNT,
          f'{len(available)} 个文件 / LEVEL_COUNT={c.LEVEL_COUNT}')


# ---------------------------------------------------------------- 小车
def test_car_removal_during_iteration():
    """self.level.cars 是普通 list，边遍历边 remove 曾漏删。"""
    lvl = make_level(0)
    for car in lvl.cars:
        car.rect.x = c.SCREEN_WIDTH + 10
        car.dead = True
    lvl.collision_handler.checkCarCollisions()
    check('5 辆全死 -> 清空', len(lvl.cars) == 0, f'剩 {len(lvl.cars)}')

    lvl = make_level(0)
    for i, car in enumerate(lvl.cars):
        car.dead = (i % 2 == 0)
    lvl.collision_handler.checkCarCollisions()
    check('隔一死一 -> 恰好剩 1/3 号', [x.map_y for x in lvl.cars] == [1, 3],
          f'剩 {[x.map_y for x in lvl.cars]}')


# ---------------------------------------------------------------- 胜利判定
def test_victory_counts_hypno_zombies():
    """场上还有魅惑僵尸时不能判胜。"""
    lvl = make_level(0)
    lvl.zombie_list = []
    for g in lvl.zombie_groups:
        for z in list(g):
            z.kill()
    lvl.hypno_zombie_groups[2].add(zn.NormalZombie(300, 300, lvl.head_group))
    lvl.update(SCREEN, 100, None, (False, False))
    check('不判胜', not lvl.done, f'done={lvl.done}')
    for z in list(lvl.hypno_zombie_groups[2]):
        z.kill()
    lvl.update(SCREEN, 200, None, (False, False))
    check('清空后判胜', lvl.done)


# ---------------------------------------------------------------- 冰冻
def test_thaw_restores_attack():
    """解冻后要回到被冻前的状态，而不是一律回 WALK。"""
    lvl = make_level(0)
    x, y = lvl.map.getMapGridPos(4, 1)
    z = zn.NormalZombie(c.ZOMBIE_START_X, y, lvl.head_group)
    lvl.zombie_groups[1].add(z)
    wall = pm.WallNut(x, y)
    lvl.plant_groups[1].add(wall)
    z.current_time = 1000
    z.setAttack(wall)
    z.setFreeze(wall.image)
    lvl.game_info[c.CURRENT_TIME] = 1000 + c.FREEZE_TIME + 1
    z.update(lvl.game_info)
    check('恢复 ATTACK', z.state == c.ATTACK, f'state={z.state}')
    check('prey 保留', z.prey is wall)


def test_thaw_with_dead_prey_falls_back_to_walk():
    """prey 没了（health 归零）时必须回 WALK，不能 AttributeError。"""
    lvl = make_level(0)
    x, y = lvl.map.getMapGridPos(4, 1)
    z = zn.NormalZombie(c.ZOMBIE_START_X, y, lvl.head_group)
    lvl.zombie_groups[1].add(z)
    wall = pm.WallNut(x, y)
    lvl.plant_groups[1].add(wall)
    z.current_time = 1000
    z.setAttack(wall)
    z.setFreeze(wall.image)
    wall.health = 0
    try:
        lvl.game_info[c.CURRENT_TIME] = 1000 + c.FREEZE_TIME + 1
        z.update(lvl.game_info)
        check('回 WALK 且不崩', z.state == c.WALK, f'state={z.state}')
    except Exception as e:
        check('回 WALK 且不崩', False, f'{type(e).__name__}: {e}')


# ---------------------------------------------------------------- 保龄球
def test_bowling_wall_bounce_keeps_hits_enabled():
    """撞屏幕边界弹回时 disable_hit_y 曾被写成 -1，导致伤害抑制失效。"""
    b = pm.WallNutBowling(300, 300, 2, None)
    b.map_y, b.vel_y = 2, 0
    b.changeDirection(-1)
    check('disable_hit_y 仍为 -1（=未屏蔽）', b.disable_hit_y == -1)
    check('0..4 行全部可命中', all(b.canHit(i) for i in range(5)))

    b2 = pm.WallNutBowling(300, 300, 2, None)
    b2.changeDirection(3)
    check('换行时仍屏蔽刚打过的那排',
          not b2.canHit(3) and b2.canHit(1), f'disable_hit_y={b2.disable_hit_y}')


# ---------------------------------------------------------------- 常量接线
def test_wired_constants_keep_their_values():
    """把字面量换成常量后数值必须一模一样（纯重构，行为零变化）。"""
    expect = {
        'PUFFSHROOM_SHOOT_INTERVAL': 3000,
        'SCAREDYSHROOM_SHOOT_INTERVAL': 2000,
        'SUNSHROOM_ANIMATE_INTERVAL': 200,
        'HYPNOSHROOM_ANIMATE_INTERVAL': 200,
        'CHOMPER_ANIMATE_INTERVAL': 250,
        'CHOMPER_DIGEST_INTERVAL': 15000,
        'SPIKEWEED_ANIMATE_INTERVAL_IDLE': 200,
        'SPIKEWEED_ANIMATE_INTERVAL_ATTACK': 50,
        'SPIKEWEED_ATTACK_INTERVAL': 2000,
        'POTATOMINE_ANIMATE_INTERVAL': 300,
        'POTATOMINE_INIT_TIME': 15000,
        'POTATOMINE_EXPLODE_TIME': 500,
        'POTATOMINE_EXPLODE_X_RANGE': c.GRID_X_SIZE,
        'CHERRYBOMB_EXPLODE_Y_RANGE': 1,
        'CHERRYBOMB_EXPLODE_X_RANGE': c.GRID_X_SIZE,
        'CHERRYBOMB_EXPLODE_TIME': 500,
        'CHERRYBOMB_ANIMATE_INTERVAL': 100,
        'JALAPENO_ANIMATE_INTERVAL': 100,
        'JALAPENO_EXPLODE_X_RANGE': 377,
        'ICESHROOM_ANIMATE_INTERVAL_IDLE': 100,
        'ICESHROOM_ANIMATE_INTERVAL_FREEZE': 500,
        'SQUASH_AIM_TIME': 1000,
        'SQUASH_ANIMATE_INTERVAL': 300,
        'SQUASH_ATTACK_RANGE': c.GRID_X_SIZE,
        'WALLNUTBOWLING_ANIMATE_INTERVAL': 200,
        'WALLNUTBOWLING_MOVE_INTERVAL': 70,
        'WALLNUTBOWLING_ROTATE_DEGREE': 30,
        'CHOMPER_ATTACK_X_RANGE': c.GRID_X_SIZE // 3,
        'PUFFSHROOM_ATTACK_RANGE': c.GRID_X_SIZE * 4,
        'PUFFSHROOM_BULLET_OFFSET_Y': 10,
        'SCAREDYSHROOM_CRY_X_RANGE': c.GRID_X_SIZE * 2,
        'SCAREDYSHROOM_BULLET_OFFSET_Y': 40,
        'SUNFLOWER_INITIAL_TIMER_OFFSET': 6000,
        'SUN_SCALE_BIG': 0.9,
        'SUN_SCALE_SMALL': 0.6,
        'SUN_MOVE_SPEED': 1,
    }
    for name, want in expect.items():
        got = getattr(c, name)
        check(f'{name} == {want}', got == want, f'实际 {got}')


# ---------------------------------------------------------------- 热路径
def test_no_debug_print_spam():
    """地刺反复进出 IDLE / 每次鼠标点击都不该再刷屏。"""
    import io, contextlib
    lvl = make_level(0, [11, 0, 1, 2, 3, 4, 5, 6])
    x, y = lvl.map.getMapGridPos(4, 1)
    lvl.plant_groups[1].add(pm.Spikeweed(x, y))
    lvl.entity_manager.createZombie(c.NORMAL_ZOMBIE, 1)
    z = list(lvl.zombie_groups[1])[0]
    z.rect.centerx = x + 10
    lvl.update(SCREEN, 1000, None, (False, False))
    z.rect.centerx = x + 900
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        frames(lvl, 60, start_t=1040)
    noise = [ln for ln in buf.getvalue().splitlines()
             if 'spikeweed idle' in ln or ln.startswith('pos:')]
    check('无调试刷屏', not noise, f'{len(noise)} 行残留')


# ---------------------------------------------------------------- 全关卡
def test_every_level_runs():
    """7 个关卡各跑 200 帧不抛异常（含传送带和保龄球两种卡池）。"""
    for n in range(c.LEVEL_COUNT):
        lvl = Level()
        lvl.startup(0.0, {c.CURRENT_TIME: 0.0, c.LEVEL_NUM: n})
        pool = lvl.map_data.get(c.CARD_POOL)
        if lvl.bar_type == c.CHOOSEBAR_STATIC:
            cards = [0, 1, 2, 3, 4, 5, 6, 7]
        else:
            cards = menubar.getCardPool(pool)
        lvl.input_handler.initPlay(cards)
        try:
            frames(lvl, 200)
            check(f'level_{n} 200 帧', True,
                  f'bar={lvl.bar_type} cards={len(cards)}')
        except Exception as e:
            check(f'level_{n} 200 帧', False, f'{type(e).__name__}: {e}')


TESTS = [v for k, v in sorted(globals().items()) if k.startswith('test_')]

if __name__ == '__main__':
    for fn in TESTS:
        print(f'\n{fn.__name__}')
        try:
            fn()
        except Exception:
            FAILURES.append(fn.__name__)
            traceback.print_exc()
    print('\n' + '=' * 60)
    print('ALL PASS' if not FAILURES else f'FAILURES ({len(FAILURES)}): {FAILURES}')
    print('=' * 60)
    sys.exit(1 if FAILURES else 0)
