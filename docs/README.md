
# Regional News Aggregator Backend

This backend is built to power a regional news aggregation platform focused on Lewiston. It supports user management, news aggregation, weather updates, and emergency alerts.

## Features
- User registration, login, and authentication.
- Aggregation of news articles from RSS feeds.
- Real-time weather and emergency alerts.
- Transparent source management.
- Scalable architecture with Redis caching and Celery task scheduling.

## Directory Structure
```
backend/
├── app/
│   ├── api/
│   ├── modules/
│   ├── utilities/
│   ├── models/
│   ├── tasks/
│   ├── main.py
│   ├── config.py
├── tests/
│   ├── test_general.py
│   ├── test_users.py
├── .env.example
```


