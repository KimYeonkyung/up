# -*- coding: utf-8 -*-
#coding=utf8

import os
import sys
import urllib
import urllib2
import pyglet
from darkflow.net.build import TFNet
import cv2
from imutils import paths
import numpy as np
from scipy.spatial import distance




#risk factor distinction
def mostRisk():
	#dict in list
	for o in obstacle: 
		#50% over
		if o['confidence']>0.5:
	        	xt,xb,yb=o['topleft']['x'], o['bottomright']['x'], o['bottomright']['y']
			x_mid = distance.euclidean(xt,xb)
			obs_cdn=(x_mid,xb) #obstacle_coordinate
			#closet risk
			if risk>distance.euclidean(obs_cdn, per_cdn): 
				risk=distance.euclidean(obs_cdn, per_cdn)
				risk_factor=o['label']
			
			if risk<100: # HELP HELP   
				TTS(risk_factor)
			

def TTSSET():
	client_id = "z6r28zt96q" 
	client_secret = "5JpTYO1zpUKCzGipoESGb1ixja3JWy5DR7Zqghlp"
	speaker = "mijin" 
	speed = "0" 
	val = {
		"speaker": speaker,
    	    	"speed":speed,
		}
	headers = {
    	    	"X-NCP-APIGW-API-KEY-ID" : client_id,
    	    	"X-NCP-APIGW-API-KEY" : client_secret
		}
	

def TTS(f):
	val["text"]=f
	data = urllib.urlencode(val)
	url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
	request = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(request)
	rescode = response.getcode()
	if(rescode==200):
 	    	print("TTS mp3 save")
   	    	response_body = response.read()
   	    	with open('test.mp3', 'wb') as f:
   	        	f.write(response_body)
	else:
		print("Error Code:" + rescode)

	song=pyglet.media.load('test.mp3')
	song.play()
	pyglet.app.run()

reload(sys)
sys.setdefaultencoding('utf-8')
val=dict()
headers=dict()
TTSSET()


options = {"pbLoad": "/home/yk/darkflow/object/detect-yolo.pb", "metaLoad": "/home/yk/darkflow/object/detect-yolo.meta", "threshold": 0.1}

tfnet = TFNet(options)

imgcv = cv2.imread("/home/yk/up/img/3/3_508.jpg")
obstacle = tfnet.return_predict(imgcv)

#person coordnate return? minGyu Part
per_cdn=(?,?) #HELP HELP
risk=10000
mostRisk()

