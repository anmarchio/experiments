# Function to extract features from binary images
import os
from decimal import Decimal

import cv2
import numpy as np
# from skimage.feature import graycomatrix, graycoprops
from skimage.feature.texture import graycomatrix, graycoprops
from skimage.io import imread
from skimage.measure.entropy import shannon_entropy
from sklearn.metrics import confusion_matrix

# from skimage.measure import shannon_entropy

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

            #img_array = img_to_array(img) / 255.0
            #images.append(img_array)
            images.append(img)

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
                #mask_array = img_to_array(mask) / 255.0
                mask_array = mask
            labels.append(mask_array)
    except Exception as e:
        print(str(e))
        # log_message("data_handling->load_data", get_dataset_identifier(train_images[0]), str(e))

    return np.array(images), np.array(labels)


from PIL import Image


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            img = Image.open(os.path.join(folder, filename)).convert('L')
            img = img.resize(size=(IMG_SIZE, IMG_SIZE), resample=None)
            img_array = np.array(img)

            # Convert the image to a binary array (0 for black, 1 for white)
            binary_array = np.where(img_array > 0, 1, 0)
            images.append(binary_array.flatten())
    return np.array(images)


def calculate_metrics(ground_truth_path, prediction_path):
    # Load images from both folders
    ground_truth_images = load_images_from_folder(ground_truth_path)
    prediction_images = load_images_from_folder(prediction_path)

    ground_truth_images_flat = ground_truth_images.flatten()
    prediction_images_flat = prediction_images.flatten()

    # Initialize accumulators for metrics
    tp_total = fp_total = tn_total = fn_total = 0.0

    # Iterate over the image pairs
    for gt, pred in zip(ground_truth_images_flat, prediction_images_flat):
        # Calculate TP, FP, TN, FN
        tp = np.sum((gt > 0) & (pred > 0))
        fp = np.sum((gt == 0) & (pred > 0))
        tn = np.sum((gt == 0) & (pred == 0))
        fn = np.sum((gt > 0) & (pred == 0))

        # Accumulate totals
        tp_total += float(tp)
        fp_total += float(fp)
        tn_total += float(tn)
        fn_total += float(fn)

    # Compute metrics based on TP, TN, FP, FN
    accuracy = 0.0
    acc_sum = float(tp_total + tn_total + fp_total + fn_total)
    if acc_sum > 0:
        accuracy = float(tp_total + tn_total) / acc_sum
    # Compute MCC
    numerator = Decimal(float(tp_total * tn_total)) - Decimal(float(fp_total * fn_total))
    denominator = Decimal(float(tp_total + fp_total) * float(tp_total + fn_total) * float(tn_total + fp_total) * float(tn_total + fn_total))
    mcc = 0.0
    if denominator > 0.0:
        mcc = numerator / Decimal(np.sqrt(float(denominator)))
    # Compute F1-score
    precision = tp_total / (tp_total + fp_total) if (tp_total + fp_total) != 0 else 0.0
    recall = tp_total / (tp_total + fn_total) if (tp_total + fn_total) != 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0.0
    # Compute IoU
    iou = tp_total / (tp_total + fp_total + fn_total) if (tp_total + fp_total + fn_total) != 0 else 0.0

    scores = {
        "tp": tp_total,
        "tn": tn_total,
        "fp": fp_total,
        "fn": fn_total,
        "precision": precision,
        "recall": recall,
        "mcc": mcc,
        "f1": f1,
        "jaccard": iou,
        "accuracy": accuracy
    }

    return scores


def get_scores_depr(test_labels, predictions) -> dict:
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
        mcc = 0.0
        if denominator > 0.0:
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
