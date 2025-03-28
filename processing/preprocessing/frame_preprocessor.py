import cv2
import numpy as np
import json
import os

# Բեռնենք preprocessing կարգավորումները պահեստից
CONFIG_PATH = "data/warehouses/warehouse_001/config/preprocessing.json"

with open(CONFIG_PATH, "r") as f:
    pre_cfg = json.load(f)

def apply_clahe(frame):
    clahe = cv2.createCLAHE(
        clipLimit=pre_cfg["clahe"]["clipLimit"],
        tileGridSize=tuple(pre_cfg["clahe"]["tileGridSize"])
    )
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

def adjust_gamma(frame, gamma=None):
    if gamma is None:
        gamma = pre_cfg["gamma"]
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(frame, table)

def gaussian_blur(frame):
    k = tuple(pre_cfg["gaussian_blur"]["kernel"])
    return cv2.GaussianBlur(frame, k, 0)

def resize_frame(frame):
    target_width = pre_cfg["resize"]["width"]
    preserve_aspect = pre_cfg["resize"]["preserve_aspect"]

    if not preserve_aspect:
        return cv2.resize(frame, (target_width, target_width))  # square

    h, w = frame.shape[:2]
    aspect_ratio = h / w
    target_height = int(target_width * aspect_ratio)
    return cv2.resize(frame, (target_width, target_height))

def preprocess_frame(frame):
    frame = apply_clahe(frame)
    frame = adjust_gamma(frame)
    frame = gaussian_blur(frame)
    frame = resize_frame(frame)
    return frame
