from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("base.html")