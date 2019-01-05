#!/bin/bash
#set -x

HOST=localhost
PORT=8087
DB=resim
DUR=1h

init_database() {
  curl -i -XPOST http://$HOST:$PORT/query --data-urlencode "q=DROP DATABASE $DB"
  curl -i -XPOST http://$HOST:$PORT/query --data-urlencode "q=CREATE DATABASE $DB WITH DURATION $DUR"
}

init_database

