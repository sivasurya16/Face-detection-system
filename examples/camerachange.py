import cv2

#here alone there is ../ but it wont be there in main program
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def test(Cap=cv2.VideoCapture(0)):
    # Cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frames = Cap.read()

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
        elif k == ord('c'):
            Cap.release()
            cv2.destroyAllWindows()

            Cap = cv2.VideoCapture(int(input()))
            test(Cap)

    Cap.release()
    cv2.destroyAllWindows()

test()
