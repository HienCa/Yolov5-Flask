# Yolov5-Flask
Xác thực hình ảnh (ảnh và file yolov5s.pt)
-------------------------------------------------

1. Train model:
	1.1.Chuẩn bị những tấm ảnh cần train
	1.2.Bỏ các ảnh đã chuẩn bị vào folder coco128\images\train2017
	1.3.Truy cập https://www.makesense.ai/ để tạo labels cho các ảnh (export yolo - file zip) -> giải nén nhận được các file .txt (số đầu tiên đại diện cho thứ tự đối tượng)
	1.4.Bỏ các file .txt đã giải nén vào folder coco128\labels\train2017
	1.5.Nén folder coco128
	1.6.Truy cập https://github.com/ultralytics/yolov5 , tìm kiếm link tới google colab (mục đích train bằng gpu của google colab)
	1.7.thực hiện câu lệnh "!git clone https://github.com/ultralytics/yolov5" trong google colab của link trên
	1.8.Ném coco128.rar lên google colab link trên
	1.9.Giải nén coco128.rar 
	1.10Vào file coco128.yaml trong floder yolov5/data/coco128.yaml - sau đó mở file lên
	1.11.Chỉnh sửa đường dẫn (chuột phải vào file để copy đường dẫn)
		path: ../datasets/coco128 (sửa lại đường dẫn đến folder coco128 vừa giải nén)
		train: images/train2017  (sửa lại đường dẫn đến images/train2017 trong folder coco128 vừa giải nén)
		val: images/train2017 	(sửa lại đường dẫn đến images/train2017 trong folder coco128 vừa giải nén)
		
		names:
  			0: VanHien (sửa tên theo ý muốn)
  			1: HienCa (sửa tên theo ý muốn)
	1.12.Tìm đến hoặc copy câu lệnh sau !python train.py --img 640 --batch 16 --epochs 150 --data /content/yolov5/data/coco128.yaml --weights yolov5s.pt --cache (sửa đường dẫn đến coco128.yaml nếu có thay đổi)
		Câu lệnh trên sẽ train 150 lần, mỗi lần 16 ảnh 
	1.13.Kết quả là file best.pt trong folder weight (chú ý đường dẫn kết quả sau khi train xong)
	1.14.Tải file best.pt về và thay thế vào file best.pt trong project
		
2.IDE: Visual code
Chuột phải vào tên project mở Terminal: tạo ra môi trường ảo để thực thi python, web dựa trên Flask, các thư viện trong 2 file .txt
	pip install virtualenv
	virtualenv venv
	./venv/Scripts/activate
	pip install Flask
	pip install torch
	pip install -r requirements.txt (yolov5s)
	pip install -r requirementss.txt (flask)
