from Submenu import submenu
from Submenu import Submenu
from Menu import Menu


@submenu(label='main_menu')
def main_menu(self):
    print(f"This is the main menu")
    self.select_submenus()


@submenu(label="test")
def test_submenu(self):
    print(f"This is test submenu")


@main_menu.submenu(label="Craft a mundane item")
def crafting_menu(self):
    print(f"\tThis is a crafting menu.")
    self.select_submenus()


@crafting_menu.submenu(label="Holy Water")
def holy_water_recipe(self):
    print(f"\t\tThis is a recipe. Parent menu = {self.parent.label}")
    print("\t\tWould you like to craft an item?")
    self.select_submenus()


@crafting_menu.submenu(label="Red Thaumstyn")
def red_thaumstyn_menu(self):
    print(f"\t\tThis is a menu for crafting with red thaumstyn. Parent menu = {self.parent.label}")


if __name__ == "__main__":
    main_menu.add_submenu(test_submenu)
    print(main_menu.all_submenus)
    print("\n\n")
    main_menu()

