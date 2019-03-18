from parsers.common import *
from utils.models import *

import utils.sql as sql

class ContactQueryRequestParser(RequestParser):

    def parse(self):

        page = self.int('page', default=0)
        size = self.int('size', default=None)

        limit  = size if size else None
        offset = page*size if page and size else None

        name     = self.list('filter_by_name', format='%{0}%')
        category = self.str('filter_by_category', format='%{0}%')
        comment  = self.str('filter_by_comment', format='%{0}%')

        sort_by_name     = self.enum(SortOrder, 'sort_by_name')
        sort_by_category = self.enum(SortOrder, 'sort_by_category')
        sort_by_comment  = self.enum(SortOrder, 'sort_by_comment')

        order_of_name     = self.int('order_of_name')
        order_of_category = self.int('order_of_category')
        order_of_comment  = self.int('order_of_comment')

        order_by = []

        if order_of_name is not None:     order_by.insert(order_of_name,     (Contact.LastName,     sort_by_name))
        if order_of_category is not None: order_by.insert(order_of_category, (ContactCategory.Name, sort_by_category))
        if order_of_comment is not None:  order_by.insert(order_of_comment,  (Contact.Comment,      sort_by_comment))

        query = self.db.query(Contact).join(ContactCategory)

        if name:     query = query.filter(sql.AND(*[Contact.Name.ilike(x) for x in name]))
        if category: query = query.filter(ContactCategory.Name.ilike(category))
        if comment:  query = query.filter(Contact.Comment.ilike(comment))

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

        if limit:  query = query.limit(limit)
        if offset: query = query.offset(offset)

        contacts = query.all()

        return (contacts, total)
