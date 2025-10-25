# import requests
# import os

# Server URL (use localhost if testing on same machine)
# SERVER_URL = "http://localhost:8000/detect"

# def test_detection(image_path):
#    """Send an image to the server and print detection results"""
#    
#    if not os.path.exists(image_path):
#        print(f"Error: Image file '{image_path}' not found!")
#        return
#    
#    print(f"\n{'='*50}")
#    print(f"Testing detection with: {image_path}")
#    print(f"{'='*50}\n")
#    
#    try:
#        # Open and send the image
#        with open(image_path, 'rb') as f:
#            response = requests.post(SERVER_URL, files={"file": f})
        
#        # Parse the response
#        result = response.json()
#        
#        if result['success']:
#            print(f"✓ Detection successful!")
#            print(f"✓ Objects detected: {result['count']}\n")
            
#            if result['count'] > 0:
#                print("Detected objects:")
#                print("-" * 50)
#                for i, detection in enumerate(result['detections'], 1):
#                    print(f"{i}. {detection['class'].upper()}")
#                    print(f"   Confidence: {detection['confidence']*100:.1f}%")
#                    print(f"   Location: {detection['bbox']}")
#                    print()
#            else:
#                print("No objects detected in this image.")
#        else:
#            print(f"✗ Detection failed: {result.get('error', 'Unknown error')}")
#    
#   except requests.exceptions.ConnectionError:
#        print("✗ Error: Cannot connect to server. Is it running?")
#    except Exception as e:
#        print(f"✗ Error: {e}")
#
#if __name__ == "__main__":
#    # Test with your image (change this to your image file)
#    test_detection("test_image.jpg")
#    
#    # You can add more tests:
#    # test_detection("person.jpg")
#    # test_detection("street.jpg")


import requests
import os

SERVER_URL = "http://localhost:8000/detect"

def test_detection(image_path):
    """Send an image to the server and print detection results"""
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return
    
    print(f"\n{'='*60}")
    print(f"Testing detection with: {image_path}")
    print(f"{'='*60}\n")
    
    try:
        with open(image_path, 'rb') as f:
            response = requests.post(SERVER_URL, files={"file": f})
        
        result = response.json()
        
        if result['success']:
            print(f"✓ Detection successful!")
            print(f"✓ Total objects detected: {result['total_detections']}")
            print(f"✓ Priority alerts triggered: {len(result['priority_alerts'])}\n")
            
            if result['priority_alerts']:
                print("🔔 PRIORITY ALERTS:")
                print("-" * 60)
                for alert in result['priority_alerts']:
                    print(f"🚨 {alert['message']}")
                    print(f"   Object: {alert['class']}")
                    print(f"   Confidence: {alert['confidence']*100:.1f}%\n")
            else:
                print("No priority objects detected.")
            
            if result['all_detections']:
                print("\n📋 All Detected Objects:")
                print("-" * 60)
                for i, det in enumerate(result['all_detections'], 1):
                    priority = "⭐" if det['class'] in result.get('priority_alerts', []) else "  "
                    print(f"{priority} {i}. {det['class']} ({det['confidence']*100:.1f}%)")
        else:
            print(f"✗ Detection failed: {result.get('error', 'Unknown error')}")
    
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_detection("test_image.jpg")
