# Script for retrieving, trimming down, and resaving grib2 MRMS files from IEM archive

import os
import sys
import wget

# User inputs to define start and end dates for files
start_year = input('Input starting year:')
start_month = input('Input starting month:')
start_day = input('Input starting day:')
start_hour = input('Input starting hour in UTC (enter as a single whole number; for example, 22 for 22:00 UTC):')

end_year = input('Input ending year:')
end_month = input('Input ending month:')
end_day = input('Input ending day:')
end_hour = input('Input ending hour in UTC (enter as a single whole number; for example, 22 for 22:00 UTC):')

print(f'The starting date is {start_month}-{start_day}-{start_year} {start_hour}:00 UTC')
print(f'The ending date is {end_month}-{end_day}-{end_year} {end_hour}:00 UTC')

# Confirmation from user before continuing with the download process
valid_input = False
while not valid_input:
    confirm = input('Are these dates correct? Would you like to continue with downloading MRMS data? [y/n]')
    if confirm=='y':
        print('Okay, beginning download process now...')
        valid_input=True
    elif confirm=='n':
        print('Okay, exiting script, please re-run to change dates')
        sys.exit()
    else:
        print('error: must input y or n')

# Create a new directory for files to download into
directory_name = input('Please name the directory files will download into:')
sys.mkdir(directory_name)

# Some kind of loop to create dates list

print('Downloading files now. Depending on the number of hours in your date range, this may take a while. \
    Each hourly file is approximately 6 GB')
# Some kind of wget loop
# feature something like this:
# url = f'http://mrms.agron.iastate.edu/{year}/{month}/{day}/{year}{month}{day}{hour}.zip'
# wget.download(url, out='/directory_name')

# url = https://mrms.agron.iastate.edu/2022/08/29/2022082914.zip
# wget.download(url) https://mrms.agron.iastate.edu/2022/08/29/2022082914.zip

print('File download complete!')
# Now set the lats and lons for trimming MRMS data
start_lat = 40.551599
start_lon = -88.892601
end_lat = 39.868433
end_lon = -88.153743
#Confirm these values with the user
valid_input = False
while not valid_input:
    print(f'The bounds for this analysis are Latitude: {start_lat},{end_lat}; \
        Longitude: {start_lon}, {end_lon}')
    confirm_lat_lon = input('Please confirm that these are the lat/lon bounds you need [y/n]')
    if confirm=='y':
        print('Okay, beginning trimming process now...')
        valid_input=True
    elif confirm=='n':
        print('Okay, please update the lat/lon bounds now:')
        start_lat = input('The start latitude is:')
        start_lon = input('The start longitude is:')
        end_lat = input('The end latitude is:')
        end_lon = input('The end longitude is:')
        print('Okay...')
    else:
        print('error: must input y or n')

# Trim process
# Need to trim both lat/lons and products (only need hourly precip)