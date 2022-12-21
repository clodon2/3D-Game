from ursina import Entity, invoke


# tap to get root beer from
class Tap(Entity):
    def __init__(self):
        super().__init__(
            model="3D Models/tap/tap.obj",
            texture="3D Models/tap/texture.png",
            scale=.5,
        )
