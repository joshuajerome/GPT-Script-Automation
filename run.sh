#!/bin/bash

# Authentication
filename="confidential.json"

# Use `jq` to parse the JSON file and assign values to variables
IP=$(jq -r '.IP' "$filename")
USER=$(jq -r '.USER' "$filename")
PASS=$(jq -r '.PASS' "$filename")

# Script to run
FILE=$1
BASE=$(basename "$FILE")
NAME="${BASE%.*}"

# Initial Flag
FLG0=$2

# Remaining Flags
FLGS=${@:2}

# Out file name
OUT=${NAME}_${FLG0}.txt

# Error file name
ERR=${NAME}_${FLG0}.err

if [ $# -eq 1 ]; then
    OUT=${NAME}.txt
    cd outputs && touch ${OUT}
    echo Running ${NAME}
    cd .. && python3 ${FILE} -ip ${IP} -u ${USER} -p ${PASS} > outputs/${OUT}
    echo Stored output in outputs/${NAME}.txt
else
    case "$FLG0" in
        -h|--help|--script-examples)
            echo Running ${NAME} with option ${FLG0} ...
            python3 ${FILE} -ip ${IP} -u ${USER} -p ${PASS} ${FLG0}
            ;;  
        *)
            cd outputs && touch ${OUT}
            if [ $# -gt 2 ]; then
                echo Running ${NAME} with option ${FLGS} ...
                cd .. && python3 ${FILE} -ip ${IP} -u ${USER} -p ${PASS} ${FLGS}> outputs/${OUT}
            else
                echo Running ${NAME} with option ${FLG0} ...
                cd .. && python3 ${FILE} -ip ${IP} -u ${USER} -p ${PASS} ${FLG0} > outputs/${OUT}
            fi
            echo Stored output in outputs/${OUT}
            ;;
    esac
fi
echo Execution complete