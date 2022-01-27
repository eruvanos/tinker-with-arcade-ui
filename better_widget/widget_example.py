from typing import Optional

import arcade
from arcade import Window, View
from arcade.gui import UIManager, UIWidget, Surface, UIOnChangeEvent, UIAnchorWidget, UIBoxLayout, UILabel
from arcade.gui._property import _Property, _bind
from arcade.gui.widgets import _Rect

from image_slider.slider_example import UITextureSlider
from toggle.toggle_example import UIImageToggle


class UIWidgetV2(UIWidget):
    """
    UIWidget with native border and padding support

    Todo:
    - Enable/Disable
    - Hover
    - Pressed
    - Focused (UIWidget got focus e.g. UIInputText, Tab order) [for now use hover]
    - Visible

    """
    rect: _Rect = _Property(_Rect(0, 0, 1, 1))
    visible = _Property(True)
    border_width = _Property(0)
    border_color = _Property(arcade.color.BLACK)
    bg_color = _Property(None)
    padding_top = _Property(0)
    padding_right = _Property(0)
    padding_bottom = _Property(0)
    padding_left = _Property(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # workaround for UIWidget._rect
        self.rect = self._rect

        # TODO bind all _Properties to self.trigger_full_render
        _bind(self, "rect", self.trigger_full_render)
        _bind(self, "visible", self.trigger_full_render)
        _bind(self, "border_width", self.trigger_full_render)
        _bind(self, "border_color", self.trigger_full_render)
        _bind(self, "bg_color", self.trigger_full_render)
        _bind(self, "padding_top", self.trigger_full_render)
        _bind(self, "padding_right", self.trigger_full_render)
        _bind(self, "padding_bottom", self.trigger_full_render)
        _bind(self, "padding_left", self.trigger_full_render)

    @property
    def padding(self):
        return max(self.padding_top, self.padding_right, self.padding_bottom, self.padding_left)

    @padding.setter
    def padding(self, value):
        self.padding_top = value
        self.padding_right = value
        self.padding_bottom = value
        self.padding_left = value

    @property
    def content_size(self):
        return self.content_width, self.content_height

    @property
    def content_width(self):
        return self.rect.width - 2 * self.border_width - self.padding_left - self.padding_right

    @property
    def content_height(self):
        return self.rect.height - 2 * self.border_width - self.padding_top - self.padding_bottom

    @property
    def content_rect(self):
        return _Rect(
            self.left + self.border_width + self.padding_left,
            self.bottom + self.border_width + self.padding_bottom,
            self.content_width,
            self.content_height
        )

    def with_border(self, width=2, color=(0, 0, 0)):
        self.border_width = width
        self.border_color = color

    def with_space_around(self,
                          top: float = 0,
                          right: float = 0,
                          bottom: float = 0,
                          left: float = 0,
                          bg_color: Optional[arcade.Color] = None):
        self.padding_top = top
        self.padding_right = right
        self.padding_bottom = bottom
        self.padding_left = left
        self.bg_color = bg_color

    def _do_render(self, surface: Surface, force=False):
        """Helper function to trigger :meth:`UIWidget.do_render` through the widget tree,
        should only be used by UIManager!
        """
        should_render = force or not self._rendered
        if should_render and self.visible:
            self.do_render_base(surface)
            self.do_render(surface)
            self._rendered = True

        for child in self.children:
            child._do_render(surface, should_render)

    def do_render_base(self, surface: Surface):
        surface.limit(*self.rect)

        # draw background
        if self.bg_color:
            surface.clear(self.bg_color)

        # draw border
        if self.border_width and self.border_color:
            arcade.draw_xywh_rectangle_outline(0, 0, self.width, self.height,
                                               color=self.border_color,
                                               border_width=self.border_width * 2)

    def prepare_render(self, surface):
        surface.limit(*self.content_rect)

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        arcade.draw_xywh_rectangle_filled(0, 0, self.content_width, self.content_height, color=arcade.color.WINE)


class MyView(View):
    def __init__(self):
        super().__init__()

        self.mng = UIManager()

        # Add button to UIManager, use UIAnchorWidget defaults to center on screen
        self.dummy = UIWidgetV2()
        self.dummy.center_on_screen()

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
