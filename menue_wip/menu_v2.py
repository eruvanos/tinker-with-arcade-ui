import arcade
from arcade import Window, View
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, Surface, UIAnchorWidget


class BetterUIBoxLayout(UIBoxLayout):
    visible = False

    def _do_render(self, surface: Surface, force=False):
        if self.visible:
            super(BetterUIBoxLayout, self)._do_render(surface, force)


class MenuBar(UIBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(vertical=False, size_hint=(1, None), align="left", space_between=10, **kwargs)

    def add_menu(self, text: str):
        button = self.add(UIFlatButton(text=text, height=40))

        dropdown = button.add(BetterUIBoxLayout(x=button.left, y=self.bottom, vertical=True))

        dropdown.add(UIFlatButton(text="Hallo"))

        @button.event("on_click")
        def toggle(event):
            dropdown.visible = not dropdown.visible
            dropdown.trigger_full_render()


class MyView(View):
    def __init__(self):
        super().__init__()
        self.mng = UIManager()

        bar = MenuBar()
        self.mng.add(UIAnchorWidget(anchor_y="top", anchor_x="left", child=bar))
        bar.add_menu("Start")
        bar.add_menu("Exit")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.mng.enable()

    def on_hide_view(self):
        self.mng.disable()

    def on_draw(self):
        arcade.start_render()
        self.mng.draw()


if __name__ == '__main__':
    window = Window()
    window.show_view(MyView())
    arcade.run()
