import cv2
from pathlib import Path

#here alone there is ../ but it wont be there in main program
cascPath=Path(r'../cascades/haarcascade_frontalface_default.xml').absolute()
faceCascade = cv2.CascadeClassifier(str(cascPath))

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frames = video_capture.read()

    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frames, (x, y), (x+w, y+h), (225, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frames)

    k = cv2.waitKey(1) 

    if k == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()