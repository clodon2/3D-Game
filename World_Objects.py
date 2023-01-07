# used to store entity classes used in the world

from ursina import Entity, invoke, Text, destroy

# text used in entity tooltips
Text.default_resolution = 1080 * Text.size


# tap to get root beer from
class Tap(Entity):
    def __init__(self):
        # sets up basic attributes
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


# creates a full table
class Table(Entity):
    def __init__(self, size=3, position=(0, 0, 0), parent=None):
        super().__init__(parent=parent)

        for i in range(size):
            # spawns the end of the table
            if i == 0:
                Entity(model="3D Models/tableend/tableend.obj", texture="3D Models/tableend/texture.png",
                       collider='mesh', parent=self, y=(.6 + position[1]), z=position[2], x=position[0],
                       scale=(.7, .9, 1))
            # spawns in all subsequent pieces of the table
            else:
                Entity(model="3D Models/tablemid/tablemid.obj", texture="3D Models/tablemid/texture.png",
                       collider='mesh', parent=self, y=(.6 + position[1]), z=((4.1*i) + position[2]), x=position[0],
                       scale=(.7, .9, 1))


class Customer(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position, model='cube', scale=(1, 4, 1))
        # hand is used to detect a mug
        self.hand = Entity(model='cube', parent=self, scale=(2.2, .5, 1), collider='box')
        self.hand.x -= 3
        self.hand.y += .3

    def update(self):
        # moves toward end of table
        self.z -= .05


# sent mug entities
class TableMug(Entity):
    def __init__(self, position):
        super().__init__(model="3D Models/mug/mug.obj", texture="3d Models/mug/mugtexture.png", scale=4,
                         position=position, rotation=(0, 180, 0), collider='box')

    def update(self):
        # moves toward customer spawn at tables
        self.z += .3


# handes mug-customer collisions andd deletions
class MugCustomerHandler:
    def __init__(self, mugs, customers):
        # lists of sent mugs and customers
        self.mugs = mugs
        self.customers = customers

    def update(self):
        # prevents customers from moving past the table
        for customer in self.customers:
            if customer.z <= 10:
                self.customers.remove(customer)
                destroy(customer.hand)
                destroy(customer)

        # prevents mugs from moving past the table
        for mug in self.mugs:
            if mug.z >= 30:
                destroy(mug)
                self.mugs.remove(mug)

        for mug in self.mugs:
            # gets entities intersecting the mugs
            mug_collider = mug.intersects()
            ent_collide = mug_collider.entity

            # kills mug and customer if they collide
            for customer in self.customers:
                if ent_collide == customer.hand:
                    self.customers.remove(ent_collide.parent)
                    self.mugs.remove(mug)
                    destroy(mug)
                    destroy(ent_collide.parent)
                    destroy(ent_collide)

