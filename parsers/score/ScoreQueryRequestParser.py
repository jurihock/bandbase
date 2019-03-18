from parsers.common import *
from utils.models import *

import utils.sql as sql

class ScoreQueryRequestParser(RequestParser):

    def parse(self):

        page = self.int('page', default=0)
        size = self.int('size', default=None)

        limit  = size if size else None
        offset = page*size if page and size else None

        name    = self.str('filter_by_name', format='%{0}%')
        letter  = self.str('filter_by_letter', format='{0}')
        number  = self.str('filter_by_number')
        edition = self.str('filter_by_edition', format='%{0}%')
        gsm     = self.str('filter_by_gsm', format='%{0}%')
        comment = self.str('filter_by_comment', format='%{0}%')

        sort_by_name    = self.enum(SortOrder, 'sort_by_name')
        sort_by_letter  = self.enum(SortOrder, 'sort_by_letter')
        sort_by_number  = self.enum(SortOrder, 'sort_by_number')
        sort_by_edition = self.enum(SortOrder, 'sort_by_edition')
        sort_by_comment = self.enum(SortOrder, 'sort_by_comment')

        order_of_name    = self.int('order_of_name')
        order_of_letter  = self.int('order_of_letter')
        order_of_number  = self.int('order_of_number')
        order_of_edition = self.int('order_of_edition')
        order_of_comment = self.int('order_of_comment')

        order_by = []

        if order_of_name is not None:    order_by.insert(order_of_name,    (Score.Name,        sort_by_name))
        if order_of_letter is not None:  order_by.insert(order_of_letter,  (Score.StockLetter, sort_by_letter))
        if order_of_number is not None:  order_by.insert(order_of_number,  (Score.StockNumber, sort_by_number))
        if order_of_edition is not None: order_by.insert(order_of_edition, (ScoreEdition.Name, sort_by_edition))
        if order_of_comment is not None: order_by.insert(order_of_comment, (Score.Comment,     sort_by_comment))

        query = self.db.query(Score).join(ScoreEdition)

        if name:    query = query.filter(Score.Name.ilike(name) |
                                         Score.Opus.ilike(name) |
                                         Score.Piece.ilike(name))
        if letter:  query = query.filter(Score.StockLetter.ilike(letter))
        if number:  query = query.filter(Score.StockNumber.cast(String(5)).ilike(number))
        if edition: query = query.filter(ScoreEdition.Name.ilike(edition))
        if gsm:     query = query.filter(Score.GSM.ilike(gsm))
        if comment: query = query.filter(Score.Comment.ilike(comment))

        total = query.count()

        for entry in order_by:

            is_string = type(entry[0].property.columns[0].type) is String

            if is_string:

                if entry[1] is SortOrder.desc:
                    query = query.order_by(sql.DESC(sql.IGNORECASE(entry[0])))
                else:
                    query = query.order_by(sql.ASC(sql.IGNORECASE(entry[0])))

            else:

                if entry[1] is SortOrder.desc:
                    query = query.order_by(sql.DESC(entry[0]))
                else:
                    query = query.order_by(sql.ASC(entry[0]))

        if limit:   query = query.limit(limit)
        if offset:  query = query.offset(offset)

        scores = query.all()

        return (scores, total)
