__author__ = 'marble_xu'

import os
import json
from abc import abstractmethod
from pathlib import Path
import pygame as pg
from . import constants as c

# tool.py 中定义的模块级资源变量；调用 init() 之前保持为空/None，
# 不会在 import 时触发任何 pygame 副作用，方便单元测试。
GFX: dict = {}
ZOMBIE_RECT: dict = {}
PLANT_RECT: dict = {}
MUSIC: dict = {}
SCREEN = None
music_manager = None


class State():
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.next = None
        self.persist = {}
    
    @abstractmethod
    def startup(self, current_time, persist):
        '''abstract method'''

    def cleanup(self):
        self.done = False
        return self.persist
    
    @abstractmethod
    def update(self, surface, current_time, mouse_pos, mouse_click):
        '''abstract method'''

class Control():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.mouse_pos = None
        self.mouse_click = [False, False]  # value:[left mouse click, right mouse click]
        self.current_time = 0.0
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.game_info = {c.CURRENT_TIME:0.0,
                          c.LEVEL_NUM:c.START_LEVEL_NUM}
 
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, self.game_info)

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.current_time, self.mouse_pos, self.mouse_click)
        self.mouse_pos = None
        self.mouse_click[0] = False
        self.mouse_click[1] = False

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                # Handle ESC key for pause
                if event.key == pg.K_ESCAPE:
                    if hasattr(self.state, 'paused') and hasattr(self.state, 'input_handler'):
                        if self.state.state == c.PLAY:  # Only pause during play state
                            if self.state.paused:
                                self.state.input_handler.resumeGame()
                            else:
                                self.state.input_handler.pauseGame()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pos = pg.mouse.get_pos()
                self.mouse_click[0], _, self.mouse_click[1] = pg.mouse.get_pressed()

    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
        print('game over')

def get_image(sheet, x, y, width, height, colorkey=c.BLACK, scale=1):
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(colorkey)
        image = pg.transform.scale(image,
                                   (int(rect.width*scale),
                                    int(rect.height*scale)))
        return image

def load_image_frames(directory, image_name, colorkey, accept):
    frame_list = []
    tmp = {}
    # image_name is "Peashooter", pic name is 'Peashooter_1', get the index 1
    index_start = len(image_name) + 1 
    frame_num = 0;
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            index = int(name[index_start:])
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            tmp[index]= img
            frame_num += 1

    for i in range(frame_num):
        frame_list.append(tmp[i])
    return frame_list

def load_all_gfx(directory, colorkey=c.WHITE, accept=('.png', '.jpg', '.bmp', '.gif')):
    graphics = {}
    for name1 in os.listdir(directory):
        # subfolders under the folder resources\graphics
        dir1 = os.path.join(directory, name1)
        if os.path.isdir(dir1):
            for name2 in os.listdir(dir1):
                dir2 = os.path.join(dir1, name2)
                if os.path.isdir(dir2):
                # e.g. subfolders under the folder resources\graphics\Zombies
                    for name3 in os.listdir(dir2):
                        dir3 = os.path.join(dir2, name3)
                        # e.g. subfolders or pics under the folder resources\graphics\Zombies\ConeheadZombie
                        if os.path.isdir(dir3):
                            # e.g. it's the folder resources\graphics\Zombies\ConeheadZombie\ConeheadZombieAttack
                            image_name, _ = os.path.splitext(name3)
                            graphics[image_name] = load_image_frames(dir3, image_name, colorkey, accept)
                        else:
                            # e.g. pics under the folder resources\graphics\Plants\Peashooter
                            image_name, _ = os.path.splitext(name2)
                            graphics[image_name] = load_image_frames(dir2, image_name, colorkey, accept)
                            break
                else:
                # e.g. pics under the folder resources\graphics\Screen
                    name, ext = os.path.splitext(name2)
                    if ext.lower() in accept:
                        img = pg.image.load(dir2)
                        if img.get_alpha():
                            img = img.convert_alpha()
                        else:
                            img = img.convert()
                            img.set_colorkey(colorkey)
                        graphics[name] = img
    return graphics

def loadZombieImageRect():
    """Load zombie image rectangle data from JSON file with error handling."""
    file_path = Path(__file__).parent / 'data' / 'entity' / 'zombie.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[c.ZOMBIE_IMAGE_RECT]
    except FileNotFoundError:
        print(f"Error: Zombie data file not found at {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in zombie data file: {e}")
        return {}
    except KeyError:
        print(f"Error: Missing '{c.ZOMBIE_IMAGE_RECT}' key in zombie data")
        return {}

