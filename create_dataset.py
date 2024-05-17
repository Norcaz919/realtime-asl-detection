import os
import pickle
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './dataV2'

data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    class_dir = os.path.join(DATA_DIR, dir_)
    for img_path in os.listdir(class_dir):
        if img_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            data_aux = []
            img = cv2.imread(os.path.join(class_dir, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x)
                        data_aux.append(y)
                # Ensure each feature vector has the expected length (21 landmarks * 2 coordinates)
                if len(data_aux) == 42:
                    data.append(data_aux)
                    labels.append(dir_)

with open('dataV2.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print('Dataset successfully created.')
