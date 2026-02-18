#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a,b):
    response = {'sum' : str( a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except:
        response = { 'width' : 0, 'height' : 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    try:
        data = request.get_json(force=True)
        a = data.get("a", [])
        b = data.get("b", [])

        if not isinstance(a, list) or not isinstance(b, list):
            response = {"dotproduct": 0, "error": "invalid vectors"}
        elif len(a) != len(b):
            response = {"dotproduct": 0, "error": "vectors length not equal"}
        else:
            dp = 0.0
            for x, y in zip(a, b):
                dp += float(x) * float(y)
            response = {"dotproduct": dp}

    except Exception as e:
        response = {"dotproduct": 0, "error": str(e)}

    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json"
    )


@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        data = request.get_json(force=True)
        b64 = data.get("image", "")

        img_bytes = base64.b64decode(b64)
        ioBuffer = io.BytesIO(img_bytes)
        img = Image.open(ioBuffer)

        response = {"width": img.size[0], "height": img.size[1]}

    except Exception as e:
        response = {"width": 0, "height": 0, "error": str(e)}

    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json"
    )


# start flask app
app.run(host="0.0.0.0", port=5000)