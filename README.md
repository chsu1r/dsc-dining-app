# GOOGLE DSC DINING APP WORKSHOP

## Getting Started
 1) Clone this repository.
 2) Make sure you have everything you need (Python 3, command line, Git).
 3) Start your virtual environment.

 IMPORTANT: If you end up pushing this to Github for any reason, make sure you DO NOT PUSH the file that contains your API keys (.env.constants in my case).

 ## Running the app
 * Ensure that everything is cloned and that you have installed everything within your virtual environment.

[startapp.sh](startapp.sh) or [startapp_windows.bat](startapp_windows.bat) should just initialize everything you need. Run it using the following.
```
 source ./startapp.sh  # Linux/MacOS
 or
 startapp_windows.bat  # For Windows
```
 If that doesn't work then try the following:

```
## Linux/MacOS
source dining-venv/bin/activate  # activate virtual env
source .env.constants  # initialize environment variables (API keys, etc)
source .flaskenv  # initialize Flask settings (where to find the Flask app)
flask run  # Run the Flask app

## Windows
.\dining-venv\Scripts\activate
.env.constants.bat
set FLASK_ENV=development
set FLASK_APP=main.py
flask run
```
This should bring up a locally running version of your app. The command line output should indicate where you should go to find it. For example, if my output is as below, then I would go to 'http://127.0.0.1:5000/' in my web browser.
```
Virtual environment started...
Local environment variables initialized...
Flask settings configured... Running Flask app now.
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
 * Serving Flask app "main.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
 * Debugger is active!
 * Debugger PIN: 328-663-510
 ```

 ## What's even here anyways
 The directory structure is as follows:
 * base directory contains configuration files and app startup scripts.
    * [main.py](main.py) is where the app starts (it loads in the dining directory.)
    * [requirements.txt](requirements.txt) is the list of packages that is used in the virtual environment for the app to work properly.

 * the dining directory contains most of the actual source code for the app
    * Inside the **[dining](dining/)** directory, we have a few subdirectories.
    * **[routes](dining/routes)** contains the python code for each of the pages. This is basically the app-side backend logic that fetches and pushes to databases and then determines what should display within the HTML.
    * **[templates](dining/templates)** contains the HTML file that organizes how information should be displayed on each page.
    * **[static](dining/static)** is all the css styling and any images that need to be included.
    * There are a couple of utility files just in the base dining directory that are used throughout the project. (This is in an effort to keep the routes files as clean as possible.)
    * [__ init__.py](dining/__init__.py) is important because it declares the Flask app object, which is essentially the app.
 * cloud_functions contains source code relevant to the session that will talk about cloud functions.
 * Many of the subdirectories should also contain their own README that explains further in depth what's going on in each of those files.