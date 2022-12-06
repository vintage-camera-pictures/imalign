import cv2
import numpy as np


def to_uint8(im):
    if im.dtype == np.uint8:
        return im

    if im.dtype == np.uint16:
        scaled = im / 257
        return scaled.astype(np.uint8)

    if im.dtype == float:
        scaled = 255 * im
        return scaled.astype(np.uint8)

    raise RuntimeError(f"Unsupported data type {im.dtype}")


def align(reference,
          source,
          border=0.0,
          invert_source=False):
    if len(reference.shape) == 3:
        ref_mono = cv2.cvtColor(reference, cv2.COLOR_RGB2GRAY)
    else:
        ref_mono = reference

    if len(source.shape) == 3:
        src_mono = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    else:
        src_mono = source

    ref_mono = to_uint8(ref_mono)
    src_mono = to_uint8(src_mono)

    if invert_source:
        src_mono = 255 - src_mono

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(ref_mono, None)
    kp2, des2 = sift.detectAndCompute(src_mono, None)

    flann_index_kdtree = 1
    index_params = {"algorithm": flann_index_kdtree, "trees": 5}
    search_params = {"checks": 50}
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # Find transform from reference image to the source
    inverse, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w = ref_mono.shape[:2]
    offset = int(border * max(h, w))
    offset = max(offset, 0)
    pts = np.float32([[offset, offset],
                      [offset, h - offset],
                      [w - offset, h - offset],
                      [w - offset, offset]]).reshape(-1, 1, 2)

    dst = cv2.perspectiveTransform(pts, inverse)
    x0 = int(np.round(np.min(dst[:, :, 0])))
    x1 = int(np.round(np.max(dst[:, :, 0])))
    y0 = int(np.round(np.min(dst[:, :, 1])))
    y1 = int(np.round(np.max(dst[:, :, 1])))

    # Find transform from the source image to the reference
    cropped_dst = dst_pts - dst[0, 0, :]
    cropped_src = src_pts - pts[0, 0, :]
    trans, _ = cv2.findHomography(cropped_dst, cropped_src, cv2.RANSAC, 5.0)

    target_shape = (w - 2 * offset, h - 2 * offset)
    transformed = cv2.warpPerspective(source[y0:y1, x0:x1, :], trans, target_shape, flags=cv2.INTER_LINEAR)

    if offset > 0:
        return transformed, reference[offset:-offset, offset:-offset, :]
    else:
        return transformed, reference
