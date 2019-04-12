# warehouse

Warehouse is a web application being developed using Django Framework to provide information about the company and
its products and deals to the customers. It also helps the customers to order the products from the warehouse. 
It provides staff to perform stock management operations and update the latest promotions. 

## Getting Started

##### Technology Used:
1. [Python3](https://www.python.org/)
2. [Django](https://www.djangoproject.com/)
3. [MySQL](https://www.mysql.com/) 
4. [Bootstrap](https://getbootstrap.com/)
5. [jQuery](https://jquery.com/)
6. [JavaScript](https://www.javascript.com/)
7. [AngularJS](https://angularjs.org/)
8. [SCSS](https://sass-lang.com/)
 

### Prerequisites

To get started working on this project, install Python3 as follows

[Download](https://www.python.org/downloads/) the appropriate installer for your operating system and
run it on your machine.

##### Creating and Activating Virtual Environment

```
python -m venv path/to/warehouse
source path/to/warehouse/bin/activate
``` 

### Installing

Firstly, clone [this repository](https://github.com/Mounika1705/warehouse)

```
cd path/to/warehouse
git clone https://github.com/Mounika1705/warehouse.git
cd warehouse
```

Install MySQL Database (or any other database supported by Django)

[Download](https://dev.mysql.com/downloads/) the appropriate installer for your operating system and
run it on your machine.

Create file secret_settings.py and add Database settings as follows

```
DATABASE_BACKEND = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'database_name',
    'USER': 'username',
    'PASSWORD': 'password',
    'HOST': 'localhost',
    'PORT': '3306',
    'default_character_set': 'utf-8',
}
``` 

##### Installing the dependency packages

```
pip install -r requirement_windows.txt
pip install -r requirements.txt
```

Apply database migration from Django to MySQL

```
cd src
python manage.py migrate
```

Start Django server

```
python manage.py runserver
```

Type http://127.0.0.1:8000/ in the browser to visit the web application.

## Running the tests

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](https://github.com/Mounika1705/warehouse/blob/master/README.md) file for details

