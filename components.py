import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


class SwipeableScreen(Screen):
    _screen_list = ['camera', 'main', 'avatar']
    _current = None
    _touch_pos_x = None
    _screen_manager = None

    def on_touch_down(self, touch):
        self._touch_pos_x = touch.pos[0]

        return super(SwipeableScreen, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        pos_diff = touch.pos[0] - self._touch_pos_x
        if pos_diff > 0 and self._current > 0:
            self._screen_manager.transition.direction = 'right'
            self._screen_manager.current = self._screen_list[self._current - 1]
        elif pos_diff < 0 and self._current < 2:
            self._screen_manager.transition.direction = 'left'
            self._screen_manager.current = self._screen_list[self._current + 1]

        return super(SwipeableScreen, self).on_touch_up(touch)


class CameraCV(Widget):
    def __init__(self, screen, **kw):
        super(CameraCV, self).__init__(**kw)
        self.capture = cv2.VideoCapture(0)
        self.screen = screen
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        _, frame = self.capture.read()
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        self.screen.image_camera.texture = texture
        self.screen.image_avatar.source = 'kotek.jpg'
