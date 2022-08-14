from datetime import datetime
from fastapi import APIRouter, Depends, Request, Response, HTTPException

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.schemas.database import *
from bandbase.schemas.tables import *


router = APIRouter(prefix='', tags=['tables', 'gigs'])


@router.post('/gigs', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                      response_model=Table)
def gigs(query: TableQuery):

    columns = \
    [
        {'name': 'name',     'filterable': True, 'sortable': True},
        {'name': 'date',     'filterable': True, 'sortable': True},
        {'name': 'location', 'filterable': True, 'sortable': True},
        {'name': 'comment',  'filterable': True, 'sortable': True}
    ]

    if query.probe:

        with bandbase.core.database.session() as db:

            gig_year = SQL.EXTRACT('year', Gig.BeginDate)
            last_known_gig_year = db.query(SQL.MAX(gig_year)).scalar()
            current_year = datetime.today().year
            year = min(last_known_gig_year or current_year, current_year)
            limit = db.query(Gig).filter(gig_year >= year).count()

        query = \
        {
            'probe': True,
            'sort': {'date': '-'},
            'limit': max(limit, 10)
        }

        return \
        {
            'query': query,
            'columns': columns,
            'rows': [],
            'total': 0
        }

    filter_by_name = query.get_filter_value('name')
    filter_by_date = query.get_filter_value('date')
    filter_by_location = query.get_filter_value('location')
    filter_by_comment = query.get_filter_value('comment')

    sort_by_name = query.get_sort_value('name')
    sort_by_date = query.get_sort_value('date')
    sort_by_location = query.get_sort_value('location')
    sort_by_comment = query.get_sort_value('comment')

    with bandbase.core.database.session() as db:

        gigs = db.query(Gig).join(Contact, Gig.Location)

        gigs = SQL.LIKE(gigs, Gig.Name, filter_by_name)
        gigs = SQL.LIKE(gigs, SQL.TOCHAR(Gig.BeginDate, 'DD.MM.YYYY'), filter_by_date)
        gigs = SQL.LIKE(gigs, SQL.TOCHAR(Gig.EndDate, 'DD.MM.YYYY'), filter_by_date)
        gigs = SQL.LIKE(gigs, Contact.Name, filter_by_location)
        gigs = SQL.LIKE(gigs, Gig.Comment, filter_by_comment)

        total = gigs.count()

        gigs = SQL.ORDERBY(gigs, Gig.Name, sort_by_name)
        gigs = SQL.ORDERBY(gigs, Gig.BeginDate, sort_by_date)
        gigs = SQL.ORDERBY(gigs, Gig.BeginTime, sort_by_date)
        gigs = SQL.ORDERBY(gigs, Contact.LastName, sort_by_location)
        gigs = SQL.ORDERBY(gigs, Gig.Comment, sort_by_comment)

        gigs = SQL.LIMITOFF(gigs, query.limit, query.offset).all()

        badges = \
        [
            {'column': 'name', 'tooltip': 'Versteckt', 'style': 'background:#999'},
            {'column': 'name', 'tooltip': 'Kalender',  'style': 'background:#090'},
            {'column': 'name', 'tooltip': 'Webseite',  'style': 'background:#009'},
            {'column': 'name', 'tooltip': 'Flyer',     'style': 'background:#900'},
        ]

        return \
        {
            'query': query,
            'columns': columns,
            'rows':
            [
                {'id':                  gig.ID,
                 'values': {'name':     gig.Name,
                            'date':     gig.BeginDate.strftime('%d.%m.%Y'),
                            'location': gig.Location.Name,
                            'comment':  gig.Comment},
                 'actions': {},
                 'badge':   badges[gig.VisibilityID]}
                for gig in gigs
            ],
            'total': total
        }
