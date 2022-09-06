# Script for retrieving, trimming down, and resaving grib2 MRMS files from IEM archive

import os
#import wget

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


# wget https://mrms.agron.iastate.edu/2022/08/29/2022082914.zip
# test