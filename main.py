import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
import cv2
from kivy.uix.widget import Widget


class SwipeableScreen(Screen):
    _screen_list = ['camera', 'main', 'avatar']
    _current = None
    _touch_pos_x = None
    _screen_manager = None

    def on_touch_down(self, touch):
        self._touch_pos_x = touch.pos[0]

    def on_touch_up(self, touch):
        pos_diff = touch.pos[0] - self._touch_pos_x
        if pos_diff > 0 and self._current > 0:
            self._screen_manager.transition.direction = 'right'
            self._screen_manager.current = self._screen_list[self._current - 1]
        elif pos_diff < 0 and self._current < 2:
            self._screen_manager.transition.direction = 'left'
            self._screen_manager.current = self._screen_list[self._current + 1]


class MainScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super().__init__(**kw)
        self._screen_manager = sm
        self._current = 1


class AvatarCreationScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super().__init__(**kw)
        self._screen_manager = sm
        self._current = 2


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


class CameraScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super(CameraScreen, self).__init__(**kw)
        self._screen_manager = sm
        self._current = 0
        self.camera = CameraCV(self)
        self.image_camera = self.ids['image_camera']
        self.image_avatar = self.ids['image_avatar']


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', sm=sm))
        sm.add_widget(AvatarCreationScreen(name='avatar', sm=sm))
        sm.add_widget(CameraScreen(name='camera', sm=sm))
        return sm


if __name__ == '__main__':
    MainApp().run()
