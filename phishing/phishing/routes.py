from flask import Flask, render_template, request, redirect, flash, abort, url_for,send_file
from phishing import app
from phishing.models import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from requests.structures import CaseInsensitiveDict
import json
import requests
import preprocessor as p
import pickle as pk
import glob
from flask import Flask, request, render_template,redirect
import joblib
import whois
from datetime import datetime
import cv2
import pytesseract


from flask import Flask, render_template, request, redirect,  flash, abort, url_for, session
from phishing import app
from fileinput import filename
import os
import cv2
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging (1)
tf.get_logger().setLevel('ERROR')  # Suppress TensorFlow logging (2)
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from models import CC_Module
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import time
from options import opt
import math
import shutil
from tqdm import tqdm


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/login')






@app.route('/index',methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/',methods=['GET', 'POST'])
def index1():
    return render_template("index1.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        user =Register.query.filter_by(email=email,password=password).first()
        print(user)
               
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/detect') 
        
        else:
            d="Invalid Username or Password!"
            return render_template("login.html",d=d)
    return render_template("login.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        contact= request.form['contact']
        password= request.form['password']
        check= Register.query.filter_by(email=email).first()
        if check:
            b="Email is already exist."
            return render_template("register.html",b=b)
        else:
            my_data = Register(name=name,email=email,contact=contact,password=password)
            db.session.add(my_data) 
            db.session.commit()
            c="register successfull"
            return render_template("register.html",c=c)
        
    return render_template("register.html")



@app.route('/detect',methods=['GET','POST'])
def detect():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            filename = f.filename
            file_path = os.path.join("./phishing/static/uploads/", filename)
            f.save(file_path)

            # Under Water-----------------------------------------------------------

            # Color correction
            CHECKPOINTS_DIR = opt.checkpoints_dir
            device = 'cpu'
            ch = 3
            network = CC_Module()
            checkpoint_path = os.path.join(CHECKPOINTS_DIR, "netG_295.pt")
            checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
            network.load_state_dict(checkpoint['model_state_dict'])
            network.eval()
            network.to(device)

            result_dir = './object_det/static/enhanced_images/'
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)

            print("Processing file:", filename)

            img = cv2.imread(file_path)
            if img is None:
                print("Error: Unable to read image file:", filename)
                return "Error: Unable to read image file", 400

            img = img[:, :, ::-1]  # Convert BGR to RGB

            img = np.float32(img) / 255.0
            h, w, c = img.shape
            train_x = np.zeros((1, ch, h, w)).astype(np.float32)
            train_x[0, 0, :, :] = img[:, :, 0]
            train_x[0, 1, :, :] = img[:, :, 1]
            train_x[0, 2, :, :] = img[:, :, 2]
            dataset_torchx = torch.from_numpy(train_x)
            dataset_torchx = dataset_torchx.to(device)
            output = network(dataset_torchx)
            output = (output.clamp_(0.0, 1.0)[0].detach().cpu().numpy().transpose(1, 2, 0) * 255.0).astype(np.uint8)
            output = output[:, :, ::-1]  # Convert RGB to BGR

            output_path = os.path.join(result_dir,filename)
            cv2.imwrite(output_path, output)

            print('Image processing completed.')
        else:
            print("No file uploaded.")
            return "No file uploaded", 400


        # Object Detection-------------------------------------------------------------
        
        detect_fn = tf.saved_model.load("saved_model")

        #Object label map path
        PATH_TO_LABELS = 'data/mscoco_label_map.pbtxt'

        #create index from labels
        category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
        # IMAGE_PATHS = ["/path/to/test/image1","/path/to/test/image2"]
        image_path = "./phishing/static/uploads/" +f.filename
        def load_image_into_numpy_array(path):
            return np.array(Image.open(path))


        print('Running inference for {}... '.format(image_path), end='')
        image_np = load_image_into_numpy_array(image_path)
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        # input_tensor = np.expand_dims(image_np, 0)
        detections = detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        image_np_with_detections = image_np.copy()
        img , object_list = viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.6,
            agnostic_mode=False)

        cv2.imwrite('./phishing/static/output/' + f.filename, cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))   
        print('Objects list',object_list)
        return render_template("result.html", data =f.filename, objArr=object_list)
    return render_template("index.html")
    