import os
import sys
import wget
from datetime import datetime, timedelta

# Enter your time bounds here:
start_year = 2022
start_month = 8
start_day = 25
start_hour = 0

end_year = 2022
end_month = 8
end_day = 26
end_hour = 0

# Enter lat/lon bounds here:
start_lat = 40.551599
start_lon = -88.892601
end_lat = 39.868433
end_lon = -88.153743

# Turn values into datetimes
start_date = datetime(year=int(start_year), month=int(start_month), day=int(start_day), hour=int(start_hour))
end_date = datetime(year=int(end_year), month=int(end_month), day=int(end_day), hour=int(end_hour))

# Compute event duration
duration = end_date - start_date
timedelta_seconds = duration.total_seconds()
timedelta_hours = timedelta_seconds/3600
print(timedelta_hours)

cmd = 'mkdir grib_files'
os.system(cmd)
for i in range(0, int(timedelta_hours)+1, 1):
    new_date = start_date + timedelta(hours=i)
    print(new_date)
    #s_date = int(new_date.strftime("%Y%m%d%H%M%S"))
    year = new_date.strftime("%Y")
    month = new_date.strftime("%m")
    day = new_date.strftime("%d")
    hour = new_date.strftime("%H")
    
    url = f'http://mrms.agron.iastate.edu/{year}/{month}/{day}/{year}{month}{day}{hour}.zip'
    #print(url)
    wget.download(url)
    
    date_string = f'{year}{month}{day}{hour}'
    os.system(f'mkdir {date_string}')
    file_name = f'{date_string}.zip'
    with ZipFile(file_name, 'r') as zip:
        zip.extract(f'{date_string}/CONUS/MultiSensor_QPE_01H_Pass1/MRMS_MultiSensor_QPE_01H_Pass1_00.00_{year}{month}{day}-{hour}0000.grib2.gz')
    cmd = f'gunzip {date_string}/CONUS/MultiSensor_QPE_01H_Pass1/MRMS_MultiSensor_QPE_01H_Pass1_00.00_{year}{month}{day}-{hour}0000.grib2.gz'
    os.system(cmd)
    cmd = f'mv {date_string}/CONUS/MultiSensor_QPE_01H_Pass1/MRMS_MultiSensor_QPE_01H_Pass1_00.00_{year}{month}{day}-{hour}0000.grib2 grib_files'
    os.system(cmd)
    cmd = f'rm -r {date_string}'
    os.system(cmd)