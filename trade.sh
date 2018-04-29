#! /bin/sh

while : 
do
	python main.py

	if [ -e log/complete.txt ]
	then
		break
	else
		echo "Doing again"
	fi
done




