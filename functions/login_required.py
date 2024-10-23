from functools import wraps
from flask import redirect, url_for, session, flash, request
from functions.log_out import log_out

def login_required(f):
    """
    Decorator to ensure that a user is logged in before accessing certain routes.

    If the user is not logged in, they will be redirected to the index page
    with a warning message. It checks both session and cookie to determine 
    the user's login status.

    Args:
        f (function): The view function to be decorated.

    Returns:
        function: The decorated view function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logged_in = request.cookies.get('logged_in')
        
        if not session.get('username') and not logged_in:
            log_out()  # Perform logout operations
            flash('You need to be logged in to access this page.', 'warning')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)

    return decorated_function
