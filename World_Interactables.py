from ursina import Entity, invoke, Text

Text.default_resolution = 1080 * Text.size


# tap to get root beer from
class Tap(Entity):
    def __init__(self):
        super().__init__(
            model="3D Models/tap/tap.obj",
            texture="3D Models/tap/texture.png",
            collider='mesh',
            scale=.5,
        )
        self.tooltip = Text(text='Hold Left Click To Fill', wordwrap=30, enabled=False)

    def update(self):
        # shows instruction text
        if self.hovered:
            self.tooltip.enabled = True
        elif not self.hovered and self.tooltip.enabled:
            self.tooltip.enabled = False
