#!/bin/bash

DIR=$1
AUTHTOKEN=$2
declare -a curlArgs=('-H' "Content-Type: application/json" '-H' "Authorization: Bearer ${AUTHTOKEN}")

for f in $(find $1 -name '*.json'); 
do 
   echo "curl -vX POST http://localhost:4000/new?token=${AUTHTOKEN} -d @${f} ${curlArgs[@]}\""
   curl -vX POST http://localhost:4000/new -d @${f} "${curlArgs[@]}"
done
