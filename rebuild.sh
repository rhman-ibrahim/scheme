# Delete database
rm db.sqlite3

# Delete cache files and migrations
rm -rf */__pycache__
rm -rf */migrations

# Make migrations
python3 manage.py makemigrations user
python3 manage.py makemigrations circles
python3 manage.py makemigrations signals

# Migrate
python3 manage.py migrate

# Load fixtures
python3 manage.py loaddata user/fixtures/users.json