from flask import session, request, flash, redirect, url_for, render_template
from functions.get_db_connection import get_db_connection
from functions.upload_profile_image import upload_profile_image
from functions.system_picture import system_picture

def user_dashboard():
    """
    Displays the user dashboard, allowing the user to upload a profile image
    and view their details.

    Returns:
        Response: Renders the dashboard template with user details and profile image.
    """
    username = session.get('username')

    if not username:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('index'))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Handle profile image upload
            if request.method == 'POST':
                upload_profile_image()

            # Fetch user details from the database
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            details = cursor.fetchone()

            if not details:
                flash('User not found!', 'warning')
                return redirect(url_for('index'))

            # Decode the profile picture if it exists
            # Assumes details[5] is the profile_picture column
            photo = details[5].decode('utf-8') if len(details) > 5 and details[5] else system_picture()
            return render_template('dashboard.html', img=photo, details=details)

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('index'))
