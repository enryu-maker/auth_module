from fastapi import FastAPI, Depends, Header
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from app.db.session import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import JSONResponse
import logging

from app.api.v1.endpoints import auth, admin, block
from app.core.config import settings

# Create FastAPI app instance
app = FastAPI()

app.mount("/images", StaticFiles(directory="static/images"), name="images")


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
app.include_router(admin.router)
app.include_router(block.router)


# Root endpoint


@app.get("/")
async def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # The first IP in the list is the client's IP
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.client.host,
        print(request.client.port)
    return {"client_ip": ip}

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
