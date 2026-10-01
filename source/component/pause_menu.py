"""
Pause Menu Component
"""
import pygame as pg
from .. import tool
from .. import constants as c


class PauseMenu:
    """暂停菜单"""
    
    def __init__(self):
        self.load_images()
        self.setup_menu()
    
    def load_images(self):
        """加载菜单图片素材"""
        try:
            self.background_image = tool.GFX['PauseMenuBackground']
            self.resume_button_image = tool.GFX['ResumeButton']
            self.restart_button_image = tool.GFX['RestartButton']
            self.quit_button_image = tool.GFX['QuitButton']
            self.use_images = True
        except KeyError as e:
            print(f"Warning: Pause menu image not found: {e}")
            # 临时占位：创建半透明背景
            self.background = pg.Surface((c.PAUSE_MENU_WIDTH, c.PAUSE_MENU_HEIGHT))
            self.background.fill((50, 50, 50))
            self.background.set_alpha(230)
            self.use_images = False
    
    def setup_menu(self):
        """设置菜单"""
        # 菜单背景位置
        self.menu_rect = pg.Rect(
            (c.SCREEN_WIDTH - c.PAUSE_MENU_WIDTH) // 2,
            (c.SCREEN_HEIGHT - c.PAUSE_MENU_HEIGHT) // 2,
            c.PAUSE_MENU_WIDTH,
            c.PAUSE_MENU_HEIGHT
        )
        
        # 按钮位置
        button_x = (c.PAUSE_MENU_WIDTH - c.PAUSE_BUTTON_WIDTH) // 2
        button_start_y = 60
        
        # 继续游戏按钮
        self.resume_button = pg.Rect(
            button_x,
            button_start_y,
            c.PAUSE_BUTTON_WIDTH,
            c.PAUSE_BUTTON_HEIGHT
        )
        
        # 重新开始按钮
        self.restart_button = pg.Rect(
            button_x,
            button_start_y + c.PAUSE_BUTTON_HEIGHT + c.PAUSE_BUTTON_SPACING,
            c.PAUSE_BUTTON_WIDTH,
            c.PAUSE_BUTTON_HEIGHT
        )
        
        # 退出到主菜单按钮
        self.quit_button = pg.Rect(
            button_x,
            button_start_y + (c.PAUSE_BUTTON_HEIGHT + c.PAUSE_BUTTON_SPACING) * 2,
            c.PAUSE_BUTTON_WIDTH,
            c.PAUSE_BUTTON_HEIGHT
        )
        
        # 字体
        # 用 Font(None) 而不是 SysFont('Arial')：SysFont 会扫描系统字体注册表，
        # 部分 Windows 上注册表条目不是字符串，pygame 2.6 会抛 TypeError 直接崩。
        self.title_font = pg.font.Font(None, 46)
        self.button_font = pg.font.Font(None, 28)
        
        # 悬停状态
        self.hover_button = None
    
    def _hit_test_button(self, mouse_pos):
        """将鼠标绝对坐标转换为菜单内相对坐标，返回命中的按钮名称或 None。"""
        rel = (mouse_pos[0] - self.menu_rect.x, mouse_pos[1] - self.menu_rect.y)
        if self.resume_button.collidepoint(rel):
            return 'resume'
        if self.restart_button.collidepoint(rel):
            return 'restart'
        if self.quit_button.collidepoint(rel):
            return 'quit'
        return None

    def check_click(self, mouse_pos):
        """检查点击，返回: 'resume', 'restart', 'quit' 或 None。"""
        return self._hit_test_button(mouse_pos)

    def update_hover(self, mouse_pos):
        """更新悬停状态。"""
        if not self.menu_rect.collidepoint(mouse_pos):
            self.hover_button = None
            return
        self.hover_button = self._hit_test_button(mouse_pos)
    
    def draw(self, surface):
        """绘制暂停菜单"""
        # 绘制半透明遮罩覆盖整个屏幕
        overlay = pg.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        surface.blit(overlay, (0, 0))
        
        # 绘制菜单背景
        if self.use_images:
            surface.blit(self.background_image, self.menu_rect)
        else:
            # 临时占位绘制
            surface.blit(self.background, self.menu_rect)
            pg.draw.rect(surface, c.WHITE, self.menu_rect, 3)
            
            # 绘制标题（临时占位）
            title_text = self.title_font.render('游戏暂停', True, c.WHITE)
            title_rect = title_text.get_rect(centerx=self.menu_rect.centerx, y=self.menu_rect.y + 20)
            surface.blit(title_text, title_rect)
        
        # 绘制按钮
        self.draw_button(surface, self.resume_button, '继续游戏', 'resume')
        self.draw_button(surface, self.restart_button, '重新开始', 'restart')
        self.draw_button(surface, self.quit_button, '退出到主菜单', 'quit')
    
    def draw_button(self, surface, button_rect, text, button_name):
        """绘制单个按钮"""
        # 计算按钮在屏幕上的实际位置
        actual_rect = button_rect.move(self.menu_rect.x, self.menu_rect.y)
        
        # 使用图片绘制按钮
        if self.use_images:
            button_images = {
                'resume': self.resume_button_image,
                'restart': self.restart_button_image,
                'quit': self.quit_button_image
            }
            if button_name in button_images:
                surface.blit(button_images[button_name], actual_rect)
                return
        
        # 临时占位绘制（如果图片加载失败）
        if self.hover_button == button_name:
            button_color = (100, 150, 100)
            text_color = c.GOLD
        else:
            button_color = (70, 70, 70)
            text_color = c.WHITE
        
        # 绘制按钮背景
        pg.draw.rect(surface, button_color, actual_rect)
        pg.draw.rect(surface, c.WHITE, actual_rect, 2)
        
        # 绘制按钮文字
        button_text = self.button_font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=actual_rect.center)
        surface.blit(button_text, text_rect)
