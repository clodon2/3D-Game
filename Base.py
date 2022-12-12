from ursina import Ursina, window, Entity, color, input_handler, EditorCamera, mouse, application
from Player import FirstPersonController
from World import base_floor, base_walls, FLOOR_TEXTURE, WALL_TEXTURE

window.vsync = True
app = Ursina()

base_floor.texture = FLOOR_TEXTURE
for w in base_walls:
    w.texture = FLOOR_TEXTURE

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

app.run()