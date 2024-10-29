from flask import request, redirect, url_for, flash
from functions.get_db_connection import get_db_connection
from bcrypt import hashpw, gensalt


def check_names(name):
    """Check if the name contains at least two capitalized parts."""
    names = name.split()
    return len(names) >= 2 and all(n[0].isupper() for n in names)

def check_password(password):
    """Check if the password is at least 7 characters long and contains at least one number."""
    return len(password) > 6 and any(char.isdigit() for char in password)

def user_exists(cursor, username, email, name):
    """Check if the user already exists based on username, email, or name."""
    cursor.execute(
        "SELECT * FROM users WHERE username = %s OR email = %s OR name = %s", 
        (username, email, name)
    )
    return cursor.fetchone()

def signup_user():
    """
    Handles user registration by collecting user details from the signup form,
    checking for existing name, username, or email, and storing the new user in the database.

    Returns:
        Response: Redirects to the index page upon successful registration or
                  back to the signup page in case of errors.
    """
    name, username, email, password = (request.form[key] for key in ('name', 'username', 'email', 'password'))
    
    # Validate the name format
    if not check_names(name):
        flash('Name must be in the format "First Last".', 'danger')
        return redirect(url_for('signup'))
    
    # Validate the password format
    if not check_password(password):
        flash('Password must be at least 7 characters long and contain at least one number.', 'danger')
        return redirect(url_for('signup'))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if the username, email, or name already exists in the database
            existing_user = user_exists(cursor, username, email, name)
            if existing_user:
                if existing_user[2] == username:
                    flash('Username already exists! 😞', 'danger')
                elif existing_user[4] == email:
                    flash('Email already exists! 😞', 'danger')
                return redirect(url_for('signup'))

            # Hash the password before storing it
            hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            
            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)",
                (name, username, email, hashed_password)
            )
            conn.commit()
            flash('Registration successful! 🎉', 'success')

    except Exception as e:
        flash(f'An error occurred while registering: {str(e)}', 'danger')
    
    return redirect(url_for('index'))
