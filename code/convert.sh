#!/bin/bash
cd ../files/
mkdir utf8
for f in *; do
    ENCODE=$(file  $f | awk '{print $2}')
    echo $f
    if [ $ENCODE ==  "ISO-8859" ];then
        iconv -f ISO-8859-10 -t UTF-8  $f > ./utf8/$f
    elif [ $ENCODE ==  "Unicode" ];then
        cp $f ./utf8/$f
    fi
done

#iconv -f ISO-8859-10 -t UTF-8 Ball_on_Bar_-_[Child_-_practice_2_(30s_per_level)]_-_RIGHT_-_11_57.csv > ball_practice.csv