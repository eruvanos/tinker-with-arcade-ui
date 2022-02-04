import arcade
from arcade import Window, View
from arcade.gui import UIManager, UIOnChangeEvent, UIAnchorWidget, UIBoxLayout, UILabel

from v2_gui.widget import UIWidgetV2
from image_slider.slider_example import UITextureSlider
from toggle.toggle_example import UIImageToggle


class MyView(View):
    def __init__(self):
        super().__init__()

        self.mng = UIManager()

        # Add button to UIManager, use UIAnchorWidget defaults to center on screen
        self.dummy = UIWidgetV2()

        bar_tex = arcade.load_texture("SliderBar.png")
        thumb_tex = arcade.load_texture("SliderThumb.png")
        self.padding_slider = UITextureSlider(bar_tex, thumb_tex, max_value=30, width=100)

        @self.padding_slider.event("on_change")
        def update_padding(event: UIOnChangeEvent):
            self.dummy.padding = int(event.new_value)
            print(event.new_value)

        bar_tex = arcade.load_texture("SliderBar.png")
        thumb_tex = arcade.load_texture("SliderThumb.png")
        self.border_slider = UITextureSlider(bar_tex, thumb_tex, max_value=30, width=100)

        @self.border_slider.event("on_change")
        def update_slider(event: UIOnChangeEvent):
            self.dummy.border_width = int(event.new_value)
            print(event.new_value)

        on_texture = arcade.load_texture("toggle_green.png")
        off_texture = arcade.load_texture("toggle_red.png")
        self.visible_toggle = UIImageToggle(value=True, on_texture=on_texture, off_texture=off_texture, height=20, width=20)

        @self.visible_toggle.event("on_change")
        def update_visibility(event: UIOnChangeEvent):
            self.dummy.visible = event.new_value
            print(event.new_value)

        box = UIBoxLayout(space_between=10)
        row = UIBoxLayout(vertical=False, space_between=20)
        box.add(row)

        labels = UIBoxLayout(align="left")
        row.add(labels)
        labels.add(UILabel(text="Border", text_color=arcade.color.BLACK))
        labels.add(UILabel(text="Padding", text_color=arcade.color.BLACK))
        labels.add(UILabel(text="Visible", text_color=arcade.color.BLACK))

        sliders = UIBoxLayout()
        row.add(sliders)
        sliders.add(self.border_slider)
        sliders.add(self.padding_slider)
        sliders.add(self.visible_toggle)

        box.add(row)
        box.add(self.dummy)

        self.mng.add(UIAnchorWidget(
            child=box
        ))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.mng.enable()

    def on_hide_view(self):
        self.mng.disable()

    def on_draw(self):
        arcade.start_render()
        self.mng.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        print(self.dummy.rect)
        print(self.dummy.content_rect)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if scroll_y:
            self.dummy.border_width += scroll_y / abs(scroll_y)
        if scroll_x:
            self.dummy.padding_left += scroll_x / abs(scroll_x)
            self.dummy.padding_right += scroll_x / abs(scroll_x)


if __name__ == '__main__':
    window = Window()
    window.show_view(MyView())
    arcade.run()
