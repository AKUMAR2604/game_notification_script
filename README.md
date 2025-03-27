# game_notification_script

This Python script fetches video game releases from the past week using the RAWG API and sends them via email. It's designed to run automatically every week using crontab.

Features
Fetches game releases from the RAWG API

Filters games released in the last 7 days

Formats the data into a readable email

Sends the weekly digest via SMTP

Automated scheduling with crontab

Prerequisites
Python 3.6+

RAWG API key (get it from RAWG.io)

SMTP credentials for sending emails

Required Python packages (install via pip install -r requirements.txt)
