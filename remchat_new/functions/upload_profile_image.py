from flask import request, flash, redirect, url_for, session
from functions.get_db_connection import get_db_connection
from functions.compress_img import compress_img
import base64

def encode_image(image):
    """
    Compresses and encodes the image to Base64 format.

    Args:
        image (FileStorage): The image file uploaded by the user.

    Returns:
        str: Base64 encoded string of the compressed image or None if failed.
    """
    byte_data = compress_img(image)
    return base64.b64encode(byte_data).decode('utf-8') if byte_data else None

def upload_profile_image():
    """
    Handles the uploading of a user's profile image.

    Returns:
        Response: Redirects to the dashboard with a success or error flash message.
    """
    image = request.files.get('image')

    if not image:
        flash('No image uploaded! 😞', 'danger')
        return redirect(url_for('dashboard', username=session.get('username')))

    encoded_img = encode_image(image)
    
    if not encoded_img:
        flash('Failed to compress and encode the image! 😞', 'danger')
        return redirect(url_for('dashboard', username=session.get('username')))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Update the user's profile picture in the database
            # Assumes username is unique and present in session
            cursor.execute("UPDATE users SET profile_picture = %s WHERE username = %s",
                           (encoded_img, session.get('username')))
            conn.commit()

            flash('Image uploaded successfully!', 'success')

    except Exception as e:
        flash(f'An error occurred while updating the image: {str(e)}', 'danger')

    return redirect(url_for('dashboard', username=session.get('username')))
