from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, TimeoutError

from app.api.v1.router import router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="1.0", debug=settings.debug)
app.include_router(router, prefix=settings.api_v1_prefix)


@app.exception_handler(TimeoutError)
@app.exception_handler(OperationalError)
async def database_unavailable(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": {"code": "DATABASE_UNAVAILABLE", "message": "Database temporarily unavailable."}},
    )
