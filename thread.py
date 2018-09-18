# -*- coding: utf-8 -*-
#coding=utf8
## TTS만 Thread
import os
import sys
import urllib
import urllib2
import pyglet
import time
from mss import mss
from darkflow.net.build import TFNet
import cv2
from imutils import paths
import numpy as np
from scipy.spatial import distance
from threading import Thread
from multiprocessing import Process


# Display FPS
def dp_fps(img,prevTime):
	curTime=time.time()
	sec=curTime - prevTime
	prevTime=curTime
	fps = 1/(sec)
	cv2.putText(img,"FPS : %0.1f"%fps,(0,30),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),1)
	return prevTime

def draw_rec(img,result):
	n_hand=[]
	for obj in result:
		confidence = obj['confidence']
		top_x = obj['topleft']['x']
		top_y = obj['topleft']['y']
		bottom_x = obj['bottomright']['x']
		bottom_y = obj['bottomright']['y']
		label = obj['label']
		# Person Recognition & Boxing
		if(confidence>0.5):
			cv2.rectangle(img,(top_x, top_y),(bottom_x, bottom_y), (0, 255, 0),2)
			cv2.putText(img, label+' - ' + str(  "{0:.0f}%".format(confidence * 100) ),(bottom_x, top_y-5),  cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0, 255, 0),2)
		if label == 'person':
			n_hand.append([top_x,top_y,bottom_x,bottom_y])
	return n_hand


def connect():
	img = cv2.imread("/home/yk/up/img/3/3_508.jpg")
	option_Obstacle = {"pbLoad": "/home/yk/darkflow/object/detect-yolo.pb", "metaLoad": "/home/yk/darkflow/object/detect-yolo.meta", "threshold": 0.1}
	option_Person={"pbLoad": "/home/yk/darkflow/bin/yolo180905/yolo180905.pb", "metaLoad":"/home/yk/darkflow/bin/yolo180905/yolo180905.meta", "threshold":0.4}
	obstacleTF = TFNet(option_Obstacle)
	personTF=TFNet(option_Person)
	obstacle_result=obstacleTF.return_predict(img)
	person_result=personTF.return_predict(img) 
	return obstacleTF,personTF
		


###########################################################################

#risk factor distinction
def mostRisk(obstacle, val, headers, per_cdn):
	risk_distance=10000
	#dict in list
	for o in obstacle: 
		#50% over
		if o['confidence']>0.5:
	        	xt,xb,yb=o['topleft']['x'], o['bottomright']['x'], o['bottomright']['y']
			x_mid = distance.euclidean(xt,xb)
			obs_cdn=(x_mid,xb) #obstacle_coordinate
			#closet risk
			if risk_distance>distance.euclidean(obs_cdn, per_cdn):
				risk_distance=distance.euclidean(obs_cdn, per_cdn)
				print risk_distance				
				risk_factor=o['label']
				if risk_factor=='bicycle':
					risk_factor='자전거'
				elif risk_factor=='car':
					risk_factor='자동차'
				elif risk_factor=='deskchair':
					risk_factor='책상과 의자'
				elif risk_factor=='bollard':
					risk_factor='볼라드'
			
			if risk_distance<500: # HELP HELP 
				print(risk_distance, risk_factor)
				th=Thread(target=TTS, args=(risk_factor,val,headers))
				th.start()
				#TTS(risk_factor,val,headers)
			

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
	return val, headers
	

def TTS(f,val,headers):
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
			audio()
	else:
		print("Error Code:" + rescode)


############################################################
def audio():
	song=pyglet.media.load('test.mp3')
	song.play()	
	pyglet.clock.schedule_once(exiter,song.duration)
	pyglet.app.run()
 
##############################################################33
def exiter(dt):
	  pyglet.app.exit()

def main():
	#Encoding utf-8
	reload(sys)
	sys.setdefaultencoding('utf-8')
	#baseFuntion
	val, headers=TTSSET()
	sct=mss()
	#Capture x,y position
	mon={'top':150, 'left':150, 'width':1000, 'height':800}
	obstacleTF, personTF=connect()
	#value init	
	prevTime=0
	while(True):
		person=[]
		#window ScreenCapture
		img=cv2.cvtColor(np.array(sct.grab(mon)),cv2.COLOR_RGBA2RGB)
		
		obstacle_result=obstacleTF.return_predict(img)
		person_result=personTF.return_predict(img) 
		person=draw_rec(img,person_result)
		if person:
			prevTime=dp_fps(img,prevTime)
			cv2.imshow('Image', img)
			cv2.waitKey(1)
			print person
			per_cdn=distance.euclidean((person[0][0],person[0][1]),(person[0][2],person[0][3]))
			mostRisk(obstacle_result, val, headers, per_cdn)
		print ("##one##")


if __name__=='__main__':
	main()



