import cv2
import numpy as np


cameraMatrix = np.array([[341.1772, 0.0136, 319.2622],
                [0, 341.5543, 243.6391],
                [0, 0, 1]])

distCoeffs = np.array([-0.2898, 0.0634, -0.00029521, -0.00078580, 0])

# image to be calibrated
img = cv2.imread('orig5.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w,h), 1, (w,h))
frame = cv2.undistort(img, cameraMatrix, distCoeffs, None, newcameramtx)
x, y, w, h = roi
frame = frame[y : y+h, x : x+w]

# 614 389
rows,cols, _ = frame.shape
src_points = np.float32([[85,250],[529,250],[0,rows-1],[cols-1,rows-1]])
dst_points = np.float32([[0,0],[cols-1,0],[180,rows-1],[434,rows-1]])

projective_martix = cv2.getPerspectiveTransform(src_points,dst_points)
frame_after = cv2.warpPerspective(frame,projective_martix,(cols,rows))

cv2.imshow("capture", frame_after)
cv2.imwrite('corrected5.jpg', frame_after)
cv2.imshow("ori", frame)
cv2.imshow("oriss", img)

cv2.waitKey(0)

