# from flask import Flask
# from flask_socketio import SocketIO
# from flask_sqlalchemy import SQLAlchemy

# # Create the Flask app and configure it
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'e8dc33c903d19fbbbf6a778e8cc8f2e7'
# socketio = SocketIO(app)

# # Configure SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Define the User and Message models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender = db.Column(db.String(50), nullable=False)
#     content = db.Column(db.String(500), nullable=False)
    



# # Import the routes and SocketIO events
# from routes import *

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     socketio.run(app, debug=True)



# new app.py code below
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app and configure it
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e8dc33c903d19fbbbf6a778e8cc8f2e7'
socketio = SocketIO(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User and Message models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    


# Import the routes and SocketIO events
from routes import *

# Handle new WebSocket connections
@socketio.on('connect')
def handle_connect():
    # Retrieve previous messages from the database
    messages = Message.query.all()
    # Send previous messages to the client
    for message in messages:
        send({'sender': message.sender, 'content': message.content})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
