__author__ = 'marble_xu'

START_LEVEL_NUM = 1
# 共 7 个关卡，文件为 data/map/level_0.json ~ level_6.json
LEVEL_COUNT = 7

ORIGINAL_CAPTION = 'Plant VS Zombies Game'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GRID_X_LEN = 9
GRID_Y_LEN = 5
GRID_X_SIZE = 80
GRID_Y_SIZE = 100


WHITE        = (255, 255, 255)
NAVYBLUE     = ( 60,  60, 100)
SKY_BLUE     = ( 39, 145, 251)
BLACK        = (  0,   0,   0)
LIGHTYELLOW  = (234, 233, 171)
RED          = (255,   0,   0)
GOLD         = (255, 215,   0)
GREEN        = (  0, 255,   0)

#GAME INFO DICTIONARY KEYS
CURRENT_TIME = 'current time'
LEVEL_NUM = 'level num'

#STATES FOR ENTIRE GAME
MAIN_MENU = 'main menu'
LEVEL_SELECT = 'level select'
GAME_LOSE = 'game lose'
GAME_VICTORY = 'game victory'
LEVEL = 'level'

MAIN_MENU_IMAGE = 'MainMenu'
OPTION_ADVENTURE = 'Adventure'
GAME_LOSE_IMAGE = 'GameLoose'
GAME_VICTORY_IMAGE = 'GameVictory'

#MAP COMPONENTS
BACKGROUND_NAME = 'Background'
BACKGROUND_TYPE = 'background_type'
INIT_SUN_NAME = 'init_sun_value'
ZOMBIE_LIST = 'zombie_list'

MAP_EMPTY = 0
MAP_EXIST = 1

BACKGROUND_OFFSET_X = 220
MAP_OFFSET_X = 35
MAP_OFFSET_Y = 100

#MENUBAR
CHOOSEBAR_TYPE = 'choosebar_type'
CHOOSEBAR_STATIC = 0
CHOOSEBAR_BOWLING = 2
MENUBAR_BACKGROUND = 'ChooserBackground'
MOVEBAR_BACKGROUND = 'MoveBackground'
PANEL_BACKGROUND = 'PanelBackground'
START_BUTTON = 'StartButton'
CARD_POOL = 'card_pool'
SHOVEL = 'Shovel'

MOVEBAR_CARD_FRESH_TIME = 6000
CARD_MOVE_TIME = 60

#PLANT INFO
PLANT_IMAGE_RECT = 'plant_image_rect'
CAR = 'car'
SUN = 'Sun'
SUNFLOWER = 'SunFlower'
PEASHOOTER = 'Peashooter'
SNOWPEASHOOTER = 'SnowPea'
WALLNUT = 'WallNut'
CHERRYBOMB = 'CherryBomb'
THREEPEASHOOTER = 'Threepeater'
REPEATERPEA = 'RepeaterPea'
CHOMPER = 'Chomper'
CHERRY_BOOM_IMAGE = 'Boom'
PUFFSHROOM = 'PuffShroom'
POTATOMINE = 'PotatoMine'
SQUASH = 'Squash'
SPIKEWEED = 'Spikeweed'
JALAPENO = 'Jalapeno'
SCAREDYSHROOM = 'ScaredyShroom'
SUNSHROOM = 'SunShroom'
ICESHROOM = 'IceShroom'
HYPNOSHROOM = 'HypnoShroom'
WALLNUTBOWLING = 'WallNutBowling'
REDWALLNUTBOWLING = 'RedWallNutBowling'

PLANT_HEALTH = 5
WALLNUT_HEALTH = 30
WALLNUT_CRACKED1_HEALTH = 20
WALLNUT_CRACKED2_HEALTH = 10
WALLNUT_BOWLING_DAMAGE = 10

PRODUCE_SUN_INTERVAL = 7000
FLOWER_SUN_INTERVAL = 22000
SUN_LIVE_TIME = 7000
SUN_VALUE = 25

ICE_SLOW_TIME = 2000

FREEZE_TIME = 7500

