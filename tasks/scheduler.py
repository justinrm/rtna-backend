from celery import Celery
from app.modules.weather import fetch_weather
from app.modules.market_data import fetch_market_data
from app.modules.emergency_alerts import fetch_emergency_alerts
from app.config import settings
from app.utilities.logging import log_event, log_exception
from datetime import datetime

# Celery configuration
app = Celery("scheduler", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@app.task(bind=True)
def update_weather(self, location: str):
    try:
        weather_data = fetch_weather(location)
        log_event("SCHEDULER", f"Weather updated for {location}: {weather_data}")
    except Exception as e:
        log_exception(e, f"Failed to update weather for {location}")
        raise

@app.task(bind=True)
def update_market_data(self, symbol: str):
    try:
        market_data = fetch_market_data(symbol)
        log_event("SCHEDULER", f"Market data updated for {symbol}: {market_data}")
    except Exception as e:
        log_exception(e, f"Failed to update market data for {symbol}")
        raise

@app.task(bind=True)
def update_emergency_alerts(self, region: str):
    try:
        alerts = fetch_emergency_alerts(region)
        log_event("SCHEDULER", f"Emergency alerts updated for {region}: {alerts}")
    except Exception as e:
        log_exception(e, f"Failed to update emergency alerts for {region}")
        raise

@app.task
def periodic_heartbeat():
    log_event("SCHEDULER", f"Scheduler heartbeat at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(900.0, update_weather.s(settings.DEFAULT_LOCATION), name="Update weather")
    sender.add_periodic_task(300.0, update_market_data.s("AAPL"), name="Update market data")
    sender.add_periodic_task(1800.0, update_emergency_alerts.s(settings.DEFAULT_REGION), name="Update alerts")
    sender.add_periodic_task(60.0, periodic_heartbeat.s(), name="Heartbeat")

