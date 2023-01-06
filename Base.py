from ursina import Ursina, window, Entity, EditorCamera, mouse, application, Vec3, held_keys, raycast, camera, destroy, \
    invoke
from Player import FirstPersonController, Inventory, MugCon
from random import choice

window.vsync = True
app = Ursina()

Entity.default_shader = None

# world stuff
from World_Objects import Customer, TableMug, MugCustomerHandler
from World import base_floor, FLOOR_TEXTURE, tap_holder, table1, table2, table3

tables = [table1, table2, table3]

base_floor.texture = FLOOR_TEXTURE

# player stuff
p_inventory = Inventory()

player = FirstPersonController(inventory=p_inventory, model='cube', y=5, x=5, origin_y=-.5, speed=10)

p_mug = MugCon(player, p_inventory)

editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# other stuff
cur_mugs = []
cur_customers = []

mug_cust_collisions = MugCustomerHandler(cur_mugs, cur_customers)


class SpawnCustomer:
    def __init__(self, time):
        self.time = time
        self.spawn_list = [(3, 2, 30), (23, 2, 30), (43, 2, 30)]

    def start_event(self):
        self.time = self.time
        invoke(self.execute_event, delay=self.time)

    def execute_event(self):
        g = Customer(choice(self.spawn_list))
        cur_customers.append(g)
        invoke(self.start_event, delay=0)


c_spawner = SpawnCustomer(5)
c_spawner.start_event()


def input(key):
    if key == 'escape':
        quit()

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

    if key == 'p':
        print("working")
        p_inventory.empty_mug()
    if key == 'o':
        p_inventory.delete_mug()

    if key == 'b':
        g = Customer(position=(3, 2, 25))
        cur_customers.append(g)


def update():
    p_mug.update()
    mug_cust_collisions.update()

    # filling mug with tap interaction
    tap_ray = raycast(camera.world_position, camera.forward, distance=5, traverse_target=tap_holder)
    if mouse.left and tap_ray.hit:
        if p_inventory.mug == 0:
            p_inventory.empty_mug()
        p_inventory.fill_mug()
    elif (not mouse.left or not tap_ray.hit) and p_inventory.mug == 2:
        p_inventory.delete_mug()



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
