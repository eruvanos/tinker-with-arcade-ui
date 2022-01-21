import arcade
from PIL import ImageEnhance
from arcade import Window, View
from arcade.gui import UIManager, UITextureButton, UIAnchorWidget, Surface


class UISimpleButton(UITextureButton):
    """
    A simple UIButton only requires a normal texture.

    Text will be always centered.
    """

    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = None,
                 height: float = None,
                 texture: arcade.Texture = None,
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
            surface.draw_texture(0, 0, self.width, self.height, tex)

        if self.text:
            text_margin = 2
            font_size = self._style.get("font_size", 15)
            font_color = self._style.get("font_color", arcade.color.WHITE)
            border_width = self._style.get("border_width", 2)
            # border_color = self._style.get("border_color", None)
            # bg_color = self._style.get("bg_color", (21, 19, 21))

            start_x = self.width // 2
            start_y = self.height // 2

            arcade.draw_text(
                text=self.text,
                start_x=start_x,
                start_y=start_y,
                font_size=font_size,
                color=font_color,
                align="center",
                anchor_x='center', anchor_y='center',
                width=self.width - 2 * border_width - 2 * text_margin
            )


class MyView(View):
    def __init__(self):
        super().__init__()

        self.mng = UIManager()

        tex = arcade.load_texture("button.png")
        self.button = UISimpleButton(text="Get Started", texture=tex)

        # Add button to UIManager, use UIAnchorWidget defaults to center on screen
        self.mng.add(UIAnchorWidget(child=self.button))

    def on_show_view(self):
        self.mng.enable()

    def on_hide_view(self):
        self.mng.enable()

    def on_draw(self):
        self.mng.draw()


if __name__ == '__main__':
    window = Window()
    window.show_view(MyView())
    arcade.run()
