from flask import request, render_template, flash, session, redirect, url_for
from functions.get_db_connection import get_db_connection
from functions.system_picture import system_picture
from flask_babel import format_datetime

def load_paginated_posts():
    """
    Loads posts for the specified page with pagination, and enriches them with user details,
    like status, comment counts, and proper date formatting.

    Args:
        None

    Returns:
        Response: Renders the posts page with either the fetched posts or an empty list.
    """
    # Get the page number from the request arguments, defaulting to 1
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page  # Calculate the offset for pagination
    end = start + per_page

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                # Retrieve random posts IDs if not already in session
                if 'random_ids' not in session:
                    cursor.execute("SELECT id FROM posts ORDER BY RAND() LIMIT 1000")
                    random_ids = [row[0] for row in cursor.fetchall()]
                    session['random_ids'] = random_ids
                    session['total_posts'] = len(random_ids)
                
                random_ids = session['random_ids'][start:end]
                if not random_ids:
                    return render_template('posts.html', posts=[])  # Render an empty posts page if no posts are found

                # Build the format string for the SQL query
                format_string = ', '.join(['%s'] * len(random_ids))

                # Fetch posts with pagination and include comment_count in the same query
                query = f"""
                    SELECT id, user_id, content, picture, created_at, likes, comment_count 
                    FROM posts 
                    WHERE id IN ({format_string})
                """
                cursor.execute(query, tuple(random_ids))
                post_contents = cursor.fetchall()

                # Calculate total pages
                total_pages = (session['total_posts'] + per_page - 1) // per_page
                current_user_id = session.get('user_id')  # Ensure user is logged in
                post_ids = [post[0] for post in post_contents]  # Collect post IDs for likes query
                
                # Fetch user details for the post creators
                user_ids = [post[1] for post in post_contents]
                placeholders = ', '.join(['%s'] * len(user_ids))
                cursor.execute(f"SELECT id, name, profile_picture FROM users WHERE id IN ({placeholders})", tuple(user_ids))
                user_details = {row[0]: {'name': row[1], 'picture': row[2]} for row in cursor.fetchall()}

                # Fetch liked post IDs for the current user
                liked_posts = set()
                if post_ids:
                    placeholders = ','.join(['%s'] * len(post_ids))
                    cursor.execute(f"SELECT post_id FROM likes WHERE user_id = %s AND post_id IN ({placeholders})", [current_user_id] + post_ids)
                    liked_posts = {row[0] for row in cursor.fetchall()}  # Set of liked post IDs

                # Process and enrich each post with additional details
                processed_posts = []
                for post in post_contents:
                    post_id, user_id, content, picture, created_at, likes, comment_count = post
                    
                    creator = user_details.get(user_id, {'name': 'Unknown', 'picture': system_picture()})
                    processed_post = {
                        'id': post_id,
                        'user_id': user_id,
                        'content': content,
                        'picture': picture.decode('utf-8') if picture else None,
                        'created_at': created_at,
                        'created_at_str': format_datetime(created_at),  # Add formatted version for display
                        'likes': likes or 0,  # Default to 0 if None
                        'is_liked_by_current_user': post_id in liked_posts,
                        'creator_name': creator['name'],
                        'creator_picture': creator['picture'].decode('utf-8') if creator['picture'] else system_picture(),
                        'is_my_post': session['user_id'] == user_id,
                        'comment_count': comment_count
                    }
                    
                    processed_posts.append(processed_post)  # Add to the list of processed posts

                if not processed_posts:
                    flash('No posts yet!', 'info')

                processed_posts.sort(key=lambda post: post['created_at'], reverse=True)
                # Loop through the sorted list and print the 'created_at' values
                for post in processed_posts:
                    print(post['created_at'])
                return render_template('posts.html', posts=processed_posts, page=page, total_pages=total_pages)  # Render the posts template

            except Exception as e:
                flash(f'An error occurred while loading posts: {e}', 'danger')  # Handle any errors
                return redirect(url_for('dashboard', username=session.get('username')))
