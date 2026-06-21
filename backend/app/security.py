import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

APP_API_KEY = os.getenv("APP_API_KEY")


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != APP_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    return True