## Real-Time Chat Application

A real-time chat application built with Django, Django Channels, and Redis. This project demonstrates how to use WebSockets for real-time communication between users.
Features

    Real-time messaging: Users can send and receive messages in real-time using WebSockets.

    Room-based chat: Users can join different chat rooms.

    REST API: Built with Django Rest Framework (DRF) for managing chat rooms and messages.

    Scalable: Uses Redis as a channel layer for handling multiple WebSocket connections.

## Technologies Used

    Backend:

        Django

        Django Channels

        Django Rest Framework (DRF)

        Redis (for channel layers)

        SimpleJWT

    Frontend:

        HTML, JavaScript (for WebSocket communication)

    Tools:

        Docker (for containerizing Redis)


## Prerequisites

Before running the project, ensure you have the following installed:

    Python 3.8+

    Docker (for running Redis)

    Redis (optional, if not using Docker)

## Installation
1. Clone the Repository
bash
Copy

git clone git@github.com:ramin971/websocket_chat.git 
cd websocket_chat

2. Set Up a Virtual Environment
bash
Copy

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
bash
Copy

pip install -r requirements.txt

4. Run Redis with Docker

Start the Redis container using Docker :
bash
Copy

docker run --rm --name redis -p 6379:6379 redis

5. Apply Migrations
bash
Copy

python manage.py migrate

6. Run the Development Server
bash
Copy

python manage.py runserver

Running the Project
Start Redis

If you're using Docker, Redis will already be running. Otherwise, start Redis locally:
bash
Copy

redis-server

Start the Django Application
bash
Copy

python manage.py runserver

Visit http://127.0.0.1:8000 in your browser to access the application.
Project Structure
Copy

websocket_demo/
├── core/                  # Chat app
│   ├── consumers.py       # WebSocket consumers
│   ├── routing.py         # WebSocket routing
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # DRF views
│   ├── urls.py            # DRF URL 
│   └── templates/         # HTML templates
├── websocket_demo/              # Django project settings
│   ├── settings.py        # Django settings
│   ├── asgi.py            # ASGI configuration
│   └── urls.py            # URL routing
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

API Endpoints
REST API

    List all chat rooms:
    Copy

    GET /api/rooms/

    List messages in a room:
    Copy

    GET /api/rooms/<room_id>/messages/

    Create a new message:
    Copy

    POST /api/rooms/<room_id>/messages/

## WebSocket API End-Point:

    Connect to a chat room:
    Copy

    GET /api/chat-test/<room_name>/

    create and connect to room_name by real time connection and save messages with username and room in database.
    
    websocket route:
    Copy
    
    ws://localhost:8000/ws/chat/<room_name>/

## Authentication

    JWT authentication is used for securing the API endpoints.
    To obtain a JWT token, send a POST request to http://localhost:8000/api/jwt/create/ with your username and password.
    Include the JWT token in the Authorization header of your requests as Bearer <token>.
