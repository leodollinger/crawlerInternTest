Crawler developed as a test for an Internship vacancy at Devnology
==================================================================

## Description

This project, gets all lenovo laptops from the webscraper.io website, sort it by price (low priced to high priced), get all of its data and return as a json.

---

## Libraries

Currently, we are using five Libraries, are they:

* Asyncio:
	Asyncio is a library to write concurrent code using the async/await syntax.
* Flask 2.0.1:
    Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.
* Flask-RESTPlus 0.13.0:
    Flask-RESTPlus is an extension for Flask that adds support for quickly building REST APIs. Flask-RESTPlus encourages best practices with minimal setup. 
* Json:
	Json is a lightweight data interchange format inspired by JavaScript object literal syntax.
* Pyppeteer 0.2.6:
	Unofficial Python port of puppeteer JavaScript (headless) chrome/chromium browser automation library.
* Re:
	Provides regular expression matching operations similar to those found in Perl.
* Time:
	Provides various time-related functions.
* Werkzeug 2.0.1:
    Werkzeug is a comprehensive WSGI web application library.

---

## How to use

It is necessary to create a new virtual env and then, install the listed libraries. After installing the libraries, the user must change some configurations.

### Configurations

* First:

    Go to "\venv\Lib\site-packages\flask_restplus\fields.py" and change the line 17 <br>
    From<br>
        "from werkzeug import cached_property"<br>
    To<br>
        "from werkzeug.utils import cached_property"<br>

* Secund:    

    Go to "\venv\Lib\site-packages\flask_restplus\api.py" and change the line 19<br>
    From<br>
        "from flask.helpers import _endpoint_from_view_func"<br>
    To<br>
        "import flask.scaffold<br>
        flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func"<br>
    And change the line 25<br>
    From<br>
        "from werkzeug import cached_property"<br>
    To<br>
        "from werkzeug.utils import cached_property"<br>
<br>
### Run the app
<br>
Now, to run the app, go to the app root directory and execute the "main.py" file (py .\main.py).
<br>
Once the program is running, the user can access the page "http://127.0.0.1:5000/laptops". After a couple secunds, the page will bring a json contenning all Lenovo laptops data.