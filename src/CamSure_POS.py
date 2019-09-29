# VehicleRecognize

import os
import requests
import threading
import wx
from flask import Flask, jsonify, request, redirect, url_for, render_template
import time
import json
import urllib

from base64 import b64encode

APP = Flask(__name__)

urlDriveOff = "http://153.58.141.3:5000/vehicleRecognize"
urlAddIntoDriveOff = "http://153.58.141.3:5000/updateDriveoff?"
VehicleNumber_arg="VehicleNumber="
DriveOffDue_arg="&DriveOffDue="

IMAGE_PATH = 'C:\wamp64\www\Car.png'

lbl = ""
driveoff = 0.0
vehiclenumber = ""
box_body = "!! WELCOME !! \n  to \n NCR's CamSure"

received_flag = False

@APP.route('/', methods=['POST'])
def hello_world():
    global received_flag
    received_flag = True
    return 'Hello there! This is CamSure POS'


def display_insurance(vehiclenumber):
    urlInsurance = "http://153.58.142.75:5000/insurance?vehicleNo="+vehiclenumber
    print('thread created: ')
    print(urlInsurance)
    requests.get(urlInsurance)
    print('thread completed')


def client_thread(num):
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()


def image_post_thread(num):
    global received_flag
    global vehiclenumber
    global driveoff
    global lbl

    while 1:
        if received_flag == True:
            print("Image received flag is true")
            image_file = open(IMAGE_PATH, 'rb')
            file = {'image': image_file}
            r = requests.post(urlDriveOff, files=file)
            print(r.json())
            print(r.json()["results"])

            if r.json()["results"] == []:
                print("empty results")
            else:
                print("response is not empty")
                driveoff = r.json()["results"][0]['DriveOffDue']
                vehiclenumber = r.json()["results"][0]['VehicleNumber']
                t1 = threading.Thread(target=display_insurance, args=(vehiclenumber,))
                t1.daemon = True
                t1.start()

                if driveoff == 0.0:
                    lbl.SetLabel("There is no \n Previous Drive Off found")
                else:
                    lbl.SetLabel("This vehicle is listed as Drive Off...! \n Drive Off found with due: $"+str(driveoff)+"\nPlease proceed with pre-pay\n  for the fueling.")

                print("Insurance Details are being displayed!")
            received_flag = False

#        app2 = PhotoCtrl(False, IMAGE_PATH)
#        app2.MainLoop()


class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        print("MY: "+filename)
        self.frame = wx.Frame(None, title='Photo Control')

        self.panel = wx.Panel(self.frame)

        self.PhotoMaxSize = 240

        self.createWidgets(filename)
        self.frame.Show()

    def createWidgets(self, filename):
        img = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()

    def onBrowse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()

    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()


class MyFrame(wx.Frame):
    global box_body
    global vehiclenumber
    global driveoff

    def __init__(self):
        global received_flag
        global lbl
        super(MyFrame, self).__init__(parent=None, title='NCR CamSure POS')
        panel = wx.Panel(self)

        #my_sizer1 = wx.BoxSizer(wx.VERTICAL)
        #my_btn1 = wx.Button(panel, label='Capture Image')
        #my_btn1.Bind(wx.EVT_BUTTON, self.on_press1)
        #my_sizer1.Add(my_btn1, 0, wx.ALIGN_LEFT, 5)
        #panel.SetSizer(my_sizer1)

        my_sizer2 = wx.BoxSizer(wx.VERTICAL)
        my_btn2 = wx.Button(panel, label='Add DriveOff')
        my_btn2.Bind(wx.EVT_BUTTON, self.on_press2)
        my_sizer2.Add(my_btn2, 0, wx.ALIGN_CENTER, 5)
        panel.SetSizer(my_sizer2)

        box = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel, -1, pos = (60,75), style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        lbl.SetFont(font)
        lbl.SetLabel(box_body)
        box.Add(lbl, 0, wx.ALIGN_BOTTOM, 5)

        self.Show()

        t3 = threading.Thread(target=image_post_thread, args=(10,))
        t3.daemon = True
        t3.start()


    def on_press1(self, event):
        print("Process Image is pressed")


    def on_press2(self, event):
        print("DriveOff is pressed")
        driveoff = 40.00
        lbl.SetLabel("The Vehicle: "+ vehiclenumber +"\n has been listed in Drive Off \nwith due: $"+str(driveoff))
        print("AddtoDriveOff: "+urlAddIntoDriveOff + VehicleNumber_arg + vehiclenumber + DriveOffDue_arg + str(driveoff))
        r = requests.get(urlAddIntoDriveOff + VehicleNumber_arg + vehiclenumber + DriveOffDue_arg + str(driveoff))
        print(r)


if __name__ == "__main__":
    t2 = threading.Thread(target=client_thread, args=(10, ))
    t2.daemon = True
    t2.start()
    APP.run(host="0.0.0.0")
