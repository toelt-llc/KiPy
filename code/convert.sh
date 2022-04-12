#!/bin/bash

cd ../files/
for f in *; do
    ENCODE=$(file  $f | awk '{print $2}')
    echo $f
    if [ $ENCODE ==  "ISO-8859" ];then
        iconv -f ISO-8859-10 -t UTF-8  $f > ./utf8/$f
    elif [ $ENCODE ==  "Unicode" ];then
        cp $f ./utf8/$f
    fi
done

#iconv -f ISO-8859-10 -t UTF-8 Ball\ on\ Bar\ -\ \[Child\ -\ practice\ 2\ \(30s\ per\ level\)\]\ -\ RIGHT\ -\ 11_57.csv > ball_practice.csv

# iconv -f $FROM -t $TO -o $FILE.tmp $FILE; ERROR=$?
# if [[ $ERROR -eq 0 ]]; then
#   echo "Converting $FILE..."
#   mv -f $FILE.tmp $FILE
# else
#   echo "Error on $FILE"
# fi