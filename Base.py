from ursina import Ursina, window, Entity, color, input_handler, EditorCamera, mouse, application, scene, Vec3
from ursina.shaders import lit_with_shadows_shader
from ursina.lights import PointLight
from Player import FirstPersonController

window.vsync = True
app = Ursina()

Entity.default_shader = lit_with_shadows_shader

from World import base_floor, base_walls, FLOOR_TEXTURE, WALL_TEXTURE, ceiling_light_position

base_floor.texture = FLOOR_TEXTURE
for w in base_walls:
    w.texture = FLOOR_TEXTURE

table = Entity(model='cube', collider='cube', position=Vec3(30, 1, 30), scale=(5, 2, 1), texture='floor1.png')

player = FirstPersonController(y=5, x=5, origin_y=-.5, speed=10)

editor_camera = EditorCamera(enabled=False, ignore_paused=True)


def input(key):
    if key == 'escape':
        quit()


def pause_input(key):
    if key == 'tab':  # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled


pause_handler = Entity(ignore_paused=True, input=pause_input)

light_base = Entity()
c_light = PointLight(parent=light_base, position=ceiling_light_position, shadows=True, rotation=(90, 0, 90))

app.run()
