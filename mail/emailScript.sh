#!/bin/bash

if [[ “$(date -d tomorrow +\%d)” == “01” ]]; then
	sendmail your_email@domain.com < emailDay.txt
elif [[ “$(date -d week + \%d)” == “01” ]]; then
	sendmail your_email@domain.com < emailWeek.txt
fi
