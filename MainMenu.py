from ursina import *

class MenuMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)
        self.main_menu = Entity(parent=self, enabled=True)
        self.options_menu = Entity(parent=self, enabled=False)
        self.help_menu = Entity(parent=self, enabled=False)
        self.background = Sprite('shore', x=1, z=1, color = color.black)

        txt1 = Text("3D Tapper", scale=5.2, font = "OldePixel.ttf", parent=self.main_menu, color = color.random_color(), y=0.3, x=0, origin=(0,0), resolution=1080*Text.size)

        def switch(menu1, menu2):
            menu1.enable()
            menu2.disable()

        ButtonList(button_dict={
            # Insert Coin is where it should switch to the main game, print on screen can be changed/removed
            "Insert    Coin": Func(print_on_screen, "Game Starting..."),
            "Credits": Func(lambda: switch(self.options_menu, self.main_menu)),
            "Controls": Func(lambda: switch(self.help_menu, self.main_menu)),
            "Exit": Func(lambda: application.quit())
        },y=0,parent=self.main_menu, font="OldePixel.ttf", scale = 1.5, x = -.5, resolution=1080*Text.size)


        Text ("Credits: ", parent=self.options_menu, scale=2.0, font='OldePixel.ttf', y=0.4, x=0, origin=(0, 0))
        Text ("Corey  Verkouteren   (Project   Manager)", font='OldePixel.ttf', parent=self.options_menu, y=0.4, x=0, origin=(0, 5))
        Text ("Kaydaince  Lawson   (Design)", font='OldePixel.ttf', parent=self.options_menu, y=0.4, x=0, origin=(0, 9))
        Text ("Jonathan  Carter   (Design,   Developer)", font='OldePixel.ttf', parent=self.options_menu, y=0.4, x=0, origin=(0, 13))
        Text ("Dalton  Ison   (Developer)", font='OldePixel.ttf', parent=self.options_menu, y=0.4, x=0, origin=(0, 17))
        Text ("Dustyn  Bartles   (Developer)", font='OldePixel.ttf', parent=self.options_menu, y=0.4, x=0, origin=(0, 21))


        Button("Back",parent=self.options_menu, font="OldePixel.ttf", y=-0.2,scale=(0.1,0.05),color=rgb(50,50,50),
               on_click=lambda: switch(self.main_menu, self.options_menu))


        Text ("How   to   Play: ", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 0))
        Text ("Customers   will   spawn   randomly   at   one   of   the   three   lanes   ", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 3))
        Text ("Your   Job   is   to   serve   drinks   to   the   demanding   customers   before   "
              "they   get   to   the   end   of   the   lane", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 6))
        Text ("If   they   get   to   the   end   of   the   lane   without   a   drink   you   will   lose   a   life", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 9))
        Text ("You   get   3   lives,   each   drink   served   is   100   points,   Good   Luck!", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 12))
        #Text ("----------------------------------------------", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 15))
        Text ("Controls: ", parent=self.help_menu, font='OldePixel.ttf', y=0.4, x=0, origin=(0, 17))
        Text ("WASD   or   Arrow   Keys   to   move   around", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 20))
        Text ("Space   to   Dash   or   Ctrl   if   using   Arrow   Keys", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 23))
        Text ("Hold   Left   Click   at   a   Tap   to   Fill   Up   Mug", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 26))
        Text ("Right   Click   at   a   Lane   to   Send   the   Mug   to   the   Customer", font='OldePixel.ttf', parent=self.help_menu, y=0.4, x=0, origin=(0, 29))


        Button("Back",parent=self.help_menu, font="OldePixel.ttf", y=-0.4,scale=(0.1,0.05),color=rgb(50,50,50),
               on_click=lambda: switch(self.main_menu, self.help_menu))


        for key, value in kwargs.items ():
            setattr (self, key, value)


    def input(self, key):
        if self.main_menu.enabled and key == "escape":
                application.quit()
        elif self.options_menu.enabled and key == "escape":
            self.main_menu.enable()
            self.options_menu.disable()
        elif self.help_menu.enabled and key == "escape":
            self.main_menu.enable()
            self.help_menu.disable()



    def update(self):
        pass


app = Ursina(title='Main Menu')

main_menu = MenuMenu()

app.run()
