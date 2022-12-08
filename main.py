import panda3d.core
import ursina
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader

app = Ursina()

random.seed(0)

ground = Entity(model='cube', collider='box', scale=(64, 1, 64), texture='Textures/floor1.png', texture_scale=(4,4))
tester = Entity(model='sphere', collider='box', scale=2, texture="grass")

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=10, color=color.orange, origin_y=-.5, speed=8)
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

Sky(color=color.black)


def input(key):
    if key == "g":
        print(scene.fog.getLinearOnsetPoint())
        print(scene.fog.get_linear_onset_point())


def pause_input(key):
    if key == "escape":
        quit()
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

        
scene.fog_density = .05
scene.fog_color = color.blue
        

pause_handler = Entity(ignore_paused=True, input=pause_input)

app.run()
