import argparse
import os
import imageio.v3 as iio
from align import align

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Align and resize DSLR capture to match lab-scanned image")
    parser.add_argument("--reference",
                        type=str,
                        help="file name of reference image",
                        required=True)
    parser.add_argument("--source",
                        type=str,
                        help="name of the source image",
                        required=True)
    parser.add_argument("--output",
                        type=str,
                        help="name of output aligned and resized file",
                        required=True)
    parser.add_argument("--trimmed",
                        type=str,
                        help="(optional) name of output file for the reference image with the borders removed."
                             " If not provided the trimmed image is not saved.",
                        default="",
                        required=False)
    parser.add_argument("--border",
                        type=float,
                        help="(optional) fraction of the max(height, width) of the reference image to define"
                             " the border, from 0.0 to 0.33. Default is 0.05",
                        default=0.05,
                        required=False)
    parser.add_argument("--invert-source",
                        help="(optional) convert the source image from negative to positive. Disabled by default.",
                        action="store_true")
    parser.add_argument("--flip",
                        help="(optional) flip the source image horizontally. Disabled by default.",
                        action="store_true")

    args = parser.parse_args()

    if not os.path.isfile(args.reference):
        print(f'Unable to find reference file "{args.reference}"')
        exit(1)

    if not os.path.isfile(args.source):
        print(f'Unable to find source image file "{args.source}"')
        exit(2)

    ref = iio.imread(args.reference)
    src = iio.imread(args.source)

    if args.flip:
        if len(src.shape) == 2:
            src = src[:, ::-1]
        elif len(src.shape) == 3:
            src = src[:, ::-1, :]
        else:
            print(f"Invalid source image shape {src.shape}. "
                  f"Only two-dimensional grayscale or three-dimensional RGB images are supported")

    aligned, trimmed = align(reference=ref,
                             source=src,
                             invert_source=args.invert_source,
                             border=args.border)

    iio.imwrite(args.output, aligned)
    if args.trimmed != "":
        iio.imwrite(args.trimmed, trimmed)
