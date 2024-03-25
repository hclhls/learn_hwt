#!/bin/bash

for file in `ls *.py`; do
    ls $file
    python $file > "${file%%.*}"_hwt.v
done