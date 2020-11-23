# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 08:21:00 2020

@author: Adam
"""

import pandas as pd
import numpy as np
import datetime
import os
import re
import time
from collections import Counter
from ip2geotools.databases.noncommercial import DbIpCity
import ipaddress
import urllib.request
import json
import progressbar
import ipinfo
import ast
import requests
import csv
from pandas.io.json import json_normalize
from distutils.dir_util import copy_tree
from zipfile import ZipFile
import gc
import ast
from itertools import groupby
from multiprocessing import Pool
from joblib import Parallel, delayed
from ast import literal_eval
from multiprocessing import Pool
from joblib import Parallel, delayed
from ast import literal_eval 
from itertools import groupby
import pyodbc
from pandas.tseries.offsets import MonthEnd
import datetime
# for Capstone Project
import argparse
import imutils
import cv2
from skimage.color import rgb2gray
from skimage import filters

# test directory:
# D:\SpringBoard\Capstone Project\VIRAT Video Dataset\VIRAT Video Dataset Release 2.0\VIRAT Ground Dataset\annotations

os.chdir(r"C:\Users\Adam\Documents\Data Science Personal\SpringBoard\Capstone\Coding")

# load all videos and all annotation texts
directory_video = r"D:\SpringBoard\Capstone Project\VIRAT Video Dataset\VIRAT Video Dataset Release 2.0\VIRAT Ground Dataset\videos_original"
directory_ann = r"D:\SpringBoard\Capstone Project\VIRAT Video Dataset\VIRAT Video Dataset Release 2.0\VIRAT Ground Dataset\annotations_objects"
# test
# test = os.listdir(directory_video)
# for test2 in test:
#     print(test2[8:-4])
# input_file = r"C:\Users\Adam\Documents\Data Science Personal\SpringBoard\Capstone\Coding\VIRAT_S_000200_00_000100_000171.mp4"
# output_file = r"C:\Users\Adam\Documents\Data Science Personal\SpringBoard\Capstone\Coding\output_files\VIRAT_S_000200_00_000100_000171_annotated(5).mp4"
# ann_file = r"C:\Users\Adam\Documents\Data Science Personal\SpringBoard\Capstone\Coding\VIRAT_S_000200_00_000100_000171.viratdata.objects.txt"

# change directories!!!

for filename_vid in os.listdir(directory_video):
    video_id = filename_vid[8:-4]
    for filename_ann in os.listdir(directory_ann):
        if video_id in filename_ann:
            input_file = r"D:\SpringBoard\Capstone Project\VIRAT Video Dataset\VIRAT Video Dataset Release 2.0\VIRAT Ground Dataset\videos_original\VIRAT_S_"+video_id+".mp4"
            output_file = r"D:\SpringBoard\Capstone Project\VIRAT Video Dataset\VIRAT Video Dataset Release 2.0\VIRAT Ground Dataset\videos_output\VIRAT_S_"+video_id+"_annotated.mp4"
            ann_file = r"D:\SpringBoard\Capstone Project\VIRAT Video Dataset\VIRAT Video Dataset Release 2.0\VIRAT Ground Dataset\annotations_objects\VIRAT_S_"+video_id+".viratdata.objects.txt"
        
            cap = cv2.VideoCapture(input_file)
            if cap.isOpened(): 
                width  = cap.get(3) 
                height = cap.get(4) 
            fps = 30
            
            fourcc = cv2.VideoWriter_fourcc('m','p','4','v') 
            out = cv2.VideoWriter(output_file,fourcc,fps,(int(width),int(height)))
            
            success = True
            # the below is red, but the boxes are still blue
            color = (255,0,0)
            counter = 0
            
            ann_df = pd.read_csv(ann_file,sep=" ",header=None,error_bad_lines=False)
            ann_df.rename(columns={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7'},inplace=True)
            ann_grouped = ann_df.groupby(ann_df['1'])
            ann_group_list = [ann_grouped.get_group(x) for x in ann_grouped.groups]
            
            while success:
                success,im = cap.read() 
            
                if not success:
                    break
                
                for i in range(len(ann_group_list)):
                    obj = ann_group_list[i]
                    # divide by 30 because there are 30 frames per second? No.
                    if ((len(obj.loc[(obj['2'])==counter].index)>=1) and len(obj.loc[(obj['2'])==counter].columns)<=10):
                        try:
                            lefttop_x = obj.loc[obj['2']==counter,'3'].item()
                            lefttop_y = obj.loc[obj['2']==counter,'4'].item()
                            bbox_width = obj.loc[obj['2']==counter,'5'].item()
                            bbox_height = obj.loc[obj['2']==counter,'6'].item()
                        except:
                            continue
                        if (not ((lefttop_x >=0) and (lefttop_y >=0) and (bbox_width >=0) and (bbox_height >=0))):
                            counter = counter+1
                            continue
                        cv2.rectangle(im,(lefttop_x,lefttop_y),(lefttop_x+bbox_width,lefttop_y+bbox_height),color,2)
                out.write(im)        
                counter = counter+1
                
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            print("Program ran without errors!")