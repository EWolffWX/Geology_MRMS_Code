# MRMS Precipitation Analysis

This code downloads MRMS hourly precipitation data from the IEM archive for a user-specified time period and trims this data to a user-specified domain. Given the large size of the IEM archive files, this code is designed to minimize required local storage space by downloading files one at a time and only extracting hourly precip data before deleting the zipped file. Still, adequate storage should be allocated before running this code, especially over a long time period.

### Required Packages
Running this script will require the following packages to be downloaded:
- wget
- datetime
- xarray
- cfgrib
- numpy

### Operating System Requirements
Additionally, in it's current form, this code is designed to be run on a computer with the Linux operating system as some lines execute Linux commands (such as creating directories and deleting files)
