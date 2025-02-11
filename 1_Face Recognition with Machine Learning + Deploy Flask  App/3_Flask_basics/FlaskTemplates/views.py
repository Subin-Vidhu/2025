from flask import render_template


def index():
    return "Welcome to Home page"

def index_tem(name,marks):
    #marks = 80
    return render_template('index.html',name=name,marks=marks)

def index_for():
    data ={'statistics':70,'machine learning': 50,'deep learning':75,'python':20}
    return render_template('index_for.html',data=data)