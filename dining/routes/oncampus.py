"""
dining app oncampus () routes.
URLs include:
/oncampus/maseeh/
/oncampus/mccormick/
/oncampus/baker/
/oncampus/next/
/oncampus/simmons/
"""
from flask import render_template, url_for, request, redirect, session, flash, Markup, abort
from requests import HTTPError
import requests
from dining import app, firebase_auth, firebase_db
from dining.utils import login_required, refresh_user_token
import hashlib

SAMPLE_MENU_URL = "http://clhsu.scripts.mit.edu/sample-menu.json"
DIETARY_FLAG_ABBREVS = {"halal" : "HL", "made without gluten": "GF", "vegetarian": "VT", "vegan": "VG", "humane" : "HU", "seafood watch" : "SF", "in balance": "IB"}
DIETARY_FLAG_COLORS = {"halal" : "#ff9966", "made without gluten": "#999966", "vegetarian": "#28a745", "vegan": "#ffc107", "seafood watch" : "#007bff", "humane" : "#17a2b8", "in balance": "#6c757d"}

@app.route('/oncampus/<dorm_name>', methods=["GET"])
def oncampus(dorm_name):
    """ 
    Display the menu for dorm_name. 
    This function grabs the ratings for menu items from Firebase, loads the dorm menu,
    and passes all that information to the HTML template.
    """
    r = requests.get(SAMPLE_MENU_URL)
    resp = r.json()
    house_menus = resp["venues"]["house"]
    house_menu = {}
    user_ratings = {}
    global_ratings = {}
    ## TODO(): SESSION2: Grab the user individual ratings and the global ratings across all users from the database.
    
    ## END CODE

    # Grab the requested dorm menu from the all menu json
    for menu in house_menus:
        if menu['name'].lower() == dorm_name:
            dorm_name = menu['name']
            house_menu = sorted(menu['meals_by_day'][0]['meals'], key=lambda k:k['name'])

    # Populate a few additional fields for each menu item.
    for meal_idx, meal in enumerate(house_menu):
        for i, item in enumerate(meal['items']):
            item_name = item['name']

            # This is the unique ID that represents each menu item. It hashes the dorm name with the menu item name.
            hashed = hashlib.sha256((dorm_name + item_name).encode("utf-8")).hexdigest()

            # populate some additional fields in the house_menu object for display on webpage.
            house_menu[meal_idx]['items'][i]['id'] = hashed
            house_menu[meal_idx]['items'][i]['rating'] = user_ratings.get(hashed, 0)
            house_menu[meal_idx]['items'][i]['global_rating'] = global_ratings.get(hashed, {}).get("avg_rating", 0)

            # minor hacks to fix some things in the menu json
            item['description'] = item['description'].replace('\n', ' ')
            item['name'] = item['name'].replace('\n', ' ')

    # house_menu is a list where each item is a meal of the day
    # Each item is {'name': ..., 'items': []}
    return render_template('oncampus.html', meals=house_menu, dorm_name=dorm_name, abbrevs=DIETARY_FLAG_ABBREVS, colors=DIETARY_FLAG_COLORS, js_json={"meals": house_menu,"is_logged_in":'token' in session, 'dorm':dorm_name}, pagetitle="Dining App")

@app.route('/oncampus/submit-rating', methods=["POST"])
@login_required
def submit_rating():
    """
    Function that is called by the JS side of oncampus.html to submit a user rating.
    What this does is extract fields from the request and pushes them to Firebase.
    Note that this is @login_required, which requires a user to be logged in before this is run.
    See utils.py to see what @login_required actually checks for.
    """
    rating = int(request.json['value'])
    item_id = request.json['id'].split('-')[1]
    ## TODO() SESSION2: Fill in code to push a rating the "food" table.

    ## END CODE
    return "success"
