# Main Code directory!

## [forms.py](forms.py)

This file contains code relevant to any forms you might see on the webpage (like Login forms or Register forms). These define a **class** for each form type and simply define form fields as **fields** within each class.

## [utils.py](utils.py)

This file contains a lot of code that is reused across files, or code that was exported to other helper functions to keep other files cleaner.

## [__init__.py](__init__.py)

This file initializes the flask object for the whole app, initializes Firebase components that all our other files can use, and then loads all the individual route pages for our web app. 