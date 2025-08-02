from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import winsound
import time
from alerts import send_slack_alert  # Import Slack alert function

app = Flask(__name__)

# Load the trained YOLOv8 model (correct path to the model file)
model = YOLO(r"D:\Animal detection on railway track\Animal code\runs\detect\train\weights\best.pt")  # Adjust the path
CONFIDENCE_THRESHOLD = 0.3

# Open webcam feed
cap = cv2.VideoCapture(0)  # Ensure this opens the correct camera

# Cooldown variables to avoid spamming Slack alerts
last_alert_time = 0
ALERT_COOLDOWN = 60  # seconds between alerts

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

        results = model(frame)  # Pass the frame through the YOLO model
        animal_detected = False

        for result in results:
            for box in result.boxes:
                conf = box.conf[0].item()  # Get confidence of detection
                if conf > CONFIDENCE_THRESHOLD:
                    animal_detected = True

            frame = result.plot()  # Draw bounding boxes on the frame

        if animal_detected:
            cv2.putText(frame, "⚠️ Animal Detected!", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            winsound.Beep(1000, 500)

            if can_send_alert():
                send_slack_alert()  # Send Slack alert with cooldown

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
