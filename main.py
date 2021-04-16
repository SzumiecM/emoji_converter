import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
import cv2
from kivy.uix.widget import Widget


class MainScreen(Screen):
    pass


class AvatarCreationScreen(Screen):
    pass


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


class CameraScreen(Screen):
    def __init__(self, **kw):
        super(CameraScreen, self).__init__(**kw)
        self.camera = CameraCV(self)
        self.image_camera = self.ids['image_camera']
        self.image_avatar = self.ids['image_avatar']


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AvatarCreationScreen(name='avatar'))
        sm.add_widget(CameraScreen(name='camera'))
        return sm


if __name__ == '__main__':
    MainApp().run()
