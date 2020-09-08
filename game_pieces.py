from math import sin, cos, radians
import coord_math
import pygame
import random

class Piece():
    piece_count = 0
    def __init__(self, coordinates):
        #storing stats in dictionary allows output to file such as JSON, storing & editing outside of code
        self.stats = {}
        #(x, h)
        self.stats["coordinates"] = coordinates
        #useful for mouse clicks and such
        self.stats["screen coordinates"] = (-100, -100)
        #(w, h)
        self.stats["dimensions"] = (0, 0) 
        self.stats["angle"] = 0
        self.stats["speed"] = 0
        self.stats["mass"] = 0.0
        self.stats["health"] = 1
        self.stats["image"] = ""        
        Piece.piece_count += 1
        self.stats["id"] = Piece.piece_count
        self.to_rotate = 0

    def get_coordinates(self):
        return self.stats["coordinates"]

    def get_x(self):
        return self.stats["coordinates"][0]

    def get_y(self):
        return self.stats["coordinates"][1]

    def set_coordinates(self, coordinates):
        self.stats["coordinates"] = coordinates

    def get_dimensions(self):
        return self.stats["dimensions"]

    def get_width(self):
        return self.stats["dimensions"][0]

    def get_height(self):
        return self.stats["dimensions"][1]
    
    def get_angle(self):
        return self.stats["angle"]

    def set_angle(self, angle):
        self.stats["angle"] = angle % 360

    ##issue: calling rotate before update() will result in removal from wrong buckets
    ##solution: queue the change; actually call set_angle() during update()
    def rotate(self, rotation_amount = None):
        if rotation_amount != None:
            self.to_rotate = rotation_amount
        else:
            #None default arg overloads the method for use in self.update()
            self.set_angle(self.stats["angle"] + self.to_rotate)
            self.to_rotate = 0

    def get_speed(self):
        return self.stats["speed"]

    def set_speed(self, speed):
        self.stats["speed"] = speed

    def add_speed(self, speed):
        self.stats["speed"] += speed

    def get_mass(self):
        return self.stats["mass"]

    def set_mass(self, mass):
        self.stats["mass"] = mass

    def add_mass(self, mass):
        self.stats["mass"] += mass

    def get_health(self):
        return self.stats["health"]

    def set_health(self, health):
        self.stats["health"] = health

    def add_health(self, health):
        self.stats["health"] += health

    def get_id(self):
        return self.stats["id"]

    def move(self):
        self.set_coordinates(coord_math.translate(self.get_coordinates(), self.get_angle(), self.get_speed()))       

    def update(self, board):
        board.remove_piece(self)
        self.rotate()
        self.move()
        board.add_piece(self)

    def __str__(self):
        return str(type(self))

class Vehicle(Piece):
    
    def __init__(self, coordinates):
        Piece.__init__(self, coordinates)
        self.stats["battery"] = 0
        self.stats["base drag"] = 0
        self.stats["drag coefficient"] = 0
        self.stats["motor force"] = 0
        self.stats["brake force"] = 0
        self.stats["components"] = []
        self.stats["rotation speed"] = 1
        self.turret = None
        self.armor = (None, None, None, None)
        self.battery_pack = None
        self.brake_on = False
        self.accel_on = False

    def get_mass(self):
        #this override includes mass of components for purposes of accell/decell
        tot_mass = 0
        for c in self.get_components():
            tot_mass += c.get_mass()
        return self.stats["mass"] + tot_mass

    def get_battery(self):
        return self.stats["battery"]

    def set_battery(self, battery):
        self.stats["battery"] = battery

    def add_battery(self, battery):
        self.stats["battery"] += battery

    def get_drag_coefficient(self):
        return self.stats["drag coefficient"]

    def set_drag_coefficient(self, drag):
        self.stats["drag coefficient"] = drag

    def add_drag_coefficient(self, drag):
        self.stats["drag coefficient"] += drag

    def get_motor_force(self):
        return self.stats["motor force"] 
        
    def set_motor_force(self):
        return self.stats["motor force"]

    def add_motor_force(self, force):
        self.stats["motor force"] += force

    def get_brake_force(self):
        return self.stats["brake force"]

    def set_brake_force(self, force):
        self.stats["brake force"] = force

    def get_components(self):
        return self.stats["components"]

    def add_component(self, component_item):
        if isinstance(component_item, Turret):
            self.turret = component_item
        self.stats["components"].append(component_item)  

    def remove_component(self, component_item):
        self.stats["components"].remove(component_item)

    def change_speed(self, force = 0):
        drag_force = self.get_speed() * self.get_drag_coefficient()
        self.add_speed((force - drag_force) / self.get_mass())
        #will coast very slowly forever otherwise (because of floating point precision)
        #also ensures brake doesn't reverse
        if self.get_speed() < 0.01:
            self.set_speed(0.0)

    def update(self, board):
        Piece.update(self, board)

        #add tile drag (I should reformat tiles so it's not a movement_speed mod, it's an added drag)
        for t in board.tiles_sh.get_set_for_coordinates(self.get_coordinates()):
            break
        terrain_drag = t.stats["drag"]
        self.stats["drag coefficient"] = self.stats["base drag"] + terrain_drag

        #update component positions
        if self.turret != None:
            self.turret.set_coordinates(self.get_coordinates())
            self.turret.update()
                
        #player input buttons will turn brake or accelerator on. If neither on, change_speed input = 0 and will coast to halt.
        #brake force is negative to slow speed down
        self.change_speed(-self.get_brake_force() * self.brake_on + self.get_motor_force() * self.accel_on)
        self.accel_on = False
        self.brake_on = False


