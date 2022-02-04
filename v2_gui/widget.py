from typing import Optional, Tuple

import arcade
from arcade.gui import Surface, UIWidget, UIEvent
from arcade.gui._property import _Property, _bind
from arcade.gui.widgets import _Rect
from pyglet.event import EVENT_UNHANDLED


class UIWidgetV2(UIWidget):
    """
    UIWidget with native border and padding support.

    Further features:
    - Visible Flag to hide a widget and all children


    Todo:
    - Enable/Disable
    - Hover
    - Pressed
    - Focused (UIWidget got focus e.g. UIInputText, Tab order) [for now use hover]

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
        # self.rect = self._rect

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

    # workaround for UIWidget._rect
    @property
    def _rect(self):
        return self.rect

    @_rect.setter
    def _rect(self, value):
        self.rect = value

    @property
    def center(self):
        return self.rect.center

    @center.setter
    def center(self, value: Tuple[int, int]):
        cx, cy = value
        self.rect = self.rect.align_center(cx, cy)

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

        # only render children if self is visible
        if self.visible:
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

    def on_event(self, event: UIEvent) -> Optional[bool]:
        """Passes :class:`UIEvent` s through the widget tree."""
        if self.visible:
            return super(UIWidgetV2, self).on_event(event)
        else:
            return EVENT_UNHANDLED
