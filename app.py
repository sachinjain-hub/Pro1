from flask import Flask, render_template, request
import cv2
import numpy as np
import mediapipe as mp
import base64

app = Flask(__name__)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
drawing_utils = mp.solutions.drawing_utils

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.files['frame'].read()
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            drawing_utils.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    _, jpeg = cv2.imencode('.jpg', img)
    return base64.b64encode(jpeg).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
