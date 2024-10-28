from flask import request, flash, redirect, url_for, session
from functions.get_db_connection import get_db_connection
from functions.system_picture import system_picture

def search_users(cursor, search_query, current_user_id):
    """
    Searches for users in the database by username.

    Retrieves users whose usernames match the search query, excluding the current user.

    Args:
        cursor (cursor): The database cursor for executing queries.
        search_query (str): The search term for finding users.
        current_user_id (int): The ID of the current logged-in user.

    Returns:
        list: List of user dictionaries containing user ID, name, and profile picture.
        int: Current page number.
        int: Total pages for pagination.
    """
    if not search_query:
        flash('Please enter a search query.', 'warning')
        return [], 1, 1

    page = request.args.get('page', 1, type=int)  # Get the current page number from the query
    per_page = 4  # Number of results per page
    offset = (page - 1) * per_page  # Calculate the offset for pagination

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # SQL query to search for users based on username or name
            search_sql = """
                SELECT id, name, profile_picture
                FROM users
                WHERE (username LIKE %s OR name LIKE %s) AND id != %s
                ORDER BY id LIMIT %s OFFSET %s
            """
            cursor.execute(search_sql, ('%' + search_query + '%', '%' + search_query + '%', current_user_id, per_page, offset))
            users = cursor.fetchall()

            # Count the total matching users for pagination
            cursor.execute("""
                SELECT COUNT(*) 
                FROM users 
                WHERE (username LIKE %s OR name LIKE %s) AND id != %s
            """, ('%' + search_query + '%', '%' + search_query + '%', current_user_id))
            
            users_count = cursor.fetchone()[0]
            total_pages = (users_count + per_page - 1) // per_page  # Calculate total pages

            # Prepare user data for rendering, handle NULL profile_picture
            processed_users = [
                {
                    'id': user[0], 
                    'name': user[1], 
                    'profile_picture': user[2].decode('utf-8') if user[2] else system_picture()
                }
                for user in users
            ]

            return processed_users, page, total_pages

    except Exception as e:
        flash(f'An error occurred while searching for users: {str(e)}', 'danger')
        return [], page, 1  # Return an empty list and current page, total pages as 1
