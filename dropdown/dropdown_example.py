from typing import List

import arcade
from arcade import Window, View
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIOnChangeEvent, UIOnClickEvent, UILayout, UILabel

from v2_gui.widget import UIWidgetV2


class UIBoxLayoutV2(UIWidgetV2, UIBoxLayout):
    """
    Combines UIBoxLayout with UIWidgetV2 in a hacky way, this does not support border or padding, but visibility
    """


class UIDropdown(UIWidgetV2, UILayout):
    def __init__(self,
                 default: str = None,
                 options: List[str] = None,
                 style=None,
                 **kwargs):
        if style is None:
            style = {}

        # TODO handle if default value not in options or options empty
        if options is None:
            options = []
        self._options = options
        self._value = default

        super().__init__(style=style, **kwargs)

        # Setup button showing value
        self._default_button = UIFlatButton(text=str(self._value), width=self.width, height=self.height)
        self._default_button.on_click = self._on_button_click

        self._layout = UIBoxLayoutV2()
        self._layout.visible = False
        self._update_options()

        # add children after super class setup
        self.add(self._default_button)
        self.add(self._layout)

        self.register_event_type("on_change")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        old_value = self._value
        self._value = value
        self._default_button.text = self._value

        self._update_options()
        self.dispatch_event("on_change", UIOnChangeEvent(self, old_value, value))
        self.trigger_render()

    def _update_options(self):
        # generate options
        self._layout.clear()
        for option in self._options:
            button: UIFlatButton = self._layout.add(
                UIFlatButton(
                    text=option,
                    width=self.width,
                    height=self.height,
                    style={"bg_color": (55, 66, 81) if self.value == option else (95, 111, 131)}
                )
            )
            button.on_click = self._on_option_click

    def _on_button_click(self, event: UIOnClickEvent):
        self._layout.visible = not self._layout.visible

    def _on_option_click(self, event: UIOnClickEvent):
        source: UIFlatButton = event.source
        self.value = source.text
        self._layout.visible = False
        # TODO trigger on_change

    def do_layout(self):
        # print("do layout")
        self._default_button.rect = self.rect
        self._layout.rect = self._layout.rect.align_top(self.bottom).align_left(self.left)

    def on_change(self, event: UIOnChangeEvent):
        pass


class MyView(View):
    def __init__(self):
        super().__init__()

        self.mng = UIManager()

        # Add button to UIManager, use UIAnchorWidget defaults to center on screen
        self.dropdown = UIDropdown(
            default="Platformer",
            options=[
                "Arcade",
                "Platformer",
                "Jump and Run"
            ],
            height=50,
            width=200
        )
        self.dropdown.center_on_screen()
        self.mng.add(self.dropdown)

        self.label = self.mng.add(UILabel(text=" ", text_color=(0,0,0)))

        @self.dropdown.event()
        def on_change(event: UIOnChangeEvent):
            print(f"Value changed from '{event.old_value}' to '{event.new_value}'")
            self.label.text = f"Value changed from '{event.old_value}' to '{event.new_value}'"
            self.label.fit_content()

            # place label above dropdown
            self.label.center_on_screen()
            self.label.move(dy=50)

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
