from flask import render_template



def base():
    return render_template('base.html')


def index():
    return render_template('index.html')