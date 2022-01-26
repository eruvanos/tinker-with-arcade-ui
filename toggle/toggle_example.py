import arcade
from PIL import ImageEnhance
from arcade import Window, View
from arcade.gui import UIManager, UIAnchorWidget, Surface, UIInteractiveWidget, UIOnClickEvent, \
    UIOnChangeEvent
from arcade.gui._property import _Property, _bind


class UIImageToggle(UIInteractiveWidget):
    """
    A simple toggle button
    """

    # Experimental ui class
    value: bool = _Property(False)

    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 100,
                 height: float = 50,
                 on_texture: arcade.Texture = None,
                 off_texture: arcade.Texture = None,
                 scale: float = None,
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None,
                 **kwargs):
        # Generate hover and pressed texture by changing the brightness
        self.normal_on_tex = on_texture
        enhancer = ImageEnhance.Brightness(self.normal_on_tex.image)
        self.hover_on_tex = arcade.Texture(name=self.normal_on_tex.name + "_brighter", image=enhancer.enhance(1.5))
        self.pressed_on_tex = arcade.Texture(name=self.normal_on_tex.name + "_darker", image=enhancer.enhance(0.5))

        self.normal_off_tex = off_texture
        enhancer = ImageEnhance.Brightness(self.normal_off_tex.image)
        self.hover_off_tex = arcade.Texture(name=self.normal_off_tex.name + "_brighter", image=enhancer.enhance(1.5))
        self.pressed_off_tex = arcade.Texture(name=self.normal_off_tex.name + "_darker", image=enhancer.enhance(0.5))

        _bind(self, "value", self.trigger_render)

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            scale=scale,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            style=style,
            **kwargs
        )

        self.register_event_type("on_change")

    def on_click(self, event: UIOnClickEvent):
        self.value = not self.value
        self.dispatch_event("on_change", UIOnChangeEvent(self, not self.value, self.value))

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        tex = self.normal_on_tex if self.value else self.normal_off_tex
        if self.pressed:
            tex = self.pressed_on_tex if self.value else self.pressed_off_tex
        elif self.hovered:
            tex = self.hover_on_tex if self.value else self.hover_off_tex
        surface.draw_texture(0, 0, self.width, self.height, tex)

    def on_change(self, event: UIOnChangeEvent):
        pass


class MyView(View):
    def __init__(self):
        super().__init__()

        self.mng = UIManager()

        on_texture = arcade.load_texture("switch_green.png")
        off_texture = arcade.load_texture("switch_red.png")
        self.toggle = UIImageToggle(on_texture=on_texture, off_texture=off_texture)

        # Add toggle to UIManager, use UIAnchorWidget defaults to center on screen
        self.mng.add(UIAnchorWidget(child=self.toggle))

        @self.toggle.event("on_change")
        def print_oon_change(event: UIOnChangeEvent):
            print(f"New value {event.new_value}")

    def on_show_view(self):
        self.mng.enable()

    def on_hide_view(self):
        self.mng.disable()

    def on_draw(self):
        self.mng.draw()


if __name__ == '__main__':
    window = Window()
    window.show_view(MyView())
    arcade.run()
