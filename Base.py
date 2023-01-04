from ursina import Ursina, window, Entity, EditorCamera, mouse, application, Vec3, held_keys, raycast, camera
from Player import FirstPersonController, Inventory, MugCon

window.vsync = True
app = Ursina()

Entity.default_shader = None

from World import base_floor, FLOOR_TEXTURE, WALL_TEXTURE, tap_holder

base_floor.texture = FLOOR_TEXTURE

table = Entity(model='3D Models/tablemid/tablemid.obj', collider='mesh', position=Vec3(30, .5, 30), scale=(1, .9, 4),
               texture='3D Models/tablemid/texture.png')

p_inventory = Inventory()

player = FirstPersonController(inventory=p_inventory, model='cube', y=5, x=5, origin_y=-.5, speed=10)

p_mug = MugCon(player, p_inventory)

editor_camera = EditorCamera(enabled=False, ignore_paused=True)


def input(key):
    if key == 'escape':
        quit()

    if key == 'p':
        print("working")
        p_inventory.empty_mug()
    if key == 'o':
        p_inventory.delete_mug()

    if key == 'n':
        p_mug.fill()
    if key == "b":
        p_mug.empty()
    if key == 'm':
        p_mug.full()

def update():
    p_mug.update()

    # filling mug with tap interaction
    tap_ray = raycast(camera.world_position, camera.forward, distance=5, traverse_target=tap_holder)
    if mouse.left and tap_ray.hit:
        p_inventory.fill_mug()
    elif (not mouse.left or not tap_ray.hit) and p_inventory.mug == 2:
        p_inventory.empty_mug()

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
