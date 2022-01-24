import arcade
from PIL import ImageEnhance
from arcade import Window, View
from arcade.gui import UIManager, UIAnchorWidget, Surface, UIInputText, UITextureButton, UIBoxLayout, UIOnChangeEvent
from arcade.gui._property import _Property, _bind
from arcade.gui.widgets import _Rect


class BetterUIInputText(UIInputText):
    def __init__(self, adjust_size=False, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_change")
        self.adjust_size = adjust_size

        if self.adjust_size:
            self.fit_content()

    def fit_content(self):
        """Adjusts the widget size to fit content size of text"""
        self.rect = _Rect(self.x, self.y, self.layout.content_width, self.layout.content_height)

    @property
    def text(self):
        return self.doc.text

    @text.setter
    def text(self, value):
        old_text = value
        self.doc.text = value

        if self.adjust_size:
            self.fit_content()

        self.dispatch_event("on_change", UIOnChangeEvent(self, old_text, value))
        self.trigger_full_render()

    def on_change(self, event: UIOnChangeEvent):
        pass


class BetterUIIntInputText(BetterUIInputText):
    def __init__(self, value=0, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    @property
    def value(self) -> int:
        return int(self.text)

    @value.setter
    def value(self, value: int):
        self.text = "{value:03.0f}".format(value=value)


class UISimpleButton(UITextureButton):
    """
    A simple UIButton only requires a normal texture.

    Text will always be centered.
    """

    angle = _Property(0)

    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = None,
                 height: float = None,
                 texture: arcade.Texture = None,
                 angle=0,
                 text: str = "",
                 scale: float = None,
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None,
                 **kwargs):
        # Generate hover and pressed texture by changing the brightness
        enhancer = ImageEnhance.Brightness(texture.image)
        hover_tex = arcade.Texture(name=texture.name + "_brighter", image=enhancer.enhance(1.5))
        pressed_tex = arcade.Texture(name=texture.name + "_darker", image=enhancer.enhance(0.5))
        self.angle = angle

        _bind(self, "angle", self.trigger_render())

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            text=text,
            texture=texture,
            texture_hovered=hover_tex,
            texture_pressed=pressed_tex,
            scale=scale,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            style=style,
            **kwargs
        )

    def do_render(self, surface: Surface):
        self.prepare_render(surface)

        tex = self._tex
        if self.pressed and self._tex_pressed:
            tex = self._tex_pressed
        elif self.hovered and self._tex_hovered:
            tex = self._tex_hovered

        if tex:
            surface.draw_texture(0, 0, self.width, self.height, tex, angle=self.angle)


class MyView(View):
    def __init__(self):
        super().__init__()
        self.mng = UIManager()

        # arrow left, input text, arrow right
        tex = arcade.load_texture("arrow.png")
        self.left_arrow = UISimpleButton(texture=tex, width=10, height=30)
        self.input_field = BetterUIIntInputText(
            value=0,
            font_size=20,
            text_color=(58, 46, 38),
            adjust_size=True
        )
        self.right_arrow = UISimpleButton(texture=tex, width=10, height=30, angle=180)

        # decrement on left click
        @self.left_arrow.event("on_click")
        def dec(event):
            self.input_field.value -= 1

        # increment on right click
        @self.right_arrow.event("on_click")
        def inc(event):
            self.input_field.value += 1

        self.mng.add(UIAnchorWidget(
            child=UIBoxLayout(
                children=[
                    self.left_arrow,
                    self.input_field.with_space_around(left=10, right=10),
                    self.right_arrow
                ],
                vertical=False
            ).with_border(color=arcade.color.GRAY)))

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
