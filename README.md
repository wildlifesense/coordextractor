# coordextractor
Extracts coordinates from all georeferenced photos in a folder into a csv file in the same folder.

## Requirements
All georeferenced photos must be in one folder. Photos in subfolders are ignored.

Requres the installation of python and the following python libraries: Pillow, pyproj, GPSPhoto.

## Output
A single CSV file named "&lt;year&gt;&lt;month&gt;&lt;day&gt;_&lt;hour&gt;&lt;minute&gt;&lt;seconds&gt;.csv" with the following columns: Filename, Latitude, Longitude, date, time. Longitude and Latitude are in decimal degrees.

The date is currently in Year-Month-Day format but we plan to change that to your computer's default date format. The time is UTC time of the time each photo was taken, in 24h hours:minutes:seconds format.

## Installation
  1. Install python: https://www.python.org/downloads/
  2. Install Pillow, pyproj, exifread, piexif, and GPSPhoto. Type the following in a command prompt, assuming your pip works:
  ```
  pip install pillow
  pip install pyproj
  pip install exifread
  pip install piexif
  pip install GPSPhoto
  ```
  You may need to alter the above for admin privileges. For instructions on installing python packages, see https://packaging.python.org/en/latest/tutorials/installing-packages/.

## Nearly Complete Goals
  
Convert to a Coordinate Reference System other than WGS84. This will be added to the CSV as X and Y coordinates, in addition to the default Longitude and Latitude for WGS84. Currently this defaults to GGRS but I plan to make the extra CRS a drop-down selection.
