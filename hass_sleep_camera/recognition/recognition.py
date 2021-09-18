import cv2

from hass_sleep_camera import settings


def create_detector():
    detector = cv2.CascadeClassifier()
    return detector


if __name__ == '__main__':

    face_cascade_path = f'{settings.HAAR_CASCADE_FOLDER}/haarcascade_frontalface_alt_tree.xml'
    eye_cascade_path = f'{settings.HAAR_CASCADE_FOLDER}/haarcascade_eye_tree_eyeglasses.xml'
    detector = create_detector()
    path = '/home/karol/Documents/sleep/2021-08-21/2021_08_21__01_30_00.avi'
    video = cv2.VideoCapture(path)

    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    eyes_cascade = cv2.CascadeClassifier(eye_cascade_path)

    for i in range(1):
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(frame_gray)
        for face in faces:
            x0, y0, w, h = face
            frame = cv2.rectangle(frame, (x0, y0), (x0+w, y0+h), (255, 125, 0), 5)

        cv2.imshow('f', cv2.resize(frame, (0, 0), fx=0.4, fy=0.4))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # results = detector.detectMultiScale(
        #     gray, scaleFactor=1.05, minNeighbors=5,
        #     minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        print(faces)

