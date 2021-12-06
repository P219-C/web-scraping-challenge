from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_app

# Create route that renders index.html template?
@app.route("/")
def index():
    mars = db.mars.find_one()
    # mars = list(db.mars.find()) # Same as above
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def do_scrape():
    mars_data = scrape_mars.scrape()
    # print(mars_data)

    db.mars.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)