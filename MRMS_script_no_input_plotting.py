import os
import sys
import wget
from datetime import datetime, timedelta
import xarray as xr
from zipfile import ZipFile
import numpy as np

import matplotlib.pyplot as plt
from metpy.plots import USCOUNTIES
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# Note: In addition to the packages listed above, cfgrib will also need to be installed

# Enter your time bounds here (in UTC):
start_year = 2021
start_month = 10
start_day = 23
start_hour = 5

end_year = 2021
end_month = 11
end_day = 1
end_hour = 4

# Turn values into datetimes
start_date = datetime(year=int(start_year), month=int(start_month), day=int(start_day), \
    hour=int(start_hour))
end_date = datetime(year=int(end_year), month=int(end_month), day=int(end_day), \
    hour=int(end_hour))

# Compute event duration
duration = end_date - start_date
timedelta_seconds = duration.total_seconds()
timedelta_hours = timedelta_seconds/3600
print(timedelta_hours)

# Make directory to output grib files into
os.system('mkdir grib_files')
os.system('mkdir clipped_files')
os.system('mkdir clipped_files/quick_looks')
# Loop through each hour requested
for i in range(0, int(timedelta_hours)+1, 1):
    new_date = start_date + timedelta(hours=i)
    print(new_date)
    year = new_date.strftime("%Y")
    month = new_date.strftime("%m")
    day = new_date.strftime("%d")
    hour = new_date.strftime("%H")
    # Create url for hourly file and download from IEM archive
    url = f'http://mrms.agron.iastate.edu/{year}/{month}/{day}/{year}{month}{day}{hour}.zip'
    wget.download(url)
    # Begin processing grib file
    date_string = f'{year}{month}{day}{hour}'
    # Make temp directory and unzip the grib file
    os.system(f'mkdir {date_string}')
    file_name = f'{date_string}.zip'
    with ZipFile(file_name, 'r') as zip:
        zip.extract(f'{date_string}/CONUS/MultiSensor_QPE_01H_Pass1/MRMS_MultiSensor_QPE_01H_'\
            f'Pass1_00.00_{year}{month}{day}-{hour}0000.grib2.gz')
    os.system(f'gunzip {date_string}/CONUS/MultiSensor_QPE_01H_Pass1/MRMS_MultiSensor_QPE_01H_'\
        f'Pass1_00.00_{year}{month}{day}-{hour}0000.grib2.gz')
    # Move unzipped file to output directory
    os.system(f'mv {date_string}/CONUS/MultiSensor_QPE_01H_Pass1/MRMS_MultiSensor_QPE_01H_'\
        f'Pass1_00.00_{year}{month}{day}-{hour}0000.grib2 grib_files')
    # Delete original zip file and temporary directory
    os.system(f'rm -r {date_string}.zip')
    os.system(f'rm -r {date_string}')

    # Open grib file using xarray
    filepath = f'grib_files/MRMS_MultiSensor_QPE_01H_Pass1_00.00_{year}{month}{day}-{hour}0000.grib2'
    ds = xr.open_dataset(filepath, engine="cfgrib")
    ds = ds.rename(unknown='hourly_precip')
    precip_data = ds['hourly_precip']

    # Trim the xarray dataset
    # Note: Due to the nature of the grib files, trimming is done based on index, rather than
    # lats and lons. In order to change the spatial domain, you would need to experiment with 
    # different index bounds.
    cropped_data = precip_data[np.arange(1444, 1515, 1), np.arange(4110, 4186, 1)]
    # Save the trimmed dataset as a netCDF file in the clipped_files directory
    cropped_data.to_netcdf(path=f'clipped_files/{date_string}.nc')

    # Create quick-look image of this hourly timestep
    lats = cropped_data.latitude
    lons = cropped_data.longitude
    # Set projections
    map_crs = ccrs.PlateCarree(central_longitude=0.0, globe=None)
    data_crs = ccrs.PlateCarree()
    # Set up figure and axis
    fig = plt.figure(1, figsize=(11,12))
    ax = plt.subplot(1, 1, 1, projection=map_crs)
    ax.set_extent([-88.892601, -88.153743, 39.868433 , 40.551599], data_crs)
    # Set max and min values to be displayed on map
    vmin = 0
    vmax = 20
    # Plot data
    im = ax.pcolormesh(lons, lats, cropped_data, transform=data_crs, 
                        cmap='gist_ncar', vmin=vmin, vmax=vmax)
    # Add any helpful map overlays
    ax.add_feature(USCOUNTIES.with_scale('5m'), edgecolor='darkgray')
    # Create plot title and colorbar
    plt.title('MRMS Multi-Sensor 1 hr QPE (Pass 1)', loc='left')
    plt.title(f'{month}/{day}/{year} {hour}:00', loc='right')
    cb = plt.colorbar(im, orientation='horizontal', pad=.02)
    cb.set_label('Precipitation (mm)', fontsize=10)
    # Save figure into quick looks folder
    plt.savefig(f'clipped_files/quick_looks/{date_string}', dpi=50, bbox_inches='tight')
    plt.close()


# Now delete the unclipped grib file directory
os.system('rm -r grib_files')

