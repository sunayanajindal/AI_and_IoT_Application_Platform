#!/bin/bash 

# cd to pwd
pwd
echo "running script"
# config file
python3 dockerFileGenerator.py $1


# contract , pickel
python3 wrapperClassGenerator.py $2 $3

