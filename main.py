from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from components import CameraCV, SwipeableScreen


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


class CameraScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super(CameraScreen, self).__init__(**kw)
        self._screen_manager = sm
        self._current = 0
        self.camera = CameraCV(self)
        self.image_camera = self.ids['image_camera']
        self.image_avatar = self.ids['image_avatar']

    def update_with_emotion(self):
        print('updating...')


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', sm=sm))
        sm.add_widget(AvatarCreationScreen(name='avatar', sm=sm))
        sm.add_widget(CameraScreen(name='camera', sm=sm))
        return sm


if __name__ == '__main__':
    MainApp().run()
