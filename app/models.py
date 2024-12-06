from peewee import Model, SqliteDatabase, CharField, TextField, DateTimeField, ForeignKeyField
from datetime import datetime

# Initialize the database
db = SqliteDatabase('social_media.db')

# Define the User model
class User(Model):
    username = CharField(unique=True)  # Username of the user
    email = CharField(unique=True)     # Email of the user
    created_at = DateTimeField(default=datetime.now)  # When the user was added

    class Meta:
        database = db

# Define the Post model
class Post(Model):
    user = ForeignKeyField(User, backref='posts')  # Link each post to a user
    platform = CharField()                         # Platform: twitter/facebook
    content = TextField()                          # Content of the post
    post_link = TextField()                        # Link to the post
    created_at = DateTimeField(default=datetime.now)  # Timestamp

    class Meta:
        database = db

# Create the tables and default user
db.connect()
db.create_tables([User, Post])

# Create a default user if it doesn't already exist
default_user, created = User.get_or_create(
    username="default_user", email="default@example.com"
)
