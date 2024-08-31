# Social Networking API

This is a Django Rest Framework-based API for a social networking application. It includes user authentication, user search, friend request management, and friend listing functionalities.

## Features
- User sign-up and login with email.
- Search users by email or name.
- Send, accept, and reject friend requests.
- List friends and pending friend requests.
- Rate limiting on friend requests (no more than 3 requests per minute).

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/roopeshkp34/social-network.git
cd social_network
```

### 2. Start the Development server
```bash
docker compose up --build
```

