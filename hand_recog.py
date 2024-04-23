import time
import cv2
import mediapipe as mp
import urllib.request
import numpy as np
# from facial_recognition_module import perform_facial_recognition

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, track_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, int(self.detection_confidence), self.track_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if draw:
            if self.results.multi_hand_landmarks:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), -1)
        return lm_list

def facial_recognition(frame):
    print("FACE RECOG")
def object_recognition():
    print("OBJ RECOG")
# def facial_recognition(frame):
#     perform_facial_recognition(frame) 

def main():
    tasks={1:"Facial Recognition",2:"Object Recognition"}
    detector = HandDetector()
    tip_ids = [4, 8, 12, 16, 20]
    url='http://192.168.137.68/cam-hi.jpg'
    pause=False
    while True:
        img_resp = urllib.request.urlopen(url)
        img_np=np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, -1)
        # frame = cv2.flip(frame, 0)
        if not pause:
            img = detector.find_hands(frame)
            lm_list = detector.find_position(img, draw=False)
            if len(lm_list) != 0:
                fingers = []

                if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = fingers.count(1)
                # print("Total fingers:", total_fingers)
                if total_fingers==1:
                    # print(frame)
                    print("FACE DET")
                    time.sleep(5)
                    img_resp = urllib.request.urlopen(url)
                    img_np=np.array(bytearray(img_resp.read()), dtype=np.uint8)
                    frame = cv2.imdecode(img_np, -1)
                    frame = cv2.flip(frame, 0)
                    direc="C:\\Users\\Anirudh\\Documents\\Hand1\\imgs\\"
                    file_name='haha.jpg'
                    path= direc + file_name
                    cv2.imwrite(path, frame)
                    pause=True
        else:
            cv2.putText(frame,"Busy",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.imshow('preview',frame)
            cv2.waitKey(10000)
            pause=False
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    
    