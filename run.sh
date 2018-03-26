#!/bin/bash

# Usage:
#     ./run.sh ['quoted names of departments separated by spaces']
#
# Example:
#     ./run.sh 'cse ee engr math amath phil'

# Make directories
mkdir -p out/tiddlers
mkdir -p out/p

# Default dept
#dept="aa amath cee cheme cse ee engr hcde inde info math me mse nme stat biol chem musc microm ling psych phys phil engl soc ita bioen qsci"
dept="cse ling math amath stat engr info hcde phil ee"
if [ -n "$1" ]
then
    dept="$1"
fi

# Parse
for i in $(echo $dept)
do
    echo -n "building for $i ...  " && \
    python3 src/init_data.py $i && \
    python3 src/post_proc.py $i && \
    python3 src/parse.py $i && \
    echo -e " Done"
done
