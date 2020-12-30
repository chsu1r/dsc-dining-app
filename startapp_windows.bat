CALL .\dining-venv\Scripts\activate
ECHO Virtual environment started...
if exist .env.constants.bat (
    call .env.constants.bat
    ECHO "Local environment variables initialized..."
)
set FLASK_ENV=development
set FLASK_APP=main.py
echo "Flask settings configured... Running Flask app now."

flask run