from flask import request, redirect, url_for, session, render_template, flash
from functions.get_db_connection import get_db_connection
from functions.compress_img import compress_img
import base64

def post_content():
    """
    Handles the creation of a new post, including optional content and an image

    This function processes a POST request to create a new post in the database.
    It validates the input, compresses the image if provided, and stores the post in the database.
    On success, it redirects to the posts view; on failure, it flashes an error message.

    Returns:
        Response: Redirects to the posts view on success or renders the post content page on GET request.
    """
    if request.method == 'POST':
        # Get the form content and image (if any)
        content = request.form.get('content', '').strip()  # Strip to remove excess whitespace
        image = request.files.get('image')
        user_id = session.get('user_id')

        # Check that at least content or an image is provided
        if not content and not image:
            flash('Content or image must be provided.', 'warning')
            return redirect(url_for('post_content'))  # Redirect to the same page if validation fails

        # Encode and compress the image if present
        encoded_img = None
        if image:
            byte_data = compress_img(image)  # Compress the image before storing
            encoded_img = base64.b64encode(byte_data).decode('utf-8') if byte_data else None

        # Insert post into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # SQL query to insert post data
            query = "INSERT INTO posts (user_id, content, picture) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, content, encoded_img))
            conn.commit()  # Commit the transaction
            flash('Post created successfully!', 'success')
        except Exception as e:
            conn.rollback()  # Rollback the transaction on error
            flash(f'An error occurred while creating the post: {str(e)}', 'danger')
        finally:
            cursor.close()  # Ensure cursor is closed
            conn.close()    # Ensure connection is closed

        # Redirect to the posts view after successfully creating the post
        return redirect(url_for('post_content_view', username=session['username']))

    # Render the post creation form if it's a GET request
    return render_template('post_content.html')
