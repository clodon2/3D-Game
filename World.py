from ursina import Entity, color, Vec3

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

# Z Walls
for h in range(WALL_HEIGHT):
    for w in range(Z_WALL_LENGTH):
        new_zwall_chunk = Entity(model='cube', color=color.black, scale=(CHUNK_SIZE_X, CHUNK_SIZE_Z, 1))
        new_zwall_chunk.x = w * CHUNK_SIZE_X + FLOOR_POSITION[0]
        new_zwall_chunk.z = FLOOR_POSITION[2] - CHUNK_SIZE_Z / 2
        new_zwall_chunk.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_zwall_chunk.parent = base_wall_z1

        new_zwall_chunk2 = Entity(model='cube', color=color.black, scale=(CHUNK_SIZE_X, CHUNK_SIZE_Z, 1))
        new_zwall_chunk2.x = w * CHUNK_SIZE_X + FLOOR_POSITION[0]
        new_zwall_chunk2.z = FLOOR_POSITION[2] + (FLOOR_LENGTH * CHUNK_SIZE_Z) - CHUNK_SIZE_Z / 2
        new_zwall_chunk2.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_zwall_chunk2.parent = base_wall_z2

# X Walls
for h in range(WALL_HEIGHT):
    for w in range(X_WALL_LENGTH):
        new_xwall_chunk = Entity(model='cube', color=color.black, scale=(1, CHUNK_SIZE_Z, CHUNK_SIZE_Z))
        new_xwall_chunk.x = FLOOR_POSITION[0] - CHUNK_SIZE_Z / 2
        new_xwall_chunk.z = w * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_xwall_chunk.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_xwall_chunk.parent = base_wall_x1

        new_xwall_chunk2 = Entity(model='cube', color=color.black, scale=(1, CHUNK_SIZE_Z, CHUNK_SIZE_Z))
        new_xwall_chunk2.x = FLOOR_POSITION[0] + (FLOOR_WIDTH * CHUNK_SIZE_X) - CHUNK_SIZE_X / 2
        new_xwall_chunk2.z = w * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_xwall_chunk2.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_xwall_chunk2.parent = base_wall_x2

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
