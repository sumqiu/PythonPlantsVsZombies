__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class LevelSelect(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        
        self.setupBackground()
        self.setupLevelButtons()
        self.setupBackButton()
        
        # Play main menu music
        tool.music_manager.play_music(c.MUSIC_MAIN_MENU)

    def setupBackground(self):
        # 使用主菜单背景作为占位
        frame_rect = [80, 0, 800, 600]
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0
        
        # 创建半透明遮罩
        self.overlay = pg.Surface((800, 600))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)
        
    def setupLevelButtons(self):
        """创建关卡按钮"""
        self.level_buttons = []
        self.level_count = c.LEVEL_COUNT  # level_0 到 level_6
        
        # 按钮布局：3行3列
        cols = 3
        rows = 3
        button_width = 120
        button_height = 80
        spacing_x = 40
        spacing_y = 40
        start_x = 200
        start_y = 150
        
        for i in range(self.level_count):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            
            button = {
                'rect': pg.Rect(x, y, button_width, button_height),
                'level': i,
                'hovered': False
            }
            self.level_buttons.append(button)
        
        self.selected_level = None
        
    def setupBackButton(self):
        """创建返回按钮"""
        self.back_button = {
            'rect': pg.Rect(50, 500, 100, 50),
            'hovered': False
        }
    
    def checkButtonClick(self, mouse_pos):
        """检查按钮点击"""
        x, y = mouse_pos
        
        # 检查关卡按钮
        for button in self.level_buttons:
            if button['rect'].collidepoint(x, y):
                self.selected_level = button['level']
                self.game_info[c.LEVEL_NUM] = self.selected_level
                self.game_info['from_level_select'] = True  # 标记来自关卡选择
                self.done = True
                return True
        
        # 检查返回按钮
        if self.back_button['rect'].collidepoint(x, y):
            self.next = c.MAIN_MENU
            self.done = True
            return True
        
        return False
    
    def updateHoverState(self, mouse_pos):
        """更新悬停状态"""
        x, y = mouse_pos
        
        for button in self.level_buttons:
            button['hovered'] = button['rect'].collidepoint(x, y)
        
        self.back_button['hovered'] = self.back_button['rect'].collidepoint(x, y)
        
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if mouse_pos:
            self.updateHoverState(mouse_pos)
            if mouse_click:
                self.checkButtonClick(mouse_pos)
        
        self.draw(surface)
    
    def draw(self, surface):
        """绘制界面"""
        # 绘制背景
        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.overlay, (0, 0))
        
        # 绘制标题
        title_font = pg.font.Font(None, 60)
        title_text = title_font.render('Select Level', True, c.WHITE)
        title_rect = title_text.get_rect(centerx=400, y=50)
        surface.blit(title_text, title_rect)
        
        # 绘制关卡按钮
        button_font = pg.font.Font(None, 40)
        for button in self.level_buttons:
            # 按钮背景
            color = c.GOLD if button['hovered'] else c.GREEN
            pg.draw.rect(surface, color, button['rect'])
            pg.draw.rect(surface, c.WHITE, button['rect'], 3)
            
            # 按钮文字
            text = button_font.render(f'Level {button["level"]}', True, c.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            surface.blit(text, text_rect)
        
        # 绘制返回按钮
        back_color = c.GOLD if self.back_button['hovered'] else c.RED
        pg.draw.rect(surface, back_color, self.back_button['rect'])
        pg.draw.rect(surface, c.WHITE, self.back_button['rect'], 3)
        
        back_font = pg.font.Font(None, 30)
        back_text = back_font.render('Back', True, c.WHITE)
        back_rect = back_text.get_rect(center=self.back_button['rect'].center)
        surface.blit(back_text, back_rect)
