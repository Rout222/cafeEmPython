import sys
import cv2
import numpy as np
from scipy.ndimage import label
import lib
teste = cv2.imread("./asdadsa.jpg") if cv2.imread("./asdadsa.jpg") is not None else 0
print(teste)