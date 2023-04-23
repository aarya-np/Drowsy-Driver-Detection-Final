



# # Create a Flask app
from flask import Flask, request
import cv2
import numpy as np
import tensorflow as tf
from flask import  render_template
import os
from flask import Flask, render_template, Response
import cv2


app = Flask(__name__, static_url_path='/static')

#  Load the drowsy driver detection model
model = tf.keras.models.load_model(os.path.join('models','model.h5'))

cap = cv2.VideoCapture(0)

def gen_frames():
    timer = 0
    while True:
        print('11111111',timer)
        timer +=1
        if timer >=100:
            break
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/drowsy_driver_detection',methods = ['POST'])
def detection():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')  


if __name__ == '__main__':
    app.run(debug=True)

