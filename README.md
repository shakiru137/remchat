# RemChat

RemChat is a real-time chat application built with Flask, leveraging the power of WebSockets through Flask-SocketIO. This application allows users to sign up, log in, chat with friends, follow/unfollow users, and post content.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Routes](#routes)
- [Socket Events](#socket-events)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Real-time messaging with WebSocket support
- User profiles with follow/unfollow functionality
- Post content and comments on posts
- Search for users
- Responsive design

## Technologies Used

- Python
- Flask
- Flask-SocketIO
- Flask-Babel (for localization)
- Flask-Session
- MySQL (for database management)
- HTML/CSS/JavaScript (for front-end)
- Bootstrap (for responsive design)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/shakiru137/remchat.git
   cd remchat
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**

   #### On windows

   ```bash
   venv\Scripts\activate
   ```

   #### On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

4. **Install the required packages:**

   ```bash
   Install the required packages:
   ```

5. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application:**

   ```bash
   python3 app.py
   ```

## Usage

- Navigate to http://127.0.0.1:5000 to access the login page.
- Sign up for a new account or log in if you already have one.
- Once logged in, you can access the user dashboard, send messages, follow/unfollow users, and create posts.

## Project Structure

```bash
remchat/
│
├── app.py                     # Main application file
├── requirements.txt           # Python dependencies
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                 # HTML templates
│   ├── index.html
│   ├── signup.html
│   ├── dashboard.html
│   └── search.html
├── functions/                 # Helper functions
│   ├── login_user.py
│   ├── signup_user.py
│   ├── user_dashboard.py
│   ├── follow_user.py
│   ├── unfollow_user.py
│   ├── search_users_logic.py
│   ├── log_out.py
│   ├── get_db_connection.py
│   └── login_required.py
└── chats/                     # Chat-related functionalities
    ├── messages.py
    └── chat_room.py
└── posts/                     # Post-related functionalities
    ├── load_paginated_posts.py
    ├── like_post.py
    ├── delete_post.py
    ├── post_content.py
    └── post_comment.py
```

## Routes

- / or /index: Login page
- /signup: User registration
- /dashboard/<username>: User dashboard
- /search/<username>: User search results
- /messages/<username>: User messages
- /chat_room/<username>/<int:user_id>: Chat room for messaging
- /posts/<username>/: View user posts
- /post_content/<username>: Post content
- /comment/<int:post_id>: Comment on a post
- /logout: Log out

## Socket Events

- follow: Event to follow a user
- unfollow: Event to unfollow a user
- join: Event to join a chat room
- leave: Event to leave a chat room
- message: Event to send and receive messages
- like_post: Event to like a post

## ContributingContributing

- Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or suggestions.
