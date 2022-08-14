from fastapi import APIRouter, Depends, Request, Response, HTTPException

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.schemas.database import *
from bandbase.schemas.tables import *


router = APIRouter(prefix='', tags=['tables', 'scores'])


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

        scores = SQL.LIKE(scores, (Score.Name, Score.Opus, Score.Piece), filter_by_name)
        scores = SQL.LIKE(scores, (Score.StockLetter, Score.StockNumber, Score.StockCounter), filter_by_stockid)
        scores = SQL.LIKE(scores, ScoreEdition.Name, filter_by_edition)
        scores = SQL.LIKE(scores, (Score.Genre, Score.Style, Score.MetronomeText), filter_by_gsm)
        scores = SQL.LIKE(scores, Score.Comment, filter_by_comment)

        total = scores.count()

        scores = SQL.ORDERBY(scores, Score.Name, sort_by_name)
        scores = SQL.ORDERBY(scores, Score.Opus, sort_by_name)
        scores = SQL.ORDERBY(scores, Score.Piece, sort_by_name)
        scores = SQL.ORDERBY(scores, Score.StockLetter, sort_by_stockid)
        scores = SQL.ORDERBY(scores, Score.StockNumber, sort_by_stockid)
        scores = SQL.ORDERBY(scores, Score.StockCounter, sort_by_stockid)
        scores = SQL.ORDERBY(scores, ScoreEdition.Name, sort_by_edition)
        scores = SQL.ORDERBY(scores, Score.Genre, sort_by_gsm)
        scores = SQL.ORDERBY(scores, Score.Style, sort_by_gsm)
        scores = SQL.ORDERBY(scores, Score.MetronomeText, sort_by_gsm)
        scores = SQL.ORDERBY(scores, Score.Comment, sort_by_comment)

        scores = SQL.LIMITOFF(scores, query.limit, query.offset).all()

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
