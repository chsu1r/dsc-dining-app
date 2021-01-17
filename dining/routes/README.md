# ROUTES for the app
These are the files that contain all the Python logic for communicating with databases, for making requests to external services, transforming data, and then passing that to the HTML files inside the templates folder.

This is all written in Python, but it uses a lot of the Flask package to get things done.
Important things to note about how routing works:
* This line helps us define what happens when we go to the "/login" page of our web page. When we type in something like "diningapp.com/login", that's a GET request that just fetches what to display to the user. When the user submits the login form, that's a POST request that sends information back to the server.
```
@app.route('/login/', methods=["GET", "POST"])
```
* So both requests go to this function, and we determine what to do based on information stored in the "request" object, specifically the **request.method** field.
```
@app.route('/login/', methods=["GET", "POST"])
def login():
    you can do stuff that you need to do for both POST and GET requests here.
    if request.method == "GET":
        do things specific to the GET request
    else:
        do things specific to the POST request
```
* Later on in that function, we return this **"render_template"** thing. This tells the Flask app what to produce when we request the login page. In this case, it produces the login.html file (also found in templates) that uses some parameters from the Python function that are directly passed into the HTML file.
```
return render_template('login.html', login_form=form, register_url=register_url, pagetitle="Dining App | Login" )
```
* You don't always have to return a render_template though. For example, you might have seen sometimes that if you're already logged in on a webpage and you try to login again, it might redirect you to the webpage's homepage instead. We can see this logic here, where we **redirect** the user to the index page, and we use **"url_for"** to generate the URL for the index homepage instead of typing it out.
```
if already_logged_in:
    return redirect(url_for('index'))
```
* There are a couple references to **"flash"**. Flash simply tells Flask to flash a message to the user in the form of a banner on page reload (in the case of this app). If you log in successfully, you will notice a green banner that says "Successfully logged in!" because of this line in the login function:
```
flash("Successfully logged in!", "success")
```
* Flask is also cool because it has this **'session'** object that you can use as a dictionary to store things like authentication tokens, or really anything you want. That's what happening in the following lines, as we store stuff in our session so we can access it later on.
```
session["token"] = user["idToken"]
session["refresh_token"] = user["refreshToken"]
```
