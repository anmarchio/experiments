import io
import numpy as np

import cv2

from skimage.segmentation import slic
from skimage.measure import label as connected_components, shannon_entropy
from skimage.feature import graycomatrix, graycoprops
from PIL import Image

def _to_gray(image):
    """Convert image to grayscale uint8."""
    if image is None:
        raise ValueError("image must not be None")

    image = np.asarray(image)

    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()

    if gray.dtype != np.uint8:
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        gray = gray.astype(np.uint8)

    return gray


def rectangle_size(image):
    """
    Rectangle size RS = H * W.
    """
    h, w = image.shape[:2]
    return h * w


def shannon_entr(image, base=np.e):
    """
    Shannon entropy:
    S = -sum(p_k * log(p_k))
    """
    gray = _to_gray(image)

    hist, _ = np.histogram(gray.ravel(), bins=256, range=(0, 256), density=False)
    probs = hist / hist.sum()
    probs = probs[probs > 0]

    return float(-np.sum(probs * np.log(probs) / np.log(base)))


def histogram_entr(image):
    """
    Histogram entropy using log2:
    H(X) = -sum(p(x_i) * log2(p(x_i)))
    """
    return shannon_entr(image, base=2)


def variance_of_laplacian(image):
    """
    Variance of the Laplacian response.
    High values usually indicate sharper images.
    """
    gray = _to_gray(image)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())


def brightness_metric(image):
    """
    Brightness = average pixel intensity.
    """
    gray = _to_gray(image)
    return float(np.mean(gray))


def jpeg_complexity(image, quality=75):
    """
    JPEG-based complexity:
    JR = original_size / compressed_size

    Lower compression usually indicates higher visual complexity.
    """
    img = np.asarray(image)

    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    pil_img = Image.fromarray(img)

    raw_buffer = io.BytesIO()
    pil_img.save(raw_buffer, format="PNG")
    original_size = raw_buffer.tell()

    jpeg_buffer = io.BytesIO()
    pil_img.save(jpeg_buffer, format="JPEG", quality=quality)
    compressed_size = jpeg_buffer.tell()

    if compressed_size == 0:
        return np.inf

    return float(original_size / compressed_size)

def lbl_texture_features(label_mask):

    if label_mask is None:
        return 0.0

    mask = label_mask.astype(np.uint8)

    glcm = graycomatrix(
        mask,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True
    )

    contrast = graycoprops(glcm, "contrast")[0, 0]

    return float(contrast)

def texture_features(image):

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) \
        if image.ndim == 3 else image

    gray = gray.astype(np.uint8)

    glcm = graycomatrix(
        gray,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True
    )

    contrast = graycoprops(glcm, "contrast")[0, 0]

    return float(contrast)

def texture_all_features(image, distances=(1,), angles=(0, np.pi / 4, np.pi / 2, 3 * np.pi / 4)):
    """
    GLCM texture features:
    contrast, homogeneity, correlation, energy.
    """
    gray = _to_gray(image)

    glcm = graycomatrix(
        gray,
        distances=distances,
        angles=angles,
        levels=256,
        symmetric=True,
        normed=True
    )

    features = {
        "contrast": float(graycoprops(glcm, "contrast").mean()),
        "homogeneity": float(graycoprops(glcm, "homogeneity").mean()),
        "correlation": float(graycoprops(glcm, "correlation").mean()),
        "energy": float(graycoprops(glcm, "energy").mean()),
    }

    return features


def edge_density(image, threshold1=100, threshold2=200):
    """
    Edge density:
    ED = number_of_edge_pixels / image_area
    """
    gray = _to_gray(image)
    edges = cv2.Canny(gray, threshold1, threshold2)

    num_edges = np.count_nonzero(edges)
    area = rectangle_size(gray)

    return float(num_edges / area)


def number_of_superpixels(image, n_segments=100, compactness=10):
    """
    Compute SLIC superpixels and return the number of unique superpixel regions.
    """
    img = np.asarray(image)

    segments = slic(
        img,
        n_segments=n_segments,
        compactness=compactness,
        start_label=0,
        channel_axis=-1 if img.ndim == 3 else None
    )

    return int(len(np.unique(segments)))


def number_of_labels(label_mask, background=0):
    """
    Count connected label instances in a segmentation mask.

    If label_mask contains instance IDs, this counts unique non-background IDs.
    If label_mask is binary, this counts connected components.
    """
    label_mask = np.asarray(label_mask)

    unique_labels = np.unique(label_mask)
    unique_labels = unique_labels[unique_labels != background]

    if len(unique_labels) > 1:
        return int(len(unique_labels))

    binary = label_mask != background
    cc = connected_components(binary)

    return int(cc.max())


def run_compute_complexity(image, label_mask=None):
    """
    Compute all available complexity metrics for one image.
    """
    metrics = {
        "rectangle_size": rectangle_size(image),
        "shannon_entropy": shannon_entr(image),
        "histogram_entropy": histogram_entr(image),
        "variance_of_laplacian": variance_of_laplacian(image),
        "brightness": brightness_metric(image),
        "jpeg_complexity": jpeg_complexity(image),
        "texture_features": texture_features(image),
        "edge_density": edge_density(image),
        "number_of_superpixels": number_of_superpixels(image),
    }

    if label_mask is not None:
        metrics["number_of_labels"] = number_of_labels(label_mask)

    return metrics


