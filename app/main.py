from fastapi import FastAPI
from app.config import QR_DIRECTORY
# Make sure these imports match your project structure.
from app.routers import qr_code, oauth
from app.services.qr_service import create_directory
from app.utils.common import setup_logging

# Set up logging based on the configuration specified in your logging configuration file.
# This is essential for monitoring and debugging the application.
setup_logging()

# Ensure the directory for storing QR codes exists when the application starts.
# If it doesn't exist, it will be created.
create_directory(QR_DIRECTORY)

# Create an instance of the FastAPI application with metadata.
app = FastAPI(
    title="QR Code Manager",
    description=(
        "A FastAPI application for creating, listing available codes, and deleting QR codes. "
        "It also supports OAuth for secure access."
    ),
    version="0.0.1",
    redoc_url=None,
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Include routers to define paths and operations for the API.
# QR Code management routes.
app.include_router(qr_code.router)
# OAuth authentication routes.
app.include_router(oauth.router)
