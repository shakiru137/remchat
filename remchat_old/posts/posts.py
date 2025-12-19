from flask import request, render_template, flash, session, redirect, url_for
from functions.get_db_connection import get_db_connection
from functions.system_picture import system_picture
from flask_babel import format_datetime

def load_paginated_posts():
    """
    Loads posts for the specified page with pagination, and enriches them with user details,
    like status, comment counts, and proper date formatting.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Retrieve random post IDs if not already in session
                if 'random_ids' not in session:
                    cursor.execute("SELECT id FROM posts ORDER BY RAND() LIMIT 1000")
                    random_ids = [row[0] for row in cursor.fetchall()]
                    session['random_ids'] = random_ids
                    session['total_posts'] = len(random_ids)

                random_ids = session['random_ids'][start:end]

                # If no posts on this page, show friendly message
                if not random_ids:
                    flash('No posts yet!', 'info')
                    return render_template('posts.html', posts=[], page=page, total_pages=0)

                # Build SQL query
                format_string = ', '.join(['%s'] * len(random_ids))
                query = f"""
                    SELECT id, user_id, content, picture, created_at, likes, comment_count 
                    FROM posts 
                    WHERE id IN ({format_string})
                """
                cursor.execute(query, tuple(random_ids))
                post_contents = cursor.fetchall()

                # If still no posts returned
                if not post_contents:
                    flash('No posts found for this page!', 'info')
                    return render_template('posts.html', posts=[], page=page, total_pages=0)

                total_pages = (session['total_posts'] + per_page - 1) // per_page
                current_user_id = session.get('user_id')
                post_ids = [post[0] for post in post_contents]

                # Fetch user details
                user_ids = [post[1] for post in post_contents]
                placeholders = ', '.join(['%s'] * len(user_ids))
                cursor.execute(
                    f"SELECT id, name, profile_picture FROM users WHERE id IN ({placeholders})",
                    tuple(user_ids)
                )
                user_details = {row[0]: {'name': row[1], 'picture': row[2]} for row in cursor.fetchall()}

                # Fetch liked posts for current user
                liked_posts = set()
                if post_ids:
                    placeholders = ','.join(['%s'] * len(post_ids))
                    cursor.execute(
                        f"SELECT post_id FROM likes WHERE user_id = %s AND post_id IN ({placeholders})",
                        [current_user_id] + post_ids
                    )
                    liked_posts = {row[0] for row in cursor.fetchall()}

                # Process posts
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
                        'created_at_str': format_datetime(created_at),
                        'likes': likes or 0,
                        'is_liked_by_current_user': post_id in liked_posts,
                        'creator_name': creator['name'],
                        'creator_picture': creator['picture'].decode('utf-8') if creator['picture'] else system_picture(),
                        'is_my_post': session['user_id'] == user_id,
                        'comment_count': comment_count
                    }
                    processed_posts.append(processed_post)

                processed_posts.sort(key=lambda post: post['created_at'], reverse=True)

                return render_template(
                    'posts.html',
                    posts=processed_posts,
                    page=page,
                    total_pages=total_pages
                )

    except Exception as e:
        # Only flash real errors
        flash(f'An error occurred while loading posts: {e}', 'danger')
        return redirect(url_for('dashboard', username=session.get('username')))
