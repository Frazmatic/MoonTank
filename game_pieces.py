"""Game pieces are active objects on the board; those which can move, attack, be destroyed or picked up, etc"""

from math import sin, cos, radians
import json
import pygame
import random

#I wrote:
from coord_math import Coordinates

class Piece:
    """Abstract class representing all active objects on board."""
    piece_count = 0
    #class variable which stores default stats for all pieces, loaded from a json file
    with open("Stats/piece_defaults.json", mode = "r") as f:
        stats_dict = json.loads(f.read())
    
    def __init__(self, coordinates: tuple, category: str):
        self.category = category
        #storing stats in dictionary allows output to file such as JSON, storing & editing outside of code
        #(x, h)
        self.coordinates = coordinates
        #useful for mouse clicks and such
        self.screen_coordinates = (-100, -100)
        #(w, h)
        self.dimensions = (0, 0)
        self.speed = 0
        self.__angle = 0
        self.mass = 0.0
        self.health = 1
        self.image = ""        
        Piece.piece_count += 1
        #this will be used as key for exporting board state to JSON:
        self.id = Piece.piece_count
        self.to_rotate = 0

    @property
    def x(self):
        """Allows dot notation access of x coordinate, implemented for clarity and code concision."""
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    @property
    def width(self):
        return self.dimensions[0]

    @property
    def height(self):
        return self.dimensions[1]

    @property
    def angle(self):
        return self.__angle
    
    @angle.setter
    def angle(self, angle):
        """ensures any update to angle instance variable is bound within 0 to 360 range of values"""
        self.__angle = angle % 360

    ##issue: calling rotate before update() will result in removal from wrong buckets
    ##solution: queue the change; actually call set_angle() during update()
    def rotate(self, rotation_amount = None):
        """Changes piece angle

        Since we're utilizing a spatial hash to store pieces, must not change angle state before update(), or piece will be in wrong buckets.
        This problem is avoided by by storing the change, then processing it during update.
        """
        if rotation_amount != None:
            self.to_rotate = rotation_amount
        else:
            #Having default argument of "None" allows this to act like an 'overloaded' method, for use in self.update()
            self.angle = self.__angle + self.to_rotate
            self.to_rotate = 0

    def move(self):
        """for use in update(), changes piece's coordinates according to piece's angle & speed variable values"""
        self.coordinates = Coordinates.translate(self.coordinates, self.angle, self.speed)       

    def update(self, board) -> None:
        """Called by Board every cycle, updates piece state"""
        board.remove_piece(self)
        self.rotate()
        self.move()
        board.add_piece(self)

    def __str__(self):
        return str(type(self))

class Vehicle(Piece):
    """The basic unit of the game, can move and has components"""
    
    def __init__(self, coordinates: tuple, category: str):
        Piece.__init__(self, coordinates, category)
        self.drag_coefficient = 0
        self.components = []
        self.turret = None
        self.armor = (None, None, None, None)
        self.battery_pack = None
        self.brake_on = False
        self.accel_on = False

        stats = Piece.stats_dict[self.category]
        self.dimensions = stats["dimensions"] 
        self.__mass = stats["mass"]
        self.health = stats["health"]
        self.rotation_speed = stats["rotation_speed"]
        self.image = stats["image"]
        self.battery = stats["battery"]
        self.base_drag = stats["base_drag"]
        self.motor_force = stats["motor_force"]
        self.brake_force = stats["brake_force"]
        self.add_component(Turret(coordinates, stats["turret category"]))

    @property
    def mass(self):
        """Vehicle masses should include mass of components. Allows . notation access while ensuring component masses included"""
        tot_mass = 0
        for c in self.components:
            tot_mass += c.mass
        return self.__mass + tot_mass

    @mass.setter
    def mass(self, mass: float) -> None:
        self.__mass = mass

    def add_component(self, component_item):
        """There are component 'slots' represented by member variables, as well as a list of all components on the vehicle for use in calculations"""
        if isinstance(component_item, Turret):
            #prevent multiple turrets appearing in components list
            if self.turret != None:
                self.remove_component(component_item)
            self.turret = component_item
            
        self.components.append(component_item)  

    def remove_component(self, component_item):
        self.components.remove(component_item)

    def change_speed(self, force = 0):
        """Given a motive force, change speed considering drag/friction & mass

        Will gradually slow to halt due to drag if no force given
        """
        drag_force = self.speed * self.drag_coefficient
        self.speed += (force - drag_force) / self.mass
        #to ensure this doesn't coast forever with very small float value, and that braking doesn't result in reverse:
        if self.speed < 0.01:
            self.speed = 0.0

    def update(self, board):
        Piece.update(self, board)

        #add tile drag
        for t in board.tiles_sh.get_set_for_coordinates(self.coordinates):
            break
        terrain_drag = t.drag
        self.drag_coefficient = self.base_drag + terrain_drag

        #update component positions and state in this section
        if self.turret != None:
            self.turret.coordinates = self.coordinates
            self.turret.update()
                
        #player input buttons will turn brake or accelerator on. If neither on, change_speed input = 0 and will coast to halt.
        #brake force is negative to slow speed down
        self.change_speed((-self.brake_force * self.brake_on) + (self.motor_force * self.accel_on))
        self.accel_on = False
        self.brake_on = False

