import cv2
import numpy as np

cap = cv2.VideoCapture(0)
num = 0
while(1):
    ret, frame = cap.read()

    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(str(num) + '.jpg', frame)
        num += 1
    if  cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()