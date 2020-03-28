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


# conn = "mongodb://127.0.0.1:27017"
# client = pymongo.MongoClient(conn)

pstock= ""
ohlc_url = 'static/img/ohlc_mpf.png'
mva5d_url = 'static/img/5d-wk-close.png'
mva20d_url = 'static/img/20d-wk-close.png'
mvawks_url = 'static/img/wk-close-ma.png'
ocl_url = 'static/img/ohlc.png'
weekly_vol_url = 'static/img/volume_weekly.png'

@app.route("/")
def home():

    query_new = {

        "stock":pstock,
        "wkly_vol":weekly_vol_url,
        "5dmva": mva5d_url,
        "20dmva": mva20d_url,
        "week_ma": mvawks_url,
        "ocl": ocl_url,
        "ohlc_mpf":ohlc_url

    }
    return render_template("index.html",query_new=query_new)

        
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
    
    
    
    
    