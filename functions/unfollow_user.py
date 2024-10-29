from flask import session
from flask_socketio import emit
from functions.get_db_connection import get_db_connection

def unfollow_user(data):
    """
    Handles the unfollowing of a user in the app.

    Args:
        data (dict): Contains the user_id of the user to unfollow.

    Emits:
        follow_response: Sends the status of the unfollowing action back to the client.
    """
    user_id = data.get('user_id')  # User to be unfollowed
    current_user = session.get('username')  # Current user

    if not current_user:
        emit('follow_response', {'message': 'Current user not found in session!', 'status': 'warning'})
        return

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Validate that the current user exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (current_user,))
            current_user_row = cursor.fetchone()

            if not current_user_row:
                emit('follow_response', {'message': 'Current user not found in database!', 'status': 'warning'})
                return

            current_user_id = current_user_row[0]

            # Validate that the user to be unfollowed exists
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            followed_user_row = cursor.fetchone()

            if not followed_user_row:
                emit('follow_response', {'message': 'User to unfollow not found!', 'status': 'warning'})
                return

            # Check if the follow relationship exists
            cursor.execute(
                "SELECT COUNT(*) FROM followers WHERE user_id = %s AND followed_user_id = %s",
                (current_user_id, user_id)
            )

            if cursor.fetchone()[0] > 0:  # User is currently followed
                # Remove the follow relationship
                cursor.execute("DELETE FROM followers WHERE user_id = %s AND followed_user_id = %s",
                               (current_user_id, user_id))

                # Update the followers count for the unfollowed user
                cursor.execute(
                    "UPDATE users SET followers_count = followers_count - 1 WHERE id = %s",
                    (user_id,)
                )

                # Update the following count for the current user
                cursor.execute(
                    "UPDATE users SET following_count = following_count - 1 WHERE id = %s",
                    (current_user_id,)
                )
                conn.commit()
                emit('follow_response', {'message': 'User unfollowed successfully!', 'status': 'success'})
            else:
                emit('follow_response', {'message': 'You are not following this user!', 'status': 'warning'})

    except Exception as e:
        emit('follow_response', {'message': f'An error occurred: {str(e)}', 'status': 'danger'})
