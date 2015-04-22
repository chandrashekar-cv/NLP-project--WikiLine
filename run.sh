#!/bin/sh
INPUT_DIR="wikipedia/sample"
OUTPUT_DIR="wikipedia/tarsqi_processed/"
for file in $INPUT_DIR/*
    do
        new=`basename "$file"`
        #echo "$file" >> log
        echo "$file"


        /usr/bin/python tarsqi.py simple-xml pipeline=PREPROCESSOR,GUTIME,EVITA "$file" $OUTPUT_DIR/"$new" 1>/dev/null 2>&1
        #/usr/bin/python extract_events.py out.xml 1>/dev/null 2>&1
        #rm out.xml 1>/dev/null 2>&1
    done
