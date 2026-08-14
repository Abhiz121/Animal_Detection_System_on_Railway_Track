import os
from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import winsound
import time
from alerts import send_slack_alert

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = YOLO(os.path.join(BASE_DIR, "runs", "detect", "train", "weights", "best.pt"))
CONFIDENCE_THRESHOLD = 0.3

cap = cv2.VideoCapture(0)

last_alert_time = 0
ALERT_COOLDOWN = 60

def can_send_alert():
    global last_alert_time
    current_time = time.time()
    if current_time - last_alert_time > ALERT_COOLDOWN:
        last_alert_time = current_time
        return True
    return False

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        animal_detected = False

        for result in results:
            for box in result.boxes:
                conf = box.conf[0].item()
                if conf > CONFIDENCE_THRESHOLD:
                    animal_detected = True

            frame = result.plot()

        if animal_detected:
            cv2.putText(frame, "⚠️ Animal Detected!", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            winsound.Beep(1000, 500)

            if can_send_alert():
                send_slack_alert()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
