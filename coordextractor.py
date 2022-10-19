#!/usr/bin/python3
#
# Copyright (C) 2022 Nikos Vallianos, Wildlife Sense
# 
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by the
#  Free Software Foundation, either version 2.1 of the License, or (at your
#  option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>
# 
# 
import os
import sys
import csv
import datetime
import re
from tkinter        import filedialog, messagebox
from PIL            import Image
from PIL.ExifTags   import TAGS
from pyproj         import Transformer
from GPSPhoto       import gpsphoto

# Set this to False in production version.
debugging = False

def get_datetime(filename):
    exif = Image.open(filename)._getexif()
    exif_keys = {}

    if exif is not None:
        for key, value in exif.items():
            text_key = TAGS.get(key, key)
            if text_key == 'DateTimeOriginal':
                return(value.split(' '))
    return None

def coord_directory(todays_directory):

    # Create a coordinate reference system (CRS) transformer
    # Coordinates universally come in WGS84 Latitude-Longitude (EPSG4326).
    # This transformer will produce GGRS87 (EPSG2100).
    transformer = Transformer.from_crs("epsg:4326", "epsg:2100")


    # 
    #
    #


    files = os.listdir(path=todays_directory)
    for i in range(len(files)):
        files[i] = os.path.abspath(os.path.join(todays_directory, files[i]))
        #print(files[i])

    #print(len(files))
    files.sort(key=os.path.getctime)        # Doesn't work, needs fixig TODO
    photocount = 0
    #print("Directory: {}".format(todays_directory))
    for i in range(len(files)):
        m = re.match("^(.+)\.(jpg|JPG|jpeg|JPEG)$", files[i])
        if m:
            g = m.groups()
            files[i] = os.path.abspath(os.path.join(todays_directory, files[i]))
            photocount += 1
        else:
            g = None
        if g:
            pass
    #
    # The following 'getctime' key sometimes produces an error in windows.
    # Should be tested with relative vs absolute path to see which is more
    # consistent.
    #
    csv_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    csv_fieldnames = ["Filename", "Latitude", "Longitude", "X", "Y", "Date", "UTC Time"]
    csv_file = open(os.path.join(todays_directory, csv_filename), mode='w', newline=''   )
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames, quotechar='"')
    csv_writer.writeheader()

    for dirfile in files:
        m = re.match("^(.+)\.(jpg|JPG|jpeg|JPEG)$", dirfile)
        if m:
            g = m.groups()
        else:
            g = None
        if g:
            #try:
            coords = {}
            utmcoords = {}
            absfilepath = os.path.join(todays_directory, dirfile)
            gpsdata = gpsphoto.getGPSData( absfilepath )
            if debugging:    # Get some debugging information
                for key in gpsdata.keys():
                    #print ("Key: {}".format(key))
                    pass
                for key, value in gpsdata.items():
                    #print ("Key: {}, Value: {}".format(key, value))
                    pass


            if gpsdata and ('Latitude' in gpsdata.keys()) and ('Longitude' in gpsdata.keys()):
                coords['Latitude']  = round(gpsdata['Latitude'], 6)
                coords['Longitude'] = round(gpsdata['Longitude'], 6)
                utmcoords['X'], utmcoords['Y'] = transformer.transform(gpsdata['Latitude'], gpsdata['Longitude'])
                utmcoords['X'] = round( utmcoords['X'], 3)
                utmcoords['Y'] = round( utmcoords['Y'], 3)
                
            else:
                coords['Latitude'] = ''
                coords['Longitude'] = ''
                utmcoords['X'] = ''
                utmcoords['Y'] = ''
                #print("{}: NO COORDINATES HERE".format(os.path.basename(dirfile) ))

            timedata = get_datetime(absfilepath)
            if timedata:
                coords['Date'], coords['Time'] = timedata
            else:
                coords['Date'], coords['Time'] = ('', '')
            #except:
                #csv_writer.writerow({'Filename': os.path.basename(dirfile), 'Latitude': '', 'Longitude': '', 'X': '', 'Y': '', 'Date': '', 'Time': ''})
                #
                # TODO: Any files with no coordinates should be moved to a NO_COORDINATES folder
                #
            #else:
            csv_writer.writerow({'Filename': os.path.basename(dirfile), 'Latitude': coords['Latitude'], 'Longitude': coords['Longitude'], 'X': utmcoords['X'], 'Y': utmcoords['Y'], 'Date': coords['Date'], 'UTC Time': coords['Time']})
    return csv_filename




#  ^^^ Formerly wsfunctions.py





# Formerly coordextractor3_gui.py
if __name__ == '__main__':
    #
    #
    # 
    if len(sys.argv) == 2:
        todays_directory = os.path.abspath(sys.argv[1])
        #print(todays_directory)
        if os.path.isdir(todays_directory):
            pass
        else:
            #print("The folder \"{}\" was not found".format( os.path.relpath(todays_directory)))
            exit()
    else:                       # ... so we're launching a GUI to determine the directory.
        if messagebox.askokcancel( title="Extract coordinates?",
                                message="Please select a folder with georeferenced photos."):
            # (Yes)
            todays_directory = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title='Select Folder', mustexist=True)
            todays_directory = os.path.abspath(todays_directory)
        else:
            quit()

    # From here on, the directory in todays_directory will be traversed. No other parameters are needed.
    csvname = coord_directory(todays_directory)
    messagebox.showinfo(title="Done", message="Data extracted in csv file {}".format(csvname))