class Projectile(Piece):
    """Overall weapon ammo type; instances are one of several categories"""
    def __init__(self, coordinates, category):
        Piece.__init__(self, coordinates, category)
       
        self.ammo_cost = 1
        self.cycle_time = 1
        self.damage = 1
        self.speed = 1
        self.life_time = 120

        stats = Piece.stats_dict[self.category]
        self.dimensions = stats["dimensions"]
        self.mass = stats["mass"]
        self.health = stats["health"]
        self.cycle_time = stats["cycle_time"]
        self.damage = stats["damage"]
        self.speed = stats["speed"]
        self.image = stats["image"]
        
    def update(self, board):
        Piece.update(self, board)
        self.life_time -= 1
        if self.life_time <= 0:
            self.health = 0

class Turret(Piece):
    """Basic weapon of the game, should always be attached to a vehicle"""
    def __init__(self, coordinates, category):
        Piece.__init__(self, coordinates, category)
        self.shot_counter = 0

        stats = Piece.stats_dict[self.category]
        self.dimensions = stats["dimensions"]
        self.mass = stats["mass"]
        self.health = stats["health"]
        self.image = stats["image"]
        self.ammo = stats["ammo"]
        self.ammo_type = stats["ammo_type"]

    #non-player turrets ovveride this method
    def update(self, board = None):
        #this section points turret at mouse
        x1, y1 = self.screen_coordinates
        x2, y2 = pygame.mouse.get_pos()
        #screen coordinates are "upside down"
        angle = -Coordinates.get_relative_angle((x1, y1), (x2, y2)) + 180
        self.angle = angle

    def set_ammo_category(self, projectile_class):
        self.ammo_type = projectile_class

    def shoot(self, board):
        """Creates a projectile object, sets to correct angle for turret, adds to board"""
        bullet = Projectile(self.coordinates, self.ammo_type)
        if self.ammo > 0:
            bullet.angle = self.angle
            spawn_length = self.height // 2 + bullet.height // 2 + 1
            bullet.coordinates = Coordinates.translate(bullet.coordinates, bullet.angle, spawn_length)
            board.add_piece(bullet)

class EnemyTurret(Turret):
    """Sub-class of Turret with AI control"""
    def __init__(self, coordinates):
        Turret.__init__(self, coordinates, "EnemyTurret")

        stats = Piece.stats_dict[self.category]
        self.range = stats["range"]
        self.rotation_speed = stats["rotation_speed"]

    def shoot(self, target_coord, board):
        self.shot_counter += 1
        #once have class dictionary for projectile types, can look up using Class method:
        b = Projectile((0,0), self.ammo_type)
        if self.shot_counter % b.cycle_time == 0:
            Turret.shoot(self,board)

    def update(self, board):
        pieces_list = board.get_pieces_in_range(self.coordinates, self.range)  
        for piece in pieces_list:
            if not isinstance(piece, Projectile) and piece is not self:
                 break

        #if len(list) = 1, piece could be irrelevant type; therefore, double check:
        if not isinstance(piece, Projectile) and piece is not self:
            #get_pieces_in_range is sorted by distance to self. Nearest valid piece on board is selected as target:
            target = piece.coordinates
            angle_to_target = Coordinates.get_relative_angle(self.coordinates, target)
            #e.g.: self pointed 90° (right). Azimuth to target is 180° (down). 180° - 90° = 90°; that is, directly to right of self:
            relative_angle = (angle_to_target - self.angle) % 360
            #front:
            if abs(relative_angle) <= 5:
                self.rotate(random.randrange(-5,5 + 1))
                self.shoot(target, board)
            else:
                #left. invervals: (-180°, 0°) and (180°, 360°) are equivalent.
                if (relative_angle < 0 and relative_angle > -180) or (relative_angle > 180 and relative_angle < 360):
                    self.rotate(-self.rotation_speed)
                #right:
                else:
                    self.rotate(self.rotation_speed)
        self.rotate()
        
def main():
    #testing goes here
    p = Projectile((0,0),"BasicBullet")
    print(p.__dict__)
if __name__ == "__main__":
    main()

    
        
        
        
        
        
        
    
        
