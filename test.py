import cv2

image = cv2.imread("static/knowns/Sehoon.jpg", cv2.IMREAD_COLOR)
resized = cv2.resize(image, (480, 640), interpolation=cv2.INTER_AREA )
cv2.imwrite('SehoonR.jpg', resized)