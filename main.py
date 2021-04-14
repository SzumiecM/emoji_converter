from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager


class MainScreen(Screen):
    pass


class AvatarCreationScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AvatarCreationScreen(name='avatar'))
        return sm


if __name__ == '__main__':
    MainApp().run()
