
# Real-Time News Aggregator (RTNA) Backend

This is the backend service for the Real-Time News Aggregator (RTNA), providing APIs, data processing, and services to power real-time news, emergency alerts, market data, weather information, and content aggregation. It is designed to be extensible and scalable, supporting both frontend and external applications.

## Features

- **Weather API**: Fetch real-time weather data.
- **Market Data API**: Aggregate stock and commodity market prices.
- **Emergency Alerts**: Retrieve regional emergency notifications.
- **Content Aggregation**: Process and serve RSS feed data with transparency metadata.
- **Feedback Module**: Collect and process user feedback.
- **Source Discovery**: Discover and manage news sources.
- **User Management**: Role-based access control using OAuth2.
- **Transparency Panel**: Expose metadata for transparency and debugging.

---

## Table of Contents

1. [Installation](#installation)
2. [Environment Configuration](#environment-configuration)
3. [Running the Backend](#running-the-backend)
4. [API Endpoints](#api-endpoints)
5. [Directory Structure](#directory-structure)
6. [Testing](#testing)
7. [Contributing](#contributing)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd backend-new
   ```

2. **Set Up Environment**:
   - Copy the example environment file and update configurations:
     ```bash
     cp template.env .env
     ```

3. **Install Dependencies**:
   - Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Node.js dependencies (for proxy services):
     ```bash
     npm install
     ```

4. **Database Setup**:
   - Ensure PostgreSQL is running and configured.
   - Initialize database migrations:
     ```bash
     alembic upgrade head
     ```

5. **Run Redis for Caching**:
   - Redis is required for caching mechanisms:
     ```bash
     docker run -p 6379:6379 redis
     ```

6. **Run the Backend**:
   ```bash
   python main.py
   ```

---

## Environment Configuration

The `.env` file contains configurations. Update these as needed:

- **Database**:
  ```
  DATABASE_URL=postgresql://user:password@host:port/dbname
  ```

- **Redis**:
  ```
  REDIS_URL=redis://localhost:6379/0
  ```

- **OAuth and Security**:
  ```
  SECRET_KEY=your_secret_key_here
  ```

- **API Keys**:
  Include keys for third-party integrations like weather or market data.

---

## API Endpoints

### Base URL
All endpoints are prefixed with `/api`.

| Endpoint                | Method | Description                        |
|-------------------------|--------|------------------------------------|
| `/api/health`           | GET    | Health check for the backend.      |
| `/api/weather`          | GET    | Fetch real-time weather data.      |
| `/api/market_data`      | GET    | Retrieve stock/commodity prices.   |
| `/api/emergency_alerts` | GET    | Fetch emergency alerts.            |
| `/api/articles`         | GET    | Fetch aggregated content articles. |
| `/api/feedback`         | POST   | Submit user feedback.              |
| `/api/sources`          | GET    | Get list of news sources.          |
| `/api/cache`            | GET    | Access cache status and management.|

**Example**: Fetch weather data:
```bash
curl -X GET http://localhost:8000/api/weather?city=Lewiston
```

---

## Directory Structure

```
backend-new/
│
├── api/                       # API endpoint definitions
│   ├── weather.py             # Weather API
│   ├── market_data.py         # Market data API
│   ├── transparency_panel.py  # Transparency metadata APIs
│   ├── ...                    # Other APIs
│
├── models/                    # Database ORM models
│   ├── weather.py             # Weather model
│   ├── alerts.py              # Alerts model
│   ├── ...                    # Other models
│
├── modules/                   # Core backend modules
│   ├── emergency_alerts.py    # Emergency alert processing
│   ├── source_discovery.py    # Source management module
│   ├── ...                    # Other modules
│
├── utilities/                 # Shared utilities
│   ├── database.py            # Database connection setup
│   ├── cache.py               # Redis caching
│   ├── security.py            # OAuth2 and security handling
│
├── tasks/                     # Scheduled tasks (Celery)
├── tests/                     # Unit tests
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker setup
├── docker-compose.yml         # Docker Compose for multi-service setup
├── alembic/                   # Database migrations
└── config.py                  # App configurations
```

---

## Testing

Run unit tests using `pytest`:
```bash
pytest tests/
```

---

## Contributing

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push and submit a pull request.

---

## Docker Deployment

To deploy using Docker:
```bash
docker-compose up --build
```

Ensure all environment variables are set in `.env` before deployment.

