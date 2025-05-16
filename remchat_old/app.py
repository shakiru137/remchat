from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_babel import Babel 
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
import datetime

# Import functions from your modules
from functions.login_user import login_user
from functions.user_dashboard import user_dashboard
from functions.follow_user import follow_user
from functions.unfollow_user import unfollow_user
from functions.search_users_logic import search_users_logic
from functions.signup_user import signup_user
from functions.log_out import log_out
from functions.get_db_connection import get_db_connection
from functions.login_required import login_required

from chats.messages import messages as messages_view
from chats.chat_room import chat_room

from posts.posts import load_paginated_posts
from posts.like_post import like_post
from posts.delete_post import delete_post
from posts.post_content import post_content
from posts.post_comment import comment_page

# Initialize Flask app and configure app session
app = Flask(__name__)
app.config['SECRET_KEY'] = "i_don't_have_it_yet"
app.config['SESSION_TYPE'] = "filesystem"

app.config['BABEL_DEFAULT_LOCALE'] = "en"
babel = Babel(app)

# Initialize session and Socket.IO
Session(app)
socketio = SocketIO(app, manage_session=False)

# Database connection
conn = get_db_connection()
cursor = conn.cursor()

# Index route (login page)
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Render login page or handle login submission.
    
    Returns:
        login_user() on POST request or 'index.html' on GET request.
    """
    return login_user() if request.method == 'POST' else render_template('index.html')

# User signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle user signup process.
    
    Returns:
        signup_user() on POST request or 'signup.html' on GET request.
    """
    if request.method == 'POST':
        return signup_user()
    return render_template('signup.html')

# Dashboard route
@app.route("/dashboard/<username>", methods=['GET', 'POST'])
@login_required
def dashboard(username):
    """
    Render user dashboard.
    
    Args:
        username (str): Username of the logged-in user.
        
    Returns:
        user_dashboard() with user-specific data.
    """
    session.pop('random_ids', None)
    return user_dashboard()

# Search users route with pagination
@app.route('/search/<username>', methods=['GET', 'POST'])
@login_required
def search_users_view(username):
    """
    Render search results for users.
    
    Args:
        username (str): Username of the logged-in user.
        
    Returns:
        Rendered search results page with pagination.
    """
    session.pop('random_ids', None)
    search_results, page, total_pages, query = search_users_logic()
    return render_template('search.html', search_results=search_results, page=page, total_pages=total_pages, query=query)

# SocketIO event for follow action
@socketio.on('follow')
def on_follow(data):
    """Handle follow event."""
    follow_user(data)

# SocketIO event for unfollow action
@socketio.on('unfollow')
def on_unfollow(data):
    """Handle unfollow event."""
    unfollow_user(data)

# Messages route
@app.route('/messages/<username>', methods=['GET', 'POST'])
@login_required
def messages_route(username):
    """
    Render the user's messages.
    
    Args:
        username (str): Username of the logged-in user.
        
    Returns:
        Rendered messages view.
    """
    session.pop('random_ids', None)
    return messages_view()

# Chat room route
@app.route('/chat_room/<username>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat_room_route(username, user_id):
    """
    Render chat room for messaging.
    
    Args:
        username (str): Username of the logged-in user.
        user_id (int): ID of the user to chat with.
        
    Returns:
        Rendered chat room view.
    """
    return chat_room(user_id, session.get('user_id'), session['username'])

# Posts route for viewing posts
@app.route('/posts/<username>/', methods=['GET'])
@login_required
def posts_view(username):
    """
    Load and render paginated posts.
    
    Args:
        username (str): Username of the logged-in user.
        
    Returns:
        Paginated posts view.
    """
    return load_paginated_posts()

# Post content route
@app.route('/post_content/<username>', methods=['GET', 'POST'])
@login_required
def post_content_view(username):
    """
    Handle posting content by the user.
    
    Args:
        username (str): Username of the logged-in user.
        
    Returns:
        post_content() response.
    """
    session.pop('random_ids', None)
    return post_content()

# SocketIO event for liking a post
@socketio.on('like_post')
def on_like(data):
    """Handle like post event."""
    like_post(data)

# Delete post route
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post_view(post_id):
    """
    Handle deleting a post.
    
    Args:
        post_id (int): ID of the post to delete.
        
    Returns:
        delete_post() response.
    """
    return delete_post(post_id)

# SocketIO event for joining a chat room
@socketio.on('join')
def on_join(data):
    """
    Handle user joining a chat room.
    
    Args:
        data (dict): Contains the room to join.
    """
    username = session.get('username')
    room = data.get('room')

    if room and username:
        session['room'] = room
        join_room(room)

# SocketIO event for handling messages
@socketio.on('message')
def handle_message(data):
    """
    Handle incoming chat messages and store them in the database.
    
    Args:
        data (dict): Contains the message, user_id, and room.
    """
    msg = data.get('msg')
    user_id = data.get('user_id')
    room = data.get('room')

    if not (msg and user_id and room):
        return

    try:
        username = session.get('username')
        emit('message', {'msg': msg, 'user': username}, room=room)

        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, message, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (session.get('user_id'), user_id, msg, datetime.datetime.now()))
        
        conn.commit()
    except Exception as e:
        print(f"Error handling message: {e}")
        conn.rollback()

# SocketIO event for leaving a chat room
@socketio.on('leave')
def on_leave(data):
    """
    Handle user leaving a chat room.
    
    Args:
        data (dict): Contains the room to leave.
    """
    username = session.get('username')
    room = data.get('room') or session.get('room')

    if room and username:
        leave_room(room)
        emit('message', {'msg': f'{username} has left the room.'}, room=room)

# Comment route
@app.route('/comment/<int:post_id>', methods=['POST', 'GET'])
@login_required
def comment_page_view(post_id):
    """
    Handle loading and posting comments on a post.
    
    Args:
        post_id (int): ID of the post to comment on.
        
    Returns:
        comment_page() response.
    """
    return comment_page(post_id)

# User logout route
@app.route('/logout')
def logout():
    """
    Handle user logout.
    
    Returns:
        log_out() response.
    """
    return log_out()

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
