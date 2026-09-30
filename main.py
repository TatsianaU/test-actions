from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Server Time API")


def _local_now() -> datetime:
    return datetime.now().astimezone()


def _timezone_name(now: datetime) -> str:
    return now.tzname() or "local"


@app.get("/time")
def get_server_time() -> dict[str, str]:
    now = _local_now()
    return {
        "server_time": now.isoformat(timespec="seconds"),
        "timezone": _timezone_name(now),
    }


@app.get("/date")
def get_server_date() -> dict[str, str]:
    now = _local_now()
    return {
        "server_date": now.date().isoformat(),
        "timezone": _timezone_name(now),
    }


@app.get("/date/utc")
def get_utc_date() -> dict[str, str]:
    now = datetime.now(timezone.utc)
    return {
        "server_date": now.date().isoformat(),
        "timezone": "UTC",
    }
