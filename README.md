# IMage ALIGN

Align source image with a reference image using OpenCV SIFT algorithm.

## Motivation

The task of aligning an image obtained by digitising a negative or slide with a direct digital capture of the same scene is often encountered in hybrid film/digital photography workflow. The applications include calibration of negative inversion algorithms or characterising film materials. Generally, the reference and source images have different resolution, aspect ratios, angle of view and can have a slight tilt. A script was needed that can perform this aligning task automatically.

## Installation

The `imalign` package is available from PyPI and can be installed by pip:

```bash
pip install imalign
```

## Usage

Once installed, the `imalign` script should be available in your terminal. Run

```bash
imalign --help
```

to see the list of command line arguments.

## Examples

[Sample images](https://github.com/vintage-camera-pictures/imalign/tree/main/imalign/tests/samples) are included in the source repository. They include a processed [laboratory scan](https://github.com/vintage-camera-pictures/imalign/blob/main/imalign/tests/samples/lab.jpg) of a film negative and a [DSLR capture](https://github.com/vintage-camera-pictures/imalign/blob/main/imalign/tests/samples/dslr.jpg) of the same frame on the light table.

![Laboratory Scan](https://github.com/vintage-camera-pictures/imalign/blob/main/imalign/tests/samples/lab.jpg?raw=true "Processed Lab Scan")

![DSLR Capture](https://github.com/vintage-camera-pictures/imalign/blob/main/imalign/tests/samples/dslr.jpg?raw=true "DSLR Capture")

The DSLR image is a horizontally flipped negative that includes frame borders, parts of the film holder and fragments of adjacent frames.

Running the command:

```bash
imalign --reference=tests/samples/lab.jpg
--source=tests/samples/dslr.jpg
--output=tests/samples/aligned.jpg
--trimmed=tests/samples/trimmed.jpg
--border=0.05
--invert-source
--flip
```

Produces these two images:

![Trimmed Laboratory Scan](https://github.com/vintage-camera-pictures/imalign/blob/main/imalign/tests/samples/trimmed.jpg?raw=true "Trimmed Lab Scan")

![Aligned Image](https://github.com/vintage-camera-pictures/imalign/blob/main/imalign/tests/samples/aligned.jpg?raw=true "Aligned Image")

Note, that the aligned image is flipped but not converted to positive.
