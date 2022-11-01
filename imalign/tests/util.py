import numpy as np
import cv2


def generate_samples(height, width, num_points, angle, offset_x, offset_y, scale,
                     padding=0.25,
                     seed=4756483):
    np.random.seed(seed)
    reference = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    ind_h = np.random.randint(low=height // 4, high=3 * height // 4, size=num_points)
    ind_w = np.random.randint(low=width // 4, high=3 * width // 4, size=num_points)
    rgb = np.random.randint(low=0, high=256, size=(num_points, 3))
    reference[ind_h, ind_w, :] = rgb

    resized = cv2.resize(reference, (scale*width, scale*height), interpolation=cv2.INTER_NEAREST)
    border = int(padding * np.max(resized.shape[:2]))
    padded = cv2.copyMakeBorder(resized,
                                top=border,
                                bottom=border,
                                left=border,
                                right=border,
                                borderType=cv2.BORDER_CONSTANT,
                                value=0)

    h, w = padded.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D(center=(w // 2, h // 2), angle=angle, scale=1)
    transformed = cv2.warpAffine(padded,
                                 M=rotation_matrix,
                                 dsize=(w, h))

    translation_matrix = np.float32([[1.0, 0.0, scale * offset_x],
                                     [0.0, 1.0, scale * offset_y]])
    transformed = cv2.warpAffine(transformed,
                                 M=translation_matrix,
                                 dsize=(w, h))

    return reference, ind_h, ind_w, transformed
