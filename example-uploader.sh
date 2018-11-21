#!/bin/bash

DIR=$1
for f in $(find $1 -name '*.json'); 
do 
   curl -vX POST http://localhost:4000/new -d @${f} --header "Content-Type: application/json"
done
