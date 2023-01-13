# used to store entity classes used in the world

from ursina import Entity, invoke, Text, destroy, Animator, FrameAnimation3d, color

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

        self.tooltip = Text(text='Right Click To Send Drink', wordwrap=30, enabled=False)

        for i in range(size):
            # spawns the end of the table
            if i == 0:
                Entity(model="3D Models/tableend/tableend.obj", texture="3D Models/tableend/texture.png",
                       collider='box', parent=self, y=(.6 + position[1]), z=position[2], x=position[0],
                       scale=(.7, .9, 1))
            # spawns in all subsequent pieces of the table
            else:
                Entity(model="3D Models/tablemid/tablemid.obj", texture="3D Models/tablemid/texture.png",
                       collider='box', parent=self, y=(.6 + position[1]), z=((4.1*i) + position[2]), x=position[0],
                       scale=(.7, .9, 1))

    def update(self):
        hover_list = []
        for e in self.children:
            hover_list.append(e.hovered)
        if True in hover_list and not self.tooltip.enabled:
            self.tooltip.enabled = True
        elif True not in hover_list and self.tooltip.enabled:
            self.tooltip.enabled = False


class Doorway(Entity):
    def __init__(self, position):
        super().__init__(model="3D Models/door/Dooropen.obj", texture="3D Models/door/texture.png", position=position,
                         rotation=(0, 180, 0))


class Customer(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position, model='cube', scale=(1, 4, 1), visible_self=False)
        self.display_model = CustomerAnimator(self)
        # hand is used to detect a mug
        self.hand = Entity(model='cube', parent=self, scale=(2.2, .5, 1), collider='box', visible_self=False)
        self.hand.x -= 3
        self.hand.y += .3

        self.direction = 1

        # display model stuff
        self.drinking = False
        self.angry = False
        self.drink_time = 1

    def update(self):
        # moves toward end of table
        self.z -= .05 * self.direction

        # display model updates
        if self.angry:
            self.display_model.state = "mad"
        elif self.direction == 0 and not self.drinking:
            self.display_model.state = "idle"
        elif self.direction == 0 and self.drinking:
            self.display_model.state = "drink"
        elif self.direction == 1:
            self.display_model.state = "walk forward"
        elif self.direction == -1:
            self.display_model.state = "walk backward"

    def turn_around(self):
        if self.direction == 0:
            self.direction = 1
            self.drinking = False
        self.direction *= -1

    def walk_forward(self):
        self.direction = 1
        self.drinking = False

    def walk_backward(self):
        self.direction = -1
        self.drinking = False

    def idle(self):
        self.direction = 0
        self.drinking = False

    def drink(self):
        self.direction = 0
        self.drinking = True
        invoke(self.walk_backward, delay=self.drink_time)

    def mad(self):
        self.direction = 0
        self.angry = True
        destroy(self, 1)


class CustomerAnimator(Animator):
    def __init__(self, parent):

        self.idle = Entity(model='cube', scale=(1, 1, 1), parent=parent)
        self.walk_forward = Entity(model='cube', scale=(1, 1, 1), color=color.red, parent=parent)
        self.walk_backward = Entity(model='cube', scale=(1, 1, 1), color=color.green, parent=parent)
        self.drink = Entity(model='cube', scale=(1, 1, 1), color=color.yellow, parent=parent)
        self.mad = Entity(model='cube', scale=(1, 1, 1), color=color.black, parent=parent)

        super().__init__(animations={
            "idle": self.idle,
            "walk forward": self.walk_forward,
            "walk backward": self.walk_backward,
            "drink": self.drink,
            "mad": self.mad
        })

        self.state = "walk forward"


# sent mug entities
class TableMug(Entity):
    def __init__(self, position):
        super().__init__(model="3D Models/mug/mug_fill_anim/mug_10.obj", texture="3d Models/mug/mug_fill_anim/texture_02.png", scale=1,
                         position=position, rotation=(0, 180, 0), collider='box')

    def update(self):
        # moves toward customer spawn at tables
        self.z += .3


# handles mug-customer collisions and deletions
class MugCustomerHandler:
    def __init__(self, mugs, customers, player):
        # lists of sent mugs and customers
        self.mugs = mugs
        self.customers = customers
        self.player = player

    def update(self):
        # prevents customers from moving past the table
        for customer in self.customers:
            if customer.z <= 10:
                customer.mad()
                self.customers.remove(customer)
                self.player.lives -= 1

        for customer in self.customers:
            if customer.z >= 40:
                self.customers.remove(customer)
                destroy(customer)

        # prevents mugs from moving past the table
        for mug in self.mugs:
            if mug.z >= 40:
                destroy(mug)
                self.mugs.remove(mug)

        for mug in self.mugs:
            # gets entities intersecting the mugs
            mug_collider = mug.intersects()
            ent_collide = mug_collider.entity

            # kills mug and customer if they collide
            for customer in self.customers:
                if ent_collide == customer.hand and ent_collide.parent.direction == 1:
                    self.player.score += 100
                    self.mugs.remove(mug)
                    destroy(mug)
                    ent_collide.parent.drink()

