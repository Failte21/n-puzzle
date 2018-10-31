#!/usr/bin/env bash

O_FILE=cprof_output_$(date +%s).cprof

if [[ -f $1 ]]; then
	python3 -m cProfile -s cumtime -o $O_FILE ../n-puzzle.py $1
	snakeviz $O_FILE
else
	printf "$1 is not a file."
fi