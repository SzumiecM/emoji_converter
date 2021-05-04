import pprint

import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
import os
import numpy as np

from model import model
from helpers import next_prev, select_sex, apply_element, create_avatar

cv2.ocl.setUseOpenCL(False)

EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
emotion_dict = {k: v for k, v in enumerate(EMOTIONS)}


class SwipeableScreen(Screen):
    _screen_list = ['camera', 'main', 'avatar']
    _current = None
    _touch_pos_x = None
    _screen_manager = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.image_avatar = self.ids['image_avatar']
        self.image_avatar.source = App.get_running_app().saved_avatar_path

    def on_touch_down(self, touch):
        self._touch_pos_x = touch.pos[0]

        return super(SwipeableScreen, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        pos_diff = touch.pos[0] - self._touch_pos_x
        if abs(pos_diff) > 50:
            if pos_diff > 0 and self._current > 0:
                self._screen_manager.transition.direction = 'right'
                self._screen_manager.current = self._screen_list[self._current - 1]
            elif pos_diff < 0 and self._current < 2:
                self._screen_manager.transition.direction = 'left'
                self._screen_manager.current = self._screen_list[self._current + 1]

        return super(SwipeableScreen, self).on_touch_up(touch)

    def on_pre_enter(self, *args):
        # todo think of a better way or at least put it in some function
        create_avatar()
        self.image_avatar.reload()


class CameraCV:
    def __init__(self, screen):
        self.capture = cv2.VideoCapture(0)
        self.screen = screen
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        Clock.schedule_interval(self.update_with_emotion, 1.0)
        self.tmp_emotion = None

    def update(self, dt):
        if self.screen._screen_manager.current == 'camera':
            try:
                _, frame = self.capture.read()
                buf = cv2.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
                texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
                self.screen.image_camera.texture = texture

                facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                    prediction = model.predict(cropped_img)
                    maxindex = int(np.argmax(prediction))
                    cv2.putText(frame, emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 0, 255),
                                2, cv2.LINE_AA)

                    self.tmp_emotion = emotion_dict[maxindex]
            except:
                pass

    def update_with_emotion(self, dt):
        if self.screen._screen_manager.current == 'camera':
            if self.tmp_emotion:
                self.screen.label.text = self.tmp_emotion

                create_avatar(self.tmp_emotion)
                self.screen.image_avatar.reload()

    def save(self):
        print('dupa dupa dupa ', self.tmp_emotion)
        App.get_running_app().selected_avatar_attributes['emotion'] = self.tmp_emotion

        # todo consider moving imwrite to create_avatar
        create_avatar(self.tmp_emotion)


class Avatar:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        create_avatar()
        self.screen.image_avatar.reload()

    @select_sex
    def choose_man(self):
        self.update()

    @select_sex
    def choose_woman(self):
        self.update()

    @next_prev
    def hair_left(self):
        self.update()

    @next_prev
    def hair_right(self):
        self.update()

    @next_prev
    def eyes_left(self):
        self.update()

    @next_prev
    def eyes_right(self):
        self.update()

    @next_prev
    def base_right(self):
        self.update()

    @next_prev
    def base_left(self):
        self.update()
