from ursina import Ursina
from Main_menu import MenuMenu
from Main_Game import MainGame


def start():
    menu.stop()
    game = MainGame()


app = Ursina(title='Main Menu')

menu = MenuMenu(start_fun=start)

app.run()
