# FastAPI Login and Signup Backend

A simple FastAPI backend providing user authentication with login and signup functionality using JWT tokens.

## Features

- User registration (signup)
- User authentication (login) with JWT tokens
- Password hashing with bcrypt
- In-memory user storage (for development/demo purposes)
- Automatic API documentation with Swagger UI

## Installation

1. **Clone or navigate to the project directory:**

   ```
   cd c:/Users/MY PC/Documents/backend/first-backend
   ```

2. **Create a virtual environment:**

   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```
   pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography] python-multipart
   ```

## Running the Server

1. **Start the FastAPI server:**

   ```
   python -m uvicorn main:app --reload
   ```

2. **Access the API:**
   - Server will be running at: `http://127.0.0.1:8000`
   - Interactive API documentation: `http://127.0.0.1:8000/docs`
   - Alternative docs: `http://127.0.0.1:8000/redoc`

## API Endpoints

### 1. Signup

- **Endpoint:** `POST /signup`
- **Description:** Register a new user
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "hashed_password": "string"
  }
  ```

### 2. Login

- **Endpoint:** `POST /login`
- **Description:** Authenticate user and get JWT token
- **Request Body (form data):**
  ```
  username: string
  password: string
  ```
- **Response:**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

### 3. Get Current User

- **Endpoint:** `GET /users/me`
- **Description:** Get current authenticated user information
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "hashed_password": "string"
  }
  ```

## Usage Examples

### Using curl

1. **Signup:**

   ```bash
   curl -X POST "http://127.0.0.1:8000/signup" \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
   ```

2. **Login:**

   ```bash
   curl -X POST "http://127.0.0.1:8000/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=testuser&password=password123"
   ```

3. **Get User Info (replace TOKEN with actual token):**
   ```bash
   curl -X GET "http://127.0.0.1:8000/users/me" \
        -H "Authorization: Bearer TOKEN"
   ```

### Using Python requests

```python
import requests

# Signup
signup_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
response = requests.post("http://127.0.0.1:8000/signup", json=signup_data)
print(response.json())

# Login
login_data = {
    "username": "testuser",
    "password": "password123"
}
response = requests.post("http://127.0.0.1:8000/login", data=login_data)
token = response.json()["access_token"]

# Get user info
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://127.0.0.1:8000/users/me", headers=headers)
print(response.json())
```

## Project Structure

```
first-backend/
├── main.py          # FastAPI application and routes
├── models.py        # Pydantic models for API schemas
├── auth.py          # Authentication utilities (hashing, JWT)
├── README.md        # This documentation
├── TODO.md          # Development notes
└── venv/            # Virtual environment (created during setup)
```

## Security Notes

- Passwords are hashed using bcrypt before storage
- JWT tokens are used for authentication
- In production, replace in-memory storage with a proper database
- Change the SECRET_KEY in auth.py for production use
- Implement proper CORS settings if needed
- Add rate limiting for production deployment

## Development

- The server runs with `--reload` flag for automatic reloading on code changes
- API documentation is automatically generated and available at `/docs`
- All endpoints include proper error handling and validation

## Next Steps

For production use, consider:

- Integrating a database (PostgreSQL, MongoDB, etc.)
- Adding email verification for signup
- Implementing password reset functionality
- Adding user roles and permissions
- Setting up proper logging and monitoring
- Adding rate limiting and security middleware