#PLANT CARD INFO
CARD_SUNFLOWER = 'card_sunflower'
CARD_PEASHOOTER = 'card_peashooter'
CARD_SNOWPEASHOOTER = 'card_snowpea'
CARD_WALLNUT = 'card_wallnut'
CARD_CHERRYBOMB = 'card_cherrybomb'
CARD_THREEPEASHOOTER = 'card_threepeashooter'
CARD_REPEATERPEA = 'card_repeaterpea'
CARD_CHOMPER = 'card_chomper'
CARD_PUFFSHROOM = 'card_puffshroom'
CARD_POTATOMINE = 'card_potatomine'
CARD_SQUASH = 'card_squash'
CARD_SPIKEWEED = 'card_spikeweed'
CARD_JALAPENO = 'card_jalapeno'
CARD_SCAREDYSHROOM = 'card_scaredyshroom'
CARD_SUNSHROOM = 'card_sunshroom'
CARD_ICESHROOM = 'card_iceshroom'
CARD_HYPNOSHROOM = 'card_hypnoshroom'
CARD_REDWALLNUT = 'card_redwallnut'

# ZOMBIE CARD INFO (for playable zombies)
CARD_BUCKETHEAD_ZOMBIE = 'card_buckethead_zombie'
CARD_CONEHEAD_ZOMBIE = 'card_conehead_zombie'
CARD_NORMAL_ZOMBIE = 'card_normal_zombie'

#BULLET INFO
BULLET_PEA = 'PeaNormal'
BULLET_PEA_ICE = 'PeaIce'
BULLET_MUSHROOM = 'BulletMushRoom'
BULLET_DAMAGE_NORMAL = 1

#ZOMBIE INFO
ZOMBIE_IMAGE_RECT = 'zombie_image_rect'
ZOMBIE_HEAD = 'ZombieHead'
NORMAL_ZOMBIE = 'Zombie'
CONEHEAD_ZOMBIE = 'ConeheadZombie'
BUCKETHEAD_ZOMBIE = 'BucketheadZombie'
FLAG_ZOMBIE = 'FlagZombie'
NEWSPAPER_ZOMBIE = 'NewspaperZombie'
BOOMDIE = 'BoomDie'

LOSTHEAD_HEALTH = 5
NORMAL_HEALTH = 10
FLAG_HEALTH = 15
CONEHEAD_HEALTH = 20
BUCKETHEAD_HEALTH = 30
NEWSPAPER_HEALTH = 15

ATTACK_INTERVAL = 1000
ZOMBIE_WALK_INTERVAL = 70

ZOMBIE_START_X = SCREEN_WIDTH + 50

#STATE
IDLE = 'idle'
FLY = 'fly'
EXPLODE = 'explode'
ATTACK = 'attack'
DIGEST = 'digest'
WALK = 'walk'
DIE = 'die'
CRY = 'cry'
FREEZE = 'freeze'
SLEEP = 'sleep'

#LEVEL STATE
CHOOSE = 'choose'
PLAY = 'play'

#BACKGROUND
BACKGROUND_DAY = 0
BACKGROUND_NIGHT = 1

# ===== TIMING CONSTANTS (消除魔法数字) =====
# 注意：这里的每个常量都必须真的被代码引用，改了才有效。
ANIMATION_INTERVAL_DEFAULT = 100  # Default animation frame interval (ms)

# Plant specific timings
PLANT_SHOOT_INTERVAL = 2000       # Time between plant shots (ms)
PLANT_HIT_FLASH_TIME = 200        # Duration of hit flash effect (ms)
PLANT_ALPHA_HIT = 192             # Alpha value when hit
PLANT_ALPHA_NORMAL = 255          # Normal alpha value

# Bullet timings
BULLET_EXPLODE_TIME = 500         # Bullet explosion duration (ms)
BULLET_VELOCITY_X = 4             # Bullet horizontal speed
BULLET_VELOCITY_Y = 4             # Bullet vertical speed

# Car movement
CAR_VELOCITY = 4                  # Car movement speed

# Zombie specific timings
ZOMBIE_ANIMATE_INTERVAL_WALK = 150   # Zombie walk animation interval (ms)
ZOMBIE_ANIMATE_INTERVAL_ATTACK = 100 # Zombie attack animation interval (ms)
ZOMBIE_ANIMATE_INTERVAL_DIE = 200    # Zombie death animation interval (ms)
ZOMBIE_SPEED_NORMAL = 1              # Normal zombie movement speed
ZOMBIE_SPEED_FAST = 2                # Fast zombie movement speed (newspaper zombie)

