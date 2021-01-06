from datetime import datetime
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.core.database import *

router = APIRouter(prefix='/list', tags=['list'])


class ListItem(BaseModel):
    id: int
    name: str
    pinned: bool


class List(BaseModel):
    items: List[ListItem]
    default: Optional[int]
    nullable: bool


@router.post('/contact/category', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                                  response_model=List)
def contact_category():

    with bandbase.core.database.session() as db:

        categories = db.query(ContactCategory) \
                       .order_by(ContactCategory.Name) \
                       .all()

        return {
            'nullable': False,
            'default': 0,
            'items': [
                {'id': category.ID,
                 'name': category.Name,
                 'pinned': category.IsPersistent or category.IsRelated}
                for category in categories
            ]
        }
