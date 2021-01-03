from datetime import datetime
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.core.database import *

router = APIRouter(prefix='/table', tags=['table'])


def SQL_LIKE(sql, column, values: List[str]):
    from sqlalchemy.sql.sqltypes import String
    if type(column) in [list, tuple]:
        return sql.filter(SQL.AND(SQL.OR(subcolumn.cast(String).ilike(f'%{_}%') for subcolumn in column)
                                  for _ in values)) \
               if values else sql
    else:
        return sql.filter(SQL.AND(column.cast(String).ilike(f'%{_}%') for _ in values)) \
               if values else sql


def SQL_ORDER_BY(sql, column, value: str):
    from sqlalchemy.sql.sqltypes import String
    if type(column.property.columns[0].type) is String:
        return sql.order_by(SQL.ASC(SQL.IGNORECASE(column))) \
               if value == '+' else \
               sql.order_by(SQL.DESC(SQL.IGNORECASE(column))) \
               if value == '-' else sql
    else:
        return sql.order_by(SQL.ASC(column)) \
               if value == '+' else \
               sql.order_by(SQL.DESC(column)) \
               if value == '-' else sql


def SQL_LIMIT_OFFSET(sql, limit: int, offset: int):
    sql = sql.limit(limit) if limit > 0 else sql
    sql = sql.offset(offset) if offset > 0 else sql
    return sql


class Badge(BaseModel):
    column: str
    text: Optional[str] = None
    title: Optional[str] = None
    style: Optional[str] = None


class TableQuery(BaseModel):
    probe: Optional[bool] = False
    filter: Optional[Dict[str, str]] = {}
    sort: Optional[Dict[str, str]] = {}
    limit: Optional[int] = 0
    offset: Optional[int] = 0

    def get_filter_value(self, key: str):
        value = self.filter.get(key, None)
        value = [_.strip() for _ in value.split(' ') if _.strip()] \
                if value and value.strip() else None
        return value

    def get_sort_value(self, key: str):
        value = self.sort.get(key, None)
        value = value if value in ['+', '-'] else None
        return value


class TableColumn(BaseModel):
    name: str
    filterable: bool
    sortable: bool


class TableRow(BaseModel):
    id: int
    values: Dict[str, Optional[str]]
    actions: Dict[str, str]
    badge: Optional[Badge] = None


