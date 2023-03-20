from flask import Flask, request, send_file, Response, send_from_directory
from flask_cors import CORS, cross_origin
import base64
import json
from fileinput import filename
from PIL import Image, ImageTk
import os
import code
from stegano import lsb 
from randimage import get_random_image, show_array
import base64
import matplotlib as mp
from cryptography.fernet import Fernet
from randimage import get_random_image, show_array
import rsa
from mysteg.myfuncs import encode, decode
import cv2
# text_data=""

app = Flask(__name__)
CORS(app)
# @app.route('/generate', methods=['GET'])
# def gen_image():
#     print('inside')
#     img_size = (250,250)
#     imgarr = get_random_image(img_size)
#     mp.image.imsave('save_pic.png', imgarr)
#     return send_file('save_pic.png', mimetype='image/png')

@app.route('/decrypt', methods=['POST'])
def mydecrypt():
    data = request.files['imag']
    data.save('stego.png')
    pemfile = request.files['pemfile']
    pemfile.save('private.pem')

    with open('private.pem', mode='rb') as private2file:
        keydata1 = private2file.read()

    privkey = rsa.PrivateKey.load_pkcs1(keydata1)
    decoded_data = decode('stego.png', n_bits=1, in_bytes=True)

    with open("crypto_decoded", "wb") as f:
        f.write(decoded_data)

    print(f"[+] File decoded, crypto_decoded is saved successfully.")

    crypto = open("crypto_decoded", "rb").read()
    clear_message = rsa.decrypt(crypto, privkey)
    # clear_message = lsb.reveal(data)
    # print(f'extracting from lsb = {clear_message}')
    return clear_message

@app.route('/hide', methods=['POST'])
def Hide():
    text_data = request.form.get('plaintext')
    global secret
    message=text_data.encode('utf8')
    print(message)
    (bob_pub, bob_priv) = rsa.newkeys(512)
    global mypriv
    mypriv = bob_priv

    with open('private.pem', mode='wb') as privatefile:
        privatefile.write(bob_priv.save_pkcs1())
    
    crypto = rsa.encrypt(message, bob_pub)
    
    with open("crypto", "wb") as f:
        f.write(crypto)
    
    with open("crypto", "rb") as f:
        secret_data = f.read()
        input_image = "save_pic.png"
        # split the absolute path and the file
        path, file = os.path.split(input_image)
        # split the filename and the image extension
        filename, ext = file.split(".")
        output_image = os.path.join(path, f"{filename}_encoded.{ext}")
        # encode the data into the image
        encoded_image = encode(image_name=input_image, secret_data=secret_data, n_bits=1)
        # save the output image (encoded image)
        cv2.imwrite(output_image, encoded_image)
        print("[+] Saved encoded image.")

    # print(f'Crypto = {crypto}')
    # secret = lsb.hide('save_pic.png',crypto)
    # secret.save('img.png')
    return send_file('private.pem', as_attachment=True)

@app.route('/del', methods=['POST'])
def delit():
    os.remove('save_pic.png')
    os.remove('private.pem')
    os.remove('crypto')
    return 'deleted save_pic and private.pem'

@app.route('/del2', methods=['POST'])
def delit2():
    os.remove('save_pic_encoded.png')
    return 'deleted img.png'

@app.route('/del3', methods=['POST'])
def delit3():
    os.remove('crypto_decoded')
    os.remove('private.pem')
    os.remove('stego.png')
    return 'removed keys and stego'

@app.route('/imag', methods=['GET'])
def myimg():
    return send_file('save_pic_encoded.png', mimetype='image/png')

@app.route('/upload', methods=['POST'])
def index():
    """
    POST route handler that accepts an image, manipulates it and returns a JSON containing a possibly different image with more fields
    """
    # Read image from request and write to server's file system
    data = request.files['file']
    global text_data
    # text_data = request.form.get('plaintext')
    # print(text_data)
    data.save('save_pic.png')

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
    #return send_file('img.png', mimetype='image/png')
    return 'done'

    # For sending multiple use this
    #return Response(json.dumps(response))

if __name__=="__main__":
    app.run(debug=True)