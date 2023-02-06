from flask import Flask, request, send_file, Response, send_from_directory
from flask_cors import CORS
import os
import base64
import json

app = Flask(__name__)
CORS(app)

@app.route('/imag', methods=['GET'])
def myimg():
    return send_file('save_pic.jpg', mimetype='image/jpg')

@app.route('/success', methods=['POST'])
def index():
    """
    POST route handler that accepts an image, manipulates it and returns a JSON containing a possibly different image with more fields
    """
    # Read image from request and write to server's file system
    data = request.files['file']
    imagetext = request.form.get('plaintext')
    print(imagetext)
    data.save('save_pic.jpg')

    # Do something with the image e.g. transform, crop, scale, computer vision detection
    # some_function_you_want()

    # Return the original/manipulated image with more optional data as JSON
    # saved_img = open('save_pic.jpg', 'rb').read() # Read as binary
    # saved_img_b64 = base64.b64encode(saved_img).decode('utf-8') # UTF-8 can be converted to JSON
    # response = {}
    # response['data'] = saved_img_b64
    # print(saved_img_b64)
    # response['more_fields'] = 'more data' # Can return values such as Machine Learning accuracy or precision

    # If only the image is required, you can use send_file instead
    return send_file('image.pdf', mimetype='application/pdf')

    # For sending multiple use this
    #return Response(json.dumps(response))

if __name__=="__main__":
    app.run(debug=True)