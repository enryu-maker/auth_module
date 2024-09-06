from fastapi import FastAPI
from db.session import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import JSONResponse
import logging

from api.v1.endpoints import auth
from core.config import settings


# Create FastAPI app instance
app = FastAPI()


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (for security)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# HTTPS Redirect Middleware (optional, if you want to enforce HTTPS)
if settings.ENFORCE_HTTPS:
    app.add_middleware(HTTPSRedirectMiddleware)

# Exception handlers


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "details": exc.errors()},
    )

# Include the API routers
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

# Root endpoint


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Application startup event handler


@app.on_event("startup")
async def on_startup():
    # Initialize logging or other startup procedures
    logging.basicConfig(level=logging.INFO)
    logging.info("Application startup")

# Application shutdown event handler


@app.on_event("shutdown")
async def on_shutdown():
    # Clean up resources or other shutdown procedures
    logging.info("Application shutdown")
