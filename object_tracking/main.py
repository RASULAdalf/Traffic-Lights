import math
import time

import cv2
import requests
from flask import Flask
import threading
from ultralytics import YOLO

app = Flask(__name__)
vehicle_count = 0
base_url = 'http://192.168.1.12'
pause_img_proc_thread = threading.Event()

def notify_timer():
    pause_img_proc_thread.clear()
    params = {
        'vehicle_count': vehicle_count
    }
    response = requests.get(base_url + ':60/get-count', params=params)
    print(response.text)
    pause_img_proc_thread.set()


@app.route('/get-count', methods=['GET'])
def home():
    print('received count request...')
    notify_thread = threading.Thread(target=notify_timer)
    notify_thread.start()
    global vehicle_count
    vehicle_count = 0
    return "Count sent!"


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


def initial_request():
    while vehicle_count == 0:
        print('initiating...')
        time.sleep(3)

    response = requests.get(base_url + ':60/initiated')
    print(response.text)



# interval = 90  # 1.5 minutes

# Initial timestamp
# last_time = time.time()

def image_proc_code():

    # start webcam
    cap = cv2.VideoCapture(base_url+":81/stream")
    cap.set(3, 640)
    cap.set(4, 480)

    # model
    model = YOLO("yolo-Weights/yolov8n.pt")
    classNames_vehicles = ["bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat"]


    # object classes
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush"
                  ]



    while True:
        pause_img_proc_thread.wait()
        success, img = cap.read()
        results = model(img, stream=True)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0]*100))/100
                print("Confidence --->",confidence)

                # class name
                cls = int(box.cls[0])
                if classNames[cls] in classNames_vehicles:
                    print(f'{classNames[cls]} added')
                    global vehicle_count
                    vehicle_count+=1

                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                time.sleep(0.6)

                # current_time = time.time()
                # if current_time - last_time >= interval:
                #     notify_timer()
                #     vehicle_count = 0
                #     # Reset the last_time to current_time
                #     last_time = current_time

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    print(vehicle_count)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    init_thread = threading.Thread(target=initial_request)
    init_thread.start()

    # Run other code in parallel
    img_proc_thread = threading.Thread(target=image_proc_code)
    pause_img_proc_thread.set()
    img_proc_thread.start()

    # Optionally wait for the Flask thread to finish
    flask_thread.join()

