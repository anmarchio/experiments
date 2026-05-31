import io
import numpy as np

import cv2

from skimage.segmentation import slic
from skimage.measure import label as connected_components
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


def texture_features(image, distances=(1,), angles=(0, np.pi / 4, np.pi / 2, 3 * np.pi / 4)):
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