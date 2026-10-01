"""
Game state checking - victory and lose conditions
"""
from ... import constants as c


class GameStateChecker:
    def __init__(self, level):
        self.level = level
    
    def checkVictory(self):
        """Check if player has won"""
        if len(self.level.zombie_list) > 0:
            return False
        for i in range(self.level.map_y_len):
            # 魅惑后的僵尸在另一个组里，同样算“还活着”
            if (len(self.level.zombie_groups[i]) > 0 or
                    len(self.level.hypno_zombie_groups[i]) > 0):
                return False
        return True
    
    def checkLose(self):
        """Check if player has lost"""
        for i in range(self.level.map_y_len):
            for zombie in self.level.zombie_groups[i]:
                if zombie.rect.right < 0:
                    return True
        return False

    def checkGameState(self):
        """Check game state and transition if needed"""
        if self.checkVictory():
            self.level.game_info[c.LEVEL_NUM] += 1
            self.level.next = c.GAME_VICTORY
            self.level.done = True
        elif self.checkLose():
            self.level.next = c.GAME_LOSE
            self.level.done = True
