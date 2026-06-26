# Edge Detection — Paperback Cover Splitting

## Overview

Split a full paperback cover image (back + spine + front) into 3 separate files using vertical edge detection.

## Recommended Package

**scikit-image** (`skimage`) — specifically `skimage.feature.canny`

### Installation

```bash
pip install scikit-image scipy numpy Pillow
```

## Method: Canny Edge Detection

### Why Canny?

- Detects sharp intensity gradients (color boundaries)
- The spine boundaries are vertical lines where the background color changes
- Canny produces clean 1-pixel-wide edges that can be strength-ranked
- Works regardless of spine color (dark, light, or any shade)

### Algorithm

1. **Load image** as numpy array (H × W × 3)
2. **Convert to grayscale** — average across RGB channels
3. **Apply Canny edge detection** — `feature.canny(gray, sigma=2, low_threshold=30, high_threshold=80)`
4. **Compute vertical edge strength** — for each column, fraction of rows that contain an edge pixel
5. **Smooth** the strength profile with a uniform filter (size=5)
6. **Find peaks** using `scipy.signal.find_peaks` with `distance=30` and `prominence=0.05`
7. **Select the two strongest peaks** separated by 30–250px as spine boundaries
8. **Split** the image into 3 parts using the two boundary columns

### Full Script

```python
import numpy as np
from PIL import Image
from skimage import feature
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks

def split_cover(image_path, output_dir):
    """Split a paperback cover image into back, spine, and front."""
    img = np.array(Image.open(image_path))
    h, w = img.shape[:2]

    # 1. Grayscale
    gray = img.mean(axis=2)

    # 2. Canny edge detection
    edges = feature.canny(gray, sigma=2, low_threshold=30, high_threshold=80)

    # 3. Vertical edge strength per column
    vertical_edge_strength = edges.mean(axis=0)
    smooth_strength = uniform_filter1d(vertical_edge_strength, size=5)

    # 4. Find peaks
    peaks, _ = find_peaks(smooth_strength, distance=30, prominence=0.05)

    # 5. Select two strongest peaks with reasonable separation (30–250px)
    sorted_peaks = peaks[np.argsort(smooth_strength[peaks])[::-1]]
    edge1, edge2 = None, None
    for i in range(len(sorted_peaks)):
        for j in range(i + 1, len(sorted_peaks)):
            sep = abs(sorted_peaks[i] - sorted_peaks[j])
            if 30 <= sep <= 250:
                edge1, edge2 = sorted([sorted_peaks[i], sorted_peaks[j]])
                break
        if edge1 is not None:
            break

    if edge1 is None:
        raise ValueError("Could not detect spine boundaries")

    spine_start, spine_end = edge1, edge2

    # 6. Extract and save
    Image.fromarray(img[:, :spine_start, :]).save(f"{output_dir}/back_cover.png")
    Image.fromarray(img[:, spine_start:spine_end + 1, :]).save(f"{output_dir}/spine_cover.png")
    Image.fromarray(img[:, spine_end + 1:, :]).save(f"{output_dir}/front_cover.png")

    print(f"Back:  cols 0-{spine_start - 1} (width {spine_start})")
    print(f"Spine: cols {spine_start}-{spine_end} (width {edge2 - edge1 + 1})")
    print(f"Front: cols {spine_end + 1}-{w - 1} (width {w - edge2 - 1})")

# Usage
split_cover("Paperback image.png", ".")
```

## Parameters to Tune

| Parameter | Default | When to adjust |
|---|---|---|
| `sigma` | 2 | Increase for noisy images, decrease for fine detail |
| `low_threshold` | 30 | Lower to detect faint boundaries |
| `high_threshold` | 80 | Lower if edges are not detected |
| `distance` (peaks) | 30 | Increase if spine is wide |
| `prominence` (peaks) | 0.05 | Increase to filter weak edges |
| Separation range | 30–250px | Adjust for unusual spine widths |

## Why Other Methods Failed

| Method | Problem |
|---|---|
| Brightness thresholding | Fails with varying lighting in 3D mockup photos |
| Color clustering (k-means) | Groups by color, not by spatial continuity |
| Otsu on L-channel | Picks up dark content, not spine |
| Column std deviation | Finds uniform columns, not boundaries |
| Horizontal gradient | Picks up text/design edges on covers |

## Key Insight

The spine boundary is a **vertical line where the background color changes**. Canny detects this as a strong vertical edge. The two strongest vertical edges (separated by 30–250px) are the spine boundaries. This works regardless of whether the spine is dark, light, or any color — it only requires a color difference between the spine and the adjacent covers.
