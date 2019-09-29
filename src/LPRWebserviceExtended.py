from flask import Flask, jsonify, request
import json
import urllib
from base64 import b64encode
import requests

from openalpr import Alpr
import openalpr
import pymongo
import os
import json
import threading

app = Flask(__name__)


#This will fetch the driveOff
def fetchDriveOff(vehicleNumber):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["local"]
    mycol = mydb["VehicleInfo"]
    myquery = {"VehicleNumber": vehicleNumber}
    mydoc = mycol.find(myquery)
    if mydoc.count() != 0:
        return mydoc[0]["DriveOffDue"]
    return 0.00

#This method inserts/updates the driveoff information
def updateDriveOff(vehicleNumber, driveoffdue):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["local"]
    mycol = mydb["VehicleInfo"]
    try:
     mycol.find_one_and_update({"VehicleNumber": vehicleNumber},
                                   {"$set": {"DriveOffDue": float(driveoffdue)}},
                                   upsert=True)
    except ValueError:
        print("DriveOff should be float")

@app.route('/')
def hello_world():
    return """ Usage : This service provides the below functionalities
               Update driveoff         : GET: http://localhost:5000/updateDriveoff?VehicleNumber=MH12DE1433&DriveOffDue=20.00
               Vehicle Recognition     : POST: http://localhost:5000/vehicleRecognize
               """

@app.route('/updateDriveoff', methods=['GET'])
def updateDriveOffService():
    if 'DriveOffDue' not in request.args:
        return 'No DriveOff'
    if 'VehicleNumber' not in request.args:
        return 'No DriveOff'
    vnum = request.args['VehicleNumber']
    due = request.args['DriveOffDue']
    updateDriveOff( vnum , due )
    return 'OK'

@app.route('/vehicleRecognize', methods=['POST'])
def vehicleRecognizeService():
    alpr = Alpr("in", os.path.abspath("C:\OpenALPR\openalpr_64\openalpr.conf"), os.path.abspath("C:\OpenALPR\openalpr_64\\runtime_data"))
    alpr.set_top_n(20)
    if 'image' not in request.files:
        print("image was not in files")
        return 'Image parameter not provided'

    jpeg_bytes = request.files['image'].read()

    if len(jpeg_bytes) <= 0:
        print
        "there are no bytes!"
        return False

    results = alpr.recognize_array(jpeg_bytes)

    jsonResultList = []
    jsonResult = {'results' : jsonResultList }

    for plate in results['results']:
        jsonResultList.append({'VehicleNumber': plate['plate'], 'Confidence': plate['confidence'], 'DriveOffDue': fetchDriveOff(plate['plate'])})

    return jsonify(jsonResult);


if __name__ == "__main__":
    #app.run(host= 'localhost', port='5010')
    app.run(host='0.0.0.0')