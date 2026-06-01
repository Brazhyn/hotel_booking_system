# Hotel Booking System

[stylio.org/docs](https://staylio.org/docs)

An asynchronous comprehensive hotel booking application built with FastAPI, providing features for managing hotels, rooms, bookings, users, and facilities.

## Functionality

- **User Management**: Registration, authentication, and user profiles
- **Hotel Management**: Create, update, and manage hotel listings
- **Room Management**: Add and manage rooms within hotels with pricing and availability
- **Booking System**: Users can book rooms, view bookings, and manage reservations
- **Facilities**: Manage hotel facilities and amenities
- **Image Handling**: Upload and manage images for hotels and rooms
- **Authentication**: JWT-based authentication for secure access
- **Background Tasks**: Asynchronous task processing with Celery and Redis

## Usage

### Prerequisites
- Docker and Docker Compose
- Python 3.11+

### Running with Docker
1. Clone the repository:
   ```
   git clone https://github.com/Brazhyn/hotel_booking_system.git
   cd hotel_booking
   ```

2. Create a `.env` file in the root directory with the values in .env_example

3. Create a Docker network:
   ```
   docker network create mynetwork
   ```

4. Create postgres container:
   ```
   docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=booking --network=mynetwork --volume pg-booking-data:/var/lib/postgresql/data -d postgres:17
   ```

5. Create redis container:
   ```
   docker run --name booking_cache -p 7379:6379 --network=mynetwork -d redis:8
   ```

6. Start the services:
   **Uncomment ports for local development in docker-compose.yml**
   ```
   docker-compose up --build
   ```

7. Create Nginx container:
   ```
   docker run --name booking_nginx -v ./nginx/nginx.dev.conf:/etc/nginx/conf.d/default.conf --rm -p 80:80 --network=mynetwork -d nginx
   ```

8. The API will be available at `http://localhost/docs`


### Testing
Run tests with pytest:
```
pytest
```

## Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Authentication**: JWT
- **Task Queue**: Celery with Redis
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest
- **Other**: Redis for caching, static file handling