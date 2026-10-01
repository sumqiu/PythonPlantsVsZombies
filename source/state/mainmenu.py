__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Menu(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        
        self.setupBackground()
        self.setupOption()
        
        # Play main menu music
        tool.music_manager.play_music(c.MUSIC_MAIN_MENU)

    def setupBackground(self):
        frame_rect = [80, 0, 800, 600]
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0
        
    def setupOption(self):
        # 冒险模式按钮
        self.option_frames = []
        frame_names = [c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1']
        frame_rect = [0, 0, 165, 77]
        
        for name in frame_names:
            self.option_frames.append(tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 1.7))
        
        self.option_frame_index = 0
        self.option_image = self.option_frames[self.option_frame_index]
        self.option_rect = self.option_image.get_rect()
        self.option_rect.x = 435
        self.option_rect.y = 75
        
        self.option_start = 0
        self.option_timer = 0
        self.option_clicked = False
        
        # 关卡选择按钮（占位符）
        self.level_select_button = pg.Rect(435, 200, 200, 60)
        self.level_select_hovered = False
        self.level_select_clicked = False
    
    def checkOptionClick(self, mouse_pos):
        x, y = mouse_pos
        
        # 检查冒险模式按钮
        if(x >= self.option_rect.x and x <= self.option_rect.right and
           y >= self.option_rect.y and y <= self.option_rect.bottom):
            self.option_clicked = True
            self.option_timer = self.option_start = self.current_time
            self.next = c.LEVEL
            self.game_info['from_level_select'] = False  # 清除关卡选择标记
            return True
        
        # 检查关卡选择按钮
        if self.level_select_button.collidepoint(x, y):
            self.level_select_clicked = True
            self.next = c.LEVEL_SELECT
            self.done = True
            return True
        
        return False
    
    def updateHoverState(self, mouse_pos):
        """更新悬停状态"""
        x, y = mouse_pos
        self.level_select_hovered = self.level_select_button.collidepoint(x, y)
        
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if not self.option_clicked and not self.level_select_clicked:
            if mouse_pos:
                self.updateHoverState(mouse_pos)
                if mouse_click:
                    self.checkOptionClick(mouse_pos)
        else:
            if self.option_clicked:
                if(self.current_time - self.option_timer) > 200:
                    self.option_frame_index += 1
                    if self.option_frame_index >= 2:
                        self.option_frame_index = 0
                    self.option_timer = self.current_time
                    self.option_image = self.option_frames[self.option_frame_index]
                if(self.current_time - self.option_start) > 1300:
                    self.done = True

        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.option_image, self.option_rect)
        
        # 绘制关卡选择按钮
        self.drawLevelSelectButton(surface)

    def drawLevelSelectButton(self, surface):
        """绘制关卡选择按钮"""
        # 按钮背景
        color = c.GOLD if self.level_select_hovered else c.SKY_BLUE
        pg.draw.rect(surface, color, self.level_select_button)
        pg.draw.rect(surface, c.WHITE, self.level_select_button, 3)
        
        # 按钮文字
        font = pg.font.Font(None, 36)
        text = font.render('Level Select', True, c.WHITE)
        text_rect = text.get_rect(center=self.level_select_button.center)
        surface.blit(text, text_rect)
