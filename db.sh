#!/bin/sh

BANDBASE=$(dirname "$(readlink -f "$0")")

source $BANDBASE/db.config

if [ $(ls -1 $BANDBASE/db.*.config 2>/dev/null | wc -l) -gt 0 ]
then

	for DBCONFIG in $BANDBASE/db.*.config
	do
		source $DBCONFIG
	done

fi

DBSCHEMA=$DBBACKUP/schema.sql
DBDATA=$DBBACKUP/data.sql

TIMESTAMP=$(date --iso-8601=ns)
DATESTAMP=$(date --iso-8601=date)
YEAR=$(date +%Y)

case "$1" in

	i|config)

		echo "-- db.config"
		echo "$(cat -sn $BANDBASE/db.config)"

		if [ $(ls -1 $BANDBASE/db.*.config 2>/dev/null | wc -l) -gt 0 ]
		then

			for DBCONFIG in $BANDBASE/db.*.config
			do
				echo "-- $(basename $DBCONFIG)"
				echo "$(cat -sn $DBCONFIG)"
			done

		fi

		echo "-- done"

		;;

	c|create)

		read -p "-- press [ENTER] key to create a blank new database \"$DBNAME\""

		echo "-- drop database \"$DBNAME\""
		dropdb --if-exists $DBNAME

		echo "-- create database \"$DBNAME\""
		createdb $DBNAME

        echo "-- execute script $BANDBASE/db.py"
		python3 $BANDBASE/db.py

		echo "-- done"

		;;

	d|drop)

		read -p "-- press [ENTER] key to drop the database \"$DBNAME\""

		echo "-- drop database \"$DBNAME\""
		dropdb --if-exists $DBNAME

		echo "-- done"

		;;

	b|backup)

		read -p "-- press [ENTER] key to backup the database \"$DBNAME\""

		mkdir -p $DBBACKUP

		echo "-- backup schema of \"$DBNAME\""
		echo "-- BANDBASE SCHEMA DUMP" > $DBSCHEMA
		echo "-- TIMESTAMP: $TIMESTAMP" >> $DBSCHEMA
		echo "-- FILEPATH:  $DBSCHEMA" >> $DBSCHEMA
		echo >> $DBSCHEMA
		echo "BEGIN;" >> $DBSCHEMA
		echo >> $DBSCHEMA
		pg_dump $DBNAME --no-owner --schema-only >> $DBSCHEMA
		echo >> $DBSCHEMA
		echo "COMMIT;" >> $DBSCHEMA

		echo "-- backup data of \"$DBNAME\""
		echo "-- BANDBASE DATA DUMP" > $DBDATA
		echo "-- TIMESTAMP: $TIMESTAMP" >> $DBDATA
		echo "-- FILEPATH:  $DBDATA" >> $DBDATA
		echo >> $DBDATA
		echo "BEGIN;" >> $DBDATA
		echo >> $DBDATA
		pg_dump $DBNAME --no-owner --data-only >> $DBDATA
		echo >> $DBDATA
		echo "COMMIT;" >> $DBDATA

		echo "-- zip schema.sql and data.sql"
		pushd $DBBACKUP > /dev/null
		zip -q schema+data.zip schema.sql data.sql
		mkdir -p $YEAR
		cp schema+data.zip $YEAR/$DATESTAMP.zip
		popd > /dev/null

		echo "-- done"

		;;

	r|restore)

		[ -f "$DBSCHEMA" ] || { echo "ERROR: Schema file \"$DBSCHEMA\" not found!" ; exit 1 ; }
		[ -f "$DBDATA" ]   || { echo "ERROR: Data file \"$DBDATA\" not found!" ; exit 1 ; }

		read -p "-- press [ENTER] key to restore the database \"$DBNAME\""

		echo "-- drop database \"$DBNAME\""
		dropdb --if-exists $DBNAME

		echo "-- create database \"$DBNAME\""
		createdb $DBNAME

		echo "-- restore schema of \"$DBNAME\""
		psql -q $DBNAME < $DBSCHEMA

		echo "-- restore data of \"$DBNAME\""
		psql -q $DBNAME < $DBDATA

		echo "-- done"

		;;

	v|vacuum)

		psql $DBNAME -c "VACUUM VERBOSE ANALYZE;"

		;;

	q|sql)

		psql $DBNAME

		;;

	s|csv)

        TABLE="$2"
        ROWID="$3"
        FILE="${@:4}"

        [ -n "$TABLE" ] || { echo "ERROR: Please specify the table name!" ; exit 1 ; }
        [ -n "$ROWID" ] || { echo "ERROR: Please specify the row id!" ; exit 1 ; }

	    QUERY="SELECT * FROM \"$TABLE\" WHERE \"ID\" = $ROWID"
	    OPTIONS="FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'utf-8'"

        if [ -z "$FILE" ]
        then

            psql $DBNAME -c "COPY ($QUERY) TO STDOUT WITH ($OPTIONS);"

        else

            echo "-- write query result $QUERY to file $FILE"
            psql $DBNAME -c "COPY ($QUERY) TO STDOUT WITH ($OPTIONS);" > $FILE

        fi

	    ;;

	*)

		echo $"Usage: $0 {config|create|drop|backup|restore|vacuum|sql|csv}"
		echo $"       $0 {    i |c     |d   |b     |r      |v     | q | s }"
		exit 1

esac
