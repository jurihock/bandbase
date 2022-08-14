from fastapi import APIRouter, Depends, Request, Response, HTTPException

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.schemas.database import *
from bandbase.schemas.lists import *


router = APIRouter(prefix='', tags=['lists', 'contacts'])

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
                 'pinned': category.IsPersistent or category.IsReferenced}
                for category in categories
            ]
        }
