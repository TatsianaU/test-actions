from datetime import datetime

from fastapi import FastAPI

app = FastAPI(title="Server Time API")


@app.get("/time")
def get_server_time() -> dict[str, str]:
    now = datetime.now().astimezone()
    return {
        "server_time": now.isoformat(timespec="seconds"),
        "timezone": now.tzname() or "local",
    }
