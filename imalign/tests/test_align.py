import numpy as np
import cv2
from imalign.align import align
from util import generate_samples
import matplotlib.pyplot as plt

WIDTH = 100
HEIGHT = 80
N = 200
DX = 2
DY = 3
SCALE = 3
BORDER = 0.01


def test_random_image():
    reference, ih, iw, source = generate_samples(height=HEIGHT,
                                                 width=WIDTH,
                                                 num_points=N,
                                                 angle=0.0,
                                                 offset_x=DX,
                                                 offset_y=DY,
                                                 scale=SCALE)

    aligned, cropped = align(reference=reference,
                             source=source,
                             border=BORDER)

    offset = int(BORDER * max(WIDTH, HEIGHT))
    diff = aligned[ih - offset, iw - offset, :] - cropped[ih - offset, iw - offset, :]
    assert np.mean(diff.astype(float)) < 5


if __name__ == "__main__":
    test_random_image()
