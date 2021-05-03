import cv2
import numpy as np

base = cv2.imread('images/man/base/b4m.png', -1)
eyes = cv2.imread('images/man/eyes/brown/happy.png', -1)
mouth = cv2.imread('images/man/mouth/neutral.png', -1)
hair = cv2.imread('images/man/hair/black/almost bald.png', -1)


def apply_element(template, element, x_offset, y_offset):
    for y in range(y_offset, y_offset + element.shape[0]):
        for x in range(x_offset, x_offset + element.shape[1]):
            if not all(element[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
                template[y, x] = element[y - y_offset, x - x_offset]
    return template

base = apply_element(
        apply_element(base, eyes, 32, 28),
        mouth, 52, 80
    )

base = apply_element(
    apply_element(
        apply_element(
            base, eyes, 32, 28
        ),
        mouth, 52, 80
    ),
    hair, 19, -42
)

file_name = 'test.png'
cv2.imwrite(file_name, base)
