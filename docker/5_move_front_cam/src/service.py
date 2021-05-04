from multiprocessing import Process
from flask import Flask
import time
import cv2


def detect_move():
    cap = cv2.VideoCapture(0)
    while True:
        there, frame = cap.read()
        if there:
            cv2.imshow('my webcam', frame)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
    cv2.destroyAllWindows()


Process(target=detect_move).start()


app = Flask(__name__)


@app.route('/')
def hola():
    return 'Move Detect by Wisrovi'


@app.route('/move', methods=['GET'])
def move():
    return "queso"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006)