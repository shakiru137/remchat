from flask import session, make_response, flash, redirect, url_for
from functions.get_db_connection import get_db_connection

def log_out():
    """
    Logs out the current user by clearing the session and cookies.

    This function closes the database connection, removes the user's session 
    information, and redirects the user to the index page. It also sets the 
    'logged_in' cookie to expire.

    Returns:
        Response: The response object with a redirect to the index page.
    """
    conn = get_db_connection()
    
    if conn:
        conn.close()  # Close the database connection if it exists

    session.pop('username', None)  # Remove the username from the session
    session.pop('user_id', None)
    session.pop('name', None)
    response = make_response(redirect(url_for('index')))
    response.set_cookie('logged_in', '', expires=0)  # Expire the login cookie
    flash('You have been logged out!', 'info')  # Notify the user

    return response
