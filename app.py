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
@app.route("/deleteHistory")
def delete_History():
    folder_path_detect = "./static/detectImage"
    file_names_detect = os.listdir(folder_path_detect)
    for file_name in file_names_detect:
        os.remove(os.path.join(folder_path_detect, file_name))


    folder_path_runs_detect = "./runs/detect"

    # Kiểm tra nếu thư mục tồn tại
    if os.path.exists(folder_path_runs_detect):
        # Xóa tất cả các tệp và thư mục trong thư mục
        for filename in os.listdir(folder_path_runs_detect):
            file_path = os.path.join(folder_path_runs_detect, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Không thể xóa %s. Lỗi: %s' % (file_path, e))
    else:
        print("Thư mục không tồn tại.")

    return "ok"
@app.route("/deleteHistory2")
def delete_History2():

    folder_path_nodetect = "./static/nodetectImage"
    file_names_nodetect = os.listdir(folder_path_nodetect)
    for file_name in file_names_nodetect:
        os.remove(os.path.join(folder_path_nodetect, file_name))


    folder_path_runs_detect = "./runs/detect"

    # Kiểm tra nếu thư mục tồn tại
    if os.path.exists(folder_path_runs_detect):
        # Xóa tất cả các tệp và thư mục trong thư mục
        for filename in os.listdir(folder_path_runs_detect):
            file_path = os.path.join(folder_path_runs_detect, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Không thể xóa %s. Lỗi: %s' % (file_path, e))
    else:
        print("Thư mục không tồn tại.")

    return "ok"
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
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov')):
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
    
    a_dir = "./static/detectImage"
    b_dir = "./static/nodetectImage"

    for filename in os.listdir(a_dir):
        a_file_path = os.path.join(a_dir, filename)
        b_file_path = os.path.join(b_dir, filename)
        if os.path.isfile(a_file_path) and os.path.isfile(b_file_path):
            os.remove(a_file_path)

    imagesDetect = os.listdir('static/detectImage')
    noImagesDetect = os.listdir('static/nodetectImage')
    obj = request.args.get('obj')
    # do something with obj
    return render_template('LightSystem.html',  imagesDetect=imagesDetect, noImagesDetect=noImagesDetect)