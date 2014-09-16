#!/bin/bash

###############################################################################
# Get unique compound identifiers for actives and decoys in DUD-E.
#
# Author: Steven Kearnes
# Copyright 2014, Stanford University
# License: 3-clause BSD
#
# Usage: get_dude_ids PATH_TO_DUDE
###############################################################################

for dataset in $1/*
do
    if [ ! -d $dataset ]
    then
        continue
    fi
    name=`basename $dataset`
    echo $name
    mkdir -p $name
    zgrep CHEMBL $dataset/actives_final.mol2.gz | sort | uniq \
        > $name/actives_final.txt
    zgrep ZINC $dataset/decoys_final.mol2.gz | sort | uniq \
        > $name/decoys_final.txt
done
