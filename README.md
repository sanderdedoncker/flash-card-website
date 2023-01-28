# Flash Cards


Website to store, manage and learn personal flash card collections. 

Feel free to try out the [live version](https://sade-flash-cards.herokuapp.com/)! (Deployed on Heroku as of 29/05/2022)

## Main website features

- Creating accounts and managing your user data;
- Creating, editing, and deleting cards (in-browser and via RESTful API);
- Getting a card overview with sorting and filtering capability (in-browser and via RESTful API);
- Learning cards interactively in a system based on spaced repetition;
- Obtaining statistics of learning progress;
- Responsive styling that is friendly to all viewport sizes.

## Under the hood

The source code is written with a primary focus on good software engineering practices - readability, modularity, extendibility, efficiency. It is meant to be mostly self-documenting.

Everything is built in Python, around the Flask framework. Several extensions are used:
- Flask-Login for user authentication and authorization in the browser;
- Flask-HTTPAuth for authentication and authorization in the API;
- Flask-SQLAlchemy, Flask-Migrate for interacting with a database via ORM;
- Flask-Bootstrap for responsive styling;
- Flask-WTF for dynamic forms.

The code comes with a suite of functional and unit tests implemented in Pytest. The API was tested and documented using Postman (read the docs [here](https://documenter.getpostman.com/view/21200551/Uz5CKxWk)).

## Running a local test server

1. Clone the repository and enter the directory

```shell
> git clone https://github.com/sanderdedoncker/flash-card-website.git
> cd flash-card-website
```

2. Create a new virtual environment, activate and install the necessary packages

```shell
> py -3 -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
```

3. Set up the necessary environment variables

```shell
> set FLASK_APP=application.wsgi
> set FLASK_ENV=development
> set SECRET_KEY=development
> set DEV_DATABASE_URI=sqlite:///flash-card-website.db
```

4. Create a new database (you only need to do this once, the database will persist afterwards)

```shell
> flask db upgrade
```

5. Run the server

```shell
> flask run
```

6. Open the given address in your browser and have fun!

## License

&copy; Sander Dedoncker, 2022
