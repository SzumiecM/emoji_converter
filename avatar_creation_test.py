import cv2
import numpy as np

base = cv2.imread('images/woman/base/b1f.png', -1)
eyes = cv2.imread('eyes_blue_f_smile.png', -1)
nose = cv2.imread('nose_with_freckles.png', -1)
lips = cv2.imread('smile_f.png', -1)
# print(base.shape)
# print(eyes.shape)

x_offset = 32
y_offset = 28

for y in range(y_offset, y_offset + eyes.shape[0]):
    for x in range(x_offset, x_offset + eyes.shape[1]):
        if not all(eyes[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
            base[y, x] = eyes[y - y_offset, x - x_offset]

x_offset = 38
y_offset = 48

for y in range(y_offset, y_offset + nose.shape[0]):
    for x in range(x_offset, x_offset + nose.shape[1]):
        if not all(nose[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
            base[y, x] = nose[y - y_offset, x - x_offset]

x_offset = 52
y_offset = 80

for y in range(y_offset, y_offset + lips.shape[0]):
    for x in range(x_offset, x_offset + lips.shape[1]):
        if not all(lips[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
            base[y, x] = lips[y - y_offset, x - x_offset]


file_name = 'test.png'
cv2.imwrite(file_name, base)
