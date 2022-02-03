# jg_diff

Jungle diff is a player and team composition anaylsis tool built with Django

![image](https://user-images.githubusercontent.com/70884733/152388727-49062af8-e2a1-4260-b858-bfb97c144dcd.png)

# Demo

## Match Details
![image](https://user-images.githubusercontent.com/70884733/152389133-cc7b9135-d515-4baa-a1fd-bd9a90bfc16d.png)


# How to install Repo

To install this repository on your machine
1. Clone this repository: `$ git clone https://github.com/galaddirie/jg_diff.git` 
2. Create a virtual environment: `$ python3 -m venv venv`
3. activate virtual environment: `$ source venv/bin/activate`
4. navigate to the repository and install all the dependencies in requirements.txt: `$ pip install -r requirements.txt`
6. Populate environment variables
7. make migrations 
  ```
  $ python manage.py makemigrations 
  $ python manage.py migrate
  ```
8. Run the application: `$ python manage.py runserver`
