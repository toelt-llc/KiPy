#!/bin/bash

## Practice script, TO CLEAN

cp ../files/Ball\ on\ Bar\ -\ Child\ -\ RIGHT\ -\ 11_59.csv ball_copy.csv
var=$(grep -n  "Trial #" ball_copy.csv | cut -f 1 -d:)
array=("${var[@]}")
#declare -a array; 
echo $array


for i in ${!array[@]}; do 
    echo "element $i is ${array[$i]}"
done

declare -i j=0
declare -i k=0
for i in $var; do 
    #echo "New trial detected line $i."

    #tail -n +$((i)) ball_copy.csv | head -n $((i-j)) > df$i.csv
    j=i

    if test -f df$i.csv; then
        echo "> Trial saved."
    fi
done

echo "${!var[@]}"