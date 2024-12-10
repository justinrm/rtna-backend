from celery import Celery
from app.modules.content_aggregation import aggregate_articles
from app.modules.weather import fetch_weather
from app.modules.market_data import fetch_market_data
from app.modules.emergency_alerts import fetch_emergency_alerts
from app.utilities.logging import log_event, log_exception
from datetime import datetime

# Celery configuration
app = Celery("scheduler", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

@app.task(bind=True)
def aggregate_content(self):
    """
    Celery task to aggregate articles from active sources.
    """
    log_event("SCHEDULER", "Starting scheduled content aggregation.")
    try:
        result = aggregate_articles()
        log_event("SCHEDULER", f"Content aggregation completed. Articles aggregated: {result['total_articles']}")
    except Exception as e:
        log_exception(e, "Failed to aggregate content during scheduled task")
        raise

@app.task(bind=True)
def update_weather(self, location: str):
    """
    Celery task to update weather data for a specific location.
    """
    log_event("SCHEDULER", f"Starting weather update for {location}.")
    try:
        weather_data = fetch_weather(location)
        log_event("SCHEDULER", f"Weather updated for {location}: {weather_data}")
    except Exception as e:
        log_exception(e, f"Failed to update weather for {location}")
        raise

@app.task(bind=True)
def update_market_data(self, symbol: str):
    """
    Celery task to update market data for a specific stock symbol.
    """
    log_event("SCHEDULER", f"Starting market data update for {symbol}.")
    try:
        market_data = fetch_market_data(symbol)
        log_event("SCHEDULER", f"Market data updated for {symbol}: {market_data}")
    except Exception as e:
        log_exception(e, f"Failed to update market data for {symbol}")
        raise

@app.task(bind=True)
def update_emergency_alerts(self, region: str):
    """
    Celery task to fetch emergency alerts for a specific region.
    """
    log_event("SCHEDULER", f"Starting emergency alerts update for {region}.")
    try:
        alerts = fetch_emergency_alerts(region)
        log_event("SCHEDULER", f"Emergency alerts updated for {region}: {alerts}")
    except Exception as e:
        log_exception(e, f"Failed to update emergency alerts for {region}")
        raise

@app.task
def periodic_heartbeat():
    """
    A periodic heartbeat task for monitoring the scheduler's health.
    """
    log_event("SCHEDULER", f"Scheduler heartbeat at {datetime.now().isoformat()}")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Register periodic tasks with the Celery scheduler.
    """
    # Schedule content aggregation every hour
    sender.add_periodic_task(3600.0, aggregate_content.s(), name="Aggregate content every hour")

    # Schedule weather updates every 30 minutes for default location
    sender.add_periodic_task(1800.0, update_weather.s("Lewiston"), name="Update weather every 30 minutes")

    # Schedule market data updates every 15 minutes for AAPL stock
    sender.add_periodic_task(900.0, update_market_data.s("AAPL"), name="Update market data every 15 minutes")

    # Schedule emergency alerts updates every 45 minutes for default region
    sender.add_periodic_task(2700.0, update_emergency_alerts.s("Lewiston"), name="Update emergency alerts every 45 minutes")

    # Schedule heartbeat every minute
    sender.add_periodic_task(60.0, periodic_heartbeat.s(), name="Scheduler heartbeat every minute")

