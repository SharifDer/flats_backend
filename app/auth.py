from firebase_admin import auth
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials and credentials.scheme == "Bearer":
            try:
                decoded_token = my_verify_id_token(credentials.credentials)
                return decoded_token
            except Exception:
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
        raise HTTPException(status_code=403, detail="Invalid authorization scheme.")

def my_verify_id_token(token: str):
    return auth.verify_id_token(token)
