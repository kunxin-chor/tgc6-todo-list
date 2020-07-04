# Requirements

```
click==7.1.2
dnspython==1.16.0
Flask==1.1.2
itsdangerous==1.1.0
pymongo==3.10.1
python-dotenv==0.13.0
Werkzeug==1.0.1
```

The requirements we are installing are:

* `pip3 install flask`
* `pip3 install pymongo` -- to use Mongo DB
* `pip3 install dnspython` -- is to allow us to connect to Mongo with just the URL
* `pip3 install python-dotenv` -- allows the use of `.env` files for environment variables

## How to use requirements.txt
```
pip3 install -r requirements.txt
```
## Session keys
Generated from https://randomkeygen.com/

# Tasks
What fields or information do we want to track for each todo
* The task name
* Due date
* Whether it is done
* Comments

# Flash Messages
1. Ensure sessions are enabled. We have to make sure `app.secret_key` has been set

2. In the `layout.template.html` add in the code to display the flash messages:

    ```
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for m in messages %}
            <div class="alert alert-success">
                {{m}}
            </div>
            {% endfor %}
        {%endif%}
    {%endwith%}
    ```

    Check https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/ for documentation
    on how to show a different class for errors