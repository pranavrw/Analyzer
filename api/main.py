# api/main.py
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import auth, routes_dataset, routes_analyzer  # these modules should only define routers

app = FastAPI(title="YOLO Weekly Training Service")

# include routers (each must expose `router`)
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(routes_dataset.router, prefix="/api", tags=["dataset"])
app.include_router(routes_analyzer.router, prefix="/api", tags=["analyzer"])


@app.get("/api/ping", tags=["health"])
def ping():
    return {"message": "pong"}


# developer-friendly error handler — shows traceback in JSON (remove in production)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "traceback": traceback.format_exc()
        },
    )
