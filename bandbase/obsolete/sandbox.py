if __name__ == '__main__':

    from app import app

    import utils.database as database

    from utils.models import *

    import sys

    database.setup(app)

    with database.session() as db:

        with open('/tmp/test.csv', 'w', encoding='utf-8') as file:

            cursor = db.connection().connection.cursor()

            query = 'SELECT * FROM "Currencies" WHERE "ID" = 276'
            options = 'FORMAT CSV, HEADER TRUE, DELIMITER \';\', ENCODING \'utf-8\''
            sql = 'COPY ({0}) TO STDOUT WITH ({1});'.format(query, options)

            cursor.copy_expert(sql, file)
