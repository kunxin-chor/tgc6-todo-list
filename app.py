from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
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


@app.route('/')
def home():
    return "Welcome home"


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
        'comments': comments
    })

    return "Task created successfully!"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
