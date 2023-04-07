from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import shutil
import cv2
import numpy as np

app = Flask(__name__)

import time
uploads_dir = os.path.join(app.instance_path, './uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world():
    
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    subprocess.run("dir", shell=True)
    #subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename)), '--conf-thres', '0.5'], shell=True)

    result = subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename)), '--conf-thres', '0.5'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = result.stdout.decode('utf-8')
    print(output)

    if not "no detections" in output:
        obj = secure_filename(video.filename)
        print(obj) #file image name
        status = 'success'
        for root, dirs, files in os.walk('runs/detect'):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    shutil.copy(os.path.join(root, file), os.path.join('static/detectImage', file))
    if "no detections" in output:
        status ='fail'
        obj = secure_filename(video.filename)
        
        source_path = "instance/uploads/" + obj
        destination_path = "static/nodetectImage/" + obj
        shutil.copy(source_path, destination_path)

    return {'filename':obj, 'output':output, 'status':status}

@app.route("/opencam", methods=['GET'])
def opencam():
    print("Opening camera...")
    key = cv2.waitKey(1)

    while True:
        result = subprocess.run(['python', 'detect.py', '--source', '0', '--conf-thres', '0.5'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        if "success" not in output:
            print("Camera not found")
            break
        if "no detections" not in output:
            print("Object detected")
            time.sleep(2)
            break
        else:
            print("No detections")
        if key == 27:  # ESC key to stop
            break

    subprocess.run(['python', 'detect.py', '--source', '0', '--conf-thres', '0.5', '--cam-disable'])
    cv2.destroyAllWindows()

    return "done"
    # net = cv2.dnn.readNet('./static/best.pt', './static/yolov5s.yaml')
    # print("here")
    # cap = cv2.VideoCapture(0)

    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     height, width, _ = frame.shape

    #     # Pass frame through the model
    #     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    #     net.setInput(blob)
    #     outputs = net.forward(['yolo'])

    #     # Process detections
    #     for output in outputs:
    #         for detection in output:
    #             scores = detection[5:]
    #             class_id = np.argmax(scores)
    #             confidence = scores[class_id]
    #             if confidence > 0.5:
    #                 print("Detected object with class ID: ", class_id)

    #                 # Sleep for 2 seconds
    #                 time.sleep(2)

    #                 # Turn off camera
    #                 cap.release()
    #                 cv2.destroyAllWindows()
    #                 return "done"

    # # Release resources
    # cap.release()
    # cv2.destroyAllWindows()

    # return "no object detected"   
   
    


    

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)

# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))

@app.route('/light_system')
def light_system():
   
    images = os.listdir('static/detectImage')
    obj = request.args.get('obj')
    # do something with obj
    return render_template('LightSystem.html',  images=images)