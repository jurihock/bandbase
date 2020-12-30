import secrets

from fastapi import status as STATUS
from fastapi import APIRouter, Body, Depends, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse

import bandbase.core.common
import bandbase.core.security
import bandbase.core.session

router = APIRouter(prefix='/session', tags=['session'])

# see also
# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2
# https://github.com/tiangolo/fastapi/issues/480


@router.post('/login', dependencies=[Depends(bandbase.core.security.ssl)],
                       response_class=PlainTextResponse)
def login(request: Request,
          response: Response,
          config: bandbase.core.common.Config = Depends(bandbase.core.common.config),
          logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger),
          secret: str = Body(..., embed=True)):

    bandbase.core.session.service.login(request, response, secret)

    return 'HELLO'


@router.get('/logout', dependencies=[Depends(bandbase.core.security.ssl)],
                       response_class=PlainTextResponse)
def logout(request: Request,
           response: Response):

    bandbase.core.session.service.logout(request, response)

    return 'GOODBYE'


@router.get('/check', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                      response_class=PlainTextResponse)
def check():

    return 'OKAY'