def loadPlantImageRect():
    """Load plant image rectangle data from JSON file with error handling."""
    file_path = Path(__file__).parent / 'data' / 'entity' / 'plant.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[c.PLANT_IMAGE_RECT]
    except FileNotFoundError:
        print(f"Error: Plant data file not found at {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in plant data file: {e}")
        return {}
    except KeyError:
        print(f"Error: Missing '{c.PLANT_IMAGE_RECT}' key in plant data")
        return {}

def load_music(directory, accept=('.wav', '.mp3', '.ogg', '.midi', '.m4a')):
    """Load all music files from the specified directory."""
    music = {}
    if not os.path.exists(directory):
        print(f"Warning: Music directory '{directory}' not found")
        return music
    
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lower() in accept:
            music[name] = os.path.join(directory, filename)
    return music

class MusicManager:
    """Manages background music playback."""
    def __init__(self):
        self.music_dict = {}
        self.current_music = None
        self.volume = c.MUSIC_VOLUME
        pg.mixer.music.set_volume(self.volume)
        self._converted_cache = {}  # Cache converted files
    
    def load_music_files(self, music_dict):
        """Load music file paths and pre-convert m4a files if needed."""
        self.music_dict = music_dict
        
        # Pre-convert m4a files
        for name, path in music_dict.items():
            if path.lower().endswith('.m4a'):
                print(f"Pre-converting {name}.m4a to ogg format...")
                converted = self._convert_m4a_to_ogg(path)
                if converted:
                    self._converted_cache[name] = converted
                    print(f"Conversion complete for {name}")
    
    def _convert_m4a_to_ogg(self, m4a_path):
        """Convert m4a file to ogg file using pydub."""
        try:
            from pydub import AudioSegment
            
            # Create output path in same directory
            base_path = os.path.splitext(m4a_path)[0]
            ogg_path = base_path + '_converted.ogg'
            
            # Skip if already converted
            if os.path.exists(ogg_path):
                print(f"Using existing converted file: {ogg_path}")
                return ogg_path
            
            # Convert m4a to ogg
            audio = AudioSegment.from_file(m4a_path, format='m4a')
            audio.export(ogg_path, format='ogg')
            
            return ogg_path
        except ImportError:
            print(f"Error: pydub not installed. Install with: pip install pydub")
            print(f"Also ensure ffmpeg is installed on your system.")
            return None
        except Exception as e:
            print(f"Error converting m4a to ogg: {e}")
            return None
    
    def play_music(self, music_name, loops=-1):
        """Play background music. loops=-1 means infinite loop."""
        if music_name == self.current_music:
            return
        
        if music_name not in self.music_dict:
            print(f"Warning: Music '{music_name}' not found")
            return
        
        # Use converted file if available
        if music_name in self._converted_cache:
            music_path = self._converted_cache[music_name]
        else:
            music_path = self.music_dict[music_name]
        
        try:
            pg.mixer.music.load(music_path)
            pg.mixer.music.play(loops)
            self.current_music = music_name
        except Exception as e:
            print(f"Error playing music '{music_name}': {e}")
    
    def stop_music(self):
        """Stop the currently playing music."""
        pg.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self):
        """Pause the currently playing music."""
        pg.mixer.music.pause()
    
    def unpause_music(self):
        """Resume the paused music."""
        pg.mixer.music.unpause()
    
    def set_volume(self, volume):
        """Set music volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pg.mixer.music.set_volume(self.volume)

def init():
    """显式初始化函数：启动 pygame、创建显示窗口并加载所有资源。
    必须在创建 Control 实例之前调用一次；不在模块导入时执行，
    使单元测试可以安全地 import tool 而无需真实的显示环境。
    """
    global GFX, ZOMBIE_RECT, PLANT_RECT, MUSIC, SCREEN, music_manager

    pg.init()
    pg.mixer.init()
    pg.display.set_caption(c.ORIGINAL_CAPTION)
    SCREEN = pg.display.set_mode(c.SCREEN_SIZE)

    _res = Path(__file__).parent.parent / 'resources'
    GFX = load_all_gfx(str(_res / 'graphics'))
    ZOMBIE_RECT = loadZombieImageRect()
    PLANT_RECT = loadPlantImageRect()
    MUSIC = load_music(str(_res / 'music'))
    music_manager = MusicManager()
    music_manager.load_music_files(MUSIC)
