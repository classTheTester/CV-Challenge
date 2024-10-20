from ultralytics import YOLO
model = YOLO("yolov8n.yaml")
results = model.train(data="mydata.yaml", epochs=30)