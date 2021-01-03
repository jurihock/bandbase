import json

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from typing import Optional

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security

from bandbase.core.database import *

router = APIRouter()


@router.get('/', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)])
def read_root():
    return {"Hello": "World"}


@router.get('/test')
def test(request: Request):

    with bandbase.core.database.session() as db:

        contacts = db.query(Contact).all()

        total = len(contacts)

        print(total)

    return {}


@router.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
