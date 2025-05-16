from flask import session, flash, redirect, url_for
from functions.get_db_connection import get_db_connection
from functions.system_picture import system_picture

def load_previous_users(user_id):
    """
    Loads the previous chat users for the current user.

    Fetches users with whom the current user has previously chatted, 
    excluding the current user.

    Args:
        user_id (int): The ID of the current user.

    Returns:
        list: A list of previous chats users.
    """
    previous_chats = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT u.id, u.name, u.profile_picture, MAX(m.timestamp) AS last_message
                FROM messages m
                JOIN users u ON (u.id = m.sender_id AND m.receiver_id = %s)
                            OR (u.id = m.receiver_id AND m.sender_id = %s)
                GROUP BY u.id, u.name, u.profile_picture
                ORDER BY last_message DESC
            """
            cursor.execute(query, (user_id, user_id))
            
            # Handle NULL profile pictures and prepare chat user data
            previous_chats = [
                {
                    'id': user[0], 
                    'name': user[1], 
                    'profile_picture': user[2].decode('utf-8') if user[2] else system_picture()
                }
                for user in cursor.fetchall()
            ]
    
    except Exception as e:
        flash('An error occurred while loading previous chats: {}'.format(str(e)), 'danger')
        return []  # Return an empty list on error

    return previous_chats
