# JWT Authentication Implementation with Flask

This project demonstrates a secure JWT (JSON Web Token) authentication system implemented using Flask. It includes user registration, login, protected routes, and automatic session expiration.

## Features

- User registration with password hashing
- Secure login system with JWT
- Protected dashboard route
- Automatic token expiration and logout
- Environment variable configuration
- Clean and responsive UI using Bootstrap
- Flash messages for user feedback

## Technical Stack

- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-JWT-Extended**: JWT implementation
- **Werkzeug**: Password hashing
- **Python-dotenv**: Environment variable management
- **SQLite**: Database (can be easily changed to other databases)
- **Bootstrap 5**: Frontend styling

## Project Structure

```
JWT_Implementation/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
└── templates/         # HTML templates
    ├── login.html
    ├── signup.html
    └── dashboard.html
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   SECRET_KEY=your_super_secret_key_here
   JWT_SECRET_KEY=jwt_super_secret_key_123
   DATABASE_URL=sqlite:///jwt_auth.db
   JWT_ACCESS_TOKEN_EXPIRES=30
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Security Features

1. **Password Hashing**: All passwords are hashed using Werkzeug's security functions
2. **JWT Authentication**: Secure token-based authentication using Flask-JWT-Extended
3. **Environment Variables**: Sensitive configuration stored in .env file
4. **Token Expiration**: Automatic session timeout after configured period
5. **Protected Routes**: Secure routes using JWT authentication decorator

## API Endpoints

- `GET /`: Home page (redirects to login)
- `GET/POST /signup`: User registration
- `GET/POST /login`: User login
- `GET /dashboard`: Protected dashboard (requires valid JWT)
- `GET /logout`: User logout

## Frontend Features

- Responsive design using Bootstrap 5
- Clean and modern UI
- Flash messages for user feedback
- Automatic session expiration handling
- Token-based authentication

## Best Practices Implemented

1. **Security**:
   - Password hashing
   - Environment variable usage
   - JWT token expiration
   - Protected routes

2. **Code Organization**:
   - Modular template structure
   - Clean separation of concerns
   - Clear file organization

3. **User Experience**:
   - Responsive design
   - Clear feedback messages
   - Automatic session handling

## Future Enhancements

1. Add email verification
2. Implement password reset functionality
3. Add remember me functionality
4. Implement refresh tokens
5. Add user profile management
6. Implement role-based access control

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.