from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utilities.database import execute_query
from app.utilities.security import hash_password, verify_password, create_access_token
from app.utilities.validation import is_valid_email, is_strong_password, sanitize_input
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

@router.post("/register")
async def register_user(username: str, email: str, password: str):
    """
    Register a new user.
    """
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format.")
    if not is_strong_password(password):
        raise HTTPException(status_code=400, detail="Password does not meet strength requirements.")

    hashed_password = hash_password(password)
    query = """
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (%s, %s, %s, NOW())
    """
    try:
        execute_query(query, (sanitize_input(username), sanitize_input(email), hashed_password))
        return {"message": "User registered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in and retrieve an access token.
    """
    query = "SELECT id, password_hash FROM users WHERE email = %s"
    try:
        result = execute_query(query, (sanitize_input(form_data.username),))
        if not result["data"]:
            raise HTTPException(status_code=401, detail="Invalid credentials.")

        user = result["data"][0]
        if not verify_password(form_data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials.")

        token = create_access_token({"sub": str(user["id"])}, expires_delta=timedelta(minutes=15))
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

