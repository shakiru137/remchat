from flask import request, flash, redirect, url_for, session, render_template
from functions.get_db_connection import get_db_connection

def comment_page(post_id):
    """
    Handles both loading and posting comments for a specific post

    Args:
        post_id (int): The ID of the post to add or view comments.

    If the request method is POST, this function adds a new comment for the post.
    If the request method is GET, it retrieves and displays all comments for the post.

    Returns:
        Response: Renders the post with comments or redirects after posting a comment.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to be logged in to comment.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle posting a comment
        comment_content = request.form.get('comment')

        if not comment_content:
            flash('Comment cannot be empty.', 'warning')
        else:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    try:
                        # Fetch the user's name based on their user_id
                        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
                        name = cursor.fetchone()[0]

                        # Update the comment count for the post
                        cursor.execute("SELECT comment_count FROM posts WHERE id = %s", (post_id,))
                        value = cursor.fetchone()[0]
                        value += 1
                        cursor.execute("UPDATE posts SET comment_count = %s WHERE id = %s", (value, post_id))
                        conn.commit()

                        # Insert the new comment into the comments table
                        cursor.execute(
                            "INSERT INTO comments (post_id, user_id, content, name) VALUES (%s, %s, %s, %s)",
                            (post_id, user_id, comment_content, name)
                        )
                        conn.commit()  # Commit the transaction
                        flash('Comment posted successfully!', 'success')
                    except Exception as e:
                        conn.rollback()  # Rollback in case of error
                        flash(f'An error occurred while posting your comment: {e}', 'danger')

        return redirect(url_for('comment_page_view', post_id=post_id))

    # Handle loading comments (GET request)
    comments = load_comments(post_id)
    return render_template('post_comment.html', post_id=post_id, comments=comments)

def load_comments(post_id):
    """
    Loads comments for a specific post.

    Args:
        post_id (int): The ID of the post to load comments for.

    This function retrieves all comments related to the specified post, 
    ordered by the time they were created.

    Returns:
        list: A list of comments, each containing the name of the commenter, 
              the content of the comment, and the timestamp.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT name, content, created_at FROM comments WHERE post_id = %s ORDER BY created_at ASC",
                (post_id,)
            )
            return cursor.fetchall()
