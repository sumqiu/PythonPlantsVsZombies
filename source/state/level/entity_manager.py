"""
Entity management - plants, zombies, bullets, etc.
"""
import pygame as pg
from ... import tool
from ... import constants as c
from ...component import plant, zombie


class EntityManager:
    def __init__(self, level):
        self.level = level
    
    def setupGroups(self):
        """Initialize all sprite groups"""
        self.level.sun_group = pg.sprite.Group()
        self.level.head_group = pg.sprite.Group()

        self.level.plant_groups = []
        self.level.zombie_groups = []
        self.level.hypno_zombie_groups = []
        self.level.bullet_groups = []
        for i in range(self.level.map_y_len):
            self.level.plant_groups.append(pg.sprite.Group())
            self.level.zombie_groups.append(pg.sprite.Group())
            self.level.hypno_zombie_groups.append(pg.sprite.Group())
            self.level.bullet_groups.append(pg.sprite.Group())
    
    def setupZombies(self):
        """Setup zombie spawn list"""
        def takeTime(element):
            return element[0]

        self.level.zombie_list = []
        for data in self.level.map_data[c.ZOMBIE_LIST]:
            self.level.zombie_list.append((data['time'], data['name'], data['map_y']))
        self.level.zombie_start_time = 0
        self.level.zombie_list.sort(key=takeTime)

    def setupCars(self):
        """Setup lawn mowers"""
        self.level.cars = []
        for i in range(self.level.map_y_len):
            _, y = self.level.map.getMapGridPos(0, i)
            self.level.cars.append(plant.Car(-25, y+20, i))

    def initBowlingMap(self):
        """Initialize bowling mode map"""
        for x in range(3, self.level.map.width):
            for y in range(self.level.map.height):
                self.level.map.setMapGridType(x, y, c.MAP_EXIST)

    def createZombie(self, name, map_y):
        """Create a zombie at specified position"""
        x, y = self.level.map.getMapGridPos(0, map_y)
        if name == c.NORMAL_ZOMBIE:
            self.level.zombie_groups[map_y].add(zombie.NormalZombie(c.ZOMBIE_START_X, y, self.level.head_group))
        elif name == c.CONEHEAD_ZOMBIE:
            self.level.zombie_groups[map_y].add(zombie.ConeHeadZombie(c.ZOMBIE_START_X, y, self.level.head_group))
        elif name == c.BUCKETHEAD_ZOMBIE:
            self.level.zombie_groups[map_y].add(zombie.BucketHeadZombie(c.ZOMBIE_START_X, y, self.level.head_group))
        elif name == c.FLAG_ZOMBIE:
            self.level.zombie_groups[map_y].add(zombie.FlagZombie(c.ZOMBIE_START_X, y, self.level.head_group))
        elif name == c.NEWSPAPER_ZOMBIE:
            self.level.zombie_groups[map_y].add(zombie.NewspaperZombie(c.ZOMBIE_START_X, y, self.level.head_group))

    def updateEntities(self):
        """Update all entities"""
        # Spawn zombies
        if self.level.zombie_start_time == 0:
            self.level.zombie_start_time = self.level.current_time
        elif len(self.level.zombie_list) > 0:
            data = self.level.zombie_list[0]
            if data[0] <= (self.level.current_time - self.level.zombie_start_time):
                self.createZombie(data[1], data[2])
                self.level.zombie_list.remove(data)

        # Update all sprite groups
        for i in range(self.level.map_y_len):
            self.level.bullet_groups[i].update(self.level.game_info)
            self.level.plant_groups[i].update(self.level.game_info)
            self.level.zombie_groups[i].update(self.level.game_info)
            self.level.hypno_zombie_groups[i].update(self.level.game_info)
            
            # Remove hypno zombies that moved off screen (to the right)
            for zombie in self.level.hypno_zombie_groups[i]:
                if zombie.rect.x > c.SCREEN_WIDTH:
                    zombie.kill()
            
            # Remove playable zombies that moved off screen (to the right)
            for zombie in list(self.level.zombie_groups[i]):
                if hasattr(zombie, 'is_playable') and zombie.is_playable:
                    if zombie.rect.x > c.SCREEN_WIDTH:
                        zombie.kill()

        self.level.head_group.update(self.level.game_info)
        self.level.sun_group.update(self.level.game_info)
        
        # Update cars
        for car in self.level.cars:
            car.update(self.level.game_info)

    def boomZombies(self, x, map_y, y_range, x_range):
        """Explode zombies in range"""
        for i in range(self.level.map_y_len):
            if abs(i - map_y) > y_range:
                continue
            for zombie in self.level.zombie_groups[i]:
                if abs(zombie.rect.centerx - x) <= x_range:
                    zombie.setBoomDie()

    def freezeZombies(self, plant):
        """Freeze all zombies on screen"""
        for i in range(self.level.map_y_len):
            for zombie in self.level.zombie_groups[i]:
                if zombie.rect.centerx < c.SCREEN_WIDTH:
                    zombie.setFreeze(plant.trap_frames[0])

    def killPlant(self, plant):
        """Remove plant and handle special effects"""
        x, y = plant.getPosition()
        map_x, map_y = self.level.map.getMapIndex(x, y)
        if self.level.bar_type != c.CHOOSEBAR_BOWLING:
            self.level.map.setMapGridType(map_x, map_y, c.MAP_EMPTY)
        
        if (plant.name == c.CHERRYBOMB or plant.name == c.JALAPENO or
            (plant.name == c.POTATOMINE and not plant.is_init) or
            plant.name == c.REDWALLNUTBOWLING):
            self.boomZombies(plant.rect.centerx, map_y, plant.explode_y_range,
                            plant.explode_x_range)
        elif plant.name == c.ICESHROOM and plant.state != c.SLEEP:
            self.freezeZombies(plant)
        elif plant.name == c.HYPNOSHROOM and plant.state != c.SLEEP and plant.kill_zombie is not None:
            # 啃到它的僵尸必然在同一行（碰撞检测就是按行做的），
            # 所以直接复用上面算好的 map_y，不要按僵尸坐标重算（可能越界）。
            zombie = plant.kill_zombie
            zombie.setHypno()
            self.level.zombie_groups[map_y].remove(zombie)
            self.level.hypno_zombie_groups[map_y].add(zombie)
        plant.kill()
