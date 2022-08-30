from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
db = mongo.db

@app.route("/")
def home(): 

    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    
    # Create a Mars database
    mars_info = mongo.db.mars
    # Call the scrape function in the scrape_mars file which will scrape and save to mongo
    mars_scrape = scrape()
    # Update database with data being scraped
    mars_info.update_one({}, {"$set": mars_scrape}, upsert=True)

    # Redirect back to home page and return a message to show it was succesful
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)