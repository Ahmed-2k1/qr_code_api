# Import necessary modules and functions from FastAPI and the standard library
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES  # Custom configuration setting
from app.schema import Token  # Import the Token model from our application
from app.utils.common import authenticate_user, create_access_token

# Initialize OAuth2PasswordBearer for OAuth2 Password Flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create an API router for registering the endpoint(s)
router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login and access token issuance.

    Parameters:
    - form_data (OAuth2PasswordRequestForm): The form containing username and password, automatically parsed.

    Returns:
    - A dictionary containing the access token and its type (Bearer).
    """
    # Authenticate the user with the provided credentials
    user = authenticate_user(form_data.username, form_data.password)

    # If authentication fails, raise an exception
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # Notify client to use Bearer token
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Calculate token expiration based on configuration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Generate the access token
    access_token = create_access_token(
        data={"sub": user["username"]},  # Subject of the token
        expires_delta=access_token_expires
    )

    # Return the access token and its type
    return {"access_token": access_token, "token_type": "bearer"}
