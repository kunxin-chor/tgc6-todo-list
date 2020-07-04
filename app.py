from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from dotenv import load_dotenv
from bson import ObjectId
import os
import datetime

# load in the variables in the .env file into our operating system environment
load_dotenv()

app = Flask(__name__)

# connect to mongo
MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

# define my db_name
DB_NAME = "todolist"

# read in the SESSION_KEY variable from the operating system environment
SESSION_KEY = os.environ.get('SESSION_KEY')

# set the session key
app.secret_key = SESSION_KEY


# The Home Route
# Display all the tasks
@app.route('/')
def home():
    tasks = client[DB_NAME].todos.find()
    return render_template('home.template.html', tasks=tasks)


# For the "C" part of the CRUD
# one route to show the form and ask the user to type in
# one route to actually process the form (extract the data) and
# send it to the database

# this is the route that collects the user data with the form
@app.route('/tasks/create')
def show_create_form():
    return render_template('create_task.template.html')


# this is the route that process the form (extract data from it)
# and write  it to the Mongo database
@app.route('/tasks/create', methods=['POST'])
def create_task():
    # extract information from the form
    task_name = request.form.get('task-name')
    due_date = request.form.get('due-date')
    comments = request.form.get('comments')

    client[DB_NAME].todos.insert_one({
        'task_name': task_name,
        'due_date': datetime.datetime.strptime(due_date, "%Y-%m-%d"),
        'comments': comments,
        'done': False
    })
    flash(f"New task '{task_name}' has been created")
    return redirect(url_for('home'))

# RESTFUL API Review
# POST - create new data
# PUT - modify existing data by replacing the old entirely with the new
# PATCH - modify existing data by changing one aspect of the old data
# DELETE - delete existing date
# GET - fetch data


@app.route('/tasks/check', methods=['PATCH'])
def check_task():

    task_id = request.json.get('task_id')

    task = client[DB_NAME].todos.find_one({
        "_id": ObjectId(task_id)
    })
    print(task)

    # there is a chance task has no "done"
    # so if there is no key named "done", we just set "done" to False
    if task.get('done') is None:
        task['done'] = False

    client[DB_NAME].todos.update({
        "_id": ObjectId(task_id)
    }, {
        '$set': {
            'done': not task['done']
        }
    })

    # if we return a dictionary in Flask, Flask will auto-convert to JSON
    return {
        "status": "OK"
    }


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
