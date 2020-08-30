import env as config
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


# creates an instance of flask and assign it to the app variable
app = Flask(__name__)


# connecting DB to the app
app.config["MONGO_DBNAME"] = 'meet_event'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    ca = list(mongo.db.event_categories.find())
    the_event = list(mongo.db.events.find())
    return render_template("index.html", events=the_event, event_categories=ca)


@app.route("/create_event")
def create_evet():
    event_cat = mongo.db.event_categories.find()
    return render_template("createevent.html", event_categories=event_cat)


@app.route("/insert_event", methods=["POST"])
def insert_event():
    mongo.db.events.insert_one(request.form.to_dict())
    return redirect(url_for('index'))


@app.route("/edit_event/<event_id>")
def edit_event(event_id):
    events = mongo.db.events.find_one({"_id": ObjectId(event_id)})
    cats = mongo.db.event_categories.find()
    return render_template("editevent.html",
                           event=events, event_categories=cats)


@app.route('/update_event/<event_id>', methods=['POST'])
def update_event(event_id):
    event = mongo.db.events
    event.update({'_id': ObjectId(event_id)},
                 {
        'event_name': request.form.get('event_name'),
        'event_description': request.form.get('event_description'),
        'event_date': request.form.get('event_date'),
        'places': request.form.get('places'),
        'event_pic': request.form.get('event_pic')
    })
    return redirect(url_for('index'))


@app.route('/remove_event/<event_id>')
def remove_event(event_id):
    mongo.db.events.remove({'_id': ObjectId(event_id)})
    return redirect(url_for('index'))


@app.route('/insert_attender/<event_id>', methods=['POST'])
def insert_attender(event_id):
    event = mongo.db.events
    event.update({'_id': ObjectId(event_id)},
                 {'$addToSet': {
                    "guests": {
                        'fname': request.form.get('fname'),
                        'lname': request.form.get('lname'),
                        'email': request.form.get('email')
                    }
                 }})
    the_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    return render_template('index.html', the_event=the_event)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

