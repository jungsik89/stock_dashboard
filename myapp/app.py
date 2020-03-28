from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import stock_api
import pymongo
import os
import numpy as np
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


conn = "mongodb://127.0.0.1:27017"
client = pymongo.MongoClient(conn)


db = client.mission_mars
collection = db.info_mars

@app.route("/")
def home():


    return render_template("index.html")

        
@app.route("/search")
def search_data():


    return "done search"

@app.route("/getStock", methods=["GET", "POST"])
def getBook():
    if request.method == "POST":
        
        stockName = request.form["stock"]
        query_new = stock_api.getStock(stockName)
        

            
    return render_template("index.html",query_new=query_new)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
  
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    