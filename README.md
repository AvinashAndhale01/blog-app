# FastAPI Blog API

A simple Blog REST API built with **FastAPI** featuring JWT authentication, blog management, comments, and user profiles.

## Features

* User Signup & Login
* JWT Authentication
* CRUD operations for Blog Posts
* CRUD operations for Comments
* User Profile (`/users/me`)
* CORS support
* Automatic database table creation

## Installation

```bash
git clone https://github.com/AvinashAndhale01/blog-app.git
cd blog-app

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

API URL:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

## Main Endpoints

### Authentication

* `POST /auth/signup`
* `POST /auth/login`

### Blogs

* `GET /blogs`
* `GET /blogs/{id}`
* `POST /blogs`
* `PUT /blogs/{id}`
* `DELETE /blogs/{id}`

### Comments

* `GET /blogs/{post_id}/comments`
* `POST /blogs/{post_id}/comments`
* `PUT /blogs/{post_id}/comments/{comment_id}`
* `DELETE /blogs/{post_id}/comments/{comment_id}`

### Users

* `GET /users/me`

### Health Check

* `GET /status`

## Tech Stack

* FastAPI
* SQLAlchemy
* JWT Authentication
* Pydantic
* Uvicorn

Built with FastAPI 🚀
