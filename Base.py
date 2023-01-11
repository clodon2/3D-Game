# 3D Root-Beer Tapper
# this file is currently being used to handle all base game needs, and the entire game,
# it should be made into a separate file at some point to enable menu support


from ursina import Ursina, window, Entity, EditorCamera, mouse, application, Vec3, held_keys, raycast, camera, destroy, \
    invoke, Audio
from Player import FirstPersonController, Inventory, MugCon
from random import choice

window.vsync = True
app = Ursina()

Entity.default_shader = None

# world stuff
from World_Objects import Customer, TableMug, MugCustomerHandler
from World import base_floor, FLOOR_TEXTURE, tap_holder, table1, table2, table3

# bar tables which customers move along and mugs spawn on
tables = [table1, table2, table3]

# setting floor texture
base_floor.texture = FLOOR_TEXTURE

# player stuff
p_inventory = Inventory()

# player
player = FirstPersonController(inventory=p_inventory, model='cube', y=5, x=5, origin_y=-.5, speed=10)

# display mug
p_mug = MugCon(player, p_inventory)

# editor cam, used on spawn (depricated)
editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# other stuff
# holds sent mugs, given to mug-customer handler
cur_mugs = []
# holds customers, given to mug-customer handler
cur_customers = []

# handles mug-customer collisions and deletion
mug_cust_collisions = MugCustomerHandler(cur_mugs, cur_customers, player)

# SOUNDS (wont work when in another file)

drink_sound = Audio("Sounds/drink.mp3", autoplay=False)
mug_fill_sound = Audio("Sounds/pouring_1.mp3", autoplay=False, volume=2)
bg_music = Audio("Sounds/bg-song.mp3", autoplay=True, loops=10000000)
dash_sound = Audio("Sounds/dash.mp3", autoplay=False, volume=2)


# begins a recurring event (spawning customers in)
class SpawnCustomer:
    def __init__(self, event_start_delay=5, event_delay=4):
        self.event_start_delay = event_start_delay
        self.event_delay = event_delay
        self.spawn_list = [(3, 2, 40), (23, 2, 40), (43, 2, 40)]

    def start_event(self):
        invoke(self.execute_event, delay=self.event_start_delay)

    def event_cooldown(self):
        invoke(self.execute_event, delay=self.event_delay)

    def execute_event(self):
        g = Customer(choice(self.spawn_list))
        cur_customers.append(g)
        invoke(self.event_cooldown, delay=0)


# start spawner
c_spawner = SpawnCustomer()
c_spawner.start_event()


# handle inputs (l click in updates)
def input(key):
    # FINAL INPUTS
    if key == 'escape':
        quit()

    # sends mug down table if right clicked on
    if key == "right mouse down":
        table_ray = raycast(camera.world_position, camera.forward, distance=5)
        table = table_ray.entity
        try:
            if p_inventory.mug == 3 and table.parent in tables:
                sent_mug = TableMug(position=(table.x, (table.y + 1.2), table.z))
                cur_mugs.append(sent_mug)
                p_inventory.delete_mug()
        except:
            pass

    # plays dash sound if player dashes
    if key == "space" and not player.dashing:
        dash_sound.play()

    # DEV INPUTS
    # spawn in empty inv mug
    if key == 'p':
        print("working")
        p_inventory.empty_mug()
    # delete cur mug in hand (may be needed in final release)
    if key == 'o':
        p_inventory.delete_mug()
    # spawns in a customer at first table (depricated)
    if key == 'b':
        g = Customer(position=(3, 2, 25))
        cur_customers.append(g)
    # sound tests
    if key == "l":
        mug_fill_sound.play()


# updates for each frame (i think)
def update():
    # updated display mug
    p_mug.update()
    # updates collisions between sent mugs and customers
    mug_cust_collisions.update()

    # filling display mug with tap interaction
    # left click input use
    tap_ray = raycast(camera.world_position, camera.forward, distance=5, traverse_target=tap_holder)
    if mouse.left and tap_ray.hit:
        if p_inventory.mug == 0:
            p_inventory.empty_mug()
        if not mug_fill_sound.status == 2:
            mug_fill_sound.play()
        p_inventory.fill_mug()
    elif (not mouse.left or not tap_ray.hit) and p_inventory.mug == 2:
        print("L")
        p_mug.filling_mug.current_frame = 0
        if mug_fill_sound.status == 2:
            mug_fill_sound.stop(destroy=True)
        p_inventory.delete_mug()
    if p_inventory.mug == 3 and mug_fill_sound.status == 2:
        mug_fill_sound.stop()


# inputs used when game is paused
def pause_input(key):
    if key == 'tab':  # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled


pause_handler = Entity(ignore_paused=True, input=pause_input)

app.run()
