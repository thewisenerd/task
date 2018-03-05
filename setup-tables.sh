#!/bin/bash

if [ "$1" == "-f" ]; then
	rm app.db
fi

if [ -e app.db ]; then
	echo "tables already setup"
	exit
fi

sqlite3 app.db < setup-tables.sqlite3
