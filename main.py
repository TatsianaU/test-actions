from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import FastAPI, HTTPException, Query

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


def _zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown timezone: {name}") from exc


def _parse_time(value: str | None, source: ZoneInfo) -> datetime:
    if value is None:
        return datetime.now(source)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid time. Use ISO 8601, for example 2026-09-30T15:32:38",
        ) from exc
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=source)
    return parsed


@app.get("/time/convert")
def convert_time(
    to: str,
    time: str | None = None,
    from_tz: str = Query(default="UTC", alias="from"),
) -> dict[str, str]:
    source = _zone(from_tz)
    target = _zone(to)
    moment = _parse_time(time, source)
    return {
        "from_time": moment.astimezone(source).isoformat(timespec="seconds"),
        "from_timezone": from_tz,
        "to_time": moment.astimezone(target).isoformat(timespec="seconds"),
        "to_timezone": to,
    }
