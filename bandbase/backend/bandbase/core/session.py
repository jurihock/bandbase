import secrets

from fastapi import status as STATUS
from fastapi import Request, Response, HTTPException
from typing import Any, Optional


class SessionException(HTTPException):

    def __init__(self, cookie: str, status_code: int, detail: Any = None) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.cookie = cookie


class SessionService:

    def __init__(self, cookie: str = 'token'):

        self.cookie = cookie

    def login(self, request: Request, response: Response, secret: Optional[str] = None):

        if not secret or 'x' not in secret:
            raise SessionException(cookie=self.cookie, status_code=STATUS.HTTP_401_UNAUTHORIZED)

        token = secrets.token_hex(32)
        max_age_seconds = None
        secure = False
        httponly = True
        samesite = 'lax'

        response.set_cookie(key=self.cookie,
                            value=token,
                            max_age=max_age_seconds,
                            secure=secure,
                            httponly=httponly,
                            samesite=samesite)

    def logout(self, request: Request, response: Response):

        response.delete_cookie(self.cookie)

    def verify(self, request: Request, response: Response):

        token = request.cookies.get(self.cookie)

        if not token:

            raise SessionException(cookie=self.cookie, status_code=STATUS.HTTP_401_UNAUTHORIZED)


service = SessionService()
