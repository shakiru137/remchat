from flask import flash, redirect, url_for, session
from flask_socketio import emit
from functions.get_db_connection import get_db_connection

def like_post(data):
    """
    Handles the 'like_post' event when a user likes or unlikes any post.

    Args:
        data (dict): Contains the 'post_id' for the post the user interacts with.

    The function checks if the current user has already liked the post:
        - If yes, it unlikes the post and decrements the like count.
        - If no, it likes the post and increments the like count.

    Emits:
        - 'like_response': Sends a response back to the client with a success or error message.

    Raises:
        Exception: If any database operation fails.
    """
    post_id = data.get('post_id')
    user_id = session.get('user_id')

    # Ensure user is logged in before allowing them to like/unlike
    if user_id is None:
        flash('You need to be logged in to like posts.', 'danger')
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                # Check if the user already liked the post
                cursor.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
                like = cursor.fetchone()

                # Retrieve current like count
                cursor.execute("SELECT likes FROM posts WHERE id = %s", (post_id,))
                likes = cursor.fetchone()[0]

                if like:  # User has already liked the post, so unlike it
                    if likes > 0:
                        likes -= 1  # Decrement the like count
                        cursor.execute("UPDATE posts SET likes = %s WHERE id = %s", (likes, post_id))
                        cursor.execute("DELETE FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
                        emit('like_response', {'message': 'You unliked the post!', 'status': 'info'})
                    else:
                        emit('like_response', {'message': 'Cannot unlike a post with 0 likes!', 'status': 'warning'})
                else:  # User likes the post
                    likes += 1  # Increment the like count
                    cursor.execute("UPDATE posts SET likes = %s WHERE id = %s", (likes, post_id))
                    cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (post_id, user_id))
                    emit('like_response', {'message': 'You liked the post!', 'status': 'info'})
                
                conn.commit()  # Commit the transaction to save changes

            except Exception as e:
                emit('like_response', {'message': f'An error occurred while liking the post: {str(e)}', 'status': 'danger'})
