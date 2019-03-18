from parsers.common import *
from utils.models import *

import utils.sql as sql

class GigQueryRequestParser(RequestParser):

    def parse(self):

        page = self.int('page', default=0)
        size = self.int('size', default=None)
    
        limit  = size if size else None
        offset = page*size if page and size else None
    
        name     = self.str('filter_by_name', format='%{0}%')
        date     = self.str('filter_by_date', format='%{0}%')
        location = self.str('filter_by_location', format='%{0}%')
        comment  = self.str('filter_by_comment', format='%{0}%')
    
        sort_by_name     = self.enum(SortOrder, 'sort_by_name')
        sort_by_date     = self.enum(SortOrder, 'sort_by_date')
        sort_by_location = self.enum(SortOrder, 'sort_by_location')
        sort_by_comment  = self.enum(SortOrder, 'sort_by_comment')
    
        order_of_name     = self.int('order_of_name')
        order_of_date     = self.int('order_of_date')
        order_of_location = self.int('order_of_location')
        order_of_comment  = self.int('order_of_comment')
    
        order_by = []
    
        if order_of_name is not None:     order_by.insert(order_of_name,     (Gig.Name,         sort_by_name))
        if order_of_date is not None:     order_by.insert(order_of_date,     (Gig.EndDate,      sort_by_date))
        if order_of_location is not None: order_by.insert(order_of_location, (Contact.LastName, sort_by_location))
        if order_of_comment is not None:  order_by.insert(order_of_comment,  (Gig.Comment,      sort_by_comment))
    
        query = self.db.query(Gig).join(Contact, Gig.Location)
    
        if name:     query = query.filter(Gig.Name.ilike(name))
        if date:     query = query.filter(sql.TOCHAR(Gig.BeginDate, 'DD.MM.YYYY').ilike(date))
        if date:     query = query.filter(sql.TOCHAR(Gig.EndDate, 'DD.MM.YYYY').ilike(date))
        if location: query = query.filter(Contact.Name.ilike(location))
        if comment:  query = query.filter(Gig.Comment.ilike(comment))
    
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

        gigs = query.all()
    
        return (gigs, total)
