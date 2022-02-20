from typing import Optional, Union

import arcade
import arcade.gui
from arcade.gui import UIFlatButton, UIOnClickEvent, UIManager, UIBoxLayout

INTERFACE_BG_COLOR = (102, 51, 0)
INTERFACE_BORDER_INT_COLOR = (128, 64, 0)
INTERFACE_BORDER_EXT_COLOR = (0, 0, 0)


class DropDownMenuButton(UIFlatButton):
    def __init__(self, menu: "Menu", text, callback, **button_options):
        self.menu = menu  # parent menu reference
        self.callback = callback

        style = button_options.get('style', {})
        style['font_color'] = style.get('font_color', button_options.get('font_color', arcade.color.YELLOW_ORANGE))
        style['bg_color'] = style.get('bg_color', button_options.get('bg_color'))
        style['font_size'] = style.get('font_size', button_options.get('font_size', 9))
        button_options['style'] = style

        button_options['text'] = text
        button_options['width'] = button_options.get('width') or self.menu.dropdown.width
        button_options['height'] = button_options.get('height') or 25

        super().__init__(**button_options)

    def on_click(self, event: UIOnClickEvent):
        """
        This is de event handler for click events, but here is used to auto close the parent menu.
        Child classes SHOULD NOT subclass "on_click" and instead always subclass "on_click_event"
        """
        self.callback(self.menu.menu_bar.game, self)  # allways pass the game object to the callback
        # CAUTION at the momment arcade: 2.6.9 click events propagate to the view or window
        # this is a hack to check for events at this point and not execute them
        # self.menu.menu_bar.game._ui_menu_clicked_at = (event.x, event.y)
        self.menu.close()  # close the menu after the button is clicked


class DropDownMenu:

    def __init__(self, menu: "Menu"):
        self.menu = menu
        self.is_open = False  # default state is menu closed
        self.height = 300
        self.width = self.menu.button.width or 130
        self.x = self.menu.button.x
        self.y = self.menu.button.y - self.height - self.menu_bar.buttons_margin
        self.manager = UIManager()
        self.menu_box = UIBoxLayout(x=self.x, y=self.y + self.height, vertical=True)
        self.manager.add(self.menu_box)

    @property
    def menu_bar(self):
        return self.menu.menu_bar

    def add_button(self, text, callback, **kwargs):
        new_button = DropDownMenuButton(self.menu, text, callback, **kwargs)
        self.menu_box.add(new_button)

        # reconfigure "y" and "height" of the dropdown
        self.y = self.menu_box.y
        self.height = self.menu_box.height

    def draw_menu_frame(self):
        arcade.draw_xywh_rectangle_filled(self.x, self.y, self.width, self.height, INTERFACE_BG_COLOR)
        arcade.draw_xywh_rectangle_outline(self.x + 1, self.y, self.width, self.height, INTERFACE_BORDER_EXT_COLOR, 2)
        arcade.draw_xywh_rectangle_outline(self.x + 3, self.y + 2, self.width - 4, self.height - 4, INTERFACE_BORDER_INT_COLOR, 2)

    def draw(self):
        self.draw_menu_frame()
        self.manager.draw()

    def is_mouse_on_top(self, x, y):
        """ Check if the mouse is on top of this menu """
        return self.x <= x <= self.right and self.y <= y <= self.top

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y + self.height


class MenuButton(UIFlatButton):

    def __init__(self, menu: "Menu", text, **kwargs):
        self.menu = menu

        style = kwargs.get('button_style') or {
            'font_color': kwargs.get('button_font_color', arcade.color.YELLOW_ORANGE),
            'bg_color': kwargs.get('button_bg_color'),
            'font_size': kwargs.get('button_font_size', 13),
        }
        button_kwargs = {
            'text': text,
            'style': style,
            'width': kwargs.get('button_width') or 130,
            'height': self.menu_bar.height - 2 * self.menu_bar.buttons_margin,
        }
        super().__init__(**button_kwargs)

        # add the button to the menu_box so it's position is set
        self.menu.menu_bar.menu_box.add(self)

    @property
    def menu_bar(self):
        return self.menu.menu_bar

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        if self.menu_bar.display_menu is not None:
            if self.menu_bar.display_menu is self.menu:
                self.menu.close()
            else:
                self.menu_bar.display_menu.close()  # close opened menu
                self.menu.open()  # open this menu
        else:
            self.menu.toogle()


