from flask import request, flash, session
from functions.get_db_connection import get_db_connection
from functions.system_picture import system_picture

def search_users_logic():
    """
    Handles user search functionality by querying users based on the search query.
    
    Returns:
        - search_results: List of user search results for the current page.
        - page: Current page number for pagination.
        - total_pages: Total number of pages for pagination.
        - query: The search query used.
    """
    # Get the current page number from the query parameters, default is 1
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of results per page
    offset = (page - 1) * per_page  # Calculate the offset for pagination

    # Determine if it's a POST request (form submission) or GET request (query string)
    query = request.form.get('search_query', '').strip() if request.method == 'POST' else request.args.get('q', '').strip()
    print("Search query:", query)

    # If no query is provided, return an empty result set
    if not query:
        flash('Please enter a search query.', 'warning')
        return [], page, 1, ''

    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection error!', 'danger')
            return [], page, 1, ''

        cursor = conn.cursor()
        current_user_id = session.get('user_id')
        
        # Fetch total user count for pagination (excluding the current user)
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE name LIKE %s AND id != %s",
            ('%' + query + '%', current_user_id)
        )
        total_users = cursor.fetchone()[0]
        
        if total_users == 0:
            flash('No users found for your search query.', 'info')
            return [], page, 1, query

        # Fetch users for the current page
        cursor.execute(
            "SELECT id, name, profile_picture FROM users WHERE name LIKE %s AND id != %s ORDER BY id LIMIT %s OFFSET %s",
            ('%' + query + '%', current_user_id, per_page, offset)
        )
        results = cursor.fetchall()

        # Get the current user's following list
        cursor.execute(
            "SELECT followed_user_id FROM followers WHERE user_id = %s",
            (current_user_id,)
        )
        following_list = {row[0] for row in cursor.fetchall()}
        
        # Prepare search results
        search_results = [
            {
                'id': user[0],
                'name': user[1],
                'profile_picture': user[2].decode('utf-8') if user[2] else system_picture(),
                'is_following': user[0] in following_list
            }
            for user in results
        ]

    except Exception as e:
        flash(f'An error occurred while searching for users: {str(e)}', 'danger')
        return [], page, 1, query  # Consistent return in case of error

    finally:
        conn.close()

    # Calculate total pages for pagination
    total_pages = (total_users + per_page - 1) // per_page

    # Return search results and current page
    return search_results, page, total_pages, query
