from ultralytics import YOLO
import cv2
import winsound  

model = YOLO("yolov8n.pt")  

model.train(
    data="D:\Animal detection on railway track\animals-detection.v3i.yolov8\data.yaml",
    epochs=50,        
    imgsz=640,        
    batch=8,          
    device="cuda"  
)

print("Training Completed!")

model_path = r"D:\Animal detection on railway track\Animal code\runs\detect\train\weights\best.pt"
model = YOLO(model_path)

CONFIDENCE_THRESHOLD = 0.6  

cap = cv2.VideoCapture(0)  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    results = model(frame)

    animal_detected = False  


    for result in results:
        for box in result.boxes:
            conf = box.conf[0].item()  
            label = result.names[int(box.cls[0].item())] 
            
            if conf > CONFIDENCE_THRESHOLD:
                animal_detected = True  
        

        frame = result.plot()


    if animal_detected:
        print("⚠️ Animal detected on the railway track!")
        winsound.Beep(1000, 500) 
        

    cv2.imshow("Live Animal/Person Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):  
        break

cap.release()
cv2.destroyAllWindows()
