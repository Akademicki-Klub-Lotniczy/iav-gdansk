#import field
import json
from json import JSONEncoder

from mesh.Mesh import generatingRectangles
from mesh.SingleSquare import SingleSquare
import numpy as np

from flask import Flask, send_from_directory
app = Flask(__name__)


class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    





@app.route("/")
def hello():
    return send_from_directory('.', 'site.html')  # "Hello World!"


@app.route('/field')
def field():
    fourCornerrs=np.array([[51.113853,17.064804], [51.113897, 17.064989], [51.114106, 17.064855],[51.114055, 17.064676]])
    results=[]
    x_divider=10
    y_divider=10

    xx_dim, xy_dim, yx_dim,yy_dim=generatingRectangles(fourCornerrs,x_divider,y_divider)
    for j in range (y_divider) :
            for i in range (x_divider):          
                    results.append(
                    SingleSquare(
                    fourCornerrs[0][0]+i*xx_dim+j*yx_dim,
                    fourCornerrs[0][1]+i*xy_dim+j*yy_dim,
                    fourCornerrs[0][0]+(i+1)*xx_dim+j*yx_dim,
                    fourCornerrs[0][1]+(i+1)*xy_dim+j*yy_dim,
                    fourCornerrs[0][0]+(i+1)*xx_dim+(j+1)*yx_dim,
                    fourCornerrs[0][1]+(i+1)*xy_dim+(j+1)*yy_dim,
                    fourCornerrs[0][0]+i*xx_dim+(j+1)*yx_dim,
                    fourCornerrs[0][1]+i*xy_dim+(j+1)*yy_dim
                    ))
    return MyEncoder().encode(results)



@app.route('/lib/<path:filename>', methods=['GET'])
def get_media(filename):
    return send_from_directory('./lib/', filename)


app.run('0.0.0.0')
