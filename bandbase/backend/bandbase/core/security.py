import secrets

from fastapi import status as STATUS
from fastapi import Depends, Request, Response, HTTPException

import bandbase.core.common
import bandbase.core.session


def ssl(request: Request,
        response: Response,
        config: bandbase.core.common.Config = Depends(bandbase.core.common.config),
        logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    # print('SSL', request.scope)

    if 'HTTP' not in request.scope['type'].upper():
        raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND)


def auth(request: Request,
         response: Response,
         config: bandbase.core.common.Config = Depends(bandbase.core.common.config),
         logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    bandbase.core.session.service.verify(request, response)
