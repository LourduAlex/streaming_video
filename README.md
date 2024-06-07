git clone
setup python version to run 3.9.0
conda create -n envename python==3.9.0
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
