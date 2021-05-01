import pprint

import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights('model3.h5')

cv2.ocl.setUseOpenCL(False)

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
emotions = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']


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
        if abs(pos_diff) > 50:
            if pos_diff > 0 and self._current > 0:
                self._screen_manager.transition.direction = 'right'
                self._screen_manager.current = self._screen_list[self._current - 1]
            elif pos_diff < 0 and self._current < 2:
                self._screen_manager.transition.direction = 'left'
                self._screen_manager.current = self._screen_list[self._current + 1]

        return super(SwipeableScreen, self).on_touch_up(touch)


class CameraCV:
    def __init__(self, screen):
        self.capture = cv2.VideoCapture(0)
        self.screen = screen
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.screen.image_avatar.source = App.get_running_app().saved_avatar_path

    def update(self, dt):
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
                cv2.putText(frame, emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),
                            2, cv2.LINE_AA)
                self.screen.label.text = emotion_dict[maxindex]
        except:
            pass
        # self.screen.image_avatar.source = os.path.join('img', 'base.png')

    def update_with_emotion(self):
        pprint.pprint(App.get_running_app().selected_avatar_attributes)


def next_prev(func):
    def wrapper(self):
        name, direction = func.__name__.split('_')
        list_ = App.get_running_app().paths.get(App.get_running_app().selected_avatar_attributes['sex']).get(name)
        curr_file = App.get_running_app().selected_avatar_attributes.get(name)
        curr_index = list_.index(curr_file)

        if direction == 'right':
            try:
                App.get_running_app().selected_avatar_attributes[name] = list_[curr_index + 1]
            except IndexError:
                App.get_running_app().selected_avatar_attributes[name] = list_[0]
        elif direction == 'left':
            try:
                App.get_running_app().selected_avatar_attributes[name] = list_[curr_index - 1]
            except IndexError:
                App.get_running_app().selected_avatar_attributes[name] = list_[-1]

        return func(self)

    return wrapper


def select_sex(func):
    def wrapper(self):
        _, name = func.__name__.split('_')

        App.get_running_app().selected_avatar_attributes['sex'], \
        previous = name, App.get_running_app().selected_avatar_attributes['sex']

        if previous != name:
            for x in ('base', 'eyes', 'mouth'):  # todo add hair
                App.get_running_app().selected_avatar_attributes[x] = App.get_running_app().paths.get(name).get(x)[
                    App.get_running_app().paths.get(previous).get(x).index(
                        App.get_running_app().selected_avatar_attributes.get(x)
                        # getattr(App.get_running_app(), f'selected_{x}')
                    )
                ]

        return func(self)

    return wrapper


def apply_element(template, element, x_offset, y_offset):
    for y in range(y_offset, y_offset + element.shape[0]):
        for x in range(x_offset, x_offset + element.shape[1]):
            if not all(element[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
                template[y, x] = element[y - y_offset, x - x_offset]
    return template


class Avatar:
    def __init__(self, screen):
        self.screen = screen
        self.screen.image_avatar.source = App.get_running_app().saved_avatar_path

    def update(self):
        pprint.pprint(App.get_running_app().selected_avatar_attributes)

        base = cv2.imread(App.get_running_app().selected_avatar_attributes['base'], -1)
        eyes = cv2.imread(os.path.join(App.get_running_app().selected_avatar_attributes['eyes'], 'smile.png'), -1)
        mouth = cv2.imread(App.get_running_app().selected_avatar_attributes['mouth'], -1)

        base = apply_element(
            apply_element(base, eyes, 32, 28),
            mouth, 52, 80
        )

        cv2.imwrite(App.get_running_app().saved_avatar_path, base)
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
