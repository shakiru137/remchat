from flask import session
from flask_socketio import emit
from functions.get_db_connection import get_db_connection

def follow_user(data):
    """
    Handles the logic for following a user in real-time using Socket.IO.

    Args:
        data (dict): Contains 'user_id', representing the ID of the user to follow.

    Emits:
        'follow_response': A message containing the result of the follow action ('success', 'warning', 'danger').
    """
    user_id = data.get('user_id')  # User to be followed
    current_user = session.get('username')  # Current user
    
    if not current_user:
        emit('follow_response', {'message': 'You need to be logged in to follow users.', 'status': 'danger'})
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validate that the current user exists and get the ID in a single query
        cursor.execute("SELECT id FROM users WHERE username = %s", (current_user,))
        current_user_id = cursor.fetchone()

        if not current_user_id:
            emit('follow_response', {'message': 'Current user not found!', 'status': 'warning'})
            return
        
        current_user_id = current_user_id[0]

        print("Current user username:", current_user)
        print("Current user ID:", current_user_id)
        print("User ID to be followed:", user_id)

        # Validate that the user to be followed exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        followed_user_id = cursor.fetchone()

        if not followed_user_id:
            emit('follow_response', {'message': 'User to follow not found!', 'status': 'warning'})
            return

        followed_user_id = followed_user_id[0]

        # Check if the current user is already following the target user
        cursor.execute(
            "SELECT COUNT(*) FROM followers WHERE user_id = %s AND followed_user_id = %s",
            (current_user_id, followed_user_id)
        )

        if cursor.fetchone()[0] == 0:
            # Insert new follow record and update follower/following counts
            cursor.execute(
                "INSERT INTO followers (user_id, followed_user_id) VALUES (%s, %s)",
                (current_user_id, followed_user_id)
            )
            cursor.execute(
                "UPDATE users SET followers_count = followers_count + 1 WHERE id = %s",
                (followed_user_id,)
            )
            cursor.execute(
                "UPDATE users SET following_count = following_count + 1 WHERE id = %s",
                (current_user_id,)
            )
            conn.commit()
            emit('follow_response', {'message': 'User followed successfully!', 'status': 'success'})
        else:
            emit('follow_response', {'message': 'Already following this user!', 'status': 'warning'})

    except Exception as e:
        emit('follow_response', {'message': f'An error occurred: {str(e)}', 'status': 'danger'})
    finally:
        cursor.close()
        conn.close()  # Ensure the connection is properly closed
