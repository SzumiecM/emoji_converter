import cv2
import numpy as np

base = cv2.imread('images/woman/base/b7f.png', -1)
eyes = cv2.imread('images/man/eyes/brown/happy.png', -1)
mouth = cv2.imread('images/man/mouth/angry.png', -1)
hair = cv2.imread('images/woman/hair/long gray.png', -1)


# nose = cv2.imread('nose.png', -1)


def apply_element(template, element, y_offset, x_offset=None):
    if not x_offset:
        x_offset = int(template.shape[1] / 2 - element.shape[1] / 2) - 1

    for y in range(y_offset, y_offset + element.shape[0]):
        for x in range(x_offset, x_offset + element.shape[1]):
            if not all(element[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
                template[y, x] = element[y - y_offset, x - x_offset]
    return template


base = apply_element(
    apply_element(
        apply_element(base, mouth, y_offset=134),
        eyes, y_offset=80
    ),
    hair, x_offset=0, y_offset=0
)

file_name = 'test.png'
cv2.imwrite(file_name, base)
