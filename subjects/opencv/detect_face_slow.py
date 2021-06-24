'''
Date: 2021-03-15 22:39:16
LastEditors: Rustle Karl
LastEditTime: 2021-03-15 22:39:16
'''
import cv2
import face_recognition

video_capture = cv2.VideoCapture(r"D:\OneDrive\Repositories\projects\renderers\ffmpeg-generator\testdata\v1.mp4")
# video_capture = cv2.VideoCapture(0)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
video_capture.set(cv2.CAP_PROP_FPS, 25)