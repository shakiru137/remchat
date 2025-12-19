# Remchat - Real-time Chat Application

Remchat is a real-time chat application built with Flask and Socket.IO, featuring user authentication, direct messaging, and post sharing capabilities.

## Features

- User authentication (signup, login, logout)
- Real-time chat functionality
- Post creation and sharing
- User profiles and following system
- Direct messaging
- Image sharing
- Like and comment system
- Search functionality

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shakiru137/remchat.git
cd remchat
```

2. Create and activate a virtual environment:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Database Setup

1. Create a MySQL database:

```sql
CREATE DATABASE remchat;
```

2. Create a MySQL user and grant privileges:

```sql
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON remchat.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;
```

3. Import the database schema:

```bash
mysql -u myuser -p remchat < database.sql
```

4. Configure the database connection:
   - Copy `.env.example` to `.env`
   - Update the database credentials in `.env`:

```
DB_USER=remchat_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=remchat
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your_secret_key
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=remchat
```

## Running the Application

1. Start the Flask development server:

```bash
python app.py
```

2. Access the application at `http://localhost:5000`

## Project Structure

```
remchat/
├── app.py                 # Main application file
├── database.sql          # Database schema
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── static/              # Static files
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Image assets
├── templates/           # HTML templates
└── tests/              # Test files
```

## Testing

Run the test suite:

```bash
pytest
```

## Security Features

- Password hashing using bcrypt
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure session management
- Input sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Flask
- Socket.IO
- MySQL
- Bootstrap
- Font Awesome
