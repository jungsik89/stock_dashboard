from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import scrape_mars
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

        
        query_mars = list(db.info_mars.find())

        return render_template("index.html",query_mars=query_mars)

@app.route("/scrape")
def scrape_data():

        query_new = scrape_mars.scrape()
        db.info_mars.update({}, query_new, upsert=True)

        return "done"
        
@app.route("/search")
def search_data():


        return "done search"

@app.route("/getStock", methods=["GET", "POST"])
def getBook():
    if request.method == "POST":
        
        stockName = request.form["stock"]
        query_new = scrape_stocks.getData(stockName)
        db.info_stock.update({}, query_new, upsert=True)
        

            
    return render_template("index.html")
  
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    