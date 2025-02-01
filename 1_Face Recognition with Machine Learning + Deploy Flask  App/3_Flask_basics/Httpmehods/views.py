from flask import render_template, request
from flask import redirect, url_for
import json

def index():

    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email_id = request.form['email']
        
        data = {"first":first_name,'last':last_name,'email':email_id}

        return redirect(url_for('response',data=json.dumps(data)))


    return render_template('index.html')

def response(data):
    js_data = json.loads(data) # data will receive in text covnert back into json
    # convert again into dictionary
    data = dict(js_data)
    return render_template('response.html',data=data)