import glob
import os.path
import pprint
import json

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from components import CameraCV, SwipeableScreen, Avatar


class MainScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super(MainScreen, self).__init__(**kw)
        self._screen_manager = sm
        self._current = 1


class AvatarCreationScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super(AvatarCreationScreen, self).__init__(**kw)
        self._screen_manager = sm
        self._current = 2

        self.image_avatar = self.ids['image_avatar']

        self.avatar = Avatar(self)


class CameraScreen(SwipeableScreen):
    def __init__(self, sm=None, **kw):
        super(CameraScreen, self).__init__(**kw)
        self._screen_manager = sm
        self._current = 0

        self.image_camera = self.ids['image_camera']
        self.image_avatar = self.ids['image_avatar']
        self.label = self.ids['label']

        self.camera = CameraCV(self)

    def update_with_emotion(self):
        pprint.pprint(self.current_base)


class MainApp(App):
    # todo consider moving build stuff to on_start, shitty documentation, gotta verify behaviour on android
    # access via App.get_running_app().<variable_name>
    saved_avatar_path = os.path.join('images', 'saved_avatar.png')
    # selected_sex = 'man'
    # selected_base = None
    # selected_hair = None
    # selected_eyes = None
    # selected_mouth = None
    with open('saved_avatar.json') as file:
        selected_avatar_attributes = json.load(file)

    emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

    # how i see it is that with paths we gain access to all images, but when it comes to for example eyes
    # that change with the emotions and are classified by colors, from path we get the right path, but file name
    # will be extracted from emotions list like images/woman/eyes/blue/happy.png

    def build(self):
        # todo consider saving to file with additional script to update it
        self.paths = {
            'man': {
                'base': glob.glob(os.path.join('images', 'man', 'base', '*.png')),
                'eyes': glob.glob(os.path.join('images', 'man', 'eyes', '*')),
                'hair': glob.glob(os.path.join('images', 'man', 'hair', '*.png')),
                'mouth': glob.glob(os.path.join('images', 'man', 'mouth', '*.png'))
            },
            'woman': {
                'base': glob.glob(os.path.join('images', 'woman', 'base', '*.png')),
                'eyes': glob.glob(os.path.join('images', 'woman', 'eyes', '*')),
                'hair': glob.glob(os.path.join('images', 'woman', 'hair', '*.png')),
                'mouth': glob.glob(os.path.join('images', 'woman', 'mouth', '*.png'))

            }
        }

        # todo delete these if and lets assume all file will be there
        self.selected_avatar_attributes['sex'] = 'man'
        self.selected_avatar_attributes['hair'] = self.paths.get('man').get('hair')[0] if len(
            self.paths.get('man').get('hair')) > 0 else None
        self.selected_avatar_attributes['eyes'] = self.paths.get('man').get('eyes')[0] if len(
            self.paths.get('man').get('eyes')) > 0 else None
        self.selected_avatar_attributes['base'] = self.paths.get('man').get('base')[0] if len(
            self.paths.get('man').get('base')) > 0 else None
        self.selected_avatar_attributes['mouth'] = self.paths.get('man').get('mouth')[0] if len(
            self.paths.get('man').get('mouth')) > 0 else None

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', sm=sm))
        sm.add_widget(AvatarCreationScreen(name='avatar', sm=sm))
        sm.add_widget(CameraScreen(name='camera', sm=sm))
        return sm

    def on_start(self):
        # todo load saved selected paths
        pass

    def on_stop(self):
        # todo save currently selected paths
        pass


if __name__ == '__main__':
    MainApp().run()
