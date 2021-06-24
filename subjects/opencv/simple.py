'''
Date: 2021-03-15 22:39:16
LastEditors: Rustle Karl
LastEditTime: 2021-03-15 22:39:16
'''
import cv2

# img = cv2.imread(jpg1.as_posix(), 1)
# cv2.imshow("image", img)
# cv2.waitKey(1)  # ms

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FPS, 25)
# camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

while True:
    ret, frame = camera.read()

    if not ret:
        break

    # cv2.imshow("capture", frame)

    # 显示物体轮廓
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gb = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gb, 100, 200)
    cv2.imshow("capture", edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