class Menu:

    def __init__(self, menu_bar: "MenuBar", text, **kwargs):
        """ kwargs holds options for the menu_button and dropdown_menu"""
        self.menu_bar = menu_bar
        self.button = MenuButton(self, text, **kwargs)
        self.dropdown = DropDownMenu(self)

        self.is_open: bool = False

    def draw(self):
        if self.is_open:
            self.dropdown.draw()

    def add_button(self, text: str, on_click_method, **button_options):
        """ Adds a button to thi menu """
        self.dropdown.add_button(text, on_click_method, **button_options)

    def close(self):
        self.dropdown.manager.disable()
        self.is_open = False
        self.menu_bar.display_menu = None

    def open(self):
        self.dropdown.manager.enable()
        self.is_open = True
        self.menu_bar.display_menu = self

    def toogle(self):
        """ Toogle the open/close state"""
        if self.is_open:
            self.close()
        else:
            self.open()

    def is_mouse_on_top(self, x, y):
        return self.dropdown.is_mouse_on_top(x, y)


class MenuBar:
    """
    Currently only horizontal Menu at the top of the screen
    Requires to set a camera.use() after the camera of the game (if the game map uses a camera)
    """

    def __init__(self, game, window: arcade.Window, height: int = 32,
                 width: Optional[int] = None, *, buttons_margin: int = 3):
        self.game = game  # holds the game object that will be passed to each menu callback
        self.window_or_view = window
        self.menus_list: list = []  # holds the menu objects

        # Dimensions
        self.height = height
        self.width = width or window.width

        # Position
        self.centered_x = self.width / 2
        self.centered_y = window.height - (self.height / 2)
        self.buttons_margin = buttons_margin

        # Menu content manager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.menu_box = arcade.gui.UIBoxLayout(x=0, y=self.top - buttons_margin, vertical=False)

        self.manager.add(self.menu_box)

        self.display_menu = None  # holds the menu to display

    def add_menu(self, text, **button_options):
        menu = Menu(self, text, **button_options)
        self.menus_list.append(menu)

        return menu

    @property
    def top(self):
        return self.centered_y + (self.height / 2)

    @property
    def bottom(self):
        return self.centered_y - (self.height / 2)

    @property
    def is_menu_opened(self):
        return self.display_menu is not None

    def is_mouse_on_top(self, x, y):
        """ Check if x, y coordinates are within the top bar"""
        if y > self.bottom:
            return True
        else:
            if self.display_menu is not None:
                return self.display_menu.is_mouse_on_top(x, y)

    def draw_menu_bar_frame(self):
        arcade.draw_rectangle_filled(self.centered_x, self.centered_y, self.width, self.height, INTERFACE_BG_COLOR)
        arcade.draw_rectangle_outline(self.centered_x, self.centered_y - 1, self.width, self.height - 1, INTERFACE_BORDER_EXT_COLOR, 2)
        arcade.draw_rectangle_outline(self.centered_x, self.centered_y - 1, self.width - 6, self.height - 6, INTERFACE_BORDER_INT_COLOR, 2)

    def draw(self):
        self.draw_menu_bar_frame()

        self.manager.draw()

        if self.display_menu:
            self.display_menu.draw()


if __name__ == '__main__':
    window = arcade.Window()

    def open_game(game, button):
        # do something potentially using the game object or the dropdownmenubutton
        print('Game openend')

    def quit_game(game, button):
        print('Exit!!')

    menu_bar = MenuBar(None, arcade.get_window())
    menu = menu_bar.add_menu('Game', width=100)
    menu.add_button('Open Game', open_game)
    menu.add_button('Close Game', quit_game)


    @window.event
    def on_draw():
        arcade.start_render()
        menu_bar.draw()


    arcade.run()