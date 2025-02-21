import os
from threading import Thread

import cv2
import time
import glob
from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

# This will clean the images folder after every run.
def clean_folder():
    images = glob.glob("images/*.png")
    for image1 in images:
        os.remove(image1)

while True:
    status = 0
    check , frame = video.read()
    # next line will grayscale the frame.
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # next line will blur the frame
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21), 0)
    # opens a new tab to show the video
    #cv2.imshow("My video", gray_frame_gau)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame,125, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame,None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            image = cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_image = glob.glob("images/*.png")
            index = int(len(all_image) / 2)
            image_with_object = all_image[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0]==1 and status_list[1]==0:
        # Threading to avoid lagging while email is sent.
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()


    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
clean_thread.start()
