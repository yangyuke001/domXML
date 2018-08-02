#coding=utf-8  
import os  
import os.path  
from xml.dom.minidom import parse
import xml.dom.minidom
import glob as gb
from PIL import Image
from pylab import *
import cv2
import numpy as np 
from os import listdir
import random 
import shutil

xml_path = "/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/xml/"
xml_selected = "/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/xml_selected/"
files=os.listdir(xml_path)  #得到文件夹下所有文件名称  
s=[]
illumination_init = 'normal'
distance_inti = 100  
yaw_init = 45
pitch_init = 0
roll_init = 0
glasses_init = 'boldglasses'
list = ['421','300','215','154','110','78','56','40','28','20']
left = 0.5
right = 0.5
top = 0
bottom = 1
h = 1920
w = 480
for xmlFile in files: #遍历文件夹
    #if not os.path.isdir(xmlFile): #判断是否是文件夹,不是文件夹才打开  
        #print xmlFile

    dom=xml.dom.minidom.parse(os.path.join(xml_path,xmlFile))  ###最核心的部分,路径拼接,输入的是具体路径  
    annotation=dom.documentElement  
    #获取标签对name/pose之间的值  
    objects=annotation.getElementsByTagName('object')  

    for object in objects:
        xmlFile = str(xmlFile)
        xml_name = xmlFile.split('.')[0]
        xml_name_jpg = xml_name + '.jpg' #这里用路径拼接的方式拿到所有图片里的那个图
        #print (xml_name_jpg)
        bndbox = object.getElementsByTagName('bndbox')[0]
        illumination = object.getElementsByTagName('illumination')[0]
        illumination = illumination.childNodes[0].data
        distance = object.getElementsByTagName('distince')[0]
        distance = int(distance.childNodes[0].data)
        yaw = object.getElementsByTagName('yaw')[0]
        yaw = int(yaw.childNodes[0].data)
        pitch = object.getElementsByTagName('pitch')[0]
        pitch = int(pitch.childNodes[0].data)
        roll = object.getElementsByTagName('roll')[0]
        roll = int(roll.childNodes[0].data)
        glasses = object.getElementsByTagName('glasses')[0]
        glasses = glasses.childNodes[0].data
        
        xmin = bndbox.getElementsByTagName('xmin')[0]
        ymin = bndbox.getElementsByTagName('ymin')[0]
        xmax = bndbox.getElementsByTagName('xmax')[0]
        ymax = bndbox.getElementsByTagName('ymax')[0]

        width = int(xmax.childNodes[0].data) - int(xmin.childNodes[0].data)
        length = int(ymax.childNodes[0].data) - int(ymin.childNodes[0].data)
        xi = int(xmin.childNodes[0].data)
        yi = int(ymin.childNodes[0].data)
        xm = int(xmax.childNodes[0].data)
        ym = int(ymax.childNodes[0].data)
        
        if (illumination_init == illumination and distance_inti == distance and yaw_init == yaw and pitch_init == pitch and roll_init == roll):
            print(xml_name_jpg + ' satisfied')
            object_img_path = '/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/img_all/' + xml_name_jpg
            #print (object_img_path)
            #img_all = gb.glob('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/img_all/*.jpg')
            img_selected  = '/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/img_selected/'
            image = cv2.imread(object_img_path)
            image_select = cv2.imwrite(img_selected + xml_name_jpg ,image) 
            cv2.waitKey(1)
            img_path = gb.glob("/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/img_selected/*.jpg")
            for jpg in img_path: 
                img_name = str(jpg) 
                img_name = img_name.split('/')[-1]#.split('.')[0]
                if (img_name == xml_name_jpg):
                    image_path = '/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/img_selected/' + xml_name_jpg
                    image = cv2.imread(image_path)
                    cropImg = image[yi:yi+(2*bottom*length),xi-int(left*length):xi+length+int(right*length)]
                    for i in list:
                        x = int(i)
                        cropImg = cv2.resize(cropImg,(x,x))
                        length = str(x)
                        width = str(width)
                        cv2.imwrite('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/face/' + xml_name + '_' + length +'.jpg' ,cropImg)
                        cv2.waitKey(1)
                    face_path = gb.glob('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/face/*.jpg')
                    #face_path = '/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/face/'
                    for jpg in face_path:
                        ims = [Image.open(jpg) for jpg in face_path if (jpg.split('/')[-1].split('_')[0] == xml_name) ]
                        ims.sort(key=lambda  x: x.size[0])
                        result = Image.new(ims[0].mode,(1920,480))
                        random_jpg_path = gb.glob('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/random_jpg/*.jpg')
                        for random_jpg in random_jpg_path:
                            img_name = random_jpg.split('/')[-1]
                            y = random.randint(1, 2500)
                            x = random.randint(1, 1150)
                            image_path = '/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/random_jpg/' + img_name
                            image = cv2.imread(image_path)
                            cropImg = image[y:(y+w),x:(x+h)]
                            cv2.imwrite('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/random_background/' + img_name ,cropImg)
                            cv2.waitKey(1)
                            background_path = gb.glob('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/random_background/*.jpg')
                            for img in background_path:
                                randoms = [Image.open(img) for img in background_path]
                            for i,im in enumerate(randoms):
                                result.paste(im)
                        for i, im in enumerate(ims):
                            result.paste(im,box=(3*im.size[0],0))
                        result = result.save('/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/face_sum/'+ xml_name_jpg)
                        cv2.waitKey(1)
            xml_name_all = xml_name + '.xml'
            shutil.copy(os.path.join(xml_path,xml_name_all), r'/media/yyk/30169dd2-697d-443b-805b-571bc40fd688/yyk/FacePictures/test/xml_selected/')
           
