# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# import uvicorn
# from ultralytics import YOLO
# from PIL import Image
# from io import BytesIO
# import pyttsx3
# from threading import Thread

# app = FastAPI()

# # Load YOLO11m model once at startup
# print("Loading YOLO11m model...")
# model = YOLO('yolo11m.pt')
# print("Model loaded successfully!")

# # Initialize text-to-speech engine
# tts_engine = pyttsx3.init()
# tts_engine.setProperty('rate', 150)  # Speech speed
# tts_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# # Define priority objects and their custom messages
# ALERT_MESSAGES = {
#     "bicycle": "Bicycle on way. STOP!",
#     "car": "Car coming! Move back.",
#     "motorcycle": "Motorbike on way. STOP!",
#     "bus": "Bus coming. Move back!",
#     "train": "Train en route. MOVE BACK IMMEDIATELY!",
#     "truck": "Truck coming. Move back!",
#     "bench": "Bench detected. May sit down.",
#     "chair": "Chair detected. May sit down.",
#     "bed": "Bed detected. May take rest.",
#     "couch": "Couch detected. May take rest.",
#     "banana": "Banana!! YAY!!"
# }

# def speak_alert(message):
#     """Speak the alert message in a separate thread"""
#     def _speak():
#         tts_engine.say(message)
#         tts_engine.runAndWait()
    
#     Thread(target=_speak, daemon=True).start()

# @app.post("/detect")
# async def detect_objects(file: UploadFile = File(...)):
#     try:
#         # Read image from upload
#         contents = await file.read()
#         img = Image.open(BytesIO(contents)).convert('RGB')
        
#         # Run YOLO11 inference
#         results = model(img)
        
#         # Parse detections and filter for priority objects
#         all_detections = []
#         priority_alerts = []
        
#         for result in results:
#             boxes = result.boxes
#             for box in boxes:
#                 class_name = model.names[int(box.cls[0])]
#                 confidence = float(box.conf[0])
                
#                 detection = {
#                     "class": class_name,
#                     "confidence": confidence,
#                     "bbox": box.xyxy[0].tolist()
#                 }
#                 all_detections.append(detection)
                
#                 # Check if this is a priority object
#                 if class_name in ALERT_MESSAGES and confidence > 0.5:
#                     alert_message = ALERT_MESSAGES[class_name]
#                     priority_alerts.append({
#                         "class": class_name,
#                         "message": alert_message,
#                         "confidence": confidence
#                     })
                    
#                     # Speak the alert
#                     print(f"🔊 Alert: {alert_message}")
#                     speak_alert(alert_message)
        
#         return JSONResponse(content={
#             "success": True,
#             "total_detections": len(all_detections),
#             "priority_alerts": priority_alerts,
#             "all_detections": all_detections
#         })
        
#     except Exception as e:
#         return JSONResponse(content={
#             "success": False,
#             "error": str(e)
#         }, status_code=500)

# @app.get("/")
# async def root():
#     return {
#         "message": "Sense-Aid YOLO11 Detection Server with Audio Alerts",
#         "monitored_objects": list(ALERT_MESSAGES.keys())
#     }

# @app.get("/alerts")
# async def get_alert_list():
#     """Endpoint to see all configured alerts"""
#     return {"alert_messages": ALERT_MESSAGES}

# if __name__ == "__main__":
#     print("Starting Sense-Aid server with audio alerts on http://0.0.0.0:8000")
#     print(f"Monitoring {len(ALERT_MESSAGES)} priority objects")
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import pyttsx3
from threading import Thread

app = FastAPI()

# Load YOLO11m model once at startup
print("Loading YOLO11m model...")
model = YOLO('yolo11m.pt')
print("Model loaded successfully!")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Speech speed
tts_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Define priority objects and their custom messages
ALERT_MESSAGES = {
    "bicycle": "Bicycle on way. STOP!",
    "car": "Car coming! Move back.",
    "motorcycle": "Motorbike on way. STOP!",
    "bus": "Bus coming. Move back!",
    "train": "Train en route. MOVE BACK IMMEDIATELY!",
    "truck": "Truck coming. Move back!",
    "bench": "Bench detected. May sit down.",
    "chair": "Chair detected. May sit down.",
    "bed": "Bed detected. May take rest.",
    "couch": "Couch detected. May take rest.",
    "banana": "Banana!! YAY!!"
}

def speak_alert(message):
    """Speak the alert message in a separate thread"""
    def _speak():
        tts_engine.say(message)
        tts_engine.runAndWait()
    
    Thread(target=_speak, daemon=True).start()

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    try:
        # Read image from upload
        contents = await file.read()
        img = Image.open(BytesIO(contents)).convert('RGB')
        
        # Run YOLO11 inference
        results = model(img)
        
        # Parse detections and filter for priority objects
        all_detections = []
        priority_alerts = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_name = model.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                
                detection = {
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": box.xyxy[0].tolist()
                }
                all_detections.append(detection)
                
                # Check if this is a priority object
                if class_name in ALERT_MESSAGES and confidence > 0.5:
                    alert_message = ALERT_MESSAGES[class_name]
                    priority_alerts.append({
                        "class": class_name,
                        "message": alert_message,
                        "confidence": confidence
                    })
                    
                    # Speak the alert
                    print(f"🔊 Alert: {alert_message}")
                    speak_alert(alert_message)
        
        return JSONResponse(content={
            "success": True,
            "total_detections": len(all_detections),
            "priority_alerts": priority_alerts,
            "all_detections": all_detections
        })
        
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/")
async def root():
    return {
        "message": "Sense-Aid YOLO11 Detection Server with Audio Alerts",
        "monitored_objects": list(ALERT_MESSAGES.keys())
    }

@app.get("/alerts")
async def get_alert_list():
    """Endpoint to see all configured alerts"""
    return {"alert_messages": ALERT_MESSAGES}

if __name__ == "__main__":
    print("Starting Sense-Aid server with audio alerts on http://0.0.0.0:8000")
    print(f"Monitoring {len(ALERT_MESSAGES)} priority objects")
    uvicorn.run(app, host="0.0.0.0", port=8000)