def blurriness_metric(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def fractal_dimension(image, threshold=0.5):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image
    gray = gray.astype(np.float32)
    gray = (gray - gray.min()) / (gray.max() - gray.min() + 1e-8)

    binary = gray < threshold

    def boxcount(z, k):
        s = np.add.reduceat(
            np.add.reduceat(z, np.arange(0, z.shape[0], k), axis=0),
            np.arange(0, z.shape[1], k), axis=1
        )
        return np.count_nonzero((s > 0) & (s < k * k))

    min_dim = min(binary.shape)
    sizes = 2 ** np.arange(int(np.log2(min_dim)), 1, -1)

    counts = []
    valid_sizes = []

    for size in sizes:
        count = boxcount(binary, size)
        if count > 0:
            counts.append(count)
            valid_sizes.append(size)

    if len(counts) < 2:
        return 0.0

    coeffs = np.polyfit(np.log(valid_sizes), np.log(counts), 1)
    return float(-coeffs[0])


def label_size(label_mask):
    if label_mask is None:
        return 0.0

    mask = label_mask > 0
    return float(np.count_nonzero(mask))


def relative_label_size(label_mask):
    if label_mask is None:
        return 0.0

    mask = label_mask > 0
    return float(np.count_nonzero(mask) / mask.size)


def lbl_hist_entropy(label_mask):
    if label_mask is None:
        return 0.0

    return float(shannon_entropy(label_mask))


def lbl_fractal_dimension(label_mask):
    if label_mask is None:
        return 0.0

    return fractal_dimension(label_mask)


def lbl_texture_all_features(label_mask):
    if label_mask is None:
        return {
            "contrast": 0.0,
            "dissimilarity": 0.0,
            "homogeneity": 0.0,
            "energy": 0.0,
            "correlation": 0.0,
            "ASM": 0.0,
        }

    mask = label_mask.astype(np.uint8)

    if mask.max() > 0:
        mask = (mask / mask.max() * 255).astype(np.uint8)

    glcm = graycomatrix(
        mask,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True
    )

    return {
        "contrast": float(graycoprops(glcm, "contrast")[0, 0]),
        "dissimilarity": float(graycoprops(glcm, "dissimilarity")[0, 0]),
        "homogeneity": float(graycoprops(glcm, "homogeneity")[0, 0]),
        "energy": float(graycoprops(glcm, "energy")[0, 0]),
        "correlation": float(graycoprops(glcm, "correlation")[0, 0]),
        "ASM": float(graycoprops(glcm, "ASM")[0, 0]),
    }


def lbl_edge_density(label_mask):
    if label_mask is None:
        return 0.0

    mask = label_mask.astype(np.uint8)

    if mask.max() > 0:
        mask = (mask > 0).astype(np.uint8) * 255

    edges = cv2.Canny(mask, 100, 200)
    return float(np.count_nonzero(edges) / edges.size)


def lbl_laplacian_variance(label_mask):
    if label_mask is None:
        return 0.0

    mask = label_mask.astype(np.uint8)

    if mask.max() > 0:
        mask = (mask > 0).astype(np.uint8) * 255

    return float(cv2.Laplacian(mask, cv2.CV_64F).var())


def lbl_num_superpixels(label_mask, n_segments=100, compactness=10):
    if label_mask is None:
        return 0.0

    mask = label_mask.astype(np.float32)

    if mask.max() > 0:
        mask = mask / mask.max()

    segments = slic(
        mask,
        n_segments=n_segments,
        compactness=compactness,
        channel_axis=None,
        start_label=0
    )

    return float(len(np.unique(segments)))

def minmax_normalize(values):
    values = np.asarray(values, dtype=float)

    finite_mask = np.isfinite(values)
    result = np.zeros_like(values, dtype=float)

    if not np.any(finite_mask):
        return result.tolist()

    finite_values = values[finite_mask]
    vmin = finite_values.min()
    vmax = finite_values.max()

    if vmax == vmin:
        result[finite_mask] = 0.0
    else:
        result[finite_mask] = (finite_values - vmin) / (vmax - vmin)

    return result.tolist()


def normalize_metric_values(metric, values, image_area=None, n_segments=100):
    values = np.asarray(values, dtype=float)

    if metric in {
        "edge_density",
        "relative_label_size",
        "lbl_edge_density",
    }:
        return np.clip(values, 0.0, 1.0).tolist()

    if metric == "brightness_arr":
        return np.clip(values / 255.0, 0.0, 1.0).tolist()

    if metric == "entropy_arr":
        # shannon_entr uses natural log by default.
        # Max entropy for 8-bit grayscale is ln(256).
        return np.clip(values / np.log(256), 0.0, 1.0).tolist()

    if metric in {
        "hist_entropy",
        "lbl_hist_entropy",
    }:
        # histogram_entr uses log2.
        # Max entropy for 8-bit data is log2(256) = 8.
        return np.clip(values / 8.0, 0.0, 1.0).tolist()

    if metric in {
        "fractal_dimension",
        "lbl_fractal_dimension",
    }:
        # For 2D images, fractal dimension is usually interpreted in [1, 2].
        return np.clip(values - 1.0, 0.0, 1.0).tolist()

    if metric in {
        "label_size",
    } and image_area is not None:
        return np.clip(values / image_area, 0.0, 1.0).tolist()

    if metric in {
        "num_superpixels",
        "lbl_num_superpixels",
    }:
        return np.clip(values / n_segments, 0.0, 1.0).tolist()

    return minmax_normalize(values)