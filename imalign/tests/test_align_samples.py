import cv2
import numpy as np
import imageio.v3 as iio
from imalign.align import align


def normalize(im, max_level=255, dtype=np.uint8):
    x0 = np.min(im)
    x1 = np.max(im)
    n = max_level * (im.astype(float) - x0)/(x1 - x0)
    return n.astype(dtype)


def test_align_samples():
    ref = iio.imread("samples/lab.jpg")
    src = iio.imread("samples/dslr.jpg")
    src = src[:, ::-1, :]

    aligned, trimmed = align(reference=ref,
                             source=src,
                             invert_source=True,
                             border=0.05)

    assert aligned.shape == trimmed.shape

    ref_mono = normalize(cv2.cvtColor(trimmed, cv2.COLOR_RGB2GRAY))
    ref_edges = cv2.Canny(ref_mono, 150, 200) / 255

    mono = normalize(cv2.cvtColor(aligned, cv2.COLOR_RGB2GRAY))
    mono = 255 - mono
    edges = cv2.Canny(mono, 150, 200) / 255

    min_count = min(np.count_nonzero(ref_edges), np.count_nonzero(edges))
    common = np.count_nonzero(ref_edges * edges)
    assert min_count / common > 0.5


if __name__ == "__main__":
    test_align_samples()
