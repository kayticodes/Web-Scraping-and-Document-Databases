from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

app = Flask(__name__)

app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_info = mongo.db.info.find_one()
    return render_template("index.html", mars_info = mars_info) 

@app.route("/scrape")
def scraper():
    info_reference = mongo.db.info
    mars_document = scrape_mars2.scrape()
    info_reference.update({}, mars_document, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
