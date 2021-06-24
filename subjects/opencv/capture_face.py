'''
Date: 2021-03-15 22:39:16
LastEditors: Rustle Karl
LastEditTime: 2021-03-15 22:39:16
'''
import cv2

camera = cv2.VideoCapture(r"D:\OneDrive\Repositories\projects\renderers\ffmpeg-generator\testdata\v1.mp4")
# camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FPS, 25)

meta = r'C:\Mirror\weights\haarcascade_frontalface_default.xml'
delta = 4
process_this_frame = True
faces = []

while True:
    ret, frame = camera.read()

    if not ret:
        break

    if process_this_frame:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(meta)

        _faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.15,
                minNeighbors=5,
                minSize=(5, 5),
        )

        if len(_faces) > 0:
            faces = _faces

    process_this_frame = not process_this_frame

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)
        break

    cv2.imshow("capture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
