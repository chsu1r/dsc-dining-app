source dining-venv/bin/activate
echo "Virtual environment started..."
source .env.constants
echo "Local environment variables initialized..."
source .flaskenv
echo "Flask settings configured... Running Flask app now."

flask run