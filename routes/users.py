from app import app, forbidden
from flask import jsonify, request
from fastai.vision.all import *

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


@app.route('/cats-and-dogs', methods=['GET'])
def infer_cats():
    try:

        if request.method == 'GET':
            # check if the post request has the file part
            if 'image' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                learn_inf = load_learner('models/cats_and_dogs.pkl')
                res = learn_inf.predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                res.status_code = 200
                return jsonify(res)

        else:
            return forbidden()

    except Exception as e:
        print(e)
