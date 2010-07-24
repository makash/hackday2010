import pymongo
import json
from flask import Flask, render_template, request

cameraurl = 'http://www.btis.in/cameras/images/%s.jpg'

db = pymongo.Connection().hackday
app = Flask(__name__)


def preparedata(cursor, callback=None):
    data = json.dumps([{'imgurl': cameraurl % i['imgid'],
                        'lat': i['latlon'][0],
                        'lon': i['latlon'][1],
                        'name': i['name'],
                        'location': i['location'],
                        } for i in cursor])
    if callback:
        return '%s(%s);' % (callback, data)
    else:
        return data

@app.route('/findcamera')
def findcamera():
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))
    callback = request.args.get('jsonp', None)
    if lat == 0 or lon == 0:
        return preparedata(db.trafficam.find().sort('name'), callback)
    else:
        return preparedata(db.trafficam.find({"latlon": {"$near": [lat, lon]}}), callback)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)