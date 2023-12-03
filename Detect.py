from ultralytics import YOLO
model=YOLO("Ball.onnx")
import cv2
cap = cv2.VideoCapture(0)
xx,yy=0,0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Change 'output.avi' to the desired filename
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()
while True:
    ret, frame = cap.read()
    results=model.predict(source=frame,conf=0.3,verbose=False)
    try:
        x=results[0]
        box = x.boxes[0]
        anss=box.xyxy[0].tolist()
        start_point = (int(anss[0]),int(anss[1]))
        end_point = (int(anss[2]),int(anss[3]))
        pointx=((int(anss[0])+int(anss[2]))//2)
        pointy = ((int(anss[1]) + int(anss[3])) // 2)
        color = (255, 0, 0)
        thickness = 3
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
        frame = cv2.circle(frame, (pointx, pointy), radius=3, color=(0, 0, 255), thickness=-1)
        print(pointx,xx)
        if pointx>xx+10:
            Text="Moving Left"
            xx=pointx
        elif pointx<xx-10:
            Text="Moving Right"
            xx=pointx
        else:
            Text="No Movement"
        print(Text)
    except:
        pass
    cv2.imshow("Ballx",frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
