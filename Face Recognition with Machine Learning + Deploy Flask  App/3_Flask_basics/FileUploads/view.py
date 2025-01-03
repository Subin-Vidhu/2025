from flask import render_template, request
from flask import redirect, url_for
import os

UPLOAD_FOLDER = 'static/uploads/'

def index():
    
    if request.method == 'POST':
        f = request.files['upload']
        path = os.path.join(UPLOAD_FOLDER,f.filename)
        f.save(path)
        print('File saved sucessfully in \n',path)
        return render_template('index.html',upload=True,fname=f.filename)

    return render_template('index.html',upload=False)