from fastapi import APIRouter, Depends, Request, Response, HTTPException

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.schemas.database import *
from bandbase.schemas.tables import *


router = APIRouter(prefix='', tags=['tables', 'contacts'])


@router.post('/contacts', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                          response_model=Table)
def contacts(query: TableQuery):

    columns = \
    [
        {'name': 'name',     'filterable': True, 'sortable': True},
        {'name': 'category', 'filterable': True, 'sortable': True},
        {'name': 'comment',  'filterable': True, 'sortable': True}
    ]

    if query.probe:

        query = \
        {
            'probe': True,
            'sort': {'name': '+'},
            'limit': 10
        }

        return \
        {
            'query': query,
            'columns': columns,
            'rows': [],
            'total': 0
        }

    filter_by_name = query.get_filter_value('name')
    filter_by_category = query.get_filter_value('category')
    filter_by_comment = query.get_filter_value('comment')

    sort_by_name = query.get_sort_value('name')
    sort_by_category = query.get_sort_value('category')
    sort_by_comment = query.get_sort_value('comment')

    with bandbase.core.database.session() as db:

        contacts = db.query(Contact).join(ContactCategory)

        contacts = SQL.LIKE(contacts, Contact.Name, filter_by_name)
        contacts = SQL.LIKE(contacts, ContactCategory.Name, filter_by_category)
        contacts = SQL.LIKE(contacts, Contact.Comment, filter_by_comment)

        total = contacts.count()

        contacts = SQL.ORDERBY(contacts, Contact.LastName, sort_by_name)
        contacts = SQL.ORDERBY(contacts, ContactCategory.Name, sort_by_category)
        contacts = SQL.ORDERBY(contacts, Contact.Comment, sort_by_comment)

        contacts = SQL.LIMITOFF(contacts, query.limit, query.offset).all()

        return \
        {
            'query': query,
            'columns': columns,
            'rows':
            [
                {'id':                  contact.ID,
                 'values': {'name':     contact.Name,
                            'category': contact.Category.Name,
                            'comment':  contact.Comment},
                 'actions': {}}
                for contact in contacts
            ],
            'total': total
        }
