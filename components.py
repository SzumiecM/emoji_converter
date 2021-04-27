import cv2
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

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
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


class CameraCV:
    def __init__(self, screen):
        self.capture = cv2.VideoCapture(0)
        self.screen = screen
        Clock.schedule_interval(self.update, 1.0 / 60.0)

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
        self.screen.image_avatar.source = os.path.join('img', 'base.png')



class Avatar:
    def __init__(self, screen):
        self.screen = screen
        if os.path.isfile(os.path.join('img', 'saved_avatar.png')):
            self.screen.image_avatar.source = os.path.join('img', 'saved_avatar.png')
        else:
            self.screen.image_avatar.source = os.path.join('img', 'base.png')
