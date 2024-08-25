# Function to extract features from binary images
import os

import cv2
import numpy as np
from keras.src.utils import img_to_array
# from keras.src.utils import img_to_array

# from skimage.feature import graycomatrix, graycoprops
# from keras.src.utils import img_to_array
from skimage.feature.texture import graycomatrix, graycoprops
from skimage.io import imread
# from skimage.measure import shannon_entropy

from decimal import Decimal

from skimage.measure.entropy import shannon_entropy
from sklearn.metrics import confusion_matrix

# IMG_SIZE = 256
IMG_SIZE = 128


def extract_features(image):
    # Example: Using Grey Level Co-occurrence Matrix (GLCM) and Shannon Entropy
    glcm = graycomatrix(image, distances=[1], angles=[0], levels=2 ** 8, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    entropy = shannon_entropy(image)
    return [contrast, homogeneity, entropy]


def load_binary_images(data_path):
    images = []
    for img_file in os.listdir(data_path):
        if img_file.endswith('.jpg') or \
                img_file.endswith('.png') or \
                img_file.endswith('.jpeg') or \
                img_file.endswith('.bmp'):
            img = imread(os.path.join(data_path, img_file))
            img = np.expand_dims(img, axis=-1)
            images.append(img)

    return np.array(images)


# Function to load binary images
def load_binary_images_and_labels(data_path):
    images = []
    labels = []
    for img_file in os.listdir(os.path.join(data_path, "images")):
        if img_file.endswith('.jpg') or \
                img_file.endswith('.png') or \
                img_file.endswith('.jpeg') or \
                img_file.endswith('.bmp'):
            # Load binary images and extract features
            img = imread(os.path.join(data_path, "images", img_file), as_gray=True)
            features = extract_features(img)
            images.append(img)

            # Load corresponding labeled masks
            mask = imread(
                os.path.join(data_path, "labels",
                             img_file.replace('.jpg', '.png')))  # Assuming masks end with '_mask.png'
            mask = np.expand_dims(mask, axis=-1)
            labels.append(mask)
    return np.array(images), np.array(labels)


def load_data(train_images: [], train_labels: [], mask_as_gray=True, default_size=True):
    try:
        images = []
        labels = []
        for i in range(len(train_images)):
            img = cv2.imread(train_images[i])
            if default_size:
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            img_array = img_to_array(img) / 255.0
            images.append(img_array)

            mask_array = None
            if mask_as_gray:
                # mask_array = imread(train_labels[i], as_gray=True)
                mask = cv2.imread(train_labels[i], cv2.IMREAD_GRAYSCALE)
                if default_size:
                    mask_array = mask = cv2.resize(mask, (IMG_SIZE, IMG_SIZE))
                mask_array = mask
            else:
                mask = cv2.imread(train_labels[i])
                if default_size:
                    mask = cv2.resize(mask, (IMG_SIZE, IMG_SIZE))
                mask_array = img_to_array(mask) / 255.0
            labels.append(mask_array)
    except Exception as e:
        print(str(e))
        # log_message("data_handling->load_data", get_dataset_identifier(train_images[0]), str(e))

    return np.array(images), np.array(labels)


def get_scores(test_labels, predictions) -> dict:
    # Flatten the arrays for computation
    test_labels_flat = test_labels.flatten()
    predictions_flat = predictions.flatten()

    # Calculate confusion matrix components
    tn = 'nan'
    fp = 'nan'
    fn = 'nan'
    tp = 'nan'
    precision = 'nan'
    recall = 'nan'
    accuracy = 'nan'
    mcc = 'nan'
    f1 = 'nan'
    iou = 'nan'
    try:
        # tn, fp, fn, tp = confusion_matrix(test_labels_flat, predictions_flat).ravel()
        # Flatten the arrays for computation
        test_labels_flat = test_labels.flatten()
        predictions_flat = predictions.flatten()

        # Calculate confusion matrix
        cm = confusion_matrix(test_labels_flat, predictions_flat)

        # Calculate TP, TN, FP, FN for each class
        tp = cm[0][0]
        fn = cm[0][1]
        fp = cm[1][0]
        tn = cm[1][1]

        # Compute metrics based on TP, TN, FP, FN
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        # Compute MCC
        numerator = Decimal(float(tp * tn)) - Decimal(float(fp * fn))
        denominator = Decimal(float(tp + fp) * float(tp + fn) * float(tn + fp) * float(tn + fn))
        mcc = 0
        if denominator > 0:
            mcc = numerator / Decimal(np.sqrt(float(denominator)))
        # Compute F1-score
        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        # Compute IoU
        iou = tp / (tp + fp + fn) if (tp + fp + fn) != 0 else 0

        """
        Weighted Scores
        NOT USED for computation - instead nan is returned
        ---
        accuracy = accuracy_score(test_labels_flat, predictions_flat)
        mcc = matthews_corrcoef(test_labels_flat, predictions_flat)
        f1 = fbeta_score(test_labels_flat, predictions_flat, average='weighted', beta=1.0)
        iou = jaccard_score(test_labels_flat, predictions_flat, average='weighted')
        """
    except Exception as e:
        print(str(e))
        # log_message("utils->get_scores", "", str(e))

    # Store scores in a dictionary
    scores = {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "mcc": mcc,
        "f1": f1,
        "jaccard": iou,
        "accuracy": accuracy
    }

    return scores