class Projectile(Piece):
    def __init__(self, coordinates, category):
        Piece.__init__(self, coordinates)
        self.stats["category"] = category
        self.stats["ammo cost"] = 1
        self.stats["cycle time"] = 1
        self.stats["damage"] = 1
        self.stats["speed"] = 1
        self.stats["life time"] = 120

    def update(self, board):
        Piece.update(self, board)
        self.stats["life time"] -= 1
        if self.stats["life time"] <= 0:
            self.stats["health"] = 0

class Component(Piece):
    def __init__(self, coordinates, category):
        Piece.__init__(self, coordinates)
        self.stats["category"] = category

class Turret(Component):
    def __init__(self, coordinates):
        Component.__init__(self, coordinates, "Turret")
        self.stats["ammo"] = 0
        self.ammo_type = Projectile
        self.shot_counter = 0

    #will override this for non-player turrets
    def update(self, board = None):
        #this section points turret at mouse
        x1, y1 = self.stats["screen coordinates"]
        x2, y2 = pygame.mouse.get_pos()
        #screen coordinates are "upside down"
        angle = -coord_math.get_relative_angle((x1, y1), (x2, y2)) + 180
        self.set_angle(angle)

    def set_ammo_category(self, projectile_class):
        self.ammo_type = projectile_class

    def shoot(self, board):
        bullet = self.ammo_type(self.get_coordinates())
        if self.stats["ammo"] > 0:
            bullet.set_angle(self.get_angle())
            spawn_length = self.get_dimensions()[1]//2 + bullet.get_dimensions()[1]//2 + 1
            bullet.set_coordinates((coord_math.translate(bullet.get_coordinates(), bullet.get_angle(), spawn_length)))
            board.add_piece(bullet)

class BasicBullet(Projectile):
    def __init__(self, coordinates):
        Projectile.__init__(self, coordinates, "BasicBullet")
        self.stats["speed"] = 10
        self.stats["dimensions"] = (3, 3) 
        self.stats["angle"] = 0
        self.stats["mass"] = 1.0
        self.stats["health"] = 1
        self.stats["image"] = "Images/Projectile/basic_bullet.bmp"
        self.stats["cycle time"] = 5
        self.stats["damage"] = 2
        
class BasicTurret(Turret):
    def __init__(self, coordinates):
        Turret.__init__(self, coordinates)
        self.stats["dimensions"] = (13, 25) 
        self.stats["angle"] = 0
        self.stats["speed"] = 0
        self.stats["mass"] = 30.0
        self.stats["health"] = 100
        self.stats["image"] = "Images/Components/basic_turret.bmp"
        self.stats["ammo"] = 300
        self.ammo_type = BasicBullet
        
class BasicVehicle(Vehicle):
    def __init__(self, coordinates):
        Vehicle.__init__(self, coordinates)
        self.add_component(BasicTurret(coordinates))
        self.stats["dimensions"] = (25, 25) 
        self.stats["angle"] = 0
        self.stats["speed"] = 0
        self.stats["mass"] = 30.0
        self.stats["health"] = 100
        self.stats["rotation speed"] = 3
        self.stats["image"] = "Images/Vehicles/basic_vehicle.bmp"
        self.stats["battery"] = 1500
        self.stats["base drag"] = 0.75
        self.stats["motor force"] = 2
        self.stats["brake force"] = 2

class EnemyTurret(Turret):
    def __init__(self, coordinates):
        Turret.__init__(self, coordinates)
        self.stats["dimensions"] = (13, 25) 
        self.stats["angle"] = 0
        self.stats["speed"] = 0
        self.stats["mass"] = 5
        self.stats["health"] = 10
        self.stats["image"] = "Images/Components/basic_turret.bmp"
        self.stats["ammo"] = 300
        self.stats["range"] = 300
        self.stats["rotation speed"] = 2
        self.ammo_type = BasicBullet

    def shoot(self, target_coord, board):
        self.shot_counter += 1
        b = self.ammo_type((0,0))
        if self.shot_counter % b.stats["cycle time"] == 0:
            Turret.shoot(self,board)

    def update(self, board):
        pieces_list = board.get_pieces_in_range(self.get_coordinates(), self.stats["range"])  
        for piece in pieces_list:
            if not isinstance(piece, Projectile) and piece is not self:
                 break
        #need to check this again because if there's only one item in list, piece will be that item
        if not isinstance(piece, Projectile) and piece is not self:
            target = piece.get_coordinates()
            angle_to_target = coord_math.get_relative_angle(self.get_coordinates(), target)
            relative_angle = (angle_to_target - self.get_angle()) % 360
            if abs(relative_angle) <= 5:
                #self.set_angle(angle_to_target)
                self.rotate(random.randrange(-5,5 + 1))
                self.shoot(target, board)
            else:
                if (relative_angle < 0 and relative_angle > -180) or (relative_angle > 180 and relative_angle < 360):
                    self.rotate(-self.stats["rotation speed"])
                else:
                    self.rotate(self.stats["rotation speed"])
        self.rotate()
def main():
    #testing goes here
    pass
if __name__ == "__main__":
    main()

    
        
        
        
        
        
        
    
        
