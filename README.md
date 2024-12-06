# socialdashboard
The Social Media Management Dashboard is a web app that enables users to manage their social media accounts from one place. Twitter, Facebook, and Instagram of users posting content, retrieving metrics and checking historical postings. It uses the APIs of such platforms to communicate with their services.

## Project Overview
The Social Media Management Dashboard is a web application that enables users to manage their social media accounts from one place. Links to post, get metrics, and historical posts on Twitter, Facebook, and Instagram It uses the APIs from the respective platforms to communicate with the services themselves.

## Features
- Go to Twitter, Facebook, Instagram and post content.
- Retrieve metrics of likes, shares, retweets, impressions, etc.
- See past posts and their links and metrics.
- A dashboard to manage posts easily.
---

## Setup and Execute the Code
### Prerequisites
1. **Python 3.9+** on your local machine
2. **Pipenv** or any tool for virtual environments in Python.
3. SQLite (bundled with Python)}}
   
### Steps
1. **Clone the Repository**
---
git clone https://github.com/RachaRajesh/socialdashboard
---
2. **Virtual Environment Setup**
   
  ``` python3 -m venv venv ```
  
  ``` source venv/bin/activate ``` (MAC OR LINUX)
  
           (or)

  ``` source venv/Scripts/activate ```(WINDOWS)

   
  ``` pip install -r requirements. txt ```
   
4. **Set Up the Database**

Set up the SQLite database and tables:

  in  python
  ---
>>> from app. models import db, User, Post
   >>> db.connect()
>>> db. create_tables([User, Post])
>>> User. create(username="default_user", email="default@example.com")
  ---
4. **Set Up Environment Variables**
   
Create a `. env` file then you add the below:example.env is given in repo
   
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_BEARER_TOKEN=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
FACEBOOK_ACCESS_TOKEN=
FACEBOOK_PAGE_ID=
INSTAGRAM_ACCESS_TOKEN =
INSTAGRAM_USER_ID=
#optional
SECRET_KEY=your_flask_secret_key
   ```

5. **Run the Application**
   
   python run.py
   
6. **Access the Dashboard**

In your browser visit `http://127.0.0.1:5000`

---

## External Dependencies and Prerequisites

- **Flask**: A web framework to create the application.
- **Peewee**: A simple, small, expressive ORM used with SQLite.
- **Requests**: To make requests to the API of the social media platform.
- **Python-dotenv** — To manage environment variables.
– **Jinja2**: For HTML template rendering on Flask.
You will need to install these dependencies with:

pip install -r requirements. txt
```

---
## Description on Core Files

### `run.py`
Application entry point. It sets up the Flask app and launches the server.
### `app/__init__.py`
Initialize the Flask app and setup blueprints and the database connection

### `app/models.py`
Defines the database models:
- `User`: A user of the platform.
- `Post`: Holds social media posts with extra fields for platform-specific information.
### `app/services.py`
It has the logic to connect with TWTR, FB and IG APIs:
- Posting content.
- Fetching metrics.

### `app/routes.py`
Specifies routes for handling http requests and template rendering.
### `app/templates/`
HTML templates for the web interface:
- `base.html`: Base layout.
- `index.html`: Landing page.
- `twitter. html`: Twitter dashboard.
- `facebook. html`: Facebook dashboard.
- `instagram. html`: Instagram dashboard.
### `app/static/`
Includes static assets, such as CSS, for styling the dashboard.

### `config.py`
Store the application configuration such as db connection, secret keys etc.
---

## Authors and Contributions

- Rajesh: App Development adn Testing
- Vishnu: UI Development and creation of API ID's
---
