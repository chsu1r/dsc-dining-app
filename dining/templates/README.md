# Template (HTML Files)

This is the directory with all the HTML files that determines how each page will look.

index.html contains the base template that all the other files inherit from, and it is the html file for the homepage. 

In index.html, you can see something that looks like

```
{% block content %}
...
{% end block %}
```

and all the other files to start with 
```
{% extends "index.html" %}
{% block content %}
```
and end with
```
{% endblock %}
```
This means that all the other pages will look exactly like the homepage (extending the index.html file) except for the stuff inside the block content section, which is redefined in each individual page's html file.

You might notice that this is not normal HTML syntax - with Python Flask, you can use a template engine called "Jinja" that basically allows you to use Python like syntax within HTML files. This means you can do cool things like
* **Pass in arguments into the HTML file.** Look at how render_template is called in routes/oncampus.py and how parameters like "meals" is passed in. Then look at templates/oncampus.html and note that we iterate through "meals" and access fields inside the meals data structure in the HTML file.
```
oncampus.py

def oncampus(dorm_name):
    """ Display the menu for dorm_name """
    house_menu = [{'name': 'Lunch', ....}, {'name': 'Breakfast', ....}, ...]
    ...
    return render_template('oncampus.html', meals=house_menu, ...)


oncampus.html

{% for meal in meals %}
...
<button>{{ meal['name'] }}</button>
...
{% endfor %}

becomes something like
<button>{{ Breakfast }}</button>
<button>{{ Lunch }}</button>
<button>{{ Dinner }}</button>
```
* Similarly, you can also define **if else** blocks in Jinja using the following. For example, this is really useful for the login/logout button at the top right, which should change what it says and does based on whether the user is logged in or not.
``` 
{% if 'token' in session %}
...
{% endif %}
```
