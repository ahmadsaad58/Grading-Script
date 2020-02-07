#!/bin/bash

# for this file to work, we need to assume the directory looks like this

# we have 3 folders: Grade, Regrade, and Submissions

# steps:

pwd # show the current directory

# move all the files from Graded and Regrade to Submission
mv ./Graded/*.py ./Submissions
mv ./Regrade/*.py ./Submissions

# remove the Fails.txt and Grades.csv
rm -r ./Graded/*
rm -r ./Regrade/*