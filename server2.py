from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import pyttsx3
from threading import Thread, Lock
from queue import PriorityQueue
import time

app = FastAPI()

# Load YOLO11m model once at startup
print("Loading YOLO11m model...")
model = YOLO('yolo11m.pt')
print("Model loaded successfully!")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)
tts_engine.setProperty('volume', 1.0)

# Thread-safe alert queue and lock
alert_queue = PriorityQueue()
tts_lock = Lock()
last_alerts = {}  # Track last alert time for each object class

# Define priority levels (lower number = higher priority)
PRIORITY_LEVELS = {
    "train": 1,      # CRITICAL - immediate danger
    "truck": 2,      # HIGH - large vehicle
    "bus": 2,        # HIGH - large vehicle
    "car": 3,        # MEDIUM - vehicle
    "motorcycle": 3, # MEDIUM - vehicle
    "bicycle": 3,    # MEDIUM - moving obstacle
    "bench": 4,      # LOW - stationary, informational
    "chair": 4,      # LOW - stationary, informational
    "bed": 4,        # LOW - stationary, informational
    "couch": 4,      # LOW - stationary, informational
    "banana": 5      # LOWEST - fun/informational
}

# Custom alert messages
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

# Alert cooldown period (seconds) - prevents repeating same alert too quickly
ALERT_COOLDOWN = {
    1: 2,   # Critical: 2 seconds
    2: 3,   # High: 3 seconds
    3: 4,   # Medium: 4 seconds
    4: 8,   # Low: 8 seconds
    5: 10   # Lowest: 10 seconds
}

def should_alert(object_class, priority):
    """Check if enough time has passed since last alert for this object"""
    current_time = time.time()
    
    if object_class not in last_alerts:
        last_alerts[object_class] = current_time
        return True
    
    time_since_last = current_time - last_alerts[object_class]
    cooldown = ALERT_COOLDOWN.get(priority, 5)
    
    if time_since_last >= cooldown:
        last_alerts[object_class] = current_time
        return True
    
    return False

def speak_alert(priority, message, object_class):
    """Speak alert with priority handling"""
    def _speak():
        with tts_lock:
            # Add slight pause for critical alerts
            if priority == 1:
                tts_engine.say("ALERT!")
                tts_engine.runAndWait()
                time.sleep(0.2)
            
            tts_engine.say(message)
            tts_engine.runAndWait()
    
    Thread(target=_speak, daemon=True).start()

def process_alert_queue():
    """Background thread to process alerts from queue"""
    while True:
        if not alert_queue.empty():
            priority, timestamp, object_class, message = alert_queue.get()
            
            if should_alert(object_class, priority):
                print(f"🔊 [{priority}] {message}")
                speak_alert(priority, message, object_class)
            else:
                print(f"⏭️  Skipped (cooldown): {object_class}")
        
        time.sleep(0.1)

# Start background alert processor
Thread(target=process_alert_queue, daemon=True).start()

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
                bbox = box.xyxy[0].tolist()
                
                detection = {
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": bbox
                }
                all_detections.append(detection)
                
                # Check if this is a priority object
                if class_name in ALERT_MESSAGES and confidence > 0.3:
                    priority = PRIORITY_LEVELS.get(class_name, 5)
                    alert_message = ALERT_MESSAGES[class_name]
                    
                    # Add to priority queue (lower priority number = processed first)
                    alert_queue.put((
                        priority,
                        time.time(),
                        class_name,
                        alert_message
                    ))
                    
                    priority_alerts.append({
                        "class": class_name,
                        "message": alert_message,
                        "confidence": confidence,
                        "priority": priority,
                        "bbox": bbox
                    })
        
        # Sort priority alerts by urgency for response
        priority_alerts.sort(key=lambda x: x['priority'])
        
        return JSONResponse(content={
            "success": True,
            "total_detections": len(all_detections),
            "priority_alerts": priority_alerts,
            "all_detections": all_detections,
            "alert_queue_size": alert_queue.qsize()
        })
        
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/")
async def root():
    return {
        "message": "Sense-Aid YOLO11 Detection Server with Smart Alert Handling",
        "monitored_objects": list(ALERT_MESSAGES.keys()),
        "priority_levels": PRIORITY_LEVELS
    }

@app.get("/stats")
async def get_stats():
    """Get current alert system statistics"""
    return {
        "alert_queue_size": alert_queue.qsize(),
        "recent_alerts": {k: time.time() - v for k, v in last_alerts.items()},
        "cooldown_periods": ALERT_COOLDOWN
    }

if __name__ == "__main__":
    print("Starting Sense-Aid server with priority-based alert handling")
    print(f"Monitoring {len(ALERT_MESSAGES)} priority objects")
    print("\nPriority Levels:")
    for obj, pri in sorted(PRIORITY_LEVELS.items(), key=lambda x: x[1]):
        print(f"  [{pri}] {obj}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
