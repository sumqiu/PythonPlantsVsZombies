"""
Plant placement and behavior management
"""
import pygame as pg
from ... import tool
from ... import constants as c
from ...component import plant
from ...component.zombies import playable


class PlantManager:
    def __init__(self, level):
        self.level = level
    
    def _getEnemyZombies(self, zombie_group):
        """Filter out playable zombies and return only enemy zombies"""
        return [z for z in zombie_group if not (hasattr(z, 'is_playable') and z.is_playable)]
    
    def canSeedPlant(self):
        """Check if plant can be placed at mouse position"""
        x, y = pg.mouse.get_pos()
        return self.level.map.showPlant(x, y)
    
    def addPlant(self):
        """Add plant or zombie at current mouse position"""
        pos = self.canSeedPlant()
        if pos is None:
            return

        if self.level.hint_image is None:
            self.setupHintImage()
        
        x, y = self.level.hint_rect.centerx, self.level.hint_rect.bottom
        map_x, map_y = self.level.map.getMapIndex(x, y)
        
        # Check if placing a zombie or plant
        plant_name = self.level.plant_name
        is_zombie = plant_name in [c.BUCKETHEAD_ZOMBIE, c.CONEHEAD_ZOMBIE, c.NORMAL_ZOMBIE]
        
        if is_zombie:
            # Create playable zombie
            new_entity = self._createPlayableZombie(x, y, map_y)
            # Add to zombie group (they attack right)
            self.level.zombie_groups[map_y].add(new_entity)
        else:
            # Create plant
            new_entity = self._createPlant(x, y, map_y)
            
            if new_entity.can_sleep and self.level.background_type == c.BACKGROUND_DAY:
                new_entity.setSleep()
            
            self.level.plant_groups[map_y].add(new_entity)
        
        # Update menubar
        if self.level.bar_type == c.CHOOSEBAR_STATIC:
            self.level.menubar.decreaseSunValue(self.level.select_plant.sun_cost)
            self.level.menubar.setCardFrozenTime(self.level.plant_name)
        else:
            self.level.menubar.deleteCard(self.level.select_plant)

        if self.level.bar_type != c.CHOOSEBAR_BOWLING:
            self.level.map.setMapGridType(map_x, map_y, c.MAP_EXIST)
        
        self.removeMouseImage()
    
    def _createPlant(self, x, y, map_y):
        """Factory method to create plant instances"""
        plant_name = self.level.plant_name
        bg = self.level.bullet_groups

        # 每种植物对应一个无参 lambda，统一调用方式，新增植物只需在此处追加一行
        PLANT_FACTORY = {
            c.SUNFLOWER:         lambda: plant.SunFlower(x, y, self.level.sun_group),
            c.PEASHOOTER:        lambda: plant.PeaShooter(x, y, bg[map_y]),
            c.SNOWPEASHOOTER:    lambda: plant.SnowPeaShooter(x, y, bg[map_y]),
            c.WALLNUT:           lambda: plant.WallNut(x, y),
            c.CHERRYBOMB:        lambda: plant.CherryBomb(x, y),
            c.THREEPEASHOOTER:   lambda: plant.ThreePeaShooter(x, y, bg, map_y),
            c.REPEATERPEA:       lambda: plant.RepeaterPea(x, y, bg[map_y]),
            c.CHOMPER:           lambda: plant.Chomper(x, y),
            c.PUFFSHROOM:        lambda: plant.PuffShroom(x, y, bg[map_y]),
            c.POTATOMINE:        lambda: plant.PotatoMine(x, y),
            c.SQUASH:            lambda: plant.Squash(x, y),
            c.SPIKEWEED:         lambda: plant.Spikeweed(x, y),
            c.JALAPENO:          lambda: plant.Jalapeno(x, y),
            c.SCAREDYSHROOM:     lambda: plant.ScaredyShroom(x, y, bg[map_y]),
            c.SUNSHROOM:         lambda: plant.SunShroom(x, y, self.level.sun_group),
            c.ICESHROOM:         lambda: plant.IceShroom(x, y),
            c.HYPNOSHROOM:       lambda: plant.HypnoShroom(x, y),
            c.WALLNUTBOWLING:    lambda: plant.WallNutBowling(x, y, map_y, self.level),
            c.REDWALLNUTBOWLING: lambda: plant.RedWallNutBowling(x, y),
        }

        factory = PLANT_FACTORY.get(plant_name)
        if factory is None:
            raise ValueError(f"Unknown plant type: {plant_name!r}")
        return factory()

    def _createPlayableZombie(self, x, y, map_y):
        """Factory method to create playable zombie instances"""
        zombie_name = self.level.plant_name

        ZOMBIE_FACTORY = {
            c.BUCKETHEAD_ZOMBIE: lambda: playable.PlayableBucketHeadZombie(x, y, self.level.head_group),
            c.CONEHEAD_ZOMBIE:   lambda: playable.PlayableConeHeadZombie(x, y, self.level.head_group),
            c.NORMAL_ZOMBIE:     lambda: playable.PlayableNormalZombie(x, y, self.level.head_group),
        }

        factory = ZOMBIE_FACTORY.get(zombie_name)
        if factory is None:
            raise ValueError(f"Unknown playable zombie type: {zombie_name!r}")
        return factory()
    
    def setupHintImage(self):
        """Setup hint image for plant placement"""
        pos = self.canSeedPlant()
        if pos and self.level.mouse_image:
            if (self.level.hint_image and pos[0] == self.level.hint_rect.x and
                pos[1] == self.level.hint_rect.y):
                return
            width, height = self.level.mouse_rect.w, self.level.mouse_rect.h
            image = pg.Surface([width, height])
            image.blit(self.level.mouse_image, (0, 0), (0, 0, width, height))
            image.set_colorkey(c.BLACK)
            image.set_alpha(128)
            self.level.hint_image = image
            self.level.hint_rect = image.get_rect()
            self.level.hint_rect.centerx = pos[0]
            self.level.hint_rect.bottom = pos[1]
            self.level.hint_plant = True
        else:
            self.level.hint_plant = False

    def setupMouseImage(self, plant_name, select_plant):
        """Setup mouse cursor image when dragging plant or zombie"""
        # Check if it's a zombie card
        is_zombie = plant_name in [c.BUCKETHEAD_ZOMBIE, c.CONEHEAD_ZOMBIE, c.NORMAL_ZOMBIE]
        
        if is_zombie:
            # Use zombie frames (will be mirrored)
            frame_list = tool.GFX[plant_name]
            if plant_name in tool.ZOMBIE_RECT:
                data = tool.ZOMBIE_RECT[plant_name]
                x = data['x']
            else:
                x = 0
            rect = frame_list[0].get_rect()
            width, height = rect.w - x, rect.h
            
            # Get the zombie image and mirror it
            zombie_image = tool.get_image(frame_list[0], x, 0, width, height, c.BLACK, 1)
            self.level.mouse_image = pg.transform.flip(zombie_image, True, False)
        else:
            # Regular plant
            frame_list = tool.GFX[plant_name]
            if plant_name in tool.PLANT_RECT:
                data = tool.PLANT_RECT[plant_name]
                x, y, width, height = data['x'], data['y'], data['width'], data['height']
            else:
                x, y = 0, 0
                rect = frame_list[0].get_rect()
                width, height = rect.w, rect.h

            if (plant_name == c.POTATOMINE or plant_name == c.SQUASH or
                plant_name == c.SPIKEWEED or plant_name == c.JALAPENO or
                plant_name == c.SCAREDYSHROOM or plant_name == c.SUNSHROOM or
                plant_name == c.ICESHROOM or plant_name == c.HYPNOSHROOM or
                plant_name == c.WALLNUTBOWLING or plant_name == c.REDWALLNUTBOWLING):
                color = c.WHITE
            else:
                color = c.BLACK
            
            self.level.mouse_image = tool.get_image(frame_list[0], x, y, width, height, color, 1)
        
        self.level.mouse_rect = self.level.mouse_image.get_rect()
        pg.mouse.set_visible(False)
        self.level.drag_plant = True
        self.level.plant_name = plant_name
        self.level.select_plant = select_plant

    def removeMouseImage(self):
        """Remove mouse cursor image"""
        pg.mouse.set_visible(True)
        self.level.drag_plant = False
        self.level.mouse_image = None
        self.level.hint_image = None
        self.level.hint_plant = False
    
    def setupShovelCursor(self):
        """Setup shovel cursor for removing plants"""
        pg.mouse.set_visible(False)
        self.level.drag_plant = False
        self.level.shovel_mode = True
        
        # 资源由 menubar.Shovel 负责兜底，这里直接复用同一张图
        self.level.mouse_image = tool.GFX[c.SHOVEL]
        self.level.mouse_rect = self.level.mouse_image.get_rect()
    
    def removeShovelCursor(self):
        """Remove shovel cursor"""
        pg.mouse.set_visible(True)
        self.level.shovel_mode = False
        self.level.mouse_image = None
    
    def removePlantAtPosition(self, mouse_pos):
        """Remove plant at mouse position"""
        x, y = mouse_pos
        map_index = self.level.map.getMapIndex(x, y)
        
        if map_index is None:
            return False
        
        map_x, map_y = map_index
        
        # Check if there's a plant at this position
        for plant_obj in self.level.plant_groups[map_y]:
            plant_rect = plant_obj.rect
            if (x >= plant_rect.x and x <= plant_rect.right and
                y >= plant_rect.y and y <= plant_rect.bottom):
                # Remove the plant
                self.level.entity_manager.killPlant(plant_obj)
                self.level.map.setMapGridType(map_x, map_y, c.MAP_EMPTY)
                return True
        
        return False

    def checkPlant(self, plant, i):
        """Check and update plant behavior based on zombies"""
        # Count only enemy zombies
        zombie_len = len(self._getEnemyZombies(self.level.zombie_groups[i]))
        
        if plant.name == c.THREEPEASHOOTER:
            self._checkThreePeaShooter(plant, i, zombie_len)
        elif plant.name == c.CHOMPER:
            self._checkChomper(plant, i)
        elif plant.name == c.POTATOMINE:
            self._checkPotatoMine(plant, i)
        elif plant.name == c.SQUASH:
            self._checkSquash(plant, i)
        elif plant.name == c.SPIKEWEED:
            self._checkSpikeweed(plant, i)
        elif plant.name == c.SCAREDYSHROOM:
            self._checkScaredyShroom(plant, i)
        elif plant.name in [c.WALLNUTBOWLING, c.REDWALLNUTBOWLING]:
            pass  # Bowling plants don't need behavior checks
        else:
            self._checkNormalPlant(plant, i, zombie_len)

    def _checkThreePeaShooter(self, plant, i, zombie_len):
        """Check ThreePeaShooter behavior"""
        # Count only enemy zombies in each row
        enemy_count_current = len(self._getEnemyZombies(self.level.zombie_groups[i]))
        enemy_count_above = len(self._getEnemyZombies(self.level.zombie_groups[i-1])) if (i-1) >= 0 else 0
        enemy_count_below = len(self._getEnemyZombies(self.level.zombie_groups[i+1])) if (i+1) < self.level.map_y_len else 0
        
        if plant.state == c.IDLE:
            if enemy_count_current > 0 or enemy_count_above > 0 or enemy_count_below > 0:
                plant.setAttack()
        elif plant.state == c.ATTACK:
            if enemy_count_current == 0 and enemy_count_above == 0 and enemy_count_below == 0:
                plant.setIdle()

    def _checkChomper(self, plant, i):
        """Check Chomper behavior"""
        for zombie in self._getEnemyZombies(self.level.zombie_groups[i]):
            if plant.canAttack(zombie):
                plant.setAttack(zombie, self.level.zombie_groups[i])
                break

    def _checkPotatoMine(self, plant, i):
        """Check PotatoMine behavior"""
        for zombie in self._getEnemyZombies(self.level.zombie_groups[i]):
            if plant.canAttack(zombie):
                plant.setAttack()
                break

    def _checkSquash(self, plant, i):
        """Check Squash behavior"""
        for zombie in self._getEnemyZombies(self.level.zombie_groups[i]):
            if plant.canAttack(zombie):
                plant.setAttack(zombie, self.level.zombie_groups[i])
                break

    def _checkSpikeweed(self, plant, i):
        """Check Spikeweed behavior"""
        can_attack = False
        for zombie in self._getEnemyZombies(self.level.zombie_groups[i]):
            if plant.canAttack(zombie):
                can_attack = True
                break
        if plant.state == c.IDLE and can_attack:
            plant.setAttack(self.level.zombie_groups[i])
        elif plant.state == c.ATTACK and not can_attack:
            plant.setIdle()

    def _checkScaredyShroom(self, plant, i):
        """Check ScaredyShroom behavior"""
        need_cry = False
        can_attack = False
        for zombie in self._getEnemyZombies(self.level.zombie_groups[i]):
            if plant.needCry(zombie):
                need_cry = True
                break
            elif plant.canAttack(zombie):
                can_attack = True
        
        if need_cry:
            if plant.state != c.CRY:
                plant.setCry()
        elif can_attack:
            if plant.state != c.ATTACK:
                plant.setAttack()
        elif plant.state != c.IDLE:
            plant.setIdle()

    def _checkNormalPlant(self, plant, i, zombie_len):
        """Check normal plant behavior"""
        can_attack = False
        if zombie_len > 0:
            for zombie in self._getEnemyZombies(self.level.zombie_groups[i]):
                if plant.canAttack(zombie):
                    can_attack = True
                    break
        if can_attack and plant.state == c.IDLE:
            plant.setAttack()
        elif not can_attack and plant.state == c.ATTACK:
            plant.setIdle()

    def checkPlants(self):
        """Check all plants and update their states"""
        for i in range(self.level.map_y_len):
            for plant in self.level.plant_groups[i]:
                if plant.state != c.SLEEP:
                    self.checkPlant(plant, i)
                if plant.health <= 0:
                    self.level.entity_manager.killPlant(plant)
