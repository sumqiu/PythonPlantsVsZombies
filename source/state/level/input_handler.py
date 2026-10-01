"""
Input handling for level state
"""
import pygame as pg
from ... import tool
from ... import constants as c
from ...component import menubar, plant

from .plant_manager import PlantManager


class InputHandler:
    def __init__(self, level):
        self.level = level
        self.plant_manager = PlantManager(level)
    
    def initChoose(self):
        """Initialize choose state"""
        self.level.state = c.CHOOSE
        self.level.panel = menubar.Panel(menubar.all_card_list, self.level.map_data[c.INIT_SUN_NAME])

    def choose(self, mouse_pos, mouse_click):
        """Handle choose state input"""
        if mouse_pos and mouse_click[0]:
            self.level.panel.checkCardClick(mouse_pos)
            if self.level.panel.checkStartButtonClick(mouse_pos):
                self.initPlay(self.level.panel.getSelectedCards())

    def initPlay(self, card_list):
        """Initialize play state"""
        self.level.state = c.PLAY
        if self.level.bar_type == c.CHOOSEBAR_STATIC:
            self.level.menubar = menubar.MenuBar(card_list, self.level.map_data[c.INIT_SUN_NAME])
        else:
            self.level.menubar = menubar.MoveBar(card_list)
        
        self.level.drag_plant = False
        self.level.hint_image = None
        self.level.hint_plant = False
        self.level.shovel_mode = False
        
        if self.level.background_type == c.BACKGROUND_DAY and self.level.bar_type == c.CHOOSEBAR_STATIC:
            self.level.produce_sun = True
        else:
            self.level.produce_sun = False
        self.level.sun_timer = self.level.current_time

        self.plant_manager.removeMouseImage()
        self.level.entity_manager.setupGroups()
        self.level.entity_manager.setupZombies()
        self.level.entity_manager.setupCars()

    def play(self, mouse_pos, mouse_click):
        """Handle play state input and updates"""
        # Update entities
        self.level.entity_manager.updateEntities()
        
        # Handle shovel mode
        if self.level.shovel_mode:
            if mouse_click[1]:  # Right click to cancel
                self.plant_manager.removeShovelCursor()
                if hasattr(self.level.menubar, 'setShovelActive'):
                    self.level.menubar.setShovelActive(False)
            elif mouse_click[0] and mouse_pos:  # Left click to remove plant
                if self.level.menubar.checkMenuBarClick(mouse_pos):
                    self.plant_manager.removeShovelCursor()
                    if hasattr(self.level.menubar, 'setShovelActive'):
                        self.level.menubar.setShovelActive(False)
                else:
                    if self.plant_manager.removePlantAtPosition(mouse_pos):
                        self.plant_manager.removeShovelCursor()
                        if hasattr(self.level.menubar, 'setShovelActive'):
                            self.level.menubar.setShovelActive(False)
        # Handle plant dragging and placement
        elif not self.level.drag_plant and mouse_pos and mouse_click[0]:
            # Check if shovel was clicked
            if (hasattr(self.level.menubar, 'checkShovelClick') and 
                self.level.menubar.checkShovelClick(mouse_pos)):
                self.plant_manager.setupShovelCursor()
                self.level.menubar.setShovelActive(True)
            else:
                result = self.level.menubar.checkCardClick(mouse_pos)
                if result:
                    self.plant_manager.setupMouseImage(result[0], result[1])
        elif self.level.drag_plant:
            if mouse_click[1]:  # Right click to cancel
                self.plant_manager.removeMouseImage()
            elif mouse_click[0]:  # Left click to place
                if self.level.menubar.checkMenuBarClick(mouse_pos):
                    self.plant_manager.removeMouseImage()
                else:
                    self.plant_manager.addPlant()
            elif mouse_pos is None:
                self.plant_manager.setupHintImage()
        
        # Handle sun production
        if self.level.produce_sun:
            if (self.level.current_time - self.level.sun_timer) > c.PRODUCE_SUN_INTERVAL:
                self.level.sun_timer = self.level.current_time
                map_x, map_y = self.level.map.getRandomMapIndex()
                x, y = self.level.map.getMapGridPos(map_x, map_y)
                self.level.sun_group.add(plant.Sun(x, 0, x, y))
        
        # Handle sun collection
        if not self.level.drag_plant and not self.level.shovel_mode and mouse_pos and mouse_click[0]:
            for sun in self.level.sun_group:
                if sun.checkCollision(mouse_pos[0], mouse_pos[1]):
                    self.level.menubar.increaseSunValue(sun.sun_value)

        # Update menubar
        self.level.menubar.update(self.level.current_time)

        # Check collisions and game state
        self.level.collision_handler.checkAllCollisions()
        self.plant_manager.checkPlants()
        self.level.game_state_checker.checkGameState()
    
    def handlePause(self, mouse_pos, mouse_click):
        """Handle pause menu input"""
        if mouse_pos:
            self.level.pause_menu.update_hover(mouse_pos)
            
            if mouse_click[0]:
                action = self.level.pause_menu.check_click(mouse_pos)
                
                if action == 'resume':
                    self.resumeGame()
                elif action == 'restart':
                    self.restartLevel()
                elif action == 'quit':
                    self.quitToMenu()
    
    def pauseGame(self):
        """暂停游戏"""
        self.level.paused = True
        tool.music_manager.pause_music()
    
    def resumeGame(self):
        """继续游戏"""
        self.level.paused = False
        tool.music_manager.unpause_music()
    
    def restartLevel(self):
        """重新开始关卡"""
        self.level.done = True
        self.level.next = c.LEVEL
    
    def quitToMenu(self):
        """退出到主菜单"""
        tool.music_manager.stop_music()
        self.level.done = True
        self.level.next = c.MAIN_MENU
