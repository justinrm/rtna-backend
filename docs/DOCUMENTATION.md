
# Developer Documentation

## Overview
This backend is designed to power a regional news aggregator. It integrates multiple modules for user management, content aggregation, and real-time updates, built with FastAPI.

## Getting Started
1. Clone the repository.
2. Create a `.env` file based on `.env.example`.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```
   uvicorn app.main:app --reload
   ```

## Key Modules
### 1. `api/`
Contains FastAPI route definitions:
- `users.py`: User management and authentication.
- `articles.py`: CRUD operations for news articles.
- `sources.py`: Manage news sources.

### 2. `modules/`
Core functionality for:
- Weather updates.
- Emergency alerts.
- RSS feed aggregation.

### 3. `utilities/`
Shared utilities for:
- Caching with Redis (`cache.py`).
- Database connections (`database.py`).
- Input validation (`validation.py`).
- Security features (`security.py`).

### 4. `tasks/`
Background tasks for periodic updates using Celery.

## Testing
Run tests using pytest:
```
pytest tests/
```

## Deployment
1. Build a production image:
   ```
   docker build -t regional-news-backend .
   ```

2. Deploy using Docker Compose:
   ```
   docker-compose up -d
   ```
