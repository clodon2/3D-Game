# sets up world environment, all map entities should be spawned in here

from ursina import Entity, color, Vec3
from World_Objects import Tap, Table

# floor characteristics (base for room)
FLOOR_CHUNKS = 10
FLOOR_LENGTH = 10
FLOOR_WIDTH = 10
CHUNK_SIZE_X = 10
FLOOR_Y = 0
CHUNK_SIZE_Z = 5

FLOOR_POSITION = (0, FLOOR_Y, 0)

FLOOR_TEXTURE = "Textures/hardwood.jpg"

# updates to fit floor
WALL_HEIGHT = 3
X_WALL_LENGTH = FLOOR_LENGTH
Z_WALL_LENGTH = FLOOR_WIDTH
WALL_THICKNESS = 1

WALL_TEXTURE = "Textures/Brick.jpg"

base_floor = Entity(model=None, collider=None)

base_wall_x1 = Entity(model=None, collider=None)
base_wall_x2 = Entity(model=None, collider=None)
base_wall_z1 = Entity(model=None, collider=None)
base_wall_z2 = Entity(model=None, collider=None)

base_walls = [base_wall_x1, base_wall_x2, base_wall_z1, base_wall_z2]

for w in range(FLOOR_WIDTH):
    for l in range(FLOOR_LENGTH):
        # floor
        new_floor_chunk = Entity(model='cube', color=color.gray, scale=(CHUNK_SIZE_X, 1, CHUNK_SIZE_Z))
        new_floor_chunk.x = w * CHUNK_SIZE_X + FLOOR_POSITION[0]
        new_floor_chunk.z = l * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_floor_chunk.y = FLOOR_Y
        new_floor_chunk.parent = base_floor


base_floor.combine()
base_floor.collider = 'mesh'

for w in base_walls:
    w.combine()
    w.collider = 'mesh'

# light
ceiling_light_x = FLOOR_POSITION[0] + (CHUNK_SIZE_X*(FLOOR_WIDTH/2))
ceiling_light_z = FLOOR_POSITION[2] + (CHUNK_SIZE_Z*(FLOOR_LENGTH/2))
ceiling_light_y = FLOOR_POSITION[1] + WALL_HEIGHT*CHUNK_SIZE_Z
ceiling_light_position = Vec3(ceiling_light_x, ceiling_light_y, ceiling_light_z)

# taps, tap holder can be used to refernce all taps
tap_holder = Entity()
tap1 = Tap()
tap2 = Tap()
tap3 = Tap()

tap1.parent = tap_holder
tap2.parent = tap_holder
tap3.parent = tap_holder

# positions taps for map
for tap in tap_holder.children:
    tap.rotation_y = 180
    tap.y = 1
    tap.z = 2

tap2.x = 20
tap3.x = 40

# tables customers move along and mugs spawn on

table1 = Table(size=7, position=(0, 0, 10))
table2 = Table(size=7, position=(20, 0, 10))
table3 = Table(size=7, position=(40, 0, 10))
