!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="Lxj2RgktXE7rOB1kVn3T")
project = rf.workspace("roboflow-jvuqo").project("football-ball-detection-rejhg")
version = project.version(1)
dataset = version.download("yolov8")

import cv2
import numpy as np
import os
from google.colab.patches import cv2_imshow

# 1. Klasör yolu
dataset_path = "/content/football-ball-detection-1/train/images" 
img_list = sorted(os.listdir(dataset_path))

# 2. HASSAS AYARLAR
segmenter = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=45, detectShadows=False)

# 3. Video Kayıt Ayarları
ornek_kare = cv2.imread(os.path.join(dataset_path, img_list[0]))
yukseklik, genislik, _ = ornek_kare.shape

# FPS: 10.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video_yazici = cv2.VideoWriter('futbol_segmentasyon_final.mp4', fourcc, 10.0, (genislik * 2, yukseklik))

print("İşlem başlıyor... Boyutu küçük tutmak için video kısa tutulacaktır.")

# --- KISALTMA DÖNGÜSÜ ---
# len(img_list) yerine 60 yazarak videoyu ilk 60 karede bitiriyoruz.
for i in range(len(img_list)):
    if i >= 60: # BURASI VİDEOYU KISALTIYOR (60 kare = 6 saniye)
        break
        
    frame = cv2.imread(os.path.join(dataset_path, img_list[i]))
    if frame is None: continue

    # MASKELME
    mask = segmenter.apply(frame)

    # 4. FUTBOLCULARI BEMBEYAZ YAPMA VE GENİŞLETME
    kernel_small = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small)
    
    kernel_big = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel_big, iterations=2)

    # GÖRSELLEŞTİRME
    mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    result = np.hstack((frame, mask_color))

    # VİDEOYA YAZ
    video_yazici.write(result)

    if i % 20 == 0:
        print(f"Kare {i} işlendi...")

video_yazici.release()
print("\nTAMAMLANDI! 'futbol_segmentasyon_final.mp4' dosyasını indirebilirsin.")