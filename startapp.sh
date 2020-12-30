source dining-venv/bin/activate
echo "Virtual environment started..."
if [ -e ".env.constants" ]; then
  source .env.constants
  echo "Local environment variables initialized..."
fi
source .flaskenv
echo "Flask settings configured... Running Flask app now."

flask run