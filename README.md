### Installing required libs and frameworks
```
pip install -r requirements.txt
```
### Configuration
```
Rename file local_settings.py.example into local_settings.py and
fill it up with your database credentials.
```
### Provide migrations
```
python card_game/manage.py migrate
```
### Run Django application
```
python card_game/manage.py runserver
```