# Special plant timings
CHOMPER_DIGEST_INTERVAL = 15000      # Chomper digestion time (ms)
CHOMPER_ANIMATE_INTERVAL = 250       # Chomper animation interval (ms)
POTATOMINE_INIT_TIME = 15000         # Potato mine initialization time (ms)
POTATOMINE_ANIMATE_INTERVAL = 300    # Potato mine animation interval (ms)
POTATOMINE_EXPLODE_TIME = 500        # Potato mine explosion duration (ms)
SUNSHROOM_GROW_TIME = 25000          # Sun shroom growth time (ms)
SUNSHROOM_ANIMATE_INTERVAL = 200     # Sun shroom animation interval (ms)
PUFFSHROOM_SHOOT_INTERVAL = 3000     # Puff shroom shoot interval (ms)
SPIKEWEED_ATTACK_INTERVAL = 2000     # Spikeweed attack interval (ms)
SPIKEWEED_ANIMATE_INTERVAL_IDLE = 200  # Spikeweed idle animation (ms)
SPIKEWEED_ANIMATE_INTERVAL_ATTACK = 50 # Spikeweed attack animation (ms)
SQUASH_AIM_TIME = 1000               # Squash aiming time (ms)
SQUASH_ANIMATE_INTERVAL = 300        # Squash animation interval (ms)
CHERRYBOMB_EXPLODE_TIME = 500        # Cherry bomb explosion time (ms)
CHERRYBOMB_ANIMATE_INTERVAL = 100    # Cherry bomb animation interval (ms)
JALAPENO_ANIMATE_INTERVAL = 100      # Jalapeno animation interval (ms)
ICESHROOM_ANIMATE_INTERVAL_IDLE = 100   # Ice shroom idle animation (ms)
ICESHROOM_ANIMATE_INTERVAL_FREEZE = 500 # Ice shroom freeze animation (ms)
SCAREDYSHROOM_SHOOT_INTERVAL = 2000  # Scaredy shroom shoot interval (ms)
HYPNOSHROOM_ANIMATE_INTERVAL = 200  # Hypno shroom animation interval (ms)

# Bowling plant timings
WALLNUTBOWLING_ANIMATE_INTERVAL = 200  # Wallnut bowling animation (ms)
WALLNUTBOWLING_MOVE_INTERVAL = 70      # Wallnut bowling movement interval (ms)
WALLNUTBOWLING_ROTATE_DEGREE = 30      # Rotation degree per frame

# ===== POSITION AND SIZE CONSTANTS =====
# Offsets and ranges
THREEPEASHOOTER_BULLET_OFFSET_Y = 9  # Bullet Y offset for three peashooter
REPEATERPEA_BULLET_OFFSET_X = 40     # Second bullet X offset for repeater pea
POTATOMINE_EXPLODE_X_RANGE = GRID_X_SIZE  # Potato mine explosion X range
CHERRYBOMB_EXPLODE_Y_RANGE = 1       # Cherry bomb explosion Y range (rows)
CHERRYBOMB_EXPLODE_X_RANGE = GRID_X_SIZE  # Cherry bomb explosion X range
JALAPENO_EXPLODE_X_RANGE = 377       # Jalapeno explosion X range
CHOMPER_ATTACK_X_RANGE = GRID_X_SIZE // 3  # Chomper attack range extension
PUFFSHROOM_ATTACK_RANGE = GRID_X_SIZE * 4  # Puff shroom attack range
PUFFSHROOM_BULLET_OFFSET_Y = 10      # Puff shroom bullet Y offset
SCAREDYSHROOM_CRY_X_RANGE = GRID_X_SIZE * 2  # Scaredy shroom cry range
SCAREDYSHROOM_BULLET_OFFSET_Y = 40   # Scaredy shroom bullet Y offset
SQUASH_ATTACK_RANGE = GRID_X_SIZE    # Squash attack range

# Sun specific
SUN_SCALE_BIG = 0.9                  # Big sun scale
SUN_SCALE_SMALL = 0.6                # Small sun scale
SUN_VALUE_SMALL = 12                 # Small sun value
SUN_MOVE_SPEED = 1                   # Sun movement speed

# Sunflower timing offset
SUNFLOWER_INITIAL_TIMER_OFFSET = 6000  # Initial sun production offset (ms)

# ===== MUSIC AND SOUND CONSTANTS =====
MUSIC_VOLUME = 0.5                   # Background music volume (0.0 to 1.0)

# Music file names
MUSIC_MAIN_MENU = 'mainmenu'
MUSIC_LEVEL_DAY = 'grasswalk'
MUSIC_LEVEL_NIGHT = 'moongrains'
MUSIC_VICTORY = 'victory'
MUSIC_LOSE = 'lose'

# PAUSE MENU
PAUSE_MENU_WIDTH = 400
PAUSE_MENU_HEIGHT = 300
PAUSE_BUTTON_WIDTH = 200
PAUSE_BUTTON_HEIGHT = 50
PAUSE_BUTTON_SPACING = 20
