import arcade
from arcade import Window, View
from arcade.experimental.uislider import UISlider
from arcade.experimental.uistyle import UISliderStyle
from arcade.gui import UIManager, UIAnchorWidget, Surface


class UITextureSlider(UISlider):
    """
    Slider using
    """

    def __init__(self, **kwargs):
        self.bar = arcade.load_texture("SliderBar.png")
        self.thumb = arcade.load_texture("SliderThumb.png")
        style = UISliderStyle(
            normal_filled_bar=(180, 180, 140),
            hovered_filled_bar=(200, 200, 165),
            pressed_filled_bar=(225, 225, 180),
        )

        super().__init__(style=style, **kwargs)

    def do_render(self, surface: Surface):
        state = "pressed" if self.pressed else "hovered" if self.hovered else "normal"

        self.prepare_render(surface)

        surface.draw_texture(0, 0, self.width, self.height, self.bar)

        # TODO accept constructor params
        slider_height = self.height // 4
        slider_left_x = self._x_for_value(self.vmin)
        cursor_center_x = self.value_x

        slider_bottom = (self.height - slider_height) // 2

        # slider
        fg_slider_color = self.style[f"{state}_filled_bar"]
        arcade.draw_xywh_rectangle_filled(slider_left_x - self.x, slider_bottom, cursor_center_x - slider_left_x,
                                          slider_height, fg_slider_color)

        # cursor
        rel_cursor_x = cursor_center_x - self.x
        surface.draw_texture(
            x=rel_cursor_x - self.thumb.width // 4,
            y=0,
            width=self.thumb.width // 2,
            height=self.height,
            tex=self.thumb
        )


class MyView(View):
    def __init__(self):
        super().__init__()

        self.mng = UIManager()

        bar_tex = arcade.load_texture("SliderBar.png")
        thumb_tex = arcade.load_texture("SliderThumb.png")
        self.button = UITextureSlider()

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
