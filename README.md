# coordextractor
Extracts coordinates from georeferenced photos into a csv file

## Requirements
All georeferenced photos must be in one folder or directory.

Requres the installation of python and the following libraries: Pillow, pyproj, GPSPhoto.

## Output
A single CSV file named "<year><month><day>_<hour><minute><seconds>.csv" with the following columns: Filename, Latitude, Longitude, date, time.

The date is currently in Year-Month-Day format but we plan to change that to your computer's default date format. The time is UTC time of the time each photo was taken, in 24h hours:minutes:seconds format.

## Installation
