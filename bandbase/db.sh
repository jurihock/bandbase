#!/bin/bash

BANDBASE=$(dirname "$(readlink -f "$0")")

source $BANDBASE/db.config

if [ $(ls -1 $BANDBASE/db.*.config 2>/dev/null | wc -l) -gt 0 ]
then

	for CONFIG in $BANDBASE/db.*.config
	do
		source $CONFIG
	done

fi

TIMESTAMP=$(date --iso-8601=ns)
DATESTAMP=$(date --iso-8601=date)
YEAR=$(date +%Y)

case "$1" in

	i|config)

		echo "-- db.config"
		echo "$(cat -sn $BANDBASE/db.config)"

		if [ $(ls -1 $BANDBASE/db.*.config 2>/dev/null | wc -l) -gt 0 ]
		then

			for CONFIG in $BANDBASE/db.*.config
			do
				echo "-- $(basename $CONFIG)"
				echo "$(cat -sn $CONFIG)"
			done

		fi

		echo "-- done"

		;;

	c|create)

		read -p "-- press [ENTER] key to create a blank new database \"$DATABASE\""

		echo "-- drop database \"$DATABASE\""
		dropdb --if-exists $DATABASE

		echo "-- create database \"$DATABASE\""
		createdb $DATABASE

        echo "-- execute script $BANDBASE/db.py"
		python3 $BANDBASE/db.py

		echo "-- done"

		;;

	d|drop)

		read -p "-- press [ENTER] key to drop the database \"$DATABASE\""

		echo "-- drop database \"$DATABASE\""
		dropdb --if-exists $DATABASE

		echo "-- done"

		;;

	b|backup)

		read -p "-- press [ENTER] key to backup the database \"$DATABASE\""

		mkdir -p $BACKUP

		echo "-- backup schema of \"$DATABASE\""
		echo "-- BANDBASE SCHEMA DUMP" > $SCHEMA
		echo "-- TIMESTAMP: $TIMESTAMP" >> $SCHEMA
		echo "-- FILEPATH:  $SCHEMA" >> $SCHEMA
		echo >> $SCHEMA
		echo "BEGIN;" >> $SCHEMA
		echo >> $SCHEMA
		pg_dump $DATABASE --no-owner --schema-only >> $SCHEMA
		echo >> $SCHEMA
		echo "COMMIT;" >> $SCHEMA

		echo "-- backup data of \"$DATABASE\""
		echo "-- BANDBASE DATA DUMP" > $DATA
		echo "-- TIMESTAMP: $TIMESTAMP" >> $DATA
		echo "-- FILEPATH:  $DATA" >> $DATA
		echo >> $DATA
		echo "BEGIN;" >> $DATA
		echo >> $DATA
		pg_dump $DATABASE --no-owner --data-only >> $DATA
		echo >> $DATA
		echo "COMMIT;" >> $DATA

		echo "-- zip schema.sql and data.sql"
		pushd $BACKUP > /dev/null
		zip -q schema+data.zip schema.sql data.sql
		mkdir -p $YEAR
		cp schema+data.zip $YEAR/$DATESTAMP.zip
		popd > /dev/null

		echo "-- done"

		;;

	r|restore)

		[ -f "$SCHEMA" ] || { echo "ERROR: Schema file \"$SCHEMA\" not found!" ; exit 1 ; }
		[ -f "$DATA" ]   || { echo "ERROR: Data file \"$DATA\" not found!" ; exit 1 ; }

		read -p "-- press [ENTER] key to restore the database \"$DATABASE\""

		echo "-- drop database \"$DATABASE\""
		dropdb --if-exists $DATABASE

		echo "-- create database \"$DATABASE\""
		createdb $DATABASE

		echo "-- restore schema of \"$DATABASE\""
		psql -q $DATABASE < $SCHEMA

		echo "-- restore data of \"$DATABASE\""
		psql -q $DATABASE < $DATA

		echo "-- done"

		;;

	v|vacuum)

		psql $DATABASE -c "VACUUM VERBOSE ANALYZE;"

		;;

	q|sql)

		psql $DATABASE

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

            psql $DATABASE -c "COPY ($QUERY) TO STDOUT WITH ($OPTIONS);"

        else

            echo "-- write query result $QUERY to file $FILE"
            psql $DATABASE -c "COPY ($QUERY) TO STDOUT WITH ($OPTIONS);" > $FILE

        fi

	    ;;

	*)

		echo $"Usage: $0 {config|create|drop|backup|restore|vacuum|sql|csv}"
		echo $"       $0 {    i |c     |d   |b     |r      |v     | q | s }"
		exit 1

esac
