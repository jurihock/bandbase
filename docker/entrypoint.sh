#!/bin/sh

: ${PGDATA:=/bandbase/postgresql}
: ${PGDATABASE:="bandbase"}
: ${PGUSER:="bandbase"}

if [ ! -d "$PGDATA" ] || [ -z "$(ls -A "$PGDATA")" ]
then

	if [ -d "$PGDATA" ]
	then
		chown -R postgres:postgres $PGDATA
	fi

	gosu postgres initdb $PGDATA

	echo "create database $PGDATABASE;" | gosu postgres postgres --single -jE
	echo "create user $PGUSER;" | gosu postgres postgres --single -jE
	echo "grant all privileges on database $PGDATABASE to $PGUSER;" | gosu postgres postgres --single -jE

fi

if [ ! -d "/run/postgresql" ]
then
	mkdir /run/postgresql
	chown postgres:postgres /run/postgresql
fi

gosu postgres pg_ctl start

echo
echo "**************************"
echo "Welcome to Bandbase shell!"
echo "**************************"
echo

exec /bin/sh "$@"
