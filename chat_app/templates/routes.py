

from flask import render_template, request, session, redirect, url_for
from app import app, socketio, db, User, Message

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect(url_for('chat'))

    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    messages = Message.query.all()
    return render_template('chat.html', username=session['username'], messages=messages)

# SocketIO events
@socketio.on('message')
def handle_message(msg):
    new_message = Message(sender=session['username'], content=msg)
    db.session.add(new_message)
    db.session.commit()

    socketio.emit('message', {'sender': session['username'], 'content': msg}, room=session['username'])




if __name__ == '__main__':
    socketio.run(app, debug=True)