class Table(BaseModel):
    query: TableQuery
    columns: List[TableColumn]
    rows: List[TableRow]
    total: int


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

        contacts = SQL_LIKE(contacts, Contact.Name, filter_by_name)
        contacts = SQL_LIKE(contacts, ContactCategory.Name, filter_by_category)
        contacts = SQL_LIKE(contacts, Contact.Comment, filter_by_comment)

        total = contacts.count()

        contacts = SQL_ORDER_BY(contacts, Contact.LastName, sort_by_name)
        contacts = SQL_ORDER_BY(contacts, ContactCategory.Name, sort_by_category)
        contacts = SQL_ORDER_BY(contacts, Contact.Comment, sort_by_comment)

        contacts = SQL_LIMIT_OFFSET(contacts, query.limit, query.offset).all()

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

        gigs = SQL_LIKE(gigs, Gig.Name, filter_by_name)
        gigs = SQL_LIKE(gigs, SQL.TOCHAR(Gig.BeginDate, 'DD.MM.YYYY'), filter_by_date)
        gigs = SQL_LIKE(gigs, SQL.TOCHAR(Gig.EndDate, 'DD.MM.YYYY'), filter_by_date)
        gigs = SQL_LIKE(gigs, Contact.Name, filter_by_location)
        gigs = SQL_LIKE(gigs, Gig.Comment, filter_by_comment)

        total = gigs.count()

        gigs = SQL_ORDER_BY(gigs, Gig.Name, sort_by_name)
        gigs = SQL_ORDER_BY(gigs, Gig.BeginDate, sort_by_date)
        gigs = SQL_ORDER_BY(gigs, Gig.BeginTime, sort_by_date)
        gigs = SQL_ORDER_BY(gigs, Contact.LastName, sort_by_location)
        gigs = SQL_ORDER_BY(gigs, Gig.Comment, sort_by_comment)

        gigs = SQL_LIMIT_OFFSET(gigs, query.limit, query.offset).all()

        badges = \
        [
            {'column': 'name', 'title': 'Versteckt', 'style': 'background:#999'},
            {'column': 'name', 'title': 'Kalender',  'style': 'background:#090'},
            {'column': 'name', 'title': 'Webseite',  'style': 'background:#009'},
            {'column': 'name', 'title': 'Flyer',     'style': 'background:#900'},
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


@router.post('/scores', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                        response_model=Table)
def scores(query: TableQuery):

    columns = \
    [
        {'name': 'name',    'filterable': True, 'sortable': True},
        {'name': 'stockid', 'filterable': True, 'sortable': True},
        {'name': 'edition', 'filterable': True, 'sortable': True},
        {'name': 'gsm',     'filterable': True, 'sortable': True},
        {'name': 'comment', 'filterable': True, 'sortable': True}
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
    filter_by_stockid = query.get_filter_value('stockid')
    filter_by_edition = query.get_filter_value('edition')
    filter_by_gsm = query.get_filter_value('gsm')
    filter_by_comment = query.get_filter_value('comment')

    sort_by_name = query.get_sort_value('name')
    sort_by_stockid = query.get_sort_value('stockid')
    sort_by_edition = query.get_sort_value('edition')
    sort_by_gsm = query.get_sort_value('gsm')
    sort_by_comment = query.get_sort_value('comment')

    with bandbase.core.database.session() as db:

        scores = db.query(Score).join(ScoreEdition)

        scores = SQL_LIKE(scores, (Score.Name, Score.Opus, Score.Piece), filter_by_name)
        scores = SQL_LIKE(scores, (Score.StockLetter, Score.StockNumber, Score.StockCounter), filter_by_stockid)
        scores = SQL_LIKE(scores, ScoreEdition.Name, filter_by_edition)
        scores = SQL_LIKE(scores, (Score.Genre, Score.Style, Score.MetronomeText), filter_by_gsm)
        scores = SQL_LIKE(scores, Score.Comment, filter_by_comment)

        total = scores.count()

        scores = SQL_ORDER_BY(scores, Score.Name, sort_by_name)
        scores = SQL_ORDER_BY(scores, Score.Opus, sort_by_name)
        scores = SQL_ORDER_BY(scores, Score.Piece, sort_by_name)
        scores = SQL_ORDER_BY(scores, Score.StockLetter, sort_by_stockid)
        scores = SQL_ORDER_BY(scores, Score.StockNumber, sort_by_stockid)
        scores = SQL_ORDER_BY(scores, Score.StockCounter, sort_by_stockid)
        scores = SQL_ORDER_BY(scores, ScoreEdition.Name, sort_by_edition)
        scores = SQL_ORDER_BY(scores, Score.Genre, sort_by_gsm)
        scores = SQL_ORDER_BY(scores, Score.Style, sort_by_gsm)
        scores = SQL_ORDER_BY(scores, Score.MetronomeText, sort_by_gsm)
        scores = SQL_ORDER_BY(scores, Score.Comment, sort_by_comment)

        scores = SQL_LIMIT_OFFSET(scores, query.limit, query.offset).all()

        return \
        {
            'query': query,
            'columns': columns,
            'rows':
            [
                {'id':                  score.ID,
                 'values': {'name':     score.NameOpusPiece,
                            'stockid':  score.StockID,
                            'edition':  score.Edition.Name,
                            'gsm':      score.GSM,
                            'comment':  score.Comment},
                 'actions': {}}
                for score in scores
            ],
            'total': total
        }
